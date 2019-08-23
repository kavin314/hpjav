# -*- coding: utf-8 -*-
import sys
import os
import socket
import ftplib
from ftplib import FTP
import datetime
from tqdm import tqdm

ftp_server='49.159.161.157'
ftp_port = 1021
ftp_user='kavin'
ftp_password=''
ftp_remote_dir='/Public/01_Personal/Kavin/01_Personal/TEMP8/'
#ftp_remote_dir='/Download/'
bufsize = 1024

todday = datetime.datetime.now().strftime('%Y%m%d')

#uploadfile = 'D:\\video\\1.jpg'

class FtpUploadTracker:
    sizeWritten = 0
    totalSize = 0
    lastShownPercent = 0

    def __init__(self, totalSize):
        self.totalSize = totalSize

    def handle(self, block):
        self.sizeWritten += 1024
        percentComplete = round((self.sizeWritten / self.totalSize) * 100)

        if (self.lastShownPercent != percentComplete):
            self.lastShownPercent = percentComplete
            print(str(percentComplete) + " percent complete")

def listfiles(path):
    files = os.listdir(path)
    #for name in files:
    #    print(name)
    return files
    
def delfiles(path,files):
    for filename in files:
        if os.path.exists(path+filename):
           os.remove(path+filename)
        else:
           print("The file ["+ path+filename +"] does not exist")

def delfile(path,file):
    if os.path.exists(path + file):
        os.remove(path + file)
    else:
        print("The file [" + path + file + "] does not exist")

def upload(path,files):
    if len(files)==0:
       print("not files can upload")
       return ""
    socket.setdefaulttimeout(60)  #超時FTP時間設置為60秒
    #ftp = FTP(ftp_server)
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.set_pasv(True)
    ftp.encoding='utf-8'
    ftp.connect(ftp_server, ftp_port)
    print("login ftp...")
    try:
        ftp.login(ftp_user, ftp_password)
        print(ftp.getwelcome())  #獲得歡迎信息
        #for a in ftp.nlst():
        #  print(a)
        ftp.cwd(ftp_remote_dir)  #設置FTP路徑
        #for b in ftp.nlst():
        #  print(b)
        """
        try:
          if ftp_backup_dir in ftp.nlst():
            print("found backup folder in ftp server, upload processing.")
          else:
            print("don't found backup folder in ftp server, try to build it.")
            ftp.mkd(ftp_backup_dir)
        except:
          print("the folder [" + ftp_backup_dir + "] doesn't exits and can't be create!")
          sys.exit()
        """
    except:
        print("ftp login failed.exit.")
        sys.exit()
        
    print("upload data...")
    try:
        file_handler = None
        for filename in files:
            uploadfile = '{}'.format(path + filename)
            print("upload file:"+uploadfile)
            filesize = os.path.getsize(uploadfile)
            #uploadTracker = FtpUploadTracker(int(filesize))
            ext = os.path.splitext(uploadfile)[1]
            if ext in (".txt", ".htm", ".html"):
                file_handler = open(uploadfile,'rb')
                #for line in file_handler:
                #    print(line.rstrip(), type(line))
                #ftp.storlines('STOR ' + filename, file_handler, uploadTracker.handle)  #上傳檔案
                #2019-07-19 Modify by Kavin Add show progressbar for ftp upload
                with tqdm(unit = 'blocks', unit_scale = True, leave = False, miniters = 1, desc = 'Uploading ['+filename+']', total = filesize) as tqdm_instance:
                    try:
                        ftp.storbinary('STOR ' + filename, file_handler, bufsize, callback = lambda sent: tqdm_instance.update(len(sent)))
                        print(result)
                        delfile(path, filename)
                    except ftplib.error_perm as e:
                        print('----ERROR:cannot write %s on %s' % (filename, ftp_server))
                        print(e)
                        return False
            else:
                file_handler = open(uploadfile, 'rb')
                #ftp.storbinary('STOR ' + filename,file_handler , bufsize, uploadTracker.handle)  #上傳檔案
                #2019-07-19 Modify by Kavin Add show progressbar for ftp upload
                with tqdm(unit = 'blocks', unit_scale = True, leave = False, miniters = 1, desc = 'Uploading ['+filename+']', total = filesize) as tqdm_instance:
                    try:
                        result=ftp.storbinary('STOR ' + filename, file_handler, bufsize, callback=lambda sent: tqdm_instance.update(len(sent)))
                        print(result)
                        delfile(path, filename)
                    except ftplib.error_perm as e:
                        print('----ERROR:cannot write %s on %s' % (filename, ftp_server))
                        print(e)
                        return False
        file_handler.close()
        ftp.close()
    except socket.error:
        print("upload failed. check your permission."+socket.error)
        return False
    """
    print("delte old file...")
    try:
      ftp.delete(os.path.basename(oldfile))  #刪除5天前的備份文件
    except:
      print("the old file in ftp doesn't exists, jumped.")
    """
    
    return True

if __name__== '__main__':
    os.system("cls")
    #path = 'C:\\video\\'
    path = "/mnt/hgfs/mp4/"
    files = listfiles(path)
    upload(path, files)
    """
    if upload(path, files):
        print("ftp upload successful")
        delfiles(path,files)
    else:
        print("ftp upload failure!")
    """
