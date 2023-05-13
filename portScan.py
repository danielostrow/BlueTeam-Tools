#!/usr/bin/env python

from scapy.all import *
from scapy.layers.inet import TCP, IP
from tqdm import tqdm
import os
print("\033[32m⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⣠⠶⡄⠀⢀⣀⣠⠄⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠉⠻⡓⢄⢰⠃⠀⢹⡴⢩⠏⠁⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠈⠳⣶⢷⣈⡏⢀⣤⡀⣇⡧⠴⡲⠟⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠀⠀⠈⢣⠈⢳⡎⠀⢳⠋⢀⠞⠁⠀⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠀⠈⠳⣦⣇⢸⠁⣀⠈⡇⡾⣶⠏⠀⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠀⠀⢀⣹⡎⢻⡼⠈⣧⠋⣴⣁⡄⠀⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⡝⠦⡇⠀⣸⠞⡽⠋⠀⠀⠀⠀")
print("\033[33m⠀⠀⠀⠀⠀⠀⠀⣠⠖⢻⠟⠛⠛⣿⠓⠳⣄⠀⠀⠀⠀⠀")
print("⠀⠀⠀⠀⠀⢠⠞⢇⡠⠁⠱⡀⡰⠁⠑⢤⡋⠱⡄⠀⠀")
print("⠀⠀⠀⠀⢀⡟⠩⡀⠀⠀⠱⡂⠀⠀⢨⠮⣀⠀⢠⠃⠸⡄")
print("⠀⠀⠀⠀⢸⠁⠀⣑⡔⠈⠀⠈⢢⣔⠁⠀⠀⢱⠣⢄⡀⡇")
print("⠀⠀⠀⠀⢸⢖⠈⠀⠈⠢⣀⠔⠁⠈⠑⢤⡔⠁⠀⠀⡘⣷")
print("⠀⠀⠀⠀⢸⡈⠢⣀⠤⠊⠉⠢⢀⠀⡠⠊⠀⠁⢒⠼⢀⡇")
print("⠀⠀⠀⠈⣇⠉⠈⠢⡀⠀⡀⠔⠉⠢⠄⣀⡠⠂⠀⢰⠃⠀⠀")
print("⠀⠀⠀⠀⠸⣄⡀⠤⠚⠙⠄⡀⠀⢀⠤⠊⠉⠀⣲⠏⠀⠀⠀")
print("⠀⠀⠀⠀⠀⠘⢗⠤⡀⠀⡀⠬⠓⠃⠤⣀⣠⣪⠏⠀⠀⠀⠀\033[0m")
# Define target IP address and the range of ports to scan
target_ip = input("Enter target IP:\t")
start_port = input("Enter start port:\t")
end_port = input("Enter end port:\t")
start_port_int = int(start_port)
end_port_int = int(end_port)

# Create a TCP SYN packet
tcp_syn_packet = IP(dst=target_ip)/TCP(dport=0, flags="S")

# Loop through the range of ports and send the TCP SYN packet
open_port = []
for port in tqdm(range(start_port_int, end_port_int+1), desc='Scanning ports'):
    # Set the destination port for the TCP SYN packet
    tcp_syn_packet[TCP].dport = port

    os.system('cls')
    # Send the packet and wait for a response
    response = sr1(tcp_syn_packet, timeout=1, verbose=0)

    # Check the response and print the result
    if response:
        if response[TCP].flags == "SA":
            # print(f"Port {port} is open")
            open_port.append(port)
       # elif response[TCP].flags == "RA":
         #   print(f"Port {port} is closed")
    #else:
    #   print(f"No response received for port {port}")

print(f"Open ports: {open_port}")
