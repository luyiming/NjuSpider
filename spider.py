#-*- coding: UTF-8 -*-
import urllib
from bs4 import BeautifulSoup
import threading
import Queue
import re
import os
import time

task_queue=Queue.Queue()
task_queue.put('http://www.nju.edu.cn')
task_queue.put('http://jw.nju.edu.cn')
pages=set()
pages.add('http://www.nju.edu.cn')
pages.add('http://jw.nju.edu.cn')
cnt=0

if not os.path.exists('D:\\nju'):
            try:
                os.mkdir('D:\\nju')
            except:
                pass
def worker():
    global task_queue
    while not task_queue.empty():
        url=task_queue.get()

        print('thread %s >>> downloading %s'%(threading.current_thread().name,url))
        idx=url.decode('utf-8').find(r'nju.edu.cn')
        pre_url=str(url)[:idx+len(r'nju.edu.cn')]
        path='D:\\nju\\'+str(url)[6:idx+len(r'nju.edu.cn')]
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except:
                pass
        try:
            req=urllib.urlopen(url)
        except:
            print('ERROR')
            continue
        global cnt
        filename=str(cnt)+'.html'
        cnt+=1
        with open(path+'\\'+filename,'wb') as f:
            f.write(req.read())
        if task_queue.qsize()>2000:
            continue
        req=urllib.urlopen(url)
        soup=BeautifulSoup(req.read(),'html.parser')
        for link in soup.find_all('a'):
            url=link.get('href')
            try:
                p=re.compile(r'\.[a-zA-Z]+$')
                postfix=re.findall(p,str(url))
                if len(postfix)>=1:
                    if postfix[0]=='.cn' or postfix[0]=='.htm' or postfix[0]=='.html' or postfix[0]=='.asp' or postfix[0]=='.aspx' or postfix[0]=='.php':
                        pass
                    else:
                        continue
            except:
                pass
            try:
                if re.search(r'nju\.edu\.cn',str(url).decode('utf-8')) and re.search('http',str(url).decode('utf-8')):
                    if url not in pages:
                        task_queue.put(str(url))
                        pages.add(str(url))
                elif re.search(re.compile(r'htm(l)?'),str(url)):
                    if url in pages:
                        task_queue.put(str(pre_url+url))
                        pages.add(str(pre_url+url))
            except:
                pass
        print('thread %s >>> %d pages remaining...'%(threading.current_thread().name,task_queue.qsize()))



#create three threads
t1=threading.Thread(target=worker,name='1')
t2=threading.Thread(target=worker,name='2')
t3=threading.Thread(target=worker,name='3')
t4=threading.Thread(target=worker,name='4')
t5=threading.Thread(target=worker,name='5')
t1.start()
time.sleep(1)
t2.start()
time.sleep(1)
t3.start()
time.sleep(1)
t4.start()
time.sleep(1)
t5.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
