# -*- coding: UTF-8 -*-

import string
import keyword
import sys
import os
import time
import datetime
import requests
import math
from bs4 import BeautifulSoup
import urllib
import certifi
import urllib3
import base64
import re
#import ast
import codecs
from selenium import webdriver
import openload
import ftp

urllib3.disable_warnings()

#search_word="IPX-3"
#search_word="園田みおん"
#search_word="ABP-852"
#search_word="GNE-223"
#search_word="EBOD-68"
#search_word="希崎 IPX-3"
#search_word="DOCP-15"
search_word="佐々木あき"
#search_word="美谷朱里"
#search_word=""

hpjav_search_url = "https://hpjav.tv/tw/?s="
hpjav_domain = "https://hpjav.tv"
#filepath="C:\\video\\"
filepath="/mnt/hgfs/mp4/"
post_list = []
url_list = []
title_List = []
decode_list = []
hpjav_host_url_list=[]
post_list_index = 0
isDownload = False
#isDownload = True

today=datetime.datetime.now().strftime('%Y/%m/%d')
print("Today is [" + today + "]")

#javascript hex code convert to string
def decoding(str_a):
    #str_a="\x6C\x6F\x63\x61\x74\x69\x6F\x6E"
    hex_byte = codecs.encode(bytes(str_a, "utf-8"), 'hex')
    #print("hex_byte--------->\n",hex_byte)
    a=codecs.decode(hex_byte, 'hex')
    #print("a--------->\n",a)
    b=str(bytearray(a), 'utf-8')
    #print("b--------->\n",b)
    return b
  
def get_browser():
    chrome_opt=webdriver.ChromeOptions()
    #chrome_opt.add_argument('--no-headless')#會顯示UI
    chrome_opt.add_argument("--headless")#不會顯UI
    chrome_opt.add_argument("--log-level=3")#不顯示log
    chrome_opt.add_argument('--disable-gpu')
    chrome_opt.add_argument("--no-sandbox")
    chrome_opt.add_argument("--disable-dev-shm-usage")
    #chrome_opt.add_argument("--verify=False")
    #browser = webdriver.Chrome(executable_path=r'c:\PortableApps\GoogleChromePortable\App\Chrome-bin\chromedriver.exe',	options=chrome_opt)
    browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_opt)
    return browser
  
def close_popups(browser):
    while(len(browser.window_handles)>1):
        browser.switch_to.window(browser.window_handles[-1])
        browser.close()
    browser.switch_to.window(browser.window_handles[0])

#改用webdriver,引用openload.py,
#開起https://hpjav.tv/download/?host=openload&vid=d30355354715855694a5555513f6d616
#取得verystream的網址
def get_host_dl_url(url, browser):
    browser.get(url)
    #browser.execute_script("document.getElementById('btnDl').click()")
    close_popups(browser)
    #Waiting 5 sec timer
    time.sleep(1)
    #browser.execute_script("document.getElementById('secondsleftouter').click()")
    close_popups(browser)
    button=browser.find_element_by_id('down_url')
    host_url=button.get_attribute('href')
    close_popups(browser)
    return host_url

def get_artist(text_title):
    #print("text_title------->"+text_title)
    s = re.split(r'\s',text_title)
    #print(s[len(s)-1])
    return s[len(s)-1]

##2019-08-06 Add by Kavin,進到主頁時，取得女優名字
def get_artists(url):
    filesize=0
    rs = requests.session()
    res = rs.get(url, verify=False)
    soup = BeautifulSoup(res.text,'html.parser')
    #print("soup1---->\n",soup1)
    artists=[]
    for artist in soup.select('div.models-content > a > p'):
        #print(artist)
        artists.append(artist.get_text())
    #print("artists:"+str(artists))
    return artists

def get_vid(text_title):
    #print("text_title------->"+text_title)
    s = re.split(r'\s',text_title)
    #print(s[0])
    m=re.search('[A-Z]{3}-[0-9]{3}|[A-Z]{4}-[0-9]{3}',s[0])
    if m:
        vid = s[0][m.start():m.end()].replace(' ','')
    else:
        vid = s[0]
    return vid

