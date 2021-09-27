from __future__ import print_function

import io
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from flask import Flask, request
import time

# If modifying these scopes, delete the file token.json.
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello Everyone"


@app.route('/wait_5_sec/')
def test():
    time.sleep(5)
    return "Hello Shubham"


@app.route('/download/')
def download():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    file_id = '1x_0P8bxFsX9IbzBiUONQ9Rx4QUA1zyQy'
    file_id = request.args.get("file_id",file_id)
    file_name = request.args.get("file_name","file_name")
    ext = request.args.get("ext","png")

    req = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, req)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    with io.open(os.getcwd()+'/'+file_name+'.'+ext, 'wb') as f:
        fh.seek(0)
        f.write(fh.read())
    return "Downloaded"

if __name__ == "__main__":
    app.run(debug=True)
