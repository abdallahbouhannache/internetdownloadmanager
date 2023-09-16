import aiohttp
import asyncio
from tool import get_file_size
from flask import Flask, request, jsonify
import os


app = Flask(__name__)

@app.route('/download_file', methods=['POST'])
async def download_file():
    data = request.get_json()
    file_url = data.get('url') or None
    save_dir = data.get('path') or None
    file_name = data.get('filename') or None
    speed_limit = data.get('speed') or None

    # # URL of the file you want to download
    # file_url = 'https://example.com/file_url'

    # # Path where you want to save the downloaded file
    # save_path = '/path/to/save/file.ext'

    # # Speed limit in bytes per second
    # speed_limit = 1024  # 1KB/s

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:

            file_name = os.path.basename(file_url) if not file_name else ""
            # Get the filename from the response headers
            if not file_name :
                content_disposition = response.headers.get('Content-Disposition')
                file_name = get_filename_from_content_disposition(content_disposition)
            
            [file_name,ext]=file_name.split('.')
            
            print(file_name,ext)
            content_dir=os.listdir(save_dir)
            file_count=content_dir.count(file_name)

            if file_count:
                file_name=f'{file_name}({file_count}).{ext}'

            print(f'filename={file_name}')
            return

            save_path = os.path.join(save_dir, file_name)
            print(file_name)
            # Get the file size from the response headers
            file_size = int(response.headers.get('Content-Length'))
            print(get_file_size(file_size))

            # Calculate the number of chunks based on the speed limit
            # chunk_size = min(speed_limit, 1024*1024)
            chunk_size=500 * 1024 
            num_chunks = file_size // chunk_size
            print(f'chunks {num_chunks} with chunk size  {get_file_size(chunk_size)} ')

            # Create a list to store the tasks for parallel downloading
            tasks = []

            file_size_on_disk = 0

            # Download the file in chunks asynchronously
            # for i in range(num_chunks):
            while file_size_on_disk < file_size :
                # Read a chunk of data from the response
                data = await response.content.read(256000)
                # print(f'downloaded :--->{get_file_size(chunk_size)}')
                print(f'downloading {get_file_size(len(data))}')
                # Create a task to write the chunk to the file
                task = asyncio.create_task(write_chunk_to_file(save_path, data))
                tasks.append(task)

                # Delay between chunks to limit the download speed
                await asyncio.sleep(1)
                file_size_on_disk=os.path.getsize(save_path)

            # Download the remaining bytes
            remaining_bytes = file_size % chunk_size
            data = await response.content.read(remaining_bytes)
            task = asyncio.create_task(write_chunk_to_file(save_path, data))
            tasks.append(task)

            # Wait for all tasks to complete
            await asyncio.gather(*tasks)

    return "File downloaded successfully"

async def write_chunk_to_file(file_path, data):
    print(f'appending {get_file_size(len(data))}')
    with open(file_path, 'ab') as file:
        file.write(data)

def get_filename_from_content_disposition(content_disposition):
    if content_disposition:
        parts = content_disposition.split(';')
        for part in parts:
            if part.strip().startswith('filename='):
                filename = part.split('=')[1].strip().strip('"')
                return filename
    return 'downloaded_file'

if __name__ == '__main__':
    app.run()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(download_file())
    asyncio.run(download_file(),debug=True)