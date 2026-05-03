# Lab Exercise 1 - Failed Login Detector:
print("Checking login attempts...")

login_attempts = [
    ("alice", "success"),
    ("bob", "failed"),
    ("bob", "failed"),
    ("charlie", "success"),
    ("bob", "failed"),
    ("alice", "failed")
]

failed_count = {}

for username, status in login_attempts:
    if status == "failed":
        failed_count[username] = failed_count.get(username, 0) + 1

for user, count in failed_count.items():
    if count >= 3:
        print(f"ALERT: User '{user}' has {count} failed login attempts")

print("Security check complete")


# Lab Exercise 2 - Lab Exercise 2 - Port Security Scanner:
print("Scanning network devices...")

devices = [
    ("192.168.1.10", [22, 80, 443]),
    ("192.168.1.11", [21, 22, 80]),
    ("192.168.1.12", [23, 80, 3389])
]

risky_ports = [21, 23, 3389]

risk_count = 0

for ip, ports in devices:
    for port in ports:
        if port in risky_ports:
            print(f"WARNING: {ip} has risky port {port} open")
            risk_count += 1  

print(f"Scan complete: {risk_count} security risks found")


# Lab Exercise 3 - Password Policy Validator:
print("Validating passwords...")

passwords = [
    "Pass123",
    "SecurePassword1",
    "week",
    "MyPassword",
    "NOLOWER123"
]

compliant = 0
non_compliant = 0

for pwd in passwords:

    length_ok = len(pwd) >= 8
    has_upper = any(ch.isupper() for ch in pwd)
    has_lower = any(ch.islower() for ch in pwd)
    has_digit = any(ch.isdigit() for ch in pwd)
    

    if length_ok and has_upper and has_lower and has_digit:
        print(f"PASS: '{pwd}' - Meets all requirements")
        compliant += 1
    else:

        errors = []
        if not length_ok:
            errors.append("Too short")
        if not has_upper:
            errors.append("No uppercase")
        if not has_lower:
            errors.append("No lowercase")
        if not has_digit:
            errors.append("No digits")

        error_msg = ", ".join(errors)
        print(f"FAIL: '{pwd}' - {error_msg}")
        non_compliant += 1


print(f"Summary: {compliant} compliant, {non_compliant} non-compliant")