import subprocess
import re
import sys
import argparse

def start_tunnel(port):
    print(f"Starting tunnel for port {port}...")
    # Use Popen to keep it running and capture output
    cmd = ["npx", "cloudflared", "tunnel", "--url", f"http://localhost:{port}"]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    found_url = False
    for line in process.stdout:
        print(line, end="")
        if "trycloudflare.com" in line:
            url_match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
            if url_match:
                print(f"\n[Tunnel URL]: {url_match.group(0)}")
                found_url = True
                # Keep running
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5176)
    args = parser.parse_args()
    try:
        start_tunnel(args.port)
    except KeyboardInterrupt:
        print("Tunnel stopped.")
        sys.exit(0)
