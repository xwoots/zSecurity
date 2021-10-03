#!/usr/bin/env python

import scapy.all as scapy


def scan(ip_address):
    scapy.arping(ip_address)


scan("192.168.0.0/16")


