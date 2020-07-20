import subprocess 
import re
import json
from datetime import timedelta, datetime

ID_DEVICES = json.load("searchList.json")
DELAY = timedelta(hours=2)

class Device():
    def __init__(self, name, mac=None, ip=None):
        assert not (mac==None and ip==None)
        self.name = name
        self.mac = mac
        self.ip = ip
        self.last_seen = datetime.fromtimestamp(0)

Devices = [Device(name, ID_DEVICES[name]["mac"], ID_DEVICES[name]["ip"]) for name in ID_DEVICES]

def success(name):
    print(name)

def scan():
    proc = subprocess.Popen(["arp", "-a"],stdout=subprocess.PIPE)
    lines = []
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        #the real code does filtering here
        line = line.decode('utf-8')
        lines.append(line)
    lines = [x.replace("\r\n", "") for x in lines]
    lines = [x for x in lines if x]
    lines = lines[2:]
    return lines

def lookup(lines):
    current_time = datetime.now()
    id_addrs = []
    for line in lines:
        patternI = "("+"\d*\."*3+"\d*)"
        patternM = "(..-..-..-..-..-..)"
        rI = re.search(patternI, line)
        rM = re.search(patternM, line)
        id_addrs.append([rM.group(1), rI.group(1)])
    for device in Devices:
        if device.mac:
            for _id in id_addrs:
                if device.mac == _id[0]:
                    device.ip = _id[1]
                    if current_time > device.last_seen + DELAY:
                        success
                    device.last_seen = current_time
        else:   #Fill inn mac address
            for _id in id_addrs:
                if device.ip == _id[1]:
                    device.mac = _id[0]
                    if current_time > device.last_seen + DELAY:
                        success
                    device.last_seen = current_time





    
            




