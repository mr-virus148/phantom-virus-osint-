#!/usr/bin/env python3
"""
PHANTOM VIRUS OSINT ELITE v7
Fixed, hardened, production-ready OSINT tool.
"""

import sys
import requests
import socket
import whois
import dns.resolver
import ipaddress
import json
import os
import platform
import subprocess
import re
from datetime import datetime
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from phonenumbers.phonenumberutil import region_code_for_number


# ---------------- CONFIG ----------------
REPORT_DIR = "osint_reports"

# ---------------- COUNTRY COORDS (ISO alpha-2 keys) ----------------
COUNTRY_COORDS = {
    "TZ": (-6.7924, 39.2083),   # Tanzania
    "KE": (-1.2921, 36.8219),   # Kenya
    "UG": (0.3476, 32.5825),    # Uganda
    "US": (38.9072, -77.0369),  # United States
    "GB": (51.5074, -0.1278),   # United Kingdom
    "IN": (28.6139, 77.2090),   # India
    "NG": (9.0820, 8.6753),     # Nigeria
    "ZA": (-25.7461, 28.1881),  # South Africa
    "GH": (5.6037, -0.1870),    # Ghana
    "RW": (-1.9403, 30.0619),   # Rwanda
    "ET": (9.0320, 38.7469),    # Ethiopia
    "ZM": (-15.4167, 28.2833),  # Zambia
    "CM": (3.8480, 11.5021),    # Cameroon
    "CI": (6.8276, -5.2893),    # Côte d'Ivoire
    "SN": (14.4974, -14.4524),  # Senegal
}


# ---------------- BANNER ----------------
def banner():
    print("""
╔════════════════════════════╗
👻 PHANTOM VIRUS OSINT ELITE v7
🧠 FULL INTELLIGENCE SUITE
🇹🇿 EDUCATIONAL CYBER TOOL
╚════════════════════════════╝
""")


# ---------------- SAVE REPORT (unique file per run) ----------------
def save_report(data):
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)

    data["timestamp"] = str(datetime.now())

    # Create a unique filename based on type + timestamp
    rtype = data.get("type", "unknown")
    target = data.get(data.get("type", ""), data.get("domain", data.get("ip", data.get("number", "unknown"))))
    safe_target = re.sub(r'[^a-zA-Z0-9]', '_', str(target))[:20]
    filename = f"{rtype}_{safe_target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(REPORT_DIR, filename)

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4, default=str)

    print(f"\n💾 Report saved -> {filepath}")
    return filepath


# ---------------- ARGUMENT GUARD ----------------
def get_arg(index, help_on_fail=True):
    if len(sys.argv) <= index:
        if help_on_fail:
            print(f"❌ Missing argument for '{sys.argv[1]}' command")
            help_menu()
        sys.exit(1)
    return sys.argv[index]


# ---------------- IP LOOKUP ----------------
def ip_lookup(ip):
    result = {"type": "ip", "ip": ip}

    try:
        ipaddress.ip_address(ip)

        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        r.raise_for_status()
        data = r.json()

        print("\n🌐 IP INFO")
        print("------------------")
        for k, v in data.items():
            print(f"  {k}: {v}")

        result["data"] = data

    except ValueError:
        print("❌ Invalid IP address:", ip)
        result["error"] = "Invalid IP address"
    except requests.exceptions.Timeout:
        print("❌ IP lookup timed out")
        result["error"] = "Timeout"
    except Exception as e:
        print("❌ IP error:", e)
        result["error"] = str(e)

    save_report(result)


# ---------------- WHOIS ----------------
def whois_lookup(domain):
    result = {"type": "whois", "domain": domain}

    try:
        # Set a timeout via socket
        old_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(15)
        w = whois.whois(domain)
        socket.setdefaulttimeout(old_timeout)

        print("\n🔎 WHOIS INFO")
        safe = str(w)
        print(safe)

        result["data"] = safe

    except Exception as e:
        print("❌ WHOIS error:", e)
        result["error"] = str(e)

    save_report(result)


# ---------------- DNS ----------------
def dns_lookup(domain):
    result = {"type": "dns", "domain": domain}

    try:
        records = {}

        for t in ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]:
            try:
                answers = dns.resolver.resolve(domain, t, lifetime=10)
                records[t] = [str(r) for r in answers]
            except dns.resolver.NoAnswer:
                records[t] = []
            except dns.resolver.NXDOMAIN:
                records[t] = []
            except dns.resolver.LifetimeTimeout:
                records[t] = ["TIMEOUT"]
            except Exception:
                records[t] = []

        print("\n📡 DNS RECORDS")
        for rtype, answers in records.items():
            if answers:
                print(f"\n  [{rtype}]")
                for a in answers:
                    print(f"    {a}")

        result["records"] = records

    except Exception as e:
        print("❌ DNS error:", e)
        result["error"] = str(e)

    save_report(result)


