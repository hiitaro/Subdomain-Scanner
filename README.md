# 🔍 Subdomain Scanner

> ⚡ A fast, colorful, and multithreaded subdomain scanner for bug bounty hunters and penetration testers.

---

## 🚀 Features

- ✅ Multithreaded scanning (adjustable with `-t`)
- ✅ HTTP / HTTPS / both support
- ✅ Only show live subdomains with `--live`
- ✅ Save results to file
- ✅ Colored terminal output for easy viewing
- ✅ Handles interruptions cleanly (Ctrl+C)
- ✅ Custom timeout value
- ✅ Simple CLI with `-h` help

---

## 🛠 Requirements

Make sure you have **Python 3** installed.

Install dependencies:

```bash
pip install requests colorama
```
or
```bash
pip install -r requirements.txt
```

---



## 📦 Usage

```bash
python3 subdomain_scanner.py <domain> -w <wordlist> [options]
```

## 📌 Required arguments:

```bash
<domain>                Target domain to scan (e.g., example.com)
-w, --wordlist <file>   Path to the subdomains wordlist file
```

## ⚙️ Optional arguments:

```bash
-t, --threads <int>     Number of threads (default: 10)
--timeout <int>         Request timeout in seconds (default: 3)
--http                  Use HTTP only
--https                 Use HTTPS only
--live                  Show only live subdomains (status 200)
-o, --output <file>     Save results to specified file
-h, --help              Show help message and exit
```

## 🖥 Example

```bash
python3 subdomain_scanner.py example.com -w subdomains450.txt -t 20 --timeout 2 --live -o results.txt
```
This command:

Scans example.com using subdomains.txt

Uses 20 threads

Times out after 2 seconds

Shows only status 200 results

Saves output to results.txt

---

##💬 Help Menu Output

```bash
usage: subdomain_scanner.py [-h] -w WORDLIST [-t THREADS] [--timeout TIMEOUT]
                            [--https] [--http] [--live] [-o OUTPUT]
                            domain

⚡ Fast Subdomain Scanner with CLI Flags and Colored Output

positional arguments:
  domain                Target domain (e.g., example.com)

options:
  -h, --help            Show this help message and exit
  -w WORDLIST, --wordlist WORDLIST
                        Path to wordlist with subdomains
  -t THREADS, --threads THREADS
                        Number of threads (default: 10)
  --timeout TIMEOUT     Request timeout in seconds (default: 5)
  --https               Scan only HTTPS
  --http                Scan only HTTP
  --live                Show only live (200 OK) results
  -o OUTPUT, --output OUTPUT
                        File to save results
```

## Wildcard DNS

Some domains use a wildcard DNS setup, which means that any subdomain you try to scan will resolve to the same IP address or return a similar HTTP response—even if the subdomain doesn't actually exist.

If `randomsub.example.com` returns HTTP 200 with some content, then any other subdomain returning exactly the same is probably a wildcard catch-all.

## ⚠️ Legal Disclaimer
This tool is for educational and authorized penetration testing only.
Do not scan domains you do not own or have explicit permission to test.


