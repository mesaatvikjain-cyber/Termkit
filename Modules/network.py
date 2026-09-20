import socket
import subprocess

import urllib.request

def ip(arguments):
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"Hostname: {hostname}")
    print(f"Local IP: {local_ip}")

    try:
        # 3-second timeout in case there's no internet connection
        with urllib.request.urlopen("https://api.ipify.org", timeout=3) as response:
            public_ip = response.read().decode('utf-8')
            print(f"Public IP: {public_ip}")
    except Exception:
        print("Public IP: Unable to fetch (offline or blocked)")

def dns(arguments):
    if len(arguments) == 0:
        print("Usage: network dns <domain> (e.g. network dns google.com)")
        return

    domain = arguments[0]
    try:
        canonical_name, aliases, ip_list = socket.gethostbyname_ex(domain)
        print(f"DNS lookup for: {domain}")
        print(f"  Canonical Name: {canonical_name}")
        print("  IP Addresses:")
        for addr in ip_list:
            print(f"    - {addr}")
    except socket.gaierror:
        print(f"Failed to resolve domain: '{domain}'. Check spelling or internet connection.")
def ping(arguments):
    if len(arguments) == 0:
        print("Usage: network ping <host>")
        return

    host = arguments[0]

    try:
        result = subprocess.run(
            ["ping", "-n", "4", host],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as error:
        print(f"Ping failed: {error}")


def help_command(arguments):
    print("Network commands:")
    print("ip")
    print("ping <host>")
    print("help")
    print("dns <domain>")
    print("port <host> <port>")
    print("web <url>")
import time

def web(arguments):
    if len(arguments) == 0:
        print("Usage: network web <url> (e.g. network web https://google.com)")
        return

    url = arguments[0]
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    start = time.time()
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}  # Avoid being blocked by basic bot filters
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            latency_ms = int((time.time() - start) * 1000)
            print(f"Status:   {response.status} {response.reason}")
            print(f"Latency:  {latency_ms} ms")
            print(f"Server:   {response.headers.get('Server', 'Not specified')}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}")
    except Exception as e:
        print(f"Failed to connect to {url}: {e}")
def port(arguments):
    if len(arguments) < 2:
        print("Usage: network port <host> <port> (e.g. network port google.com 443)")
        return

    host = arguments[0]
    try:
        port_num = int(arguments[1])
    except ValueError:
        print("Error: Port must be a number (1 - 65535).")
        return

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)  # Wait up to 2 seconds for a response

    try:
        result = s.connect_ex((host, port_num))
        if result == 0:
            print(f"Port {port_num} on {host} is [OPEN]")
        else:
            print(f"Port {port_num} on {host} is [CLOSED / UNREACHABLE]")
    except Exception as e:
        print(f"Error checking port: {e}")
    finally:
        s.close()

def network_command(arguments):
    if len(arguments) == 0:
        help_command(arguments)
        return

    command = arguments[0]

    network_commands = {
        "ip": ip,
        "ping": ping,
        "help": help_command,
        "dns": dns,
        "port":port,
        "web":web
    }

    if command in network_commands:
        network_commands[command](arguments[1:])
    else:
        print(f"Unknown network command: {command}")