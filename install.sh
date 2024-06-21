#!/bin/bash

if [ $(id -u) -ne 0 ]; then
    red_sudo=$(echo -e "\033[1;31m" "sudo" "\033[0m")
    echo -e "\033[33m[\033[31m!\033[33m] \033[37mYou need to \033[33mrun \033[37mthis program with ${red_sudo} Please !."
    exit 1
fi
clear

cd requirements && sudo bash requirements.sh && cd ScreenCopy && sudo bash install.sh
chmod +x *

clear

adb keygen adbkey
adb kill-server
adb start-server
adb devices
