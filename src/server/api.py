from flask import Flask, request, jsonify ,Response,Blueprint
from constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR ,idm_status

# import constants

from HandleDownload import download_file,get_file_info

from HandleFile import stop_files ,resume_files,delete_files

import re
import os
import urllib.parse

from tool import verify


api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/file-info',methods=['GET'])
def get_file_info_endpoint():
    file_url = request.args.get('file_url', None)
    if file_url is None:
        return jsonify({"error": "Missing 'file_url' query parameter"}), 400
    
        # Decode the URL
    decoded_url = urllib.parse.unquote(file_url)

    result = get_file_info(decoded_url)
    
    return jsonify(result)


@api_blueprint.route('/get_file_name', methods=['GET'])
def get_file_name():
    file_infos = request.args.to_dict()
    file_name = file_infos.get('name') or 'dowload_file'
    ext = file_infos.get('ext') or "html"
    # save_dir = file_infos.get('SavePath') or "./downloads"
    print("name,ext",ext)
    pattern = re.compile(f'^{re.escape(file_name)}(\(\d+\))?.{re.escape(ext)}$')
    
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

@api_blueprint.route('/download_file', methods=['POST'])
async def download_file_endpoint():
    file_infos = request.get_json()
    # verify(file_infos)
    # await download_file(file_infos)
    # return f"File  Download finish"
    try:
        verify(file_infos)  # Added verification
        await download_file(file_infos)
        return "File Download finish"
    except ValueError as e:
        return str(e), 400
    # file_name = file_infos.get('name') or 'dowload_file'

@api_blueprint.route('/stop_download', methods=['POST'])
async def stop_download():
    data = request.get_json()
    all = data.get('all') or None
    save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)
    # res=f""
    # status=500
    # if not os.path.exists(save_state_file):
    #     print("error no file is on download")  
    #     res="error no file is on download"
    #     status=500

    if not os.path.exists(save_state_file):
        return Response('{"error": "no file is downloading"}', 500, mimetype='application/json')
        # return jsonify({"error":"error no file is on download"})
    # file_name=[]
    # if all:
    #     # stop_files(all)
    #     status=500
    #     res=f"All files are stopped"
    # else:
    #     status=500
    #     res=f"the selected files are stopped"
    #     items=data.get('rows') or None
    #     file_names=[item['FileName'] for item in items if 'FileName' in item]
    #     print("filename",file_names)
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
    return Response(f'{{"message": "{res}"}}', status, mimetype='application/json')

    # return Response(res, status, mimetype='application/json')
    # return f"the {file_name} is not running"


@api_blueprint.route('/resume_download', methods=['POST'])
async def resume_download():
    data = request.get_json()
    all = data.get('all', False)
    save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)
    print("resume_download")

    if not os.path.exists(save_state_file):
        return Response('{"error": "no files in download list"}', 500, mimetype='application/json')

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
    return Response(f'{{"message": "{res}"}}', status, mimetype='application/json')


@api_blueprint.route('/delete_download', methods=['POST'])
async def delete_download():
    # global idm_status.status_track
    data = request.get_json()
    all = data.get('all') or None
    save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)

    if not os.path.exists(save_state_file):
        rs=f"error file status not found"
        # global constants
        # idm_status.status_track={}
        # print("error no file is on download")
        # return Response(rs, status=200, mimetype='application/json')
    else:
        file_names=[]
        if all:
            # delete_files(None,all)
            rs=f"the download list is emptied"
        else:
            items=data.get('rows') or None
            file_names=[item['FileName'] for item in items if 'FileName' in item]
            rs=f"the selected files are deleted"
            
        await delete_files(file_names,all)
        # idm_status.status_track=read_status_file()
        # print(idm_status.status_track)
        # idm_status.socketio.emit('progres', idm_status.status_track)

    return Response(rs, status=200, mimetype='application/json')


# @api_blueprint.route('/resume', methods=['GET'])
# def handle_my_custom_event():
#  loop = asyncio.get_event_loop()
#  loop.create_task(async_task())
# #  idm_status.socketio.start_background_task(async_task)
#  print('asyncio called1')
#  return "asyncio called1"







