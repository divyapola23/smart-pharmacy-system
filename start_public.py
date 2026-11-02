"""Standalone launcher for Smart Pharmacy System with Cloudflare Public Tunnel.
Runs independently of Antigravity or any IDE.
"""
import os
import re
import sys
import time
import subprocess
import webbrowser

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_EXE = os.path.join(ROOT_DIR, ".venv", "Scripts", "python.exe")
if not os.path.isfile(PYTHON_EXE):
    PYTHON_EXE = sys.executable

CLOUDFLARED_EXE = os.path.join(ROOT_DIR, "cloudflared.exe")
LOG_FILE = os.path.join(ROOT_DIR, "tunnel.log")
LINK_TXT = os.path.join(ROOT_DIR, "PUBLIC_LINK.txt")
LINK_URL = os.path.join(ROOT_DIR, "OPEN_PUBLIC_LINK.url")

def cleanup():
    # Remove old tunnel log
    if os.path.exists(LOG_FILE):
        try:
            os.remove(LOG_FILE)
        except Exception:
            pass

def main():
    os.chdir(ROOT_DIR)
    cleanup()

    print("=" * 70)
    print("  Smart Pharmacy System - Starting Independent Public Server")
    print("=" * 70)
    print("\n[1/3] Starting local Flask server (http://127.0.0.1:5000)...")

    # Start Flask app
    app_proc = subprocess.Popen(
        [PYTHON_EXE, "app.py"],
        cwd=ROOT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    )

    time.sleep(2)

    if not os.path.exists(CLOUDFLARED_EXE):
        print(f"[ERROR] cloudflared.exe not found in {ROOT_DIR}")
        app_proc.terminate()
        return

    print("[2/3] Launching Cloudflare public tunnel...")
    tunnel_proc = subprocess.Popen(
        [CLOUDFLARED_EXE, "tunnel", "--url", "http://127.0.0.1:5000", "--logfile", LOG_FILE],
        cwd=ROOT_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    print("[3/3] Acquiring secure public HTTPS link from Cloudflare (5-10s)...")
    tunnel_url = None
    url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")

    for _ in range(40):  # poll up to 20 seconds
        time.sleep(0.5)
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    matches = url_pattern.findall(content)
                    if matches:
                        tunnel_url = matches[-1]
                        break
            except Exception:
                pass

    if not tunnel_url:
        print("[!] Could not auto-detect URL from log file. Please check tunnel.log.")
        tunnel_url = "Check tunnel.log for your trycloudflare URL"

    # Save to file
    with open(LINK_TXT, "w", encoding="utf-8") as f:
        f.write(f"Smart Pharmacy System - Public URL:\n{tunnel_url}\n\n")
        f.write("Credentials:\n")
        f.write("Admin:       admin@pharmacy.com / Admin1234!\n")
        f.write("Pharmacist:  pharmacist@pharmacy.com / Pharmacist1234!\n")

    # Create Windows Internet Shortcut file (.url)
    if tunnel_url.startswith("https://"):
        with open(LINK_URL, "w", encoding="utf-8") as f:
            f.write(f"[InternetShortcut]\nURL={tunnel_url}\nIconIndex=0\n")

    print("\n" + "=" * 70)
    print("  >>> SUCCESS! YOUR PUBLIC WEBSITE IS READY <<<")
    print("=" * 70)
    print(f"\n  PUBLIC LINK:  {tunnel_url}\n")
    print("  SAVED TO:     PUBLIC_LINK.txt & OPEN_PUBLIC_LINK.url")
    print("  LOGIN CREDENTIALS:")
    print("    * Admin:       admin@pharmacy.com / Admin1234!")
    print("    * Pharmacist:  pharmacist@pharmacy.com / Pharmacist1234!")
    print("\n" + "-" * 70)
    print("  [IMPORTANT NOTICE]:")
    print("  - YOU CAN SAFELY CLOSE ANTIGRAVITY IDE NOW!")
    print("  - This Command Prompt window is running independently.")
    print("  - As long as this window is kept open, your website works anywhere.")
    print("  - To shut down the server when done, simply close this window.")
    print("=" * 70 + "\n")

    # Open in browser
    if tunnel_url.startswith("https://"):
        try:
            webbrowser.open(tunnel_url)
        except Exception:
            pass

    try:
        while True:
            time.sleep(1)
            if app_proc.poll() is not None:
                print("Flask app stopped.")
                break
            if tunnel_proc.poll() is not None:
                print("Tunnel stopped.")
                break
    except KeyboardInterrupt:
        print("\nStopping Smart Pharmacy System...")
    finally:
        try:
            tunnel_proc.terminate()
        except Exception:
            pass
        try:
            app_proc.terminate()
        except Exception:
            pass
        print("Stopped cleanly.")

if __name__ == "__main__":
    main()
