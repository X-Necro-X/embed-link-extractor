# Necro(ネクロ)
# sidmishra94540@gmail.com

from __future__ import print_function
import pickle, pyperclip, requests, os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload,MediaIoBaseDownload
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = None
print('Connecting...')
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(os.path.dirname(__file__) + '/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('drive', 'v3', credentials=creds)
print('Connected!')
choice = int(input('1. Local\n2. URL\n'))
if choice == 2:
    url = input()
    print('Downloading...')
    with open(os.path.dirname(__file__) + '/file/' + '\\' + url.split('/')[-1], 'wb') as f:
        f.write(requests.get(url, stream=True).content)  
    print('Downloaded!')  
print('Uploading...')
file = os.path.dirname(__file__) + '/file/' + os.listdir(os.path.dirname(__file__) + '/file/')[0]
folder = '1dynYtE8Am5dpcUtYhx_cItGFa6HulRO1'
metadata = {
'name': os.listdir(os.path.dirname(__file__) + '/file/')[0],
'parents': [folder]
}
up_file = service.files().create(body=metadata, media_body=MediaFileUpload(file), fields='id').execute()
print('Uploaded!')
os.remove(file)
pyperclip.copy('https://drive.google.com/uc?id='+up_file.get('id'))
print ('https://drive.google.com/uc?id='+up_file.get('id'))