from flask import Flask, request, jsonify ,Response,Blueprint
from Constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR 

import Constants

from HandleDownload import download_file

from HandleFile import stop_files ,resume_files,delete_files

import re
import os

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/get_file_name', methods=['GET'])
def get_file_name():
    file_infos = request.args.to_dict()
    file_name = file_infos.get('name') or 'dowload_file'
    ext = file_infos.get('ext') or "html"
    save_dir = file_infos.get('SavePath') or "./downloads"
    pattern = re.compile(f'^{re.escape(file_name)}(\(\d+\))?.{re.escape(ext)}$')
    matching_files = [key for key in Constants.status_tracker.keys() if pattern.match(key)]
    file_count = f'({len(matching_files)})' if len(matching_files) else ""
    file_name=f'{file_name}{file_count}.{ext}'
    return file_name

    # pattern = re.compile(f'^{re.escape(file_name)}(\(\d+\))?\\.{re.escape(ext)}$')
    # content_dir=os.listdir(save_dir)
    # matching_files = [f for f in content_dir if pattern.match(f)]
    # print(len(matching_files))
    # print(file_count)


@api_blueprint.route('/download_file', methods=['POST'])
async def download_file_api():
    file_infos = request.get_json()
    file_name = file_infos.get('name') or 'dowload_file'
    await download_file(file_infos)
    return f"File {file_name} Download finish"


@api_blueprint.route('/stop_download', methods=['POST'])
def stop_download():
    data = request.get_json()
    all = data.get('all') or None
    save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)

    if not os.path.exists(save_state_file):
        print("error no file is on download")  
        return jsonify({"error":"error no file is on download"})
    else:
        if all:
            stop_files(all)
            res=f"All files are stopped"
        else:
            res=f"the selected files are stopped"
            items=data.get('rows') or None
            file_names=[item['FileName'] for item in items if 'FileName' in item]
            print("filename",file_names)
            stop_files(file_names)

    return Response(res, status=200, mimetype='application/json')
    # return f"the {file_name} is not running"




@api_blueprint.route('/resume_download', methods=['POST'])
def resume_download():
    data = request.get_json()
    all = data.get('all') or None
    save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)

    if not os.path.exists(save_state_file):
        res=f"error no file in download list"
    else:
        if all:
            resume_files(all)
            res=f"All files are resumed"
        else:
            res=f"the selected files are resumed"
            items=data.get('rows') or None
            file_names=[item['FileName'] for item in items if 'FileName' in item]
            print("filename_resume",file_names)
            resume_files(file_names)

    return Response(res, status=200, mimetype='application/json')




@api_blueprint.route('/delete_download', methods=['POST'])
def delete_download():
    # global status_tracker

    data = request.get_json()
    all = data.get('all') or None
    save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)

    if not os.path.exists(save_state_file):
        # print("error no file is on download")
        rs=f"error file status not found"
        # return Response(rs, status=200, mimetype='application/json')
    else:
        if all:
            delete_files(None,all)
            rs=f"the download list is emptied"
        else:
            items=data.get('rows') or None
            file_names=[item['FileName'] for item in items if 'FileName' in item]
            delete_files(file_names,None)
            rs=f"the selected files are deleted"
            
        # status_tracker=read_status_file()
        # print(status_tracker)
        # socketio.emit('progres', status_tracker)

    return Response(rs, status=200, mimetype='application/json')


# @api_blueprint.route('/resume', methods=['GET'])
# def handle_my_custom_event():
#  loop = asyncio.get_event_loop()
#  loop.create_task(async_task())
# #  socketio.start_background_task(async_task)
#  print('asyncio called1')
#  return "asyncio called1"







