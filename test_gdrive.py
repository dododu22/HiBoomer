from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from threading import Thread, Event
import os
from time import sleep

class GDriveThread(Thread):
    def __init__(self):
        self.delay = 3
        super(GDriveThread, self).__init__()

    def gDriveSync(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
        drive = GoogleDrive(gauth)
        # View all folders and file in your Google Drive
        while True:
            fileList = drive.ListFile({'q': "'1I0in-pbKnpt4V_Q6_qIl_7_R9Zxw03qC' in parents and trashed=false"}).GetList()
            for file in fileList:
                print('Title: %s, ID: %s' % (file['title'], file['id']))
                # Get the folder ID that you want
                if file['title'] not in os.listdir("static/photos"):
                    file1 = drive.CreateFile({'id': file['id']})
                    print('Downloading file %s from Google Drive' % file['title']) # 'hello.png'
                    file1.GetContentFile("static/photos/"+file['title'])  # Save Drive file as a local file
            print("sleeping")
            sleep(self.delay)

    def run(self):
        self.gDriveSync()


if __name__ == '__main__':
        thread2 = GDriveThread()
        thread2.start()
        print("ok")