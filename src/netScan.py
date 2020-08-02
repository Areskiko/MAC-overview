#pylint: disable=W1401

import subprocess 
import re

def scan(cahceClear = None):
    if cahceClear:
        for entry in cahceClear:
            subprocess.Popen(["ping", "-n", "1", entry], stdout=subprocess.PIPE)
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
    id_addrs = []
    for line in lines:
        patternI = r"("+"\d*\."*3+"\d*)"
        patternM = r"(..-..-..-..-..-..)"
        rI = re.search(patternI, line)
        rM = re.search(patternM, line)
        id_addrs.append([rM.group(1), rI.group(1)])
    return id_addrs

def update(macDevices, ipDevices):
    addrs = lookup(scan(ipDevices))
    macs = [addr[0] for addr in addrs]
    ips = [addr[1] for addr in addrs]
    return [device for device in macDevices if device in macs], macs, ips


    
            




