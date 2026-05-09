# Metasploitable 2 Attack Chain Report
**Date:** 8 May 2026  
**Author:** Davinson Ezejesi  
**Classification:** Training Lab — Authorised Testing Only

---

## Target

| Field | Value |
|-------|-------|
| IP Address | 10.0.2.3 |
| Hostname | metasploitable.localdomain |
| OS | Ubuntu 8.04 (Hardy Heron) |
| Kernel | Linux 2.6.24-16-server |
| Architecture | i686 (32-bit) |
| Source | `uname -a` output from shell session |

---

## Reconnaissance — Phase 2 Data Used

The following specific services identified during Phase 2 Nmap 
scanning directly enabled this week's exploitation:

**Port 21 — vsftpd 2.3.4**  
Nmap's -sV flag identified the exact version string. Version 2.3.4 
is the specific release that contained the backdoor inserted into 
the official distribution. Without the version number, the correct 
Metasploit module could not have been selected.

**Port 139/445 — Samba smbd 3.0.20-Debian**  
Nmap identified the Samba version running NetBIOS on port 139. 
Version 3.0.20 falls within the range affected by CVE-2007-2447 
(versions 3.0.0 through 3.0.25rc3). The version string made this 
exploitable without guesswork.

**Port 22 — OpenSSH 4.7p1**  
Identified for potential future exploitation. Not used this week 
but documented for Phase 5 credential-based access using cracked 
passwords from /etc/shadow.

**Port 3306 — MySQL 5.0.51a**  
Identified as running as root process (confirmed in ps aux). 
SQL injection or direct MySQL exploitation would yield root 
access. Documented for Phase 5.

**Port 5432 — PostgreSQL 8.3**  
Identified and confirmed running. PostgreSQL has a known 
Metasploit module for default credential access. Documented.

**Port 6697 — UnrealIRCd 3.2.8.1**  
Identified during Phase 2 CVE research as CVE-2010-2075 — 
the same class of backdoor vulnerability as vsftpd. Documented 
for Phase 5 exploitation.

**Critical reconnaissance insight:** The combination of exact 
version numbers from -sV scanning and the -sC default scripts 
produced sufficient intelligence to select working exploits for 
two separate services before a single exploit was attempted. 
Reconnaissance quality determined exploitation success.

---

## Exploit 1: vsftpd 2.3.4 Backdoor

**Module:** `exploit/unix/ftp/vsftpd_234_backdoor`  
**CVE:** CVE-2011-2523  
**Date:** 5 May 2026  
**Duration:** Under 3 minutes from msfconsole load to root shell

### Why It Worked

vsftpd (Very Secure FTP Daemon) is legitimate open-source FTP 
server software. In July 2011, an unknown attacker compromised 
the official vsftpd download server at vsftpd.beasts.org and 
replaced the vsftpd 2.3.4 source code archive with a modified 
version containing a backdoor.

The backdoor was inserted into the authentication handling code. 
When a client sends a username containing the characters :) 
(a colon followed by a closing parenthesis — a smiley face), 
the backdoored code triggers a hidden function that opens a 
listening shell on port 6200 of the server. The FTP service 
continues to function normally, making detection by casual 
observation impossible.

This is a supply chain attack. The software was not vulnerable 
by design flaw — it was deliberately tampered with before 
administrators downloaded and installed it. Administrators who 
verified checksums against the compromised server's own listed 
checksums received incorrect verification (the attacker updated 
the checksums to match the backdoored version).

**Two-stage process:**  
Stage 1: Metasploit connects to port 21, sends :) username, 
backdoor opens shell on port 6200, Metasploit connects to 6200.  
Stage 2: Meterpreter reverse_tcp payload delivered through port 
6200 — target initiates outbound connection to Kali:4444.  
LHOST required for Stage 2 because the Meterpreter payload is 
a reverse shell that must call home.

### Result
Immediate root access. No privilege escalation required.

### Why Root Was Obtained Immediately

vsftpd was running as the root user (UID 0) due to a 
misconfiguration. The spawned shell inherited vsftpd's process 
permissions. Correct practice: run services as dedicated 
low-privilege accounts so exploitation yields restricted access, 
not root.

### Phase 3 Malware Connection

**Trojan.** vsftpd 2.3.4 performs its stated legitimate function 
(FTP file transfer) while simultaneously executing hidden 
malicious code (the backdoor). This matches the trojan definition 
exactly: malware disguised as or embedded within legitimate 
software, providing hidden functionality the user did not 
consent to. The Meterpreter payload is also trojan behaviour — 
masquerading as a normal process in memory while maintaining 
a covert communication channel to the attacker.

Secondary classification: **Supply Chain Attack** — the malware 
was inserted before distribution, not after installation.

---

## Exploit 2: Samba usermap_script

