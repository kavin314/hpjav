# -*- coding: UTF-8 -*-
#!/usr/bin/env python3
"""Usage:
    openload-dl [options] URL

Options:
    -e, --extract-dlurl     Extract only file download url
    -o <file>               Download content into <file>
    --chrome                Use chrome browser instead of firefox
    --no-headless           Show the browser
    --chunk-size <csize>    Set the downloader chunk size in 
                            bytes (default 1MB)                     
    -h, --help              Print this help and exit
    -v, --version           Print version and exit
"""

import os,sys
import requests
import time
from selenium import webdriver
from tqdm import tqdm
from docopt import docopt

__author__ ="gius-italy"
__license__="GPLv3"
__version__="1.0"
__email__="gius-italy@live.it"

#filepath="D:\\video\\"

def close_popups(browser):
    while(len(browser.window_handles)>1):
        browser.switch_to.window(browser.window_handles[-1])
        browser.close()
    browser.switch_to.window(browser.window_handles[0])

def get_dlurl(url,browser):
    browser.get(url)
    #browser.execute_script("document.getElementById('btnDl').click()")
    #browser.execute_script("document.getElementById('download').click()")
    browser.execute_script("document.getElementById('dlbutton').click()")
    close_popups(browser)
    #Waiting 5 sec timer
    time.sleep(11)
    #browser.execute_script("document.getElementById('secondsleftouter').click()")
    close_popups(browser)
    #Gathering direct url for download
    #button=browser.find_element_by_css_selector('a.main-button:nth-child(1)')
    #dlurl=button.get_attribute('href')
    ##for asianclub
    #elements=browser.find_elements_by_class_name('control')
    
    #for element in elements:
    #    button=element.find_elements_by_class_name('button')
    #    #print('element----->\n',button[0].get_attribute('href'))
    #    host_dlurl = button[0].get_attribute('href')
    #    print("asianclub_dl_url------->\n",host_dlurl)
    
    ##2019-07-17 Modify by Kavin, for verystream download 
    elements = browser.find_element_by_css_selector('#dlbutton')
    host_dlurl = elements.get_attribute('href')
    print("host_dlurl------->\n",host_dlurl)
    #We need to override requests default user-agent to avoid bot blocking by openload
    host_dlurl=requests.get(host_dlurl,headers={'User-Agent':browser.execute_script("return navigator.userAgent")},allow_redirects=False).headers['location']
    close_popups(browser)
    return host_dlurl

#2019.03.27 modify by kavin
#加入傳入參數[filepath]
#將原傳入參數[filename]設定為None
def download_file(dlurl,filepath=None,csize=1000*1000):
    filename=None
    try:
        r=requests.get(dlurl,stream=True,verify=False)
        print("status code:",r.status_code)
        file_size=int(r.headers['Content-Length'])
        #if filename is None:
        #    filename=r.url.split("/")[-1]
        filename=r.url.split("/")[-1]
        ##2019-07-17 Modify by Kavin for versystream url filename
        filename=filename.split("?")[0]
        if os.path.exists(filepath+filename):
            print("file exist:",filepath+filename)
            first_byte = os.path.getsize(filepath+filename)
        else:
            print("file not exist, will downloadt this file:",filepath+filename)
            first_byte = 0
        if first_byte >= file_size:
            return file_size
        print("filename------------------>\n",filename)
        r=requests.get(dlurl,headers={"Range": "bytes=%s-%s" % (first_byte, file_size)}, stream=True,verify=False)
        with tqdm(total=file_size, initial=first_byte, unit='B',unit_scale=True, desc=filename) as pbar:
            with open(filepath+filename,'ab') as fp:
                for chunk in r.iter_content(chunk_size=csize):
                    fp.write(chunk)
                    pbar.update(csize)
        return file_size
    except Exception as error:
        print("Error:",str(error))
        return None

#Main 
if __name__=="__main__":
    args=docopt(__doc__,version="openload-dl "+__version__)
    if args['--chunk-size'] is None:
        csize=1000*1000
    else:
        csize=int(args['--chunk-size'])
    if args['--chrome']==True:
        if args['--no-headless']==True:
        	  browser=webdriver.Chrome()
        else:
            chrome_opt=webdriver.ChromeOptions()
            chrome_opt.add_argument('--headless')
            chrome_opt.add_argment("--verify=False")
            #browser=webdriver.Chrome(chrome_options=chrome_opt)
            browser = webdriver.Chrome("c:\\PortableApps\\GoogleChromePortable\\App\\Chrome-bin\\chromedriver.exe",chrome_options=chrome_opt)
    else:
        if args['--no-headless']==True:
            browser=webdriver.Firefox()
        else:
            fox_opt=webdriver.FirefoxOptions()
            fox_opt.add_argument('--headless')
            browser=webdriver.Firefox(firefox_options=fox_opt)
    if args['--extract-dlurl']==True:
        print(get_dlurl(args['URL'],browser))
        browser.quit()
    else:
        dlurl=get_dlurl(args['URL'],browser)
        browser.quit()
        download_file(dlurl,args['-o'],csize)
    if os.path.exists('geckodriver.log'):
        os.remove('geckodriver.log')
    if os.path.exists('chromedriver.log'):
        os.remove('chromedriver.log')