def get_img(url):
    filesize=0
    rs = requests.session()
    res = rs.get(url, verify=False)
    #進入item的網頁,ex. https://hpjav.tv/tw/41081/tikb-019
    #取得OP(openload)的跳轉網頁(https://hpjav.tv/download/?host=openload&vid=d30355354715855694a5555513f6d616)
    #print("網頁編碼 : ", res.encoding)
    soup = BeautifulSoup(res.text,'html.parser')
    #print("soup1---->\n",soup1)
    #取得圖檔的src
    img_src=''
    for img in soup.select('div.col-md-5 img'):
        #print('img[\'src\']------------->',img['src'])
        img_src=img['src']
    if isDownload:
       #下載圖檔
       csize=1000*1000
       filesize = openload.download_file(img_src, filepath, csize)
    return img_src

def get_views(url):
    rs = requests.session()
    res = rs.get(url, verify=False)
    soup = BeautifulSoup(res.text,'html.parser')
    views = ''
    for v in soup.select('view'):
        #print(v.text)
        views = v.text
    regex = re.compile(r'\d+')
    match = regex.search(views)
    #print(match.group(0))
    views = match.group(0)
    return views

def datecompare(date1,date2):
    #date1 = "2019/05/01"
    #date2 = "2019/08/01"
    newdate1 = time.strptime(date1, "%Y/%m/%d")
    newdate2 = time.strptime(date2, "%Y/%m/%d")
    #print(newdate1 > newdate2)
    return (newdate1 > newdate2)

def get_post_list():
    print("start search for hpjav at keyword -->"+search_word)
    rs = requests.session()
    res = rs.get(hpjav_search_url+search_word, verify=False)
    soup = BeautifulSoup(res.text,'html.parser')
    selector_entry = "div.entry-title"
    #selector_page = "ul.pagination"
    selector_page = "div.container > div > div.models-page-box > nav > ul > li"
    #print("get_post_list  soup--------->\n",soup)
    result = soup.select(selector_entry)
    #print("result-------------->\n", ''.join(str(e) for e in result))
    #print("len(result)--------------->\n",len(result))
    item_list=[]
    #判斷有無無結
    if len(result)>0:
        page_num = soup.select(selector_page)
        #print("page_num-------------->\n", ''.join(str(e) for e in page_num))
        print("page_num:",len(page_num))
        #判斷有多頁時
        if len(page_num) >1:#就算只有1頁，也會有pagination tag
            for page_url in soup.select(selector_page):
                for p in page_url.select('a'):
                    #print(p)
                    page_href = p['href']
                    print("page_href:",page_href)
                    res = rs.get(page_href, verify=False)
                    soup_page = BeautifulSoup(res.text,'html.parser')
                    get_item_list(soup_page,selector_entry,item_list)
        else:
            #如果只有一頁時
            get_item_list(soup, selector_entry, item_list)
    #print("item_list------->\n",item_list)
    post_array='\n'.join(str(v) for v in item_list)
    print("post_array------->\n",post_array)
    #print('url:'+item_list[item_list_index]['url']+'\n'+'title:'+item_list[item_list_index]['title']+'\n'+'Date:'+item_list[item_list_index]['date'])
    return item_list

def get_item_list(soup_page, selector_entry, item_list):
    for entry in soup_page.select(selector_entry):
        # print("entry---------->\n",entry)
        entry_text = entry.get_text()
        m = re.search(r'\d+[ ][ -/][ ]\d+[ ][ -/][ ]\d+', entry_text)  # 2019 / 03 / 19
        # print("m-------->\n",m)
        # 取得entry-title裡的text,判斷是否有日期,則為[Censored JAV]如果有的話存入list裡
        if (m):
            # entry_date = datetime.datetime.strptime(entry.get_text()[m.start():m.end()].replace(' ',''), '%Y/%m/%d').date()
            #print("entry.get_text()----->\n",entry.get_text())
            #entry_date = entry.get_text()[m.start():m.end()].replace(' ', '')
            entry_date = entry.get_text()[len(entry.get_text())-14:len(entry.get_text())].replace(' ', '')
            # print("entry_date--------->\n",entry_date)
            # for a in entry.find_all('a', href=True):
            for a in entry.select('a'):
                # print("a---------->\n",a)
                # print("text--------->\n",a.get_text())
                if (a.get_text() != ""):
                    url_list.append(a['href'])
                    title_List.append(a.get_text())
                    href = a['href']
                    text = a.get_text()
                    #artist = get_artist(text)
                    artists=[]
                    vid = get_vid(text)
                    hpjav={'url': href, 'vid': vid, 'title': text, 'date': entry_date}
                    item_list.append(hpjav)
    return item_list

