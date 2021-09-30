#!/usr/bin/env python3

import subprocess
import optparse

parser = optparse.OptionParser()

parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
parser.add_option("-m", "--mac-address", dest="mac_address", help="New MAC address")

(options, arguments) = parser.parse_args()

interface = options.interface
mac_address = options.mac_address

print("[+] Changing mac address of" + interface + "to" + mac_address)

subprocess.call(["ifconfig", interface, "down"])
subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
subprocess.call(["ifconfig", interface, "up"])

# /!\ Raw commands but unsecured /!\
# subprocess.call("ifconfig " + interface + " down", shell=True)
# subprocess.call("ifconfig " + interface + " hw ether " + mac_address, shell=True)
# subprocess.call("ifconfig " + interface + " up", shell=True)

