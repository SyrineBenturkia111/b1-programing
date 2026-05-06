# Exercise 2: IoT Device Management System
import datetime
from datetime import timedelta


class AuditLog:
    _entries = []
    @classmethod
    def write(cls, message):
        timestamp = datetime.datetime.now().isoformat()
        cls._entries.append(f"[{timestamp}] {message}")
    @classmethod
    def show(cls):
        return "\n".join(cls._entries)


class User:
    def __init__(self, username, role):
        self.__username = username
        self.__role = role
    def get_username(self):
        return self.__username
    def is_admin(self):
        return self.__role == "admin"
    def get_public_info(self):
        return {"username": self.__username, "role": self.__role}

#IoT Device Class
class IoTDevice:
    """Represents a device with compliance, quarantine, and ownership"""

    def __init__(self, device_id, owner_user, device_type="sensor"):
        if not isinstance(device_id, str) or not device_id.strip():
            raise ValueError("Device ID must be non-empty")
        if not isinstance(owner_user, User):
            raise ValueError("Owner must be a User instance")

        self.__device_id = device_id.strip()
        self.__owner = owner_user
        self.__device_type = device_type
        self.__quarantined = False
        self.__compromised = False
        self.__last_scan_date = datetime.datetime.now()
        self.__firmware_version = "1.0"

        AuditLog.write(f"Device '{self.__device_id}' created, owner {owner_user.get_username()}")

#Getters
    def get_id(self):
        return self.__device_id

    def get_owner(self):
        return self.__owner

    def is_quarantined(self):
        return self.__quarantined

    def is_compromised(self):
        return self.__compromised

#Compliance logic
    def is_compliant(self):
        """Device is compliant if not quarantined, not compromised, and scanned within 30 days"""
        if self.__quarantined or self.__compromised:
            return False
        days_since_scan = (datetime.datetime.now() - self.__last_scan_date).days
        return days_since_scan <= 30

#Authorised actions
    def perform_security_scan(self, performing_user):
        """Only owner or admin can scan. Updates last scan date"""
        if performing_user != self.__owner and not performing_user.is_admin():
            AuditLog.write(f"Security scan denied on {self.__device_id} by {performing_user.get_username()}")
            raise PermissionError("Only owner or admin can scan this device")
        self.__last_scan_date = datetime.datetime.now()
        AuditLog.write(f"Security scan completed on {self.__device_id} by {performing_user.get_username()}")
        print(f"Device {self.__device_id} scan completed. Compliant: {self.is_compliant()}")
        return True

    def update_firmware(self, new_version, performing_user):
        """Only owner or admin can update firmware"""
        if performing_user != self.__owner and not performing_user.is_admin():
            raise PermissionError("Only owner or admin can update firmware")
        self.__firmware_version = new_version
        self.__last_scan_date = datetime.datetime.now()
        AuditLog.write(f"Device {self.__device_id} firmware updated to {new_version} by {performing_user.get_username()}")

    def quarantine(self, performing_user):
        """Only admin can quarantine a device"""
        if not performing_user.is_admin():
            raise PermissionError("Only admin can quarantine devices")
        self.__quarantined = True
        AuditLog.write(f"Device {self.__device_id} quarantined by admin {performing_user.get_username()}")

    def mark_compromised(self, performing_user):
        """Only admin can mark as compromised (auto‑quarantine)"""
        if not performing_user.is_admin():
            raise PermissionError("Only admin can mark device as compromised")
        self.__compromised = True
        self.__quarantined = True
        AuditLog.write(f"Device {self.__device_id} marked compromised by admin {performing_user.get_username()}")

    def override_compliance(self, admin_user):
        """Admin override for compliance checks (logged)"""
        if not admin_user.is_admin():
            return False
        AuditLog.write(f"Admin {admin_user.get_username()} overrode compliance for {self.__device_id}")
        return True

    def can_access(self, requesting_user):
        """
        Determines if a user can access this device
        - Admin always can (but action is logged)
        - Non‑admin must be owner AND device must be compliant
        """
        if requesting_user.is_admin():
            AuditLog.write(f"Admin {requesting_user.get_username()} accessed device {self.__device_id}")
            return True
        if requesting_user != self.__owner:
            AuditLog.write(f"Access denied for {requesting_user.get_username()} (not owner) to {self.__device_id}")
            return False
        if not self.is_compliant():
            AuditLog.write(f"Access denied – device {self.__device_id} non‑compliant for owner {self.__owner.get_username()}")
            return False
        AuditLog.write(f"Access granted to owner {self.__owner.get_username()} for device {self.__device_id}")
        return True

    def get_public_info(self, requesting_user):
        """Only owner or admin can see device details"""
        if requesting_user != self.__owner and not requesting_user.is_admin():
            return {"error": "Access denied"}
        return {
            "device_id": self.__device_id,
            "type": self.__device_type,
            "owner": self.__owner.get_username(),
            "firmware": self.__firmware_version,
            "quarantined": self.__quarantined,
            "compromised": self.__compromised,
            "last_scan": self.__last_scan_date.strftime("%Y-%m-%d"),
            "compliant": self.is_compliant()
        }


#Demo
if __name__ == "__main__":
#Create users
    admin = User("admin_alice", "admin")
    owner = User("bob", "standard")
    stranger = User("eve", "standard")

#Create device owned by 'bob'
    sensor = IoTDevice("TEMP-01", owner, "temperature")

    print("Initial state")
    print(sensor.get_public_info(owner))

    print("\nOwner access (compliant)")
    print(f"Can owner access? {sensor.can_access(owner)}")

#Simulate 31 days without scan
    sensor._IoTDevice__last_scan_date = datetime.datetime.now() - timedelta(days=31)
    print(f"\nAfter 31 days without scan - compliant? {sensor.is_compliant()}")
    print(f"Owner access now? {sensor.can_access(owner)}")

    print("\nAdmin override compliance")
    if sensor.override_compliance(admin):
        print("Admin override applied - but access still requires owner or admin")
        print(f"Admin access: {sensor.can_access(admin)}")

    print("\nPerform security scan (owner)")
    sensor.perform_security_scan(owner)
    print(f"Compliant after scan? {sensor.is_compliant()}")
    print(f"Owner access now? {sensor.can_access(owner)}")

    print("\nQuarantine by admin")
    sensor.quarantine(admin)
    print(sensor.get_public_info(admin))

    print("\nAudit Log (last 5 entries)")
    log_entries = AuditLog.show().split("\n")
    for entry in log_entries[-5:]:
        print(entry)