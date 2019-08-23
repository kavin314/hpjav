#-*- coding: utf-8 -*-
import os
import sys
import re
#from flask import Flask
import requests
import socket
import urllib
import urllib.request
import time

#app = Flask(__name__)

#@app.route("/callback")
#def hello():
#    return "Hello World!"

def delfiles(path,files):
    if len(files)==0:
       print("not files")
       return ""
    for filename in files:
        if os.path.exists(path+filename):
           print("The file ["+ path+filename +"] is exist, will delete !")
           os.remove(path+filename)
        else:
           print("The file ["+ path+filename +"] does not exist")

def openfile(path,files):
    uploadfile = ''
    for filename in files:
        print("Number of files:"+str(len(files)))
        print("["+filename+"]")
        uploadfile = path+filename
        print("The file ["+ uploadfile+"]")
        open('{}'.format(uploadfile), 'rb')

def datecompare(date1,date2):
    #date1 = "2019/05/01"
    #date2 = "2019/08/01"
    newdate1 = time.strptime(date1, "%Y/%m/%d")
    newdate2 = time.strptime(date2, "%Y/%m/%d")
    print(date1 > date2)
    return (date1 > date2)

if __name__ == "__main__":
    #app.run(debug=True,port=8080)

    ##path = 'c:\\video\\'
    ##files = os.listdir(path)
    #delfiles(path,files)
    ##openfile(path,files)

    #text_title = '[中文字幕]OFJE-153'
    #s = re.split(r'\s',text_title)
    #print(s[0])
    #m=re.search('[A-Z]{3}-[0-9]{3}|[A-Z]{4}-[0-9]{3}',s[0])
    #vid = s[0][m.start():m.end()].replace(' ','')
    #print(vid)
    #url_content = "https://goodcdn.verystream.net/stream/KiHGiMwigEe/4StaO2XMA3CbpNFF/yCy4ZD3uCQSZZA72MBcNwwdvuL80o15sXGhEX9aNLXRECKsV5aooMpJDXzMtxTvUm5JyzZjtsI1zilGzG6CXyeDbe3-iilFTyEShk8zkEVx3RiPZtZBdAmGwv0ikLzyvRbaY5FPNOuXH5dZxyhkvqWVKLZ-zhPZCSv99V4MS_smc5o2t3xvEDMKfZF9m-Icg8b9IQqXwCR-xetMdILwJbVYHbxBO9bV8Uhx0DAAt4yxZmLlzeaJY2sXvAO2nHRDvb502TK5S-KoosmDe_3DAqtONcF5rR8VgDlxiPWxInih2d4VyQMo-S7WDjDJ3O0t6ZaqBMm2kTHM-KAHdpraX9d_O4y-HgsfQuUPH8M4C96yis29fQuuc7_9zJFfgfnpyAzXtWkOFfRTliJ2H1R_sVjDANGvtlhF37UfUjDyFUKM/GAH-121-C.mp4?download=true"
    #file_name = "GAH-121.mp4"
    #try:
    #    urllib.request.urlretrieve(url_content, file_name) 
    #    print('下載成功!') 
    #except Exception as result:
    #    print('下載失敗:'+str(result)) 
    #print('繼續執行下面的程式')
    print(datecompare("2019/05/01","2019/08/01"))
