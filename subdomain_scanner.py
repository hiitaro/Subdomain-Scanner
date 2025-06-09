import requests
import threading
import argparse
from colorama import Fore, Style, init
from queue import Queue

init(autoreset=True)

print_lock = threading.Lock()
stop_event = threading.Event() 

def get_wildcard_signature(domain, protocol, timeout):
    import random, string
    fake_sub = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    url = f"{protocol}://{fake_sub}.{domain}"
    try:
        resp = requests.get(url, timeout=timeout)
        return resp.status_code, resp.text[:256]
    except Exception:
        return None, None

def scan_url(url, timeout, only_live, output_file=None, wildcard_sig=None):
    if stop_event.is_set():
        return
    try:
        response = requests.get(url, timeout=timeout)
        if wildcard_sig:
            wc_code, wc_body = wildcard_sig
            if response.status_code == wc_code and response.text[:256] == wc_body:
                return
        if only_live and response.status_code != 200:
            return
        status_color = (
            Fore.GREEN if response.status_code == 200 else
            Fore.YELLOW if response.status_code in (301, 302, 403) else
            Fore.RED
        )
        result = f"[{status_color}{response.status_code}{Style.RESET_ALL}] {url}"
        with print_lock:
            print(result)
        if output_file:
            with open(output_file, "a") as f:
                f.write(f"{url} - {response.status_code}\n")
    except requests.exceptions.RequestException:
        pass

def worker(queue, protocol, domain, timeout, only_live, output_file, wildcard_sig):
    while not queue.empty() and not stop_event.is_set():
        sub = queue.get()
        url = f"{protocol}://{sub}.{domain}"
        scan_url(url, timeout, only_live, output_file, wildcard_sig)
        queue.task_done()

def main():
    parser = argparse.ArgumentParser(
        prog="subdomain_scanner.py",
        description="⚡ Fast Subdomain Scanner with CLI Flags and Colored Output",
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    parser.add_argument("-w", "--wordlist", help="Path to wordlist with subdomains", required=True)
    parser.add_argument("-t", "--threads", help="Number of threads (default: 10)", type=int, default=10)
    parser.add_argument("--timeout", help="Request timeout in seconds (default: 5)", type=int, default=5)
    parser.add_argument("--https", action="store_true", help="Scan only HTTPS")
    parser.add_argument("--http", action="store_true", help="Scan only HTTP")
    parser.add_argument("--live", action="store_true", help="Show only live (200 OK) results")
    parser.add_argument("-o", "--output", help="File to save results")

    args = parser.parse_args()

    if args.https and args.http:
        protocols = ["http", "https"]
    elif args.https:
        protocols = ["https"]
    elif args.http:
        protocols = ["http"]
    else:
        protocols = ["http", "https"]

    try:
        with open(args.wordlist, 'r') as f:
            subdomains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}Wordlist file '{args.wordlist}' not found.")
        return

    global stop_event
    try:
        for protocol in protocols:
            print(f"\n{Fore.CYAN}Scanning using protocol: {protocol.upper()}")
            wildcard_sig = get_wildcard_signature(args.domain, protocol, args.timeout)
            queue = Queue()
            for sub in subdomains:
                queue.put(sub)

            threads = []
            for _ in range(args.threads):
                thread = threading.Thread(target=worker, args=(queue, protocol, args.domain, args.timeout, args.live, args.output, wildcard_sig))
                thread.daemon = True
                thread.start()
                threads.append(thread)

            while any(thread.is_alive() for thread in threads):
                for thread in threads:
                    thread.join(timeout=0.1)
                if stop_event.is_set():
                    break

            if stop_event.is_set():
                break

        if not stop_event.is_set():
            print(f"\n{Fore.GREEN}Scan completed.")
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n{Fore.RED}Aborted by user.")

if __name__ == "__main__":
    main()
