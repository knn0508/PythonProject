#!/usr/bin/env python3
"""
Secret Key Generator for Flask Applications
Run this script to generate a secure secret key
"""

import secrets
import string

def generate_secret_key(length=64):
    """Generate a secure secret key"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_hex_key(length=32):
    """Generate a secure hex secret key"""
    return secrets.token_hex(length)

if __name__ == "__main__":
    print("🔐 Flask Secret Key Generator")
    print("=" * 40)
    
    # Generate hex key (recommended)
    hex_key = generate_hex_key(32)
    print(f"Hex Secret Key (64 chars):")
    print(f"SECRET_KEY={hex_key}")
    print()
    
    # Generate alphanumeric key
    alpha_key = generate_secret_key(64)
    print(f"Alphanumeric Secret Key (64 chars):")
    print(f"SECRET_KEY={alpha_key}")
    print()
    
    print("💡 Copy one of the above SECRET_KEY values")
    print("   and set it as an environment variable in Vercel")
