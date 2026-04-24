# Bettercap MITM Lab - ARP Cache Poisoning 
**Date :** 16 April 2026
**Target : ** Metasploitable 2 (10.0.2.3)
**Attacker : ** Kali Linux
**Environment : ** VirtualBox NAT Network

## Objective
Execute an ARP cache poisoning attack to intercept HTTP credentials from a target machine.

## What I Did
I first opened a kali machine scanned to find how many host machines were up using nmap -sn 10.0.2.3/24 .The I went and ran bettercap on kali with sudo bettercap -iface eth0.then went ahead with net.probe on and net.show,which showed in a diagram or table formatte the Mac address of every machine on the network .Then went ahead with set arp.spoof.fullduplex true , set arp.spoof.targets 10.0.2.3 ,arp.spoof on ,net.sniff on .

## Result
since it was a metaspoitable Vm I could not capture much .when I went to its terminal and typed arp -a , I saw the exact result that metasploit gave me in my bettercap terminal although I opened another terminal in kail and accessed a http website it did not show on my bettercap terminal so i came to a conclusion that the lab was a success . If I had used a windows Vm as the target, I would have captured the login credentials.

## Why It Worked
ARP (Address Resolution Protocol) maps IP addresses to MAC addresses on a local network.It has no authentication ,any device can send an ARP reply claiming any MAC address.Bettercap exploited this by sending false ARP replies to the target,making it believe my Kali machine as the network gateway.All target traffic routed through me before reaching its destination.

## MITRE ATT&CK Mapping
- T1557.002 - Adversary-in-the-Middle: ARP Cache Poisoning
- T1040 - Network Sniffing

## Blue Team Detection
A defender would detect this by:
- Monitoring for duplicate ARP replies from different MACs claiming he same IP
- Wazuh ARP anomaly detection rules 
- Wireshark filter: arp.duplicate-address-detected

## Lessons Learned
even though Arp poisoning only affects the layer 2 network,its biggest weak point is that it has no authentication 