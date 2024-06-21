#!/usr/bin/env python3

import time
import os
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from prettytable import PrettyTable

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


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_device_info(device):
    info = {}

    battery_info = device.shell("dumpsys battery")
    battery_level = int(battery_info.split("level: ")[1].split("\n")[0])
    charging_status = "Charging" in battery_info

    cpu_info = device.shell("top -n 1 -b | grep 'CPU'")
    if cpu_info:
        try:
            cpu_usage = float(cpu_info.split()[2].strip('%'))
        except (IndexError, ValueError):
            cpu_usage = 0.0
    else:
        cpu_usage = 0.0

    gpu_usage = 0.0

    ram_info = device.shell("dumpsys meminfo")
    try:
        total_ram = int(ram_info.split("Total RAM: ")[1].split(" ")[0].replace(",", ""))
        free_ram = int(ram_info.split("Free RAM: ")[1].split(" ")[0].replace(",", ""))
        ram_usage = total_ram - free_ram
    except (IndexError, ValueError):
        total_ram = free_ram = ram_usage = 0

    storage_info = device.shell("df /data")
    try:
        total_storage = int(storage_info.split()[8])
        used_storage = int(storage_info.split()[9])
    except (IndexError, ValueError):
        total_storage = used_storage = 0

    fps = 0.0

    try:
        temperature = float(battery_info.split("temperature: ")[1].split("\n")[0]) / 10
    except (IndexError, ValueError):
        temperature = 0.0

    security_level = 0.0

    info['battery_level'] = battery_level
    info['charging_status'] = charging_status
    info['cpu_usage'] = cpu_usage
    info['gpu_usage'] = gpu_usage
    info['total_ram'] = total_ram
    info['ram_usage'] = ram_usage
    info['total_storage'] = total_storage
    info['used_storage'] = used_storage
    info['fps'] = fps
    info['temperature'] = temperature
    info['security_level'] = security_level

    return info

def connect_device(ip_address):
    device = AdbDeviceTcp(ip_address, 5555)
    try:
        with open("/home/kali/Android/adbkey.pub", "r") as f:
            priv = f.read()
        with open("/home/kali/Android/adbkey", "r") as f:
            pub = f.read()
        signer = PythonRSASigner(pub, priv)
        device.connect(rsa_keys=[signer], auth_timeout_s=30)
        return device
    except FileNotFoundError as e:
        print(f"{ERROR}: {e}" + W)
        print(please + "Ensure the adbkey and adbkey.pub files are in the correct directory!" + W)
        exit(1)
    except Exception as e:
        print(f"{ERROR} Unexpected error: {e}" + W)
        exit(1)

def main():
    ip_address = input(f"{Enter} Enter the IP address of the device: {Y}")
    print(W)
    device = connect_device(ip_address.strip())

    while True:
        info = get_device_info(device)
        
        clear_screen()

        table = PrettyTable()
        table.field_names = [f"{G}ID{W}", f"{B}Category{W}", f"{M}Value{W}"]
        table.add_row([f"{Y}1{W}", f"{M}Battery Level{W}", f"{info['battery_level']}%"])
        table.add_row([f"{Y}2{W}", f"{M}Charging Status{W}", "Charging" if info['charging_status'] else "Not Charging"])
        table.add_row([f"{Y}3{W}", f"{M}CPU Usage{W}", f"{info['cpu_usage']}%"])
        table.add_row([f"{Y}4{W}", f"{M}GPU Usage{W}", f"{info['gpu_usage']}%"])
        table.add_row([f"{Y}5{W}", f"{M}Total RAM{W}", f"{info['total_ram']} MB"])
        table.add_row([f"{Y}6{W}", f"{M}Used RAM{W}", f"{info['ram_usage']} MB"])
        table.add_row([f"{Y}7{W}", f"{M}Total Storage{W}", f"{info['total_storage']} MB"])
        table.add_row([f"{Y}8{W}", f"{M}Used Storage{W}", f"{info['used_storage']} MB"])
        table.add_row([f"{Y}9{W}", f"{M}FPS{W}", f"{info['fps']} fps"])
        table.add_row([f"{Y}10{W}", f"{M}Temperature{W}", f"{info['temperature']} °C"])
        table.add_row([f"{Y}11{W}", f"{M}Security Level{W}", f"{info['security_level']}%"])

        print(table)
        time.sleep(1)

if __name__ == "__main__":
    main()
