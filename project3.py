import json
import os
import secrets
import string
from cryptography.fernet import Fernet
from getpass import getpass
import hashlib

class PasswordManager:
    def __init__(self):
        self.key_file = '.secret.key'
        self.data_file = 'passwords.enc'
        self.master_hash_file = '.master.hash'
        self.key = None
        self.cipher = None
        self.passwords = {}
        
    def setup_master_password(self):
        """Setup or verify master password"""
        if os.path.exists(self.master_hash_file):
            # Verify existing master password
            stored_hash = self._load_master_hash()
            master = getpass("Enter master password: ")
            
            if self._hash_password(master) != stored_hash:
                print("❌ Incorrect master password!")
                return False
        else:
            # Create new master password
            print("First time setup - Create a master password")
            master = getpass("Enter master password: ")
            confirm = getpass("Confirm master password: ")
            
            if master != confirm:
                print("❌ Passwords don't match!")
                return False
            
            self._save_master_hash(master)
            print("✓ Master password created!")
        
        # Initialize encryption
        self._initialize_encryption()
        self.passwords = self._load_passwords()
        return True
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _save_master_hash(self, password: str):
        """Save hashed master password"""
        with open(self.master_hash_file, 'w') as f:
            f.write(self._hash_password(password))
    
    def _load_master_hash(self) -> str:
        """Load stored master password hash"""
        with open(self.master_hash_file, 'r') as f:
            return f.read()
    
    def _initialize_encryption(self):
        """Initialize or load encryption key"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(self.key)
        
        self.cipher = Fernet(self.key)
    
    def _load_passwords(self) -> dict:
        """Load encrypted passwords from file"""
        if not os.path.exists(self.data_file):
            return {}
        
        try:
            with open(self.data_file, 'rb') as f:
                encrypted_data = f.read()
                decrypted_data = self.cipher.decrypt(encrypted_data)
                return json.loads(decrypted_data.decode())
        except Exception as e:
            print(f"Error loading passwords: {e}")
            return {}
    
    def _save_passwords(self):
        """Save encrypted passwords to file"""
        try:
            data = json.dumps(self.passwords, indent=2).encode()
            encrypted_data = self.cipher.encrypt(data)
            
            with open(self.data_file, 'wb') as f:
                f.write(encrypted_data)
        except Exception as e:
            print(f"Error saving passwords: {e}")
    
    def generate_password(self, length: int = 16, 
                         use_symbols: bool = True,
                         use_numbers: bool = True) -> str:
        """Generate a strong random password"""
        chars = string.ascii_letters
        
        if use_numbers:
            chars += string.digits
        if use_symbols:
            chars += string.punctuation
        
        # Ensure at least one of each type
        password = []
        if use_numbers:
            password.append(secrets.choice(string.digits))
        if use_symbols:
            password.append(secrets.choice(string.punctuation))
        password.append(secrets.choice(string.ascii_lowercase))
        password.append(secrets.choice(string.ascii_uppercase))
        
        # Fill the rest
        for _ in range(length - len(password)):
            password.append(secrets.choice(chars))
        
        # Shuffle
        secrets.SystemRandom().shuffle(password)
        return ''.join(password)
    
    def add_password(self, service: str, username: str, 
                    password: str = None):
        """Add or update password for a service"""
        if password is None:
            password = self.generate_password()
            print(f"\n🔑 Generated password: {password}")
        
        self.passwords[service.lower()] = {
            'service': service,
            'username': username,
            'password': password
        }
        self._save_passwords()
        print(f"✓ Password saved for {service}")
    
    def get_password(self, service: str) -> dict:
        """Retrieve password for a service"""
        service_key = service.lower()
        if service_key in self.passwords:
            return self.passwords[service_key]
        return None
    
    def list_services(self):
        """List all stored services"""
        if not self.passwords:
            print("\n📝 No passwords stored yet")
            return
        
        print("\n=== STORED SERVICES ===")
        for i, (key, data) in enumerate(self.passwords.items(), 1):
            print(f"{i}. {data['service']} ({data['username']})")
    
    def delete_password(self, service: str):
        """Delete password for a service"""
        service_key = service.lower()
        if service_key in self.passwords:
            service_name = self.passwords[service_key]['service']
            del self.passwords[service_key]
            self._save_passwords()
            print(f"✓ Password deleted for {service_name}")
        else:
            print(f"❌ No password found for {service}")
    
    def search(self, query: str):
        """Search for services containing query"""
        query_lower = query.lower()
        results = {k: v for k, v in self.passwords.items() 
                  if query_lower in k or query_lower in v['username'].lower()}
        
        if results:
            print(f"\n🔍 Found {len(results)} match(es):")
            for data in results.values():
                print(f"  • {data['service']} ({data['username']})")
        else:
            print("❌ No matches found")
        
        return results
    
    def update_password(self, service: str, new_password: str = None):
        """Update password for existing service"""
        service_key = service.lower()
        if service_key not in self.passwords:
            print(f"❌ Service {service} not found")
            return
        
        if new_password is None:
            new_password = self.generate_password()
            print(f"\n🔑 Generated password: {new_password}")
        
        self.passwords[service_key]['password'] = new_password
        self._save_passwords()
        print(f"✓ Password updated for {self.passwords[service_key]['service']}")
    
    def export_passwords(self, filename: str = 'passwords_backup.json'):
        """Export passwords to unencrypted JSON (use carefully!)"""
        confirm = input("⚠️  This will export passwords unencrypted. Continue? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Export cancelled")
            return
        
        with open(filename, 'w') as f:
            json.dump(self.passwords, f, indent=2)
        print(f"✓ Passwords exported to {filename}")
        print("⚠️  Keep this file secure and delete it after use!")


def main():
    """Main menu for password manager"""
    pm = PasswordManager()
    
    print("="*50)
    print("🔐 SECURE PASSWORD MANAGER")
    print("="*50)
    
    if not pm.setup_master_password():
        return
    
    print("\n✓ Access granted!")
    
    while True:
        print("\n" + "="*50)
        print("1. Add new password")
        print("2. Get password")
        print("3. List all services")
        print("4. Search services")
        print("5. Update password")
        print("6. Delete password")
        print("7. Generate password only")
        print("8. Export passwords (backup)")
        print("9. Exit")
        print("="*50)
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == '1':
            service = input("Service name (e.g., Gmail, Facebook): ")
            username = input("Username/Email: ")
            use_gen = input("Generate password? (y/n): ").lower()
            
            if use_gen == 'y':
                length = input("Password length (default 16): ")
                length = int(length) if length else 16
                pm.add_password(service, username)
            else:
                pwd = getpass("Password: ")
                pm.add_password(service, username, pwd)
        
        elif choice == '2':
            service = input("Service name: ")
            info = pm.get_password(service)
            if info:
                print(f"\n{'='*50}")
                print(f"Service: {info['service']}")
                print(f"Username: {info['username']}")
                print(f"Password: {info['password']}")
                print("="*50)
            else:
                print("❌ Service not found")
        
        elif choice == '3':
            pm.list_services()
        
        elif choice == '4':
            query = input("Search query: ")
            pm.search(query)
        
        elif choice == '5':
            service = input("Service name: ")
            use_gen = input("Generate new password? (y/n): ").lower()
            if use_gen == 'y':
                pm.update_password(service)
            else:
                pwd = getpass("New password: ")
                pm.update_password(service, pwd)
        
        elif choice == '6':
            service = input("Service name to delete: ")
            confirm = input(f"Delete password for {service}? (yes/no): ")
            if confirm.lower() == 'yes':
                pm.delete_password(service)
        
        elif choice == '7':
            length = input("Password length (default 16): ")
            length = int(length) if length else 16
            symbols = input("Include symbols? (y/n): ").lower() == 'y'
            numbers = input("Include numbers? (y/n): ").lower() == 'y'
            password = pm.generate_password(length, symbols, numbers)
            print(f"\n🔑 Generated: {password}")
        
        elif choice == '8':
            pm.export_passwords()
        
        elif choice == '9':
            print("\n🔒 Passwords saved securely. Goodbye!")
            break
        
        else:
            print("❌ Invalid choice! Please try again.")


if __name__ == "__main__":
    main()