#Exercise 1: Secure User Authentication System
import datetime
import hashlib

#Audit Log
class AuditLog:
    """In-memory audit log for the entire system"""
    _entries = []

    @classmethod
    def write(cls, message):
        timestamp = datetime.datetime.now().isoformat()
        cls._entries.append(f"[{timestamp}] {message}")

    @classmethod
    def show(cls):
        return "\n".join(cls._entries)


#User Class (Secure Authentication)
class User:
    """Represents a system user with authentication, role, and account locking"""

    def __init__(self, username, plain_password, role="standard"):
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Username must be a non-empty string")
        if role not in ("admin", "standard", "guest"):
            raise ValueError("Role must be 'admin', 'standard', or 'guest'")

        self.__username = username.strip()
        self.__role = role
        self.__hashed_password = self.__hash_password(plain_password)
        self.__login_attempts = 0
        self.__account_locked = False

        AuditLog.write(f"User '{self.__username}' created with role '{role}'")

#Private helpers
    def __hash_password(self, plain_password):
        """Hash password using SHA-256"""
        return hashlib.sha256(plain_password.encode()).hexdigest()

#Public getters
    def get_username(self):
        return self.__username

    def get_role(self):
        return self.__role

    def is_admin(self):
        return self.__role == "admin"

    def is_locked(self):
        return self.__account_locked

#Authentication logic
    def authenticate(self, provided_password):
        """Check password, manage attempts, lock after 3 failures"""
        if self.__account_locked:
            AuditLog.write(f"Auth refused - account {self.__username} is locked")
            print(f"Account '{self.__username}' is locked. Contact admin!")
            return False

        provided_hash = self.__hash_password(provided_password)
        if provided_hash == self.__hashed_password:
            self.__login_attempts = 0
            AuditLog.write(f"Successful authentication for {self.__username}")
            return True
        else:
            self.__login_attempts += 1
            AuditLog.write(f"Failed authentication for {self.__username} (attempt #{self.__login_attempts})")
            if self.__login_attempts >= 3:
                self.__account_locked = True
                AuditLog.write(f"Account {self.__username} locked due to 3 failed attempts")
                print(f"Account '{self.__username}' has been locked.")
            return False

    def lock_account(self):
        """Lock the account (can be called by admin or system)"""
        self.__account_locked = True
        AuditLog.write(f"Account {self.__username} locked by system/admin")

    def unlock_account(self, admin_user):
        """Only an admin can unlock an account"""
        if not admin_user.is_admin():
            raise PermissionError("Only admin can unlock accounts")
        self.__account_locked = False
        self.__login_attempts = 0
        AuditLog.write(f"Account {self.__username} unlocked by admin {admin_user.get_username()}")

    def change_privilege(self, new_role, admin_user):
        """Change user role - only admin can do this"""
        if not admin_user.is_admin():
            raise PermissionError("Only admin can change privileges")
        if new_role not in ("admin", "standard", "guest"):
            raise ValueError("Invalid role")
        old_role = self.__role
        self.__role = new_role
        AuditLog.write(f"Privilege for {self.__username} changed from {old_role} to {new_role} by admin {admin_user.get_username()}")

    def get_public_info(self):
        """Return safe, non-sensitive user information"""
        return {
            "username": self.__username,
            "role": self.__role,
            "locked": self.__account_locked
        }


#Demo
if __name__ == "__main__":
#Creating admin and standard user
    admin = User("admin1", "AdminPass123", "admin")
    alice = User("alice", "AliceSecret", "standard")

    print("\nAuthentication tests")
    print(alice.authenticate("wrong"))
    print(alice.authenticate("wrong"))
    print(alice.authenticate("wrong"))
    print(alice.authenticate("AliceSecret"))

    print("\nAdmin unlocks account")
    alice.unlock_account(admin)
    print(alice.authenticate("AliceSecret"))

    print("\nPrivilege escalation (authorised)")
    alice.change_privilege("admin", admin)
    print(f"Alice is now admin? {alice.is_admin()}")

    print("\nPublic info")
    print(admin.get_public_info())
    print(alice.get_public_info())

    print("\nAudit Log")
    print(AuditLog.show())