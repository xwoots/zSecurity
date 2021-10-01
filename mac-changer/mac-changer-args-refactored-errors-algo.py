#!/usr/bin/env python3

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac-address", dest="mac_address", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.mac_address:
        parser.error("[-] Please specify a MAC address, use --help for more info.")
    return options


def change_mac(interface, mac_address):
    print("[+] Changing mac address for " + interface + " to " + mac_address)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.getoutput(["ifconfig", interface])
    # For Python 2.7 use > subprocess.check_output

    match = re.search(r".*?ether\s(.*)\s{2}txq.*", ifconfig_result)
    if match:
        return match.group(1)
    else:
        print("Could not read MAC address.")


def compare_mac():
    if current_mac == options.mac_address:
        print("[+] MAC address successfully changed to : " + str(current_mac))
    else:
        print("[-] Something went wrong, MAC address doesn't correspond")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("[+] Current MAC address is : " + str(current_mac))

change_mac(options.interface, options.mac_address)
current_mac = get_current_mac(options.interface)
compare_mac()