**Module:** `exploit/multi/samba/usermap_script`  
**CVE:** CVE-2007-2447  
**Date:** 6 May 2026  
**Payload used:** `cmd/unix/reverse`

### Why It Worked

Samba is software that allows Linux systems to share files and 
printers with Windows machines using the SMB protocol. Samba's 
configuration file supports an optional feature called 
`username map script` — a script the administrator can define 
to translate Windows usernames to Linux usernames during 
authentication.

The vulnerability is that Samba version 3.0.0 through 3.0.25rc3 
passed the client-supplied username directly to the map script 
handler without sanitising it. An attacker can inject shell 
metacharacters — specifically the backtick character or $() — 
into the username field. When Samba processes this username 
through its script handler, the OS shell executes the injected 
commands with root privileges.

This is command injection. The attacker's input was treated as 
executable code rather than as data.

### Why LHOST Was Required

The Samba exploit injects a netcat command that makes the TARGET 
initiate an outbound TCP connection to the attacker's machine. 
The target cannot connect back without knowing the destination 
address. LHOST provides that destination — the attacker's Kali 
IP (10.0.2.6).

This is a pure reverse shell. The target calls home. The 
attacker's Kali opens a listener on port 4444 before running 
the exploit and waits for the incoming connection.

Contrast with vsftpd Stage 1: the vsftpd trigger makes the 
attacker connect TO the target's new port 6200. For Samba, 
the target connects TO the attacker's port 4444. Direction 
is opposite.

Reverse shells bypass firewalls because most firewalls block 
unsolicited incoming connections but allow servers to make 
outbound connections freely.

### Double Handler

The cmd/unix/reverse payload used two connections:
- Connection A: commands flow from Kali to target
- Connection B: output flows from target to Kali

Metasploit verified both connections were correctly linked 
using an echo verification string (DugYadpzDTIvVmbT) before 
joining the channels.

### Result and Privilege Evidence
Root access on first attempt. Samba was running as root — 
same misconfiguration as vsftpd. UID 0 and GID 0 confirmed 
by the `id` command which queries the kernel directly for 
the current process's credentials.

### Phase 3 Malware Connection

**Trojan / Remote Access Trojan (RAT).** The netcat reverse 
shell established by cmd/unix/reverse creates a persistent 
covert command channel disguised as normal network traffic. 
The Samba service continues to function normally — file 
sharing appears uninterrupted — while the backdoor channel 
operates silently. This is the defining characteristic of a 
RAT: the legitimate function continues while the malicious 
channel persists in the background.

---

## Post-Exploitation Findings

### Shell Upgrade

**Command:** `python -c 'import pty; pty.spawn("/bin/bash")'`

A raw reverse shell lacks a PTY (pseudo-terminal). Without 
upgrade: tab completion fails, arrow keys print escape 
characters, Ctrl+C kills the entire session, interactive 
programs like su/passwd/ssh refuse to run. The Python pty 
module allocates a proper terminal and spawns bash inside it, 
producing a fully interactive session with the prompt 
`root@metasploitable:/#`

**Defender indicator:** This exact command string is visible 
in `ps aux` output. Any process monitor or SIEM correlating 
`python -c.*pty.spawn` following an FTP or SMB session is 
a high-confidence intrusion indicator.

### /root/.bash_history

The file exists and was accessible because I have root 
privileges. It contained the command history for the root 
account, revealing what operations have been performed on 
this machine by previous users. In a real engagement this 
file reveals: database credentials typed directly into 
terminal, SSH commands showing internal IP addresses of 
other systems, script execution patterns indicating how 
the machine is managed and what automation exists.

### /etc/shadow

Contains password hashes for all 30+ user accounts on 
the system. Root hash: `$1$/avpfBJ1$xOz8W5UF9Iv./DR9E9Lid.`

The `$1$` prefix identifies MD5 hashing — an algorithm 
that produces approximately 60 billion hash checks per 
second on modern GPU hardware. The rockyou.txt wordlist 
(14 million common passwords) would be exhausted in under 
one second against MD5 hashes.

**Next step (Phase 5):**
```bash
# On Kali — save hash and crack offline
echo 'root:$1$/avpfBJ1$xOz8W5UF9Iv./DR9E9Lid.' > hashes.txt
hashcat -m 500 hashes.txt /usr/share/wordlists/rockyou.txt
```

Cracked passwords enable legitimate SSH login — harder to 
detect than maintaining an exploit session, and passwords 
may be reused on other systems.

### SUID Binaries

Found 30+ SUID binaries. Most significant:

