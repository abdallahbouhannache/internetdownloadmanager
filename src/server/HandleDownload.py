from tool import write_chunk_to_file,retry_internet_check
from flask import jsonify
import os
import re
import asyncio
from constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR ,idm_status
import requests
import tempfile

async def download_file(file_infos):
    id = file_infos.get('id') or None
    file_url = file_infos.get('Url') or None
    file_name = file_infos.get('FileName') or None
    finished = file_infos.get('Finished') or False
    status = file_infos.get('Status') or False
    Catg=file_infos.get('Catg') or "UNKNOWN"
    # speed_limit = file_infos.get('Speed') or 2048
    speed_limit = 204800
    Conx_number = file_infos.get('Conx_number') or 2
    downloaded_size = file_infos.get('Downloaded') or 0
    save_dir = file_infos.get('SavePath') or "./downloads"
    command = file_infos.get('Cmd_Option') or "new" # values continue,restart,new
    save_state_file = os.path.join(SAVE_DIR, 'download_state.bson')
    file_save_path = os.path.join(save_dir, file_name)
    file_size = file_infos.get('File_Size') or 0

    if os.path.exists(file_save_path) :
        downloaded_size=os.path.getsize(file_save_path)
        if command=="restart":
            os.remove(file_save_path)
            downloaded_size=0
    
    local_file_status= {
        "id": id,
        "Url": file_url,
        "Finished": finished,
        "Status": status,
        "Downloaded": downloaded_size,
        "Cmd_Option": command,
        "Speed": speed_limit,
        "Catg":Catg,
        "FileName":file_name,
        "Time_Left": 0,
        "File_Size": file_size,
        "SavePath": save_dir,
        "Resume": False,
    }

    await idm_status.status_queue.put((file_name, local_file_status))
    session=idm_status.open_session

    # async with aiohttp.ClientSession() as session:
    internet=await retry_internet_check(session,"www.google.com")
    if not internet or not file_size:
        # await it here # add retry of grabbing file size here otherwise stop downloading
        local_file_status['Status'] = False
        await idm_status.status_queue.put((file_name, local_file_status))
        idm_status.session_event.set()  # Wake up session manager
        error="No internet connection" if not internet else f"File {file_name}  Filesize error"
        return jsonify({error}), 503
    print("internet and file_size is ok")

    try:
        await idm_status.status_queue.put((file_name, local_file_status))
        # Use tempfile for unique temp path
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
        tasks = []
        chunk_size = file_size // Conx_number # size of each chunk in bytes
        chunks = [(i * chunk_size, (i+1) * chunk_size - 1) for i in range(file_size // chunk_size)]
        for start, end in chunks:
            task=download_task(session, file_url, start, end,file_name,file_save_path,tmp_path)
            tasks.append(task)
            await idm_status.bandwidth_queue.put((file_name, "add", local_file_status))
            await asyncio.sleep(0.1)

        await asyncio.gather(*tasks)
        await idm_status.bandwidth_queue.put((file_name, "remove", local_file_status))
    except ConnectionError as e:
        local_file_status['Status'] = False
        await idm_status.status_queue.put((file_name, local_file_status))
        await idm_status.bandwidth_queue.put((file_name, "remove", local_file_status))
        return jsonify({'error': 'Error starting download'}), 503

async def download_task(session, url, start, end,file_name,file_save_path,tmp_path):
    File_Bytes=bytearray()
    headers = {'Range': f'bytes={start}-{end}'}
    async with session.get(url, headers=headers) as response:
        current_size = start      
        while current_size <= end :
            await asyncio.sleep(1)
            async with idm_status.status_lock:  # Ensure safe read access
                local_file_status=idm_status.status_track.get(file_name, {})
            file_status = local_file_status.get('Status', False)
            if not file_status:
                break
            speed = local_file_status.get('Speed', 50000)
            local_file_status['Speed']=speed
            try:
                remaining_bytes = end - current_size + 1
                chunk_size = min(speed, remaining_bytes)
                chunk = await asyncio.wait_for(response.content.read(chunk_size), timeout=5)
                if not chunk:
                    break  # Exit loop if no more data
                File_Bytes+=chunk
                current_size += len(chunk)
                local_file_status['Downloaded']+= len(chunk)
            except asyncio.TimeoutError:
                internet=await retry_internet_check(session,"www.google.com")
                if not internet:
                    local_file_status['Status']=False
                    break
            except Exception as e:
                local_file_status['Status']=False
                break
            await idm_status.status_queue.put((file_name, local_file_status))

    file_size=local_file_status.get('File_Size',0)
    downloaded_size=local_file_status.get('Downloaded',0)
    print(f"downloading parts of [{file_name}]",local_file_status)
    if downloaded_size >= file_size :
        local_file_status['Finished']=True
        local_file_status['Status']=False
    idm_status.session_event.set()  # Wake up session manager
    await idm_status.status_queue.put((file_name, local_file_status))   
    await idm_status.bandwidth_queue.put((file_name, "remove", local_file_status))
    await asyncio.sleep(0.5)
    await write_chunk_to_file(tmp_path,file_save_path,File_Bytes,file_name,start,file_size)

    """ match and return filename and extension """
def get_file_name(FullFileName):
    [file_name, ext] = FullFileName.rsplit(".",1) or [
        "download",
        "html",
      ]
    pattern = re.compile(f'^{re.escape(file_name)}(\\(\\d+\\))?\\.{re.escape(ext)}$')
    matching_files = [key for key in idm_status.status_track.keys() if pattern.match(key)]
    file_count = f'({len(matching_files)+1})' if len(matching_files) else ""

    unique_file_name=f'{file_name}{file_count}.{ext}'
    return unique_file_name,ext

""" fetch filename,ext,filesize from a url  """
async def get_file_info(url, max_name_length=50):
    info = {
        'FileName': "download.html",
        'ext': "html",
        'File_Size': 0,
    }
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        # Try HEAD request first
        response = requests.head(url, headers=headers, allow_redirects=True, timeout=13)
        content_length = response.headers.get('Content-Length')

        if content_length is None:
            response = requests.get(url, stream=True, allow_redirects=True, timeout=13)
            content_length = response.headers.get('Content-Length')
            if content_length is None:
                return info  # Return default info if still no size

        file_size = int(content_length)
        filename = url.split("/")[-1] or "download"
        name, ext = get_file_name(filename)
        if len(name) > max_name_length:
            name = name[:max_name_length].rstrip()

        info = {
            'File_Size': file_size,
            'FileName': name,
            'ext': ext
        }
        return info

    except requests.RequestException as e:
        return info