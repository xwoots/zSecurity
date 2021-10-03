#!/usr/bin/env python

import scapy.all as scapy


def scan(ip_address):
    arp_request = scapy.ARP(pdst=ip_address)
    broadcast = scapy.Ether(dst="FF:FF:FF:FF:FF:FF")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    print("")
    print("IP\t\t| MAC Address")
    print("------------------------------------")

    for element in answered_list:
        print(element[1].psrc + "\t| " + element[1].hwsrc)

# scapy.ls(scapy.METHOD())  >> affiche les arguments possibles de la methode.


scan("192.168.1.0/24")


