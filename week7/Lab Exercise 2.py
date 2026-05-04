# Exercise 2: Advanced Server Log Analyzer

LOG_FILE = "server.log"
ERROR_OUT = "error_log.txt"
SECURITY_OUT = "security_incidents.txt"

#Suspicious user agents
SUSPICIOUS = ["sqlmap", "curl", "nmap"]

#Paths indicating login attempts
LOGIN_PATHS = ["/login", "/admin"]

#Storing failed attempts per IP for brute force detection
failed_count = {}

#Lists to hold results
error_entries = []       # for 4xx and 5xx
security_entries = []    # for incidents

try:
    with open(LOG_FILE, "r") as f:
        log_lines = f.readlines()
except FileNotFoundError:
    print(f"Error: {LOG_FILE} not found")
    exit()
except PermissionError:
    print(f"Error: Cannot read File {LOG_FILE}")
    exit()

for line_num, line in enumerate(log_lines, 1):
    line = line.strip()
    if not line:
        continue

    parts = line.split()
    if len(parts) < 10:
        print(f"Line {line_num} has too few fields, skipping.")
        continue
    
#Extracting IP (first part)
    ip = parts[0]
    
#Extracting timestamp (between [ and ])
    timestamp = ""
    if parts[3].startswith("["):
        timestamp = parts[3][1:] + " " + parts[4][:-1]
    
#Extracting method and URL (parts[5] and parts[6])
    method = parts[5][1:]
    url = parts[6]
    
#Extracting status code (parts[8])
    try:
        status = int(parts[8])
    except ValueError:
        status = 0

    user_agent = parts[-1] if len(parts) > 9 else ""
    
# Detecting Error (4xx and 5xx)
    if 400 <= status < 600:
        error_entries.append(f"{ip} - {timestamp} - {method} {url} - {status}")
    
#Security incidents
    incident = None
    
#1. Failed authentication
    if status == 401:
        for path in LOGIN_PATHS:
            if path in url:
                incident = f"FAILED_AUTH: {ip} at {timestamp} - {method} {url}"
                failed_count[ip] = failed_count.get(ip, 0) + 1 #count for brute force
                break
    
#2. Suspicious user agent
    if not incident:
        ua_lower = user_agent.lower()
        for sus in SUSPICIOUS:
            if sus in ua_lower:
                incident = f"SUSPICIOUS_UA: {ip} used '{user_agent}' - {method} {url}"
                break
    
# 3. Internal server error (500)
    if not incident and status == 500:
        incident = f"ERROR_500: {ip} caused server error on {url}"
    
    if incident:
        security_entries.append(incident)

#After processing all lines, we are checking for brute force (e.g 5+ failures from same IP)
for ip, count in failed_count.items():
    if count >= 5:
        security_entries.append(f"BRUTE_FORCE: IP {ip} had {count} failed logins")

#Writing error log
try:
    with open(ERROR_OUT, "w") as f:
        f.write("ERROR LOG (4xx & 5xx codes)\n")
        for entry in error_entries:
            f.write(entry + "\n")
    print(f"Wrote {len(error_entries)} errors to {ERROR_OUT}")
except PermissionError:
    print("Cannot write error_log.txt")

#Writing security incidents
try:
    with open(SECURITY_OUT, "w") as f:
        f.write("SECURITY INCIDENTS\n")
        for inc in security_entries:
            f.write(inc + "\n")
    print(f"Wrote {len(security_entries)} security incidents to {SECURITY_OUT}")
except PermissionError:
    print("Cannot write security_incidents.txt")

#Summary
print("\nThe analysis is complete!")
print(f"Total errors (4xx/5xx): {len(error_entries)}")
print(f"Security incidents: {len(security_entries)}")