| Binary | Why Significant |
|--------|----------------|
| `/usr/bin/nmap` | Old nmap + `--interactive` + `!sh` = root shell |
| `/usr/bin/sudo` | Misconfigured rules could grant root |
| `/usr/bin/at` | Command scheduler — can queue root commands |
| `/usr/bin/passwd` | Needs SUID to write /etc/shadow |
| `/usr/lib/openssh/ssh-keysign` | SSH key operations run as root |

SUID (Set User ID) makes a binary execute with its owner's 
permissions instead of the caller's. If root owns it and 
SUID is set, any user executing it temporarily becomes root. 
This is the primary local privilege escalation vector — 
starting as a low-privilege user and reaching root through 
a vulnerable SUID binary.

### Most Significant Finding

The combination of every major service running as root 
(vsftpd, smbd, apache2, mysqld, unrealircd) means that 
exploiting any single service immediately yields root 
access with no privilege escalation required. This is a 
systemic architectural failure, not an isolated 
misconfiguration. In a real organisation, this single 
finding would constitute a Critical severity finding in 
the pentest report requiring immediate remediation before 
any other finding.

---

## ATT&CK Techniques Used

| Technique ID | Name | When Used |
|-------------|------|-----------|
| T1595 | Active Scanning | Phase 2 Nmap -sV -sC -p- |
| T1590.002 | DNS | dig, nslookup in Phase 2 |
| T1190 | Exploit Public-Facing Application | vsftpd + Samba exploits |
| T1059 | Command and Scripting Interpreter | Shell execution throughout |
| T1548.001 | SUID and SGID | find -perm -4000 enumeration |
| T1087.001 | Account Discovery: Local Account | cat /etc/passwd |
| T1003.008 | Credential Dumping: /etc/shadow | cat /etc/shadow |
| T1049 | System Network Connections Discovery | netstat -tulnp |
| T1057 | Process Discovery | ps aux |
| T1083 | File and Directory Discovery | find, ls /home, ls /root |
| T1552.001 | Credentials In Files | find *.conf readable |
| T1140 | Deobfuscate/Decode Files | Password hash analysis |

---

## Blue Team Perspective

A SIEM or Wazuh deployment monitoring this network would 
generate the following alerts in chronological order:

**Alert 1 — FTP anomalous username (HIGH)**  
Snort/Suricata signature SID 2001578 matches vsftpd :) 
backdoor username. Timestamp: 11:38. Source: 10.0.2.6.

**Alert 2 — New listening port opened (MEDIUM)**  
Port 6200 was not present before the attack. Auditd 
would log the socket() and bind() syscalls creating it. 
Process: SONhKaoVAoKS (random name — already suspicious).

**Alert 3 — Outbound connection from server (HIGH)**  
Metasploitable (10.0.2.3) initiated an outbound TCP 
connection to 10.0.2.6:4444. Servers do not initiate 
outbound connections to client machines. Egress filtering 
would block this; if not, the SIEM should alert.

**Alert 4 — Shell upgrade pattern (HIGH)**  
Process `python -c 'import pty; pty.spawn("/bin/bash")'` 
created as child of FTP/SMB process. Python spawning bash 
from a network service process is a known intrusion 
indicator. Wazuh rules file_integrity monitoring + 
process creation monitoring catches this.

**Alert 5 — Rapid file access pattern (CRITICAL)**  
Sequential access to /etc/passwd, /etc/shadow, 
/root/.bash_history within 60 seconds matches credential 
dumping behaviour. Wazuh's audit.log integration would 
capture each file open() syscall.

**Alert 6 — SUID enumeration (MEDIUM)**  
find / -perm -4000 generates thousands of syscalls across 
the entire filesystem. This pattern is detectable through 
auditd rules monitoring mass stat() calls.

**Alert 7 — SMB anomalous username (HIGH)**  
Samba received a username containing shell metacharacters. 
Samba logs record authentication attempts including 
malformed usernames. Wazuh's Samba log decoder parses this.

**Defender conclusion:** This attack would have generated 
seven distinct alerts across four different log sources 
(FTP logs, network connection logs, process logs, file 
access logs). A SOC analyst reviewing any one of these 
should initiate incident response. A SIEM correlating 
all seven within a 90-minute window is a confirmed 
intrusion requiring immediate isolation.

---

## What I Understand Now That I Did Not Before

Phase 3 taught me malware types as definitions to memorise. 
This week I executed a trojan (vsftpd backdoor), delivered 
a RAT (Meterpreter), performed credential dumping, and 
conducted post-exploitation enumeration — and understood 
exactly which malware category each action belonged to 
while doing it. The definitions became actions.

I also understand that reconnaissance quality is what made 
exploitation possible. The Nmap -sV output from Phase 2 
provided the exact version strings that matched specific 
CVEs. Without version identification, I would have 
needed to guess or try every available module. The Phase 2 
investment of time on thorough scanning directly paid off 
in Phase 4 exploitation speed and accuracy.

