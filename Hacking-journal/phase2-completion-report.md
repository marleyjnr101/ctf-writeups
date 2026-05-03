# Phase 2: Networking Essentials — Completion Report
Date completed: 27 April 2026

## Duration
4 weeks, approximately 60 hours

## Skills Demonstrated
OSI Model: I can name all 7 layers, protocols, attacks
Subnetting: I can calculate /24, /26, /28 by hand
TCP/IP: Can identify 3-way handshake in Wireshark
Wireshark: Captured HTTP credentials from live traffic
ARP Poisoning: Executed Bettercap MITM, ARP table 
  poisoned, documented in GitHub writeup
DNS Enumeration: [dig, nslookup, zone transfer, 
  record types]
Service Enumeration: [enum4linux, Nikto, FTP anonymous, 
  MySQL blank root on Metasploitable 2]
Python: [log parser reads files, strings chapter 
  complete, loops and conditionals working]

## Evidence
- Wireshark HTTP credential screenshot: hacking journal
- Bettercap MITM writeup: github.com/marleyjnr101/
  ctf-writeups/phase2-labs/bettercap-mitm-lab.md
- Nmap port inventory: hacking journal
- TryHackMe rooms completed: [4]
- OverTheWire Bandit: Level [7] complete

## ATT&CK Techniques Practised
T1040  — Network Sniffing (Wireshark)
T1557.002 — ARP Cache Poisoning (Bettercap)
T1046  — Network Service Scanning (Nmap)
T1018  — Remote System Discovery (ping sweep)
T1590.002 — DNS Enumeration (dig, zone transfer)
T1135  — Network Share Discovery (enum4linux)

## What Gave Me Trouble
I would say it's the Dns part , not that it was hard but like some things were missing and left me confused at some point

## What I Would Do Differently
I would have never underestimated Over the wire , i have come to understand most of the things done in the terminal all mostly linux command line .