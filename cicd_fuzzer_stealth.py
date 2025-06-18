import argparse
import httpx
import random
import re
import time
from rich.console import Console
from rich.table import Table

console = Console()

# CI/CD and config disclosure file paths
COMMON_PATHS = [
    "Jenkinsfile",
    ".env",
    ".git/config",
    ".gitignore",
    "Dockerfile",
    ".npmrc",
    "buildspec.yml",
    ".circleci/config.yml",
    ".github/workflows/main.yml",
    "pipeline/",
    "dist/",
    "logs/",
    "node_modules/",
]

HEADERS_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/137 Safari/537.36"
]

SECRET_REGEX = re.compile(r"(token|api[_-]?key|secret|passwd|auth)[\"'=:\s]{1,3}[^\s\"']+", re.IGNORECASE)

def parse_args():
    parser = argparse.ArgumentParser(description="CI/CD Config Fuzzer with Cloudflare Evasion")
    parser.add_argument("-u", "--url", required=True, help="Target base URL (e.g. https://target.com)")
    parser.add_argument("-p", "--proxy", help="Proxy URL (e.g. http://127.0.0.1:8080)")
    parser.add_argument("-d", "--delay", type=float, default=2.0, help="Delay between requests (default: 2s)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-o", "--output", help="Write results to file")
    return parser.parse_args()

def stealth_fuzz(base_url, proxy=None, delay=2.0, verbose=False, output_file=None):
    results = []

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Status", justify="right")
    table.add_column("Path")
    table.add_column("Keywords Found")

    proxies = None
    if proxy:
        proxies = {
            "http://": proxy,
            "https://": proxy
        }

    with httpx.Client(http2=True, verify=False, proxies=proxies, timeout=10.0) as client:
        for path in COMMON_PATHS:
            full_url = f"{base_url.rstrip('/')}/{path}"
            headers = {
                "User-Agent": random.choice(HEADERS_LIST),
                "Referer": base_url + "/sports.html",
                "Accept": "*/*",
            }

            try:
                resp = client.get(full_url, headers=headers)
                content = resp.text.strip()
                keywords = SECRET_REGEX.findall(content)

                if resp.status_code == 200 and len(content) > 10:
                    table.add_row(f"[green]{resp.status_code}[/]", path, ", ".join(set(keywords)) if keywords else "-")
                    results.append((resp.status_code, full_url, keywords))
                elif resp.status_code == 403:
                    if verbose:
                        console.print(f"[yellow]403 Forbidden[/] {path}")
                elif verbose:
                    console.print(f"[blue]{resp.status_code}[/] {path}")
            except Exception as e:
                console.print(f"[red]ERROR[/] {path}: {str(e)}")

            time.sleep(random.uniform(delay * 0.8, delay * 1.2))

    console.print("\n[bold green]Scan Complete[/]")
    console.print(table)

    if output_file:
        with open(output_file, "w") as f:
            for code, url, keywords in results:
                f.write(f"{code} {url} {' '.join(keywords)}\n")

if __name__ == "__main__":
    args = parse_args()
    stealth_fuzz(args.url, args.proxy, args.delay, args.verbose, args.output)
