# src/auth.py
import bcrypt
import os
from dotenv import load_dotenv
import os.path

# Force load .env from the project root (one folder above src)
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH", "")

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def login(username: str, password: str) -> bool:
    print(f"[DEBUG] Username from env: '{ADMIN_USERNAME}'")
    print(f"[DEBUG] Hash from env (first 20): '{ADMIN_PASSWORD_HASH[:20]}'")
    print(f"[DEBUG] Length of hash: {len(ADMIN_PASSWORD_HASH)}")
    print(f"[DEBUG] Password length: {len(password)}")
    print(f"[DEBUG] Password first 3 chars: '{password[:3]}'")
    print(f"[DEBUG] Password last 3 chars: '{password[-3:]}'")
    
    if username != ADMIN_USERNAME:
        print("[DEBUG] Username mismatch")
        return False
    if not ADMIN_PASSWORD_HASH:
        print("[DEBUG] No hash set – allowing any password")
        return True
    
    result = verify_password(password, ADMIN_PASSWORD_HASH)
    print(f"[DEBUG] Verification result: {result}")
    return result