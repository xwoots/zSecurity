#!/usr/bin/env python3

import scapy.all as scapy
import argparse

# scapy.ls(scapy.METHOD())  >> affiche les arguments possibles de la methode.
# For Python 2.7 use the optparse library (but deprecated)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="IP range to scan. EX : 192.168.1.0/24")
    options = parser.parse_args()
    if not options.target:
        parser.error("\n[-] Please specify an IP range, use --help for more info.")
    return options.target


def scan(ip_address):
    arp_request = scapy.ARP(pdst=ip_address)
    broadcast = scapy.Ether(dst="FF:FF:FF:FF:FF:FF")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def print_scan(scan_list):
    print("IP\t\t| MAC Address")
    print("------------------------------------")
    for element in scan_list:
        print(element["ip"] + "\t| " + element["mac"])


print("")
options = get_arguments()
scan_result = scan(options)
print_scan(scan_result)


