from flask import Flask, request, jsonify ,Response,Blueprint
from constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR ,idm_status,SAVE_STATE_FILE
from aiohttp import web
api_blueprint = web.RouteTableDef()
from HandleDownload import download_file,get_file_info
from observer_socket import get_socketio
from HandleFile import stop_files ,resume_files,delete_files
import os
import urllib.parse
from tool import verify,read_status_file

@api_blueprint.get('/file-info')
async def get_file_info_endpoint(request):
    # Extract 'file_url' parameter
    file_url = request.query.get('file_url', '')
    if not file_url:
        return web.json_response({'error': 'Missing file_url parameter'}, status=400)
    # Decode the URL
    decoded_url = urllib.parse.unquote(file_url)
    result = await get_file_info(decoded_url)
    return web.json_response(result, status=200)

@api_blueprint.post('/download_file')
async def download_file_endpoint(request):
    try:
        file_infos =await request.json()
        verify(file_infos)
        await download_file(file_infos)
        return web.json_response({'message': 'File Download finish'}, status=200)
    except ValueError as e:
        return web.json_response({'message': str(e)}, status=400)

@api_blueprint.post('/resume_download')
async def resume_download(request):
    try:
        data =await request.json()
        all = data.get('all', False)
        if not os.path.exists(SAVE_STATE_FILE):
            status=400
            res="error no file is on download"
            return web.json_response({"error": res}, status=status)
        file_names=[]
        if all:
            res=f"All files are resumed"
        else:
            items = data.get('rows', [])
            file_names=[(item['FileName'],item['Cmd_Option']) for item in items if 'FileName' in item]
            res=f"the selected files are resumed"
        status = 200 if file_names else 400
        await resume_files(file_names, all)
    except Exception as e:
        res="Server error while processing request"
        status=100

    return web.json_response({"message": res}, status=status)


@api_blueprint.post('/stop_download')
async def stop_download(request):
    try:
        data =await request.json()
        all = data.get('all') or None
        if not os.path.exists(SAVE_STATE_FILE):
            status=404
            res="error no file is on download"
            return web.json_response({"message": res}, status=status)
        file_names = []
        if all:
            res = "All files stopped"
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


@api_blueprint.post('/delete_download')
async def delete_download(request):
    data =await request.json()
    all = data.get('all', False)

    if not os.path.exists(SAVE_STATE_FILE):
        res=f"error file status not found"
        status=400
        return web.json_response({"message": res}, status=status)

    file_names=[]
    if all:
        res=f"the download list is emptied"
    else:
        items = data.get('rows', [])
        file_names=[item['FileName'] for item in items if 'FileName' in item]
        res=f"the selected files are deleted"
    status = 200 if file_names else 400
        
    await delete_files(file_names,all)

    return web.json_response({"message": res}, status=status)