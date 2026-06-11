# 👻 PHANTOM VIRUS OSINT ELITE

**OSINT Reconnaissance Tool** — Python-based Open Source Intelligence tool for gathering digital footprint data on IP addresses, domains, phone numbers, and network infrastructure.

---

## 🧠 Overview / Maelezo ya Jumla

**ENGLISH:**  
PHANTOM VIRUS OSINT ELITE is a powerful, production-ready OSINT tool written in Python 3. It performs **passive reconnaissance** to collect publicly available information without directly interacting with target systems. It supports IP geolocation, WHOIS lookups, DNS enumeration, reverse DNS, subdomain discovery via crt.sh, HTTP header analysis, ping checks, phone number OSINT, and simulated social media footprint analysis.

**KISWAHILI:**  
PHANTOM VIRUS OSINT ELITE ni tool ya kisasa ya OSINT iliyoandikwa kwa Python 3. Inafanya **uchunguzi wa kimya (passive reconnaissance)** kukusanya taarifa za wazi bila kugusa moja kwa moja mifumo inayolengwa. Inaauni kutafuta eneo la IP, taarifa za WHOIS, kukagua DNS, reverse DNS, kutafuta subdomains kupitia crt.sh, kuchambua HTTP headers, kupima ping, OSINT ya namba za simu, na uchambuzi wa mitandao ya kijamii (simulated).

---

## ✨ Features / Vipengele

| Feature | Description |
|---------|-------------|
| 🌐 **IP Geolocation** | Country, city, ISP, coordinates, Google Maps link |
| 🔎 **WHOIS Lookup** | Domain registration details, registrar, dates |
| 📡 **DNS Records** | A, AAAA, MX, NS, TXT, CNAME records |
| 🔁 **Reverse DNS** | PTR record lookup |
| 🛰️ **Subdomain Enumeration** | Passive enumeration via crt.sh (Certificate Transparency) |
| 🧾 **HTTP Headers** | Security headers, server info, response analysis |
| 📶 **Ping Check** | Network reachability test |
| 📱 **Phone OSINT** | Country, carrier, region, timezone, Google Maps coordinates |
| 👥 **Social OSINT** | Simulated WhatsApp / Telegram / Signal presence check |
| 💾 **Auto JSON Reports** | All results automatically saved to `osint_reports/` |

---

## 📦 Installation / Usakinishaji

### Requirements

- Python 3.8+
- pip (Python package manager)

### Quick Install

```bash
# Update packages (Termux users)
pkg update && pkg upgrade
pkg install python

# Install Python dependencies
pip install requests python-whois dnspython phonenumbers                                                                                     
git clone https://github.com/mr-virus148/phantom-virus-osint-.git
cd phantom-virus-osint-
python osintV6.py