# ---------------- HEADERS ----------------
def http_headers(domain):
    result = {"type": "headers", "domain": domain}

    for scheme in ["https", "http"]:
        try:
            r = requests.get(f"{scheme}://{domain}", timeout=10, allow_redirects=True)
            headers = dict(r.headers)

            print(f"\n🧾 HEADERS ({scheme.upper()})")
            for k, v in headers.items():
                print(f"  {k}: {v}")

            if r.status_code >= 400:
                print(f"  ⚠️  Status: {r.status_code}")
            else:
                print(f"  ✅ Status: {r.status_code}")

            result["scheme"] = scheme
            result["status_code"] = r.status_code
            result["headers"] = headers
            save_report(result)
            return

        except requests.exceptions.SSLError:
            continue  # Try HTTP
        except requests.exceptions.ConnectionError:
            continue  # Try next scheme
        except Exception as e:
            print("❌ Headers error:", e)
            result["error"] = str(e)
            save_report(result)
            return

    print("❌ Could not connect to domain (HTTP or HTTPS)")
    result["error"] = "Connection failed on both HTTP and HTTPS"
    save_report(result)


# ---------------- REVERSE DNS ----------------
def reverse_dns(ip):
    result = {"type": "reverse_dns", "ip": ip}

    try:
        host, aliases, addresses = socket.gethostbyaddr(ip)

        print(f"\n🔁 REVERSE DNS: {host}")
        if aliases:
            print(f"  Aliases: {', '.join(aliases)}")

        result["hostname"] = host
        result["aliases"] = aliases
        result["addresses"] = [str(a) for a in addresses]

    except socket.herror:
        print(f"❌ No reverse DNS record found for {ip}")
        result["error"] = "No reverse DNS record"
    except Exception as e:
        print("❌ Reverse DNS error:", e)
        result["error"] = str(e)

    save_report(result)


# ---------------- PING (safe subprocess) ----------------
def ping_host(ip):
    result = {"type": "ping", "target": ip}

    try:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        cmd = ["ping", param, "4", ip]

        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        output = proc.stdout + proc.stderr

        print("\n📡 PING RESULT")
        print(output)

        result["output"] = output
        result["returncode"] = proc.returncode

    except subprocess.TimeoutExpired:
        print("❌ Ping timed out")
        result["error"] = "Timeout"
    except FileNotFoundError:
        print("❌ ping command not found on this system")
        result["error"] = "ping not available"
    except Exception as e:
        print("❌ Ping error:", e)
        result["error"] = str(e)

    save_report(result)


