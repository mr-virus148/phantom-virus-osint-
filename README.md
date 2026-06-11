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

Command	Target Type	Example
ip	IP Address	python osintV6.py ip 8.8.8.8
whois	Domain	python osintV6.py whois google.com
dns	Domain	python osintV6.py dns google.com
reverse	IP Address	python osintV6.py reverse 8.8.8.8
headers	Domain/URL	python osintV6.py headers google.com
ping	IP/Domain	python osintV6.py ping 8.8.8.8
sub	Domain	python osintV6.py sub google.com
phone	Phone Number	python osintV6.py phone +255712345678
social	Phone Number	python osintV6.py social +255712345678

python osintV6.py help
╔════════════════════════════╗
👻 PHANTOM VIRUS OSINT ELITE v7
╚════════════════════════════╝

🌐 IP INFO
  IP:         8.8.8.8
  Country:    United States
  ISP:        Google LLC
  City:       Mountain View

📱 PHONE OSINT
  Number:          +255712345678
  Valid:           ✅ YES
  Country Code:    +255
  Region:          Tanzania
  Carrier:         Vodacom
  Timezone:        Africa/Dar_es_Salaam
  Coordinates:     -6.7924, 39.2083
  Maps Link:       https://www.google.com/maps?q=-6.7924,39.2083

osint_reports/
├── ip_8.8.8.8_20260611_143022.json
├── whois_google.com_20260611_143105.json
├── phone_255712345678_20260611_143200.json
└── ...

⚠️ Disclaimer / Onyo
ENGLISH:
This tool is intended for educational purposes, authorized security assessments, and ethical cybersecurity research only. The author is not responsible for any misuse or illegal activity. Always ensure you have proper authorization before testing any system.

KISWAHILI:
Tool hii imetengenezwa kwa madhumuni ya elimu, majaribio ya usalama yaliyoidhinishwa, na utafiti wa cybersecurity kwa njia ya kisheria pekee. Mwandishi hawajibiki kwa matumizi mabaya au haramu. Hakikisha una ruhusa kabla ya kutumia tool hii kwenye mfumo wowote.

🧪 Tested On / Imejaribiwa Kwenye
✅ Kali Linux
✅ Termux (Android)
✅ Windows
✅ Linux (Ubuntu/Debian)
👤 Author / Mwandishi
Mr. Virus
🇹🇿 Hacker from Tanzania 
GitHub: @mr-virus148

📄 License
This project is licensed under the MIT License — see the LICENSE [blocked] file for details.

🤝 Contributing / Kuchangia
Pull requests, issues, and feature suggestions are welcome!
Feel free to fork the repository and submit improvements.

⭐ Support / Msaada
If you find this tool useful, consider giving it a star ⭐ on GitHub!
