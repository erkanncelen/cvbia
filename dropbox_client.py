import dropbox
import yaml

class TransferData:
    def __init__(self):
        self.access_token =''
        self.dbx = dropbox.Dropbox(self.access_token)

    def upload_file_yaml(self, content, file_to):
        """upload a file to Dropbox using API v2
        """
        self.dbx.files_upload(bytes(content, 'utf-8'), file_to)

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        with open(file_from, 'rb') as f:
            self.dbx.files_upload(f.read(), file_to)
    