# ---------------- SUBDOMAINS ----------------
def subdomain_enum(domain):
    result = {"type": "subdomains", "domain": domain}

    try:
        r = requests.get(
            f"https://crt.sh/?q=%25.{domain}&output=json",
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        r.raise_for_status()
        data = r.json()

        subs = set()

        for entry in data:
            name = entry.get("name_value", "")
            if name:
                for s in name.split("\n"):
                    s = s.strip()
                    if s and s.endswith(domain):
                        # Remove wildcard prefix
                        if s.startswith("*."):
                            s = s[2:]
                        subs.add(s.lower())

        sorted_subs = sorted(subs)

        print(f"\n🌍 SUBDOMAINS ({len(sorted_subs)} found)")
        if sorted_subs:
            for s in sorted_subs:
                print(f"  - {s}")
        else:
            print("  No subdomains found.")

        result["subdomains"] = sorted_subs
        result["count"] = len(sorted_subs)

    except requests.exceptions.Timeout:
        print("❌ crt.sh request timed out")
        result["error"] = "Timeout"
    except json.JSONDecodeError:
        print("❌ Invalid JSON response from crt.sh")
        result["error"] = "Invalid JSON"
    except Exception as e:
        print("❌ Subdomain error:", e)
        result["error"] = str(e)

    save_report(result)


# ---------------- PHONE OSINT ----------------
def phone_lookup(number):
    result = {"type": "phone", "number": number}

    try:
        parsed = phonenumbers.parse(number)

        is_valid = phonenumbers.is_valid_number(parsed)
        is_possible = phonenumbers.is_possible_number(parsed)
        region = geocoder.description_for_number(parsed, "en")
        carrier_name = carrier.name_for_number(parsed, "en")
        tz = timezone.time_zones_for_number(parsed)

        # Get ISO country code for coordinate lookup
        country_code = phonenumbers.region_code_for_number(parsed)
        lat, lon = COUNTRY_COORDS.get(country_code, (None, None))
        maps_link = f"https://www.google.com/maps?q={lat},{lon}" if lat else None

        national_num = phonenumbers.national_significant_number(parsed)
        country_calling_code = parsed.country_code

        print("\n📱 PHONE OSINT")
        print(f"  Number:          {number}")
        print(f"  Valid:           {'✅ YES' if is_valid else '❌ NO'}")
        print(f"  Possible:        {'✅ YES' if is_possible else '❌ NO'}")
        print(f"  Country Code:    +{country_calling_code}")
        print(f"  National Number: {national_num}")
        print(f"  Region:          {region or 'Unknown'}")
        print(f"  ISO Code:        {country_code or 'Unknown'}")
        print(f"  Carrier:         {carrier_name or 'Unknown'}")
        print(f"  Timezone:        {', '.join(tz) if tz else 'Unknown'}")
        print(f"  Coordinates:     {lat}, {lon}" if lat else "  Coordinates:     Unknown")
        print(f"  Maps Link:       {maps_link}" if maps_link else "  Maps Link:       N/A")

        result.update({
            "valid": is_valid,
            "possible": is_possible,
            "country_code": country_calling_code,
            "national_number": national_num,
            "region": region,
            "iso_code": country_code,
            "carrier": carrier_name,
            "timezone": list(tz),
            "lat": lat,
            "lon": lon,
            "maps_link": maps_link
        })

    except phonenumbers.NumberParseException as e:
        print(f"❌ Invalid phone number format: {e}")
        result["error"] = f"Parse error: {e}"
    except Exception as e:
        print("❌ Phone error:", e)
        result["error"] = str(e)

    save_report(result)


# ---------------- SOCIAL OSINT (transparent about simulation) ----------------
def social_osint(number):
    result = {"type": "social", "number": number}

    clean = number.replace("+", "").replace(" ", "")

    print("\n📱 SOCIAL INTEL (SIMULATED — no real API calls)")
    print("  ⚠️  These results are for demonstration only.")
    print("  Real detection requires platform-specific API access.\n")

    # Only flag as "likely" if the number is in a valid format
    likely_valid = len(clean) >= 10 and len(clean) <= 15

    platforms = {
        "WhatsApp":  "Likely registered" if likely_valid else "Cannot determine",
        "Telegram":  "Likely registered" if likely_valid else "Cannot determine",
        "Signal":    "Possible (SIM-based)" if likely_valid else "Cannot determine",
    }

    print("  Platform Availability (estimated):")
    for p, status in platforms.items():
        print(f"    {p:15s}: {status}")

    # Generate plausible but transparent username suggestions
    usernames = [
        f"{clean[-4:]}_user",
        f"user{clean[:5]}",
        f"official_{clean[-3:]}",
        clean[:6]
    ]
    print(f"\n  Suggested usernames to check manually:")
    for u in usernames:
        print(f"    - {u}")

    print(f"\n  Phone: +{clean}")

    result.update({
        "platforms": platforms,
        "usernames": usernames,
        "note": "SIMULATED — no real platform API calls were made"
    })

    save_report(result)


# ---------------- HELP ----------------
def help_menu():
    banner()
    print("""
COMMANDS:

  ip <IP>            - IP geolocation & ISP info
  whois <domain>     - WHOIS lookup
  dns <domain>       - DNS record enumeration (A, AAAA, MX, NS, TXT, CNAME)
  reverse <IP>       - Reverse DNS lookup
  headers <domain>   - HTTP/HTTPS headers
  ping <IP/host>     - Ping test (safe subprocess)
  sub <domain>       - Subdomain enumeration via crt.sh
  phone <number>     - Phone number OSINT
  social <number>    - Social platform lookup (simulated)

EXAMPLES:
  python osint.py ip 8.8.8.8
  python osint.py whois example.com
  python osint.py dns google.com
  python osint.py reverse 8.8.8.8
  python osint.py headers example.com
  python osint.py ping 8.8.8.8
  python osint.py sub example.com
  python osint.py phone +255712345678
  python osint.py social +255712345678

Reports are saved to the '{REPORT_DIR}/' directory.
""")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        help_menu()
        sys.exit()

    cmd = sys.argv[1].lower()
    banner()

    if cmd == "ip":
        ip_lookup(get_arg(2))
    elif cmd == "whois":
        whois_lookup(get_arg(2))
    elif cmd == "dns":
        dns_lookup(get_arg(2))
    elif cmd == "reverse":
        reverse_dns(get_arg(2))
    elif cmd == "headers":
        http_headers(get_arg(2))
    elif cmd == "ping":
        ping_host(get_arg(2))
    elif cmd == "sub":
        subdomain_enum(get_arg(2))
    elif cmd == "phone":
        phone_lookup(get_arg(2))
    elif cmd == "social":
        social_osint(get_arg(2))
    else:
        print(f"❌ Unknown command: {cmd}")
        help_menu()