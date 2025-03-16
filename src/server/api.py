from flask import Flask, request, jsonify ,Response,Blueprint
from constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR ,idm_status
from aiohttp import web
# Define routes (equivalent to a "blueprint")
api_blueprint = web.RouteTableDef()

# import constants

from HandleDownload import download_file,get_file_info
from observer_socket import get_socketio

from HandleFile import stop_files ,resume_files,delete_files

import re
import os
import urllib.parse
from tool import verify,read_status_file

# api_blueprint = Blueprint('api', __name__)

# @api_blueprint.route('/file-info',methods=['GET'])
@api_blueprint.get('/file-info')
def get_file_info_endpoint(request):
    file_url = request.args.get('file_url', None)
    if file_url is None:
        return jsonify({"error": "Missing 'file_url' query parameter"}), 400
    
    # Decode the URL
    decoded_url = urllib.parse.unquote(file_url)
    result = get_file_info(decoded_url)
    return jsonify(result)

@api_blueprint.get('/get_file_name')
def get_file_name(request):
    file_infos = request.args.to_dict()
    file_name = file_infos.get('name') or 'dowload_file'
    ext = file_infos.get('ext') or "html"
    # save_dir = file_infos.get('SavePath') or "./downloads"
    print("name,ext",ext)
    # pattern = re.compile(f'^{re.escape(file_name)}(\(\d+\))?.{re.escape(ext)}$')
    pattern = re.compile(f'^{re.escape(file_name)}((\d+\))?.{re.escape(ext)}$')
    
    # print(pattern)
    matching_files = [key for key in idm_status.status_track.keys() if pattern.match(key)]
    # print(matching_files)
    file_count = f'({len(matching_files)})' if len(matching_files) else ""
    file_name=f'{file_name}{file_count}.{ext}'
    return file_name

    # pattern = re.compile(f'^{re.escape(file_name)}(\(\d+\))?\\.{re.escape(ext)}$')
    # content_dir=os.listdir(save_dir)
    # matching_files = [f for f in content_dir if pattern.match(f)]
    # print(len(matching_files))
    # print(file_count)


@api_blueprint.post('/download_file')
async def download_file_endpoint(request):
    
    # verify(file_infos)
    # await download_file(file_infos)
    # return f"File  Download finish"
    try:
        file_infos =await request.json()

        verify(file_infos)  # Added verification
        await download_file(file_infos)
        return "File Download finish"
    except ValueError as e:
        return str(e), 400
    # file_name = file_infos.get('name') or 'dowload_file'
    


@api_blueprint.post('/stop_download')
async def stop_download(request):

    try:
        data =await request.json()
        all = data.get('all') or None
        save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)
        if not os.path.exists(save_state_file):
            status=404
            res="error no file is on download"
            return web.json_response({"message": res}, status=status)
        file_names = []
        if all:
            res = "All files stopped"
            status = 200
        else:
            items = data.get('rows', [])
            file_names = [item['FileName'] for item in items if 'FileName' in item]
            res = "Selected files stopped"
            status = 200 if file_names else 400
        await stop_files(file_names,all)
    except Exception as e:
        res="Server error while processing request"
        status=500
    return web.json_response({"message": res}, status=status)


@api_blueprint.post('/resume_download')
async def resume_download(request):
    # data = request.get_json()
        
    try:
        data =await request.json()
        all = data.get('all', False)
        save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)
        print("resume_download")

        if not os.path.exists(save_state_file):
            status=400
            res="error no file is on download"
            # return Response('{"error": "no files in download list"}', 500, mimetype='application/json')
            return web.json_response({"error": res}, status=status)

        file_names=[]
        if all:
            res=f"All files are resumed"
            status = 200
        else:
            items = data.get('rows', [])
            file_names=[(item['FileName'],item['Cmd_Option']) for item in items if 'FileName' in item]
            res=f"the selected files are resumed"
            status = 200 if file_names else 400
            print("filename_resume",file_names)
       
        await resume_files(file_names, all)
    except Exception as e:
        print("error",e)
        print(idm_status.socketio)
        res="Server error while processing request"
        status=100

    return web.json_response({"message": res}, status=status)

    # return Response(f'{{"message": "{res}"}}', status, mimetype='application/json')


@api_blueprint.post('/delete_download')
async def delete_download(request):
    # global idm_status.status_track
    data = request.get_json()
    all = data.get('all') or None
    save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)

    if not os.path.exists(save_state_file):
        res=f"error file status not found"
        status=500
        # global constants
        # idm_status.status_track={}
        # print("error no file is on download")
        # return Response(rs, status=200, mimetype='application/json')
    else:
        file_names=[]
        if all:
            status=500
            # delete_files(None,all)
            res=f"the download list is emptied"
        else:
            items=data.get('rows') or None
            file_names=[item['FileName'] for item in items if 'FileName' in item]
            status = 200 if file_names else 400
            res=f"the selected files are deleted"
            
        await delete_files(file_names,all)
        # idm_status.status_track=read_status_file()
        # print(idm_status.status_track)
        # idm_status.socketio.emit('progres', idm_status.status_track)
    # return Response(rs, status=200, mimetype='application/json')
    return web.json_response({"message": res}, status=status)



# @api_blueprint.route('/resume', methods=['GET'])
# def handle_my_custom_event():
#  loop = asyncio.get_event_loop()
#  loop.create_task(async_task())
# #  idm_status.socketio.start_background_task(async_task)
#  print('asyncio called1')
#  return "asyncio called1"