##2019-04-16 停用
##原因:無法用base64 decode,解析出來是錯誤的url
"""
def get_download_link(url):
    rs = requests.session()
    res = rs.get(url, verify=False)
    #進入item的網頁,ex. https://hpjav.tv/tw/41081/tikb-019
    #取得OP(openload)的跳轉網頁(https://hpjav.tv/download/?host=openload&vid=d30355354715855694a5555513f6d616)
    #print("網頁編碼 : ", res.encoding)
    print("res.text---------->",res.text)
    soup = BeautifulSoup(res.text,'html.parser')
    for entry in soup.select('#down_file'):
      print("entry------>\n",entry)
      #a = 'var data = JSON.parse(atob("eyJPUCI6IlwvZG93bmxvYWRcLz9ob3N0PW9wZW5sb2FkJnZpZD1kM2I2MDNhNTk3MjU4NWE1ODQ0N2Q2NzViNmE1MTM5NSIsIlZPIjoiXC9kb3dubG9hZFwvP2hvc3Q9dmlkb3phJnZpZD0zMzA3MzNhNTY3NjQzM2E1YTdhNWE3YTU4N2M2ODVhNSIsIkZFTSI6IlwvZG93bmxvYWRcLz9ob3N0PWFzaWFuY2x1YiZ2aWQ9ZDM1NGE2NDY3NzAzOTZlNDc3MjQ4NGY0Njc1Mzc1YTUiLCJIRCI6eyJSQVAiOiJodHRwczpcL1wvcmFwaWRnYXRvci5uZXRcL2ZpbGVcLzY3NzhhYWM0NmM0MGJmNmQ3OThkNjM2MTk2MGEyMjdkIiwidXBsb2FkZWQiOiJodHRwOlwvXC91cGxvYWRlZC5uZXRcL2ZpbGVcL2RiZ3o0OGV0IiwiVUciOiJodHRwOlwvXC91cGxvYWRnaWcuY29tXC9maWxlXC9kb3dubG9hZFwvNGY4N2NkMGE5OTA0M0JFNiJ9fQ=="));'
      pattern = 'JSON.parse\(atob\(".*?"'
      match_obj = re.search(pattern, str(entry))
      print("match_obj-------->\n",match_obj)
      jason_str = str(entry)[match_obj.start() : match_obj.end()]
      print("str---------->\n",jason_str )
      jason_m = re.search('".*?"', jason_str)
      jason_base64 = jason_str[jason_m.start()+1:jason_m.end()-1]
      print("jason--------->\n",jason_base64)
      decode_bytes=base64.b64decode(jason_base64)
      decode_str = str(decode_bytes, encoding = "utf-8")
      print("decode---------->\n", decode_str )
      decode_list = ast.literal_eval(decode_str)
      print("decode_list['OP']---------->\n", decode_list['OP'] )
      print("type(decode_list['OP'])---------->\n",type(decode_list['OP']))
      hpjav_dl_url=decode_list['OP']
    return hpjav_dl_url
"""

##2019-04-16 Add by Kavin
##用base64 decode 無法反解出真正的download url
##改用webdriver,擷取出下載的url
def get_all_download_link(url,browser):
    browser.get(url)
    #browser.execute_script("document.getElementById('btnDl').click()")
    close_popups(browser)
    #Waiting 5 sec timer
    time.sleep(1)
    #browser.execute_script("document.getElementById('secondsleftouter').click()")
    close_popups(browser)
    browser.execute_script("document.getElementById('download_div').click()")
    close_popups(browser)
    #html = browser.execute_script("return document.body.innerHTML")
    #print("source code------>",html)
    elements=browser.find_elements_by_class_name('dbtn')
    close_popups(browser)
    #print("elements(single download link)-------->",elements)
    if elements!=[]:
        for element in elements:
            dl_url = element.get_attribute("href")
            #print("dl_url------->\n",dl_url)
            check_op = get_check_host_url(dl_url)
            #if check_op == "asianclub":
            if check_op == "verystream":
               return dl_url
    else:
        item_list = []
        elements=browser.find_elements_by_class_name('detail')
        #print("len(elements)-------->",len(elements))
        #print("elements(multi download link)-------->",elements)
        for element in elements:
            #print("element--------->",element.text)
            dl_url=element.find_element_by_tag_name('a').get_attribute("href")
            #print("dl_url------->\n",dl_url)
            check_op = get_check_host_url(dl_url)
            #if check_op == "asianclub":
            if check_op == "verystream":
               item_list.append(dl_url)
        #print("item_list type---->",type(item_list))
        #print("item_list---->",item_list)
        return item_list

