#!/usr/bin/env python3

import subprocess
import datetime
import time 
import pyudev
import os
import sys

R = "\033[91;1m"  # Red
G = "\033[92;1m"  # Green
B = "\033[94;1m"  # Blue
Y = "\033[93;1m"  # Yellow
C = "\033[96;1m"  # Cyan
M = "\033[95;1m"  # Magenta
W = "\033[97;1m"  # White
D = "\033[90;1m"  # Grey
S = "\033[0m"     # Reset

sign = "\033[92;1m" + "[" + "\033[94;1m" + "*" + "\033[92;1m" + "]" + "\033[94;1m"
Enter = "\033[94;1m" + "[" + "\033[92;1m" + "+" + "\033[94;1m" + "]" + "\033[92;1m"
ERROR = "\033[93;1m" + "[" + "\033[91;1m" + "ERROR" + "\033[93;1m" + "]" + "\033[91;1m"
INFO = "\033[93;1m" + "[" + "\033[92;1m" + "INFO" + "\033[93;1m" + "]" + "\033[94;1m"
warning = "\033[93;1m" + "[" + "\033[91;1m" + "WARNING" + "\033[93;1m" + "]" + "\033[91;1m"
Complete = "\033[94;1m" + "[" + "\033[92;1m" + "COMPLETE" + "\033[94;1m" + "]" + "\033[92;1m"
Failed = "\033[93;1m" + "[" + "\033[91;1m" + "FAILED" + "\033[93;1m" + "]" + "\033[91;1m"
please = "\033[93;1m" + "[" + "\033[91;1m" + "!" + "\033[93;1m" + "]" + "\033[91;1m"
Question = "\033[95;1m" + "[" + "\033[96;1m" + "?" + "\033[95;1m" + "]" + "\033[97;1m"
Help = "\033[97;1m" + "To continue anyway press or click" + "\033[94;1m" + " [" + "\033[92;1m" + "Enter" + "\033[94;1m" + "] " + "\033[97;1m" + "and to stop or exit" + "\033[93;1m" + " [" + "Ctrl" + "\033[97;1m" + " + " + "\033[93;1m" + "C" + "]" + "\033[0m"

now = datetime.datetime.now()
formatted_time = now.strftime("%I:%M %p")
formatted_day = now.strftime("%A")

date_day = "\033[94;1m" + "[" + "\033[92;1m" + "Today" + "\033[94;1m" + "]" + "\033[97;1m" + "(" + "\033[93;1m" + formatted_day + "\033[95;1m" + f" {now:%B %D %Y}" + "\033[97;1m" + ")" + "\033[94;1m" + "[" + "\033[92;1m" + "Time" + "\033[94;1m" + "]" + "\033[93;1m" + "[" + "\033[91;1m" + formatted_time + "\033[93;1m" + "]" + "\033[97;1m"


if os.geteuid() != 0:
    sudo = "\033[1;31m" + "sudo" + "\033[0m"
    root = "\033[93;1m" + "root" + "\033[97;1m"
    print(f"{please} {W}please use {root} Type a command {sudo}")
    sys.exit(1)

os.system("clear")

print(rf"""
       {R}_,.                   
     {R},` -.)                  
    {R}( _{W}{Y}/-\{Y}-._               
   {R}/,{Y}|`--._,-^|           {Y}/|{W} 
   {R}\_{Y}| {G}|`-._/|{Y}|          {Y}/ |{W} 
     {Y}|  {G}`-, /{Y} |         {Y}/  /{W} 
     {Y}|     {G}||{Y} |        {Y}/  /{W}  
      {Y}`r-._{G}||{Y}/   {B}__   {Y}/  /{W}   
  {B}__,-<_     )`-/  `.{Y}/  /{W}    
 {B}/\   `---    \   / {Y}/  /{W}     
 {B}|   |           |.{Y}/  /{W}                               {B}.{W}
 {B}|    /          /{Y}/  /{W}    _              _           {B}/ \{W}     _   
 {B}\_/  \         |{Y}/  /{W}    / \   _ __   __| |_ __ ___  {B}| |{W}  __| |   
  {B}|    |   _,^- {Y}/  /{W}    / _ \ | '_ \ / _` | '__/ {R}_{W} \ {B}|.|{W} / _` |   
  {B}|    , ``  {Y}(\{Y}/  /_{W}   / ___ \| | | | (_| | | | {R}(0){W} |{B}|.|{W}| (_| |        
   {B}\,.->._    {Y}\X-=/^{W}  /_/   \_\_| |_|\__,_|_|  \_{R}^{W}_/ {B}|:|{W} \__,_|
   {B}(  /   `-._{Y}//^`{W}                                   {B}|:|{W}
    {B}`Y-.____{Y}(__){W}                                  {W}~{Y}\==8==/{W}~{W}
     {B}|     {Y}(__){B}|{W}                                      {R}8{W}
     {B}|_________|   {W}                                   {R}0{W}
┏─────────────────────────────────────────────────────┓
│ {R}● {Y}● {G}●{W}                                               │
│ {B}INSTAGRAM {W}| {Y}https://www.instagram.com/r94xs/{W}        │
│ {B}GiTHub    {W}| {Y}https://www.github.com/MohmmadALbaqer/{W}  │
┗─────────────────────────────────────────────────────┛""")
def check_android_device():
    context = pyudev.Context()
    
    for device in context.list_devices(subsystem='usb'):
        model_id = device.get('ID_MODEL')
        if model_id and 'android' in model_id.lower():
            print(f"{sign} {G}Android device connected{W}")
            input(f"{Enter} {W}The device {B}[{G}Android{B}] {W}is now connected {Help}")
            return True
    
    print(f"{ERROR} Android device is offline !{W}")
    sys.exit(0)
    return False

if __name__ == "__main__":
    check_android_device()
    print(1*"\r\n")

def run_adb_command(command):
    try:
        result = subprocess.check_output(['adb', 'shell'] + command.split(), stderr=subprocess.STDOUT)
        return result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8')

def get_device_info():
    device_info = {}
    print(1*f"{date_day}\r\n")
    device_info[f'{B}[{G}Model{B}]{W}'] = run_adb_command("getprop ro.product.model").strip()
    
    device_info[f'{B}[{G}Android Version{B}]{W}'] = run_adb_command("getprop ro.build.version.release").strip()
    
    device_info[f'{B}[{G}Security Patch Level{B}]{W}'] = run_adb_command("getprop ro.build.version.security_patch").strip()
    
    cpu_info = run_adb_command("cat /proc/cpuinfo")
    device_info[f'{B}[{G}CPU{B}]{W}'] = cpu_info.strip()
    
    gpu_info = run_adb_command("<command to get GPU info>")
    device_info[f'{B}[{G}GPU{B}]{W}'] = gpu_info.strip()

    ram_info = run_adb_command("cat /proc/meminfo | grep MemTotal")
    device_info[f'{B}[{G}RAM{B}]{W}'] = ram_info.strip()

    storage_info = run_adb_command("df -h")
    device_info[f'{B}[{G}Storage{B}]{W}'] = storage_info.strip()
    battery_info = run_adb_command("dumpsys battery")
    device_info[f'{B}[{G}Battery{B}]{W}'] = battery_info.strip()
    
    memory_info = run_adb_command("cat /proc/meminfo")
    device_info[f'{B}[{G}Memory{B}]{W}'] = memory_info.strip()
    return device_info

def check_security(device_info):

    security_patch_level = device_info.get('Security Patch Level', '')
    if "2024-04" in security_patch_level:
        return f"{R}Dangerous{W}"
    else:
        return f"{G}Security{W}"

def check_malware():
    malware_check = run_adb_command("pm list packages --system")
    if "malware_package_name" in malware_check:
        return f"{R}Malware Detected{W}"
    else:
        return f"{Y}Not Malware Detected{W}"

def check_root():
    root_check = run_adb_command("which su")
    if "su" in root_check:
        return f"{R}Rooted{W}"
    else:
        return f"{Y}Not Rooted{W}"

def main():
    adb_check = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    print(f"{sign} Checking in progress {W}[{G}device model{W}]")
    time.sleep(0.3)
    print(f"{sign} Checking in progress {W}[{G}Android version{W}]")
    time.sleep(0.1)
    print(f"{sign} Checking in progress {W}[{G}security patch level{W}]")
    time.sleep(0.6)
    print(f"{sign} Checking in progress {W}[{G}CPU information{W}]")
    time.sleep(0.3)
    print(f"{sign} Checking in progress {W}[{G}GPU information{W}]")
    time.sleep(0.2)
    print(f"{sign} Checking in progress {W}[{G}RAM information{W}]")
    time.sleep(0.4)
    print(f"{sign} Checking in progress {W}[{G}storage information{W}]")
    time.sleep(0.1)
    print(f"{sign} Checking in progress {W}[{G}battery information{W}]")
    time.sleep(0.2)
    print(f"{sign} Checking in progress {W}[{G}memory information{W}]")
    time.sleep(0.1)
    print(f"{sign} Checking in progress {W}[{G}security patch level{W}]")
    if 'device' not in adb_check.stdout:
        print(f"{ERROR} No device connected or ADB not installed !{W}")
        return

    device_info = get_device_info()
    
    for key, value in device_info.items():
        print(key + ":", value)
    print(1*"\n\r")
    security_status = check_security(device_info)
    print(f"{INFO} Security Status:", security_status)
    
    malware_status = check_malware()
    print(f"{INFO} Malware Status:", malware_status)
    
    root_status = check_root()
    print(f"{INFO} Root Status:", root_status)

if __name__ == "__main__":
    main()
