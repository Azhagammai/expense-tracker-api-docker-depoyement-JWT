#!/usr/bin/env python3
"""
JWT Secret Key Generator for Expense Tracker API
This script generates secure secret keys for JWT authentication
"""

import secrets
import string
import hashlib
import os

def generate_url_safe_key(length=32):
    """Generate a URL-safe secret key"""
    return secrets.token_urlsafe(length)

def generate_hex_key(length=32):
    """Generate a hexadecimal secret key"""
    return secrets.token_hex(length)

def generate_custom_key(length=64):
    """Generate a custom secret key with mixed characters"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_from_passphrase(passphrase):
    """Generate a key from a passphrase using SHA-256"""
    return hashlib.sha256(passphrase.encode()).hexdigest()

def main():
    print("JWT Secret Key Generator")
    print("=" * 50)
    
    print("\n1. URL-Safe Key (32 bytes - Recommended):")
    key1 = generate_url_safe_key(32)
    print(f"   {key1}")
    
    print("\n2. URL-Safe Key (64 bytes - Extra Secure):")
    key2 = generate_url_safe_key(64)
    print(f"   {key2}")
    
    print("\n3. Hexadecimal Key (32 bytes):")
    key3 = generate_hex_key(32)
    print(f"   {key3}")
    
    print("\n4. Custom Mixed Key (64 characters):")
    key4 = generate_custom_key(64)
    print(f"   {key4}")
    
    print("\nHow to use:")
    print("1. Copy one of the keys above")
    print("2. Set it in your environment or config.py:")
    print("   JWT_SECRET_KEY='your_key_here'")
    
    print("\nEnvironment Variable Format:")
    print(f"JWT_SECRET_KEY={key1}")
    
    print("\nSecurity Tips:")
    print("- Never commit secret keys to version control")
    print("- Use different keys for development and production")
    print("- Store keys securely (environment variables, secrets manager)")
    print("- Rotate keys periodically in production")

if __name__ == "__main__":
    main()