##判斷download link是否為openload的跳轉頁面
def get_check_host_url(url):
    #pattern = 'asianclub'
    pattern = 'verystream'
    match_obj = re.search(pattern, str(url))
    #print("match_obj-------->\n",match_obj)
    if match_obj:
        #print(match_obj.group(0))
        return pattern
    else:
        #print("Not found")
        return ""

def filterdate(post_list):
    item_list=[]
    for item in post_list:
        if (datecompare(item['date'], '2019/08/01')):
            print("date than 2019/08/01")
            item_list.append(item)
        else:
            print("date not than 2019/08/01")
    return item_list

def get_host_url(post_list):
    if (len(post_list) != 0):
        print("post_list amount:" + str(len(post_list)))
        index = 0
        for item in post_list:
            img_src = get_img(item['url'])
            item.update({'img': img_src})
            views = get_views(item['url'])
            item.update({'views': views})
            # hpjav_dl_url = get_download_link(item['url'])
            browser = get_browser()
            hpjav_dl_url = get_all_download_link(item['url'], browser)
            item.update({'hpjavdl': hpjav_dl_url})
            artists = get_artists(item['url'])
            item.update({'artists': artists})
            #print("item-------->\n", str(item))
            browser.quit()
            if (type(hpjav_dl_url) == list):
                host_url_list = []
                for value in hpjav_dl_url:
                    # print("key---------->\n",key)
                    # print("value---------->\n",value)
                    # hpjav_host_url = hpjav_dl_url[key].replace("\\", "")
                    # print("value----------->\n", value)
                    hpjav_host_url = str(value)
                    browser = get_browser()
                    host_url = get_host_dl_url(hpjav_host_url, browser)
                    host_url_list.append(host_url)
                    #print("host_url---------->\n", host_url)
                    if isDownload:
                        mp4_dl_url = openload.get_dlurl(host_url, browser)
                        browser.quit()
                        print("mp4_dl_url------------>\n", mp4_dl_url)
                        ##利用openload.py進行背景下載
                        # 取得下載的連結後,進行背景下載
                        csize = 1000 * 1000
                        # openload.download_file(mp4_dl_url, None, csize)
                        # Modify by Kavin 傳入檔案路徑
                        openload.download_file(mp4_dl_url, filepath, csize)
                browser.quit()
                item.update({'host_url': host_url_list})
            else:
                if type(hpjav_dl_url) is not type(None):
                    # hpjav_host_url = hpjav_dl_url.replace("\\", "")
                    print("hpjav_dl_url------------>\n",hpjav_dl_url)
                    browser = get_browser()
                    host_url = get_host_dl_url(hpjav_dl_url, browser)
                    item.update({'host_url': host_url})
                    # print("host_url---------->\n",host_url)
                    if isDownload:
                        mp4_dl_url = openload.get_dlurl(host_url, browser)
                        browser.quit()
                        print("mp4_dl_url------------>\n", mp4_dl_url)
                        ##利用openload.py進行背景下載
                        # 取得下載的連結後,進行背景下載
                        csize = 1000 * 1000
                        # openload.download_file(mp4_dl_url, None, csize)
                        # Modify by Kavin 傳入檔案路徑
                        openload.download_file(mp4_dl_url, filepath, csize)
                    browser.quit()
            print("item with host_url-------->\n", str(item))
        return post_list
    else:
        print("-------------查無資料-------------")
        return None

"""   
def b64DecodeUnicode(str) {
    return decodeURIComponent(atob(str).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
}
"""

#主程式
if  __name__ == "__main__":
    os.system("rm -rf .com.google.Chrome.*")
    print(__name__)
    post_list=get_post_list()
    post_list=filterdate(post_list)
    get_host_url(post_list)

