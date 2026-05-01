import sys

filename = sys.argv[1]
count = 0
success = 0
unique_ips = []

with open (filename,"r") as f:
    for line in f:
        line = line.strip()
        if "404" in line:
            count += 1
            ip = line.split()[0]
            if ip not in unique_ips:
             unique_ips.append(ip)
        if "200 " in line:
                success += 1
                   
print(f"count: {count}")          
print(f"unique_ips : {len(unique_ips)}")
for ip in unique_ips:
    
 print(f"     - {ip}")
print (f"200 response:  {success}")