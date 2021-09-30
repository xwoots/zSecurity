#!/usr/bin/env python3

import subprocess
import optparse


interface = input("interface > ")
new_mac = input("new MAC > ")

# For Python 2.7 : input > raw_input

print("[+] Changing mac address of" + interface + "to" + new_mac)

# /!\ Raw commands but unsecured /!\
# subprocess.call("ifconfig " + interface + " down", shell=True)
# subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
# subprocess.call("ifconfig " + interface + " up", shell=True)

subprocess.call(["ifconfig", interface, "down"])
subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
subprocess.call(["ifconfig", interface, "up"])
