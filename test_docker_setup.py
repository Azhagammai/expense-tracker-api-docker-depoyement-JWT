#!/usr/bin/env python3
"""
Test Docker setup for Expense Tracker API
"""

import requests
import time
import subprocess
import sys

def test_docker_setup():
    print("Testing Docker Setup for Expense Tracker API")
    print("=" * 60)
    
    # Test 1: Check if Docker is running
    print("1. Checking Docker...")
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   SUCCESS: {result.stdout.strip()}")
        else:
            print("   FAILED: Docker not available")
            return False
    except Exception as e:
        print(f"   FAILED: {e}")
        return False
    
    # Test 2: Check if docker-compose is available
    print("\n2. Checking Docker Compose...")
    try:
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   SUCCESS: {result.stdout.strip()}")
        else:
            print("   FAILED: Docker Compose not available")
            return False
    except Exception as e:
        print(f"   FAILED: {e}")
        return False
    
    # Test 3: Check if required files exist
    print("\n3. Checking required files...")
    required_files = [
        'Dockerfile',
        'docker-compose.yml',
        'mongodb_api.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        try:
            with open(file, 'r') as f:
                print(f"   SUCCESS: {file} exists")
        except FileNotFoundError:
            print(f"   FAILED: {file} missing")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n   Missing files: {', '.join(missing_files)}")
        return False
    
    print("\n4. Docker setup is ready!")
    print("\nTo deploy your API:")
    print("   docker-compose up --build -d")
    print("\nTo test the API:")
    print("   curl http://localhost:5000/health")
    print("\nTo stop the API:")
    print("   docker-compose down")
    
    return True

if __name__ == "__main__":
    success = test_docker_setup()
    if success:
        print("\nDocker setup is ready for deployment!")
    else:
        print("\nDocker setup has issues. Please check the errors above.")
        sys.exit(1)
