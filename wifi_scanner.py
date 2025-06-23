from scapy.all import *
from threading import Thread
import pandas
import time
import os

#Initialize empty data frame to store network information
networks = pandas.DataFrame(columns=["SSID", "BSSID", "dBm_signal", "Channel", "Crypto"])
networks.set_index("BSSID", inplace=True)

#Implement the sniffer function to capture packets
def callback(packet):
    if packet.haslayer(Dot11Beacon):
        bssid = packet[Dot11].addr2
        ssid+packet[Dot11Elt].info.decode()
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
        stats = packet[Dot11Beacon].network_status()
        chanel = stats.get("chanel")
        crypto = stats.get("crypto")
        networks.loc[bssid] = (ssid, dbm_signal, chanel, crypto)

#Print contents of network dataframe
def print_all():
    while True:
        os.system("clear")
        print(networks)
        time.sleep(0.5)
if __name__ == "__main__":
    interface = "wlan0mon"
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()
    sniff(prn=callback, iface=interface)

#Change channel function to change the channel of the wireless interface
def change_channel():
    ch = 1
    while True:
        os.system(f"iwconfig {interface} channel {ch}")
        ch = ch %14 + 1
        time.sleep(0.5)

#Start the channel changing thread
channel_changer = Thread(target=change_channel)
channel_changer.daemon = True
channel.changer.start()