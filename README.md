🧠 Overview / Maelezo

ENGLISH:
PHANTOM VIRUS OSINT is a Python-based Open Source Intelligence (OSINT) tool designed to gather and analyze publicly available information about IP addresses, domains, and network infrastructure.

It performs passive reconnaissance to extract digital footprint data quickly and efficiently.

KISWAHILI:
PHANTOM VIRUS OSINT ni tool ya Python ya Open Source Intelligence (OSINT) inayotumika kuchambua taarifa za wazi kuhusu IP addresses, domains, na network infrastructure.

Inafanya uchunguzi wa kimya (passive reconnaissance) bila kuingilia mifumo.

⚡ Features / Vipengele
🌐 IP Geolocation Lookup (ISP, Country, City)
🔎 WHOIS Domain Information
📡 DNS Records Scanner (A, MX, NS, TXT)
🔁 Reverse DNS Lookup
🛰️ Subdomain Enumeration (Passive)
🧾 HTTP Header Analysis
📡 Ping Network Check
💾 Auto JSON Report Generation
🎯 Purpose / Lengo

ENGLISH:
This tool is designed for cybersecurity learning, OSINT research, and ethical network analysis.

KISWAHILI:
Tool hii imetengenezwa kwa ajili ya kujifunza cybersecurity, utafiti wa OSINT, na uchambuzi wa mitandao kwa njia ya kisheria.

⚙️ Installation / Usakinishaji
pkg update && pkg upgrade
pkg install python
pip install requests python-whois dnspython

Clone repository:

git clone https://github.com/yourusername/phantom-virus-osint
cd phantom-virus-osint

Run tool:

python tool.py
🚀 Usage / Matumizi
python tool.py ip 8.8.8.8
python tool.py whois google.com
python tool.py dns google.com
python tool.py reverse 8.8.8.8
python tool.py headers google.com
python tool.py ping 8.8.8.8
python tool.py sub google.com
📦 Example Output
🌐 IP INFO
IP: 8.8.8.8
Country: United States
ISP: Google LLC
City: Mountain View
⚠️ Disclaimer / Onyo

ENGLISH:
This tool is for educational and ethical cybersecurity purposes only. Any misuse is strictly prohibited.

KISWAHILI:
Tool hii ni kwa elimu na utafiti wa cybersecurity pekee. Matumizi mabaya hayaruhusiwi.

👤 Author
Mr.virus hacker from  🇹🇿
 tested on                                                                                                                       . kali linux 
       . Termux                                                                                                                   . window
