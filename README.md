# cicd_fuzzer_stealth

# CI/CD Config Fuzzer (Cloudflare Stealth Edition)

A Python-based security testing tool that fuzzes for exposed CI/CD and configuration files (e.g., `Jenkinsfile`, `.env`, `Dockerfile`) on web applications protected by **Cloudflare**.
It uses stealth techniques like randomized headers, HTTP/2 support, jittered delays, and proxy support to evade WAF detection and simulate legitimate traffic.

---

## 🔧 Features

* ✅ Detects exposed CI/CD & config files (Jenkins, Docker, Git, Node.js)
* ✅ Bypasses Cloudflare protections using:

  * Random `User-Agent`, Referer spoofing
  * HTTP/2 (`httpx` client)
  * Delay jitter to avoid rate-limiting
* ✅ Extracts secrets using regex: `token`, `secret`, `apikey`, etc.
* ✅ Rich CLI table output
* ✅ Optional file-based logging
* ✅ Proxy support (Burp/ZAP-compatible)

---

## 📂 Targeted Files

```
/Jenkinsfile
/.env
/.git/config
/.gitignore
/Dockerfile
/.npmrc
/buildspec.yml
/.circleci/config.yml
/.github/workflows/main.yml
/pipeline/
/dist/
/logs/
/node_modules/
```

---

## 🚀 Installation

```bash
git clone https://github.com/yourrepo/cicd-fuzzer-stealth.git
cd cicd-fuzzer-stealth
pip install httpx rich
```

---

## 🧪 Usage

### Basic Scan

```bash
python3 cicd_fuzzer_stealth.py -u https://target.com
```

### Verbose with Output File

```bash
python3 cicd_fuzzer_stealth.py -u https://target.com -v -o results.txt
```

### Through Burp/ZAP Proxy

```bash
python3 cicd_fuzzer_stealth.py -u https://target.com -p http://127.0.0.1:8080
```

### Custom Delay

```bash
python3 cicd_fuzzer_stealth.py -u https://target.com -d 3
```

---

## 📘 Arguments

| Argument        | Description                                          |
| --------------- | ---------------------------------------------------- |
| `-u, --url`     | Target base URL (e.g., `https://example.com`)        |
| `-v, --verbose` | Enable verbose mode                                  |
| `-p, --proxy`   | HTTP/HTTPS proxy URL (e.g., `http://127.0.0.1:8080`) |
| `-d, --delay`   | Delay between requests (default: 2s)                 |
| `-o, --output`  | Save results to a file                               |

---

## 🛡️ Use Case for Pentesters

* Discover sensitive CI/CD files leaking on the webroot
* Fingerprint internal tech stack (e.g., Vue, Node, Docker)
* Extract tokens, secrets, and misconfigurations
* Test against WAF-protected endpoints (e.g., Cloudflare)

---

## 📄 Sample Output

```plaintext
Status  | Path              | Keywords Found
--------|-------------------|------------------
200     | Jenkinsfile       | node
200     | .env              | token, secret
403     | .git/config       | -
```

---

## ⚠️ Disclaimer

This tool is intended **only for authorized security testing and educational purposes**. Unauthorized scanning may violate terms of service or local laws. Always ensure you have **written permission** before testing any system.

---

## 📬 Author

**Naimur Rahman**
*Offensive Security Engineer*
