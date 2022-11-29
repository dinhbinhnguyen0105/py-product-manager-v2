from __future__ import print_function
import os
import io
import mimetypes

from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload

from ..helper import _getExactlyPath
from ..CONSTANTS import (
    SCOPES,
    PATH_TOKEN,
    PATH_CREDENTIALS,
)

class Drive():
    def __init__(self) -> None:
        self.creds = None
        self.pathToken = _getExactlyPath(PATH_TOKEN)
        self.pathCredentials = _getExactlyPath(PATH_CREDENTIALS)

        self._loginWithToken()        

    def _loginWithToken(self):
        if os.path.exists(self.pathToken):
            self.creds = Credentials.from_authorized_user_file(self.pathToken, SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except RefreshError:
                    if os.path.exists(self.pathToken):
                        os.remove(self.pathToken)
                    self._loginWithToken()
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.pathCredentials, SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open(self.pathToken, 'w') as token:
                token.write(self.creds.to_json())
        try:
            self.service = build('drive', 'v3', credentials=self.creds)
        except HttpError as error:
            print(f'An error occurred: {error}')
        pass

    def _listItems(self):
        try:
            # Call the Drive v3 API
            results = self.service.files().list(
                pageSize=10, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')
    
    def _searchFolder(self, folderName):
        try:
            files = []
            page_token = None
            try:
                while True:
                    # pylint: disable=maybe-no-member
                    response = self.service.files().list(
                    q=f"name ='{folderName}' and mimeType='application/vnd.google-apps.folder'",
                    spaces='drive',
                    fields='nextPageToken, '
                            'files(id, name)',
                    pageToken=page_token
                    ).execute()

                    for file in response.get('files', []):
                        # Process change
                        print(F'Found folder: {file.get("name")}, {file.get("id")}')
                    files.extend(response.get('files', []))
                    page_token = response.get('nextPageToken', None)
                    if page_token is None:
                        break
            except TimeoutError as e:
                print(e)
                self._searchFolder(folderName)
        except HttpError as err:
            print(F'An error occurred: {err}')
            files = None
        return files

    def _createFolder(self, folderName):
        try:
            fileMetadata = {
                'name': folderName,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            try:
                folder = self.service.files().create(body=fileMetadata, fields = 'id').execute()
            except TimeoutError as e:
                print(e)
                self._createFolder(folderName)
            print(f'Folder has created with ID: "{folder.get("id")}".')
        except HttpError as error:
            print(F'An error occurred: {error}')
            folder = None
        return folder.get('id')
    
    def _uploadItem(self, folderId, image):
        try:
            fileMetadata = {
                'name': os.path.basename(image),
                'parents': [folderId]
            }
            media = MediaFileUpload(image, mimetype=mimetypes.guess_type(image)[0])
            try:
                file = self.service.files().create(body=fileMetadata, media_body=media, fields='id').execute()
            except TimeoutError as e:
                print(e)
                self._uploadItem(folderId, image)
            return file.get('id')
        except :
            pass
    
    def _downloadImage(self, driveImageId, imagePath):
        try:
            request = self.service.files().get_media(fileId=driveImageId)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f'{imagePath} - Download {int(status.progress() * 100)}')
            file.seek(0)
            with open(imagePath, 'wb') as f:
                f.write(file.read())
                f.close()
        except HttpError as error:
            print(f'An error occurred: {error}')
            file = None
        return imagePath




