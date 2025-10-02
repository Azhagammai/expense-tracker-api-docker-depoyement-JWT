#!/usr/bin/env python3
"""
Simple test script for the Expense Tracker API
This script tests the main functionality of the API endpoints
"""

import requests
import json
from datetime import datetime, timedelta

# Base URL for the API
BASE_URL = "http://localhost:5000/api"

class APITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.user_id = None
        self.category_id = None
        self.expense_id = None
    
    def test_user_registration(self):
        """Test user registration"""
        print("🧪 Testing User Registration...")
        
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        response = requests.post(f"{self.base_url}/users/register", json=data)
        
        if response.status_code == 201:
            result = response.json()
            self.token = result['data']['token']
            self.user_id = result['data']['user']['_id']
            print("✅ User registration successful")
            print(f"   Token: {self.token[:20]}...")
            return True
        else:
            print(f"❌ User registration failed: {response.text}")
            return False
    
    def test_user_login(self):
        """Test user login"""
        print("\n🧪 Testing User Login...")
        
        data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        response = requests.post(f"{self.base_url}/users/login", json=data)
        
        if response.status_code == 200:
            result = response.json()
            self.token = result['data']['token']
            print("✅ User login successful")
            return True
        else:
            print(f"❌ User login failed: {response.text}")
            return False
    
    def test_create_category(self):
        """Test creating a category"""
        print("\n🧪 Testing Category Creation...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "title": "Groceries",
            "description": "Food and household items"
        }
        
        response = requests.post(f"{self.base_url}/categories", json=data, headers=headers)
        
        if response.status_code == 201:
            result = response.json()
            self.category_id = result['data']['category']['_id']
            print("✅ Category creation successful")
            print(f"   Category ID: {self.category_id}")
            return True
        else:
            print(f"❌ Category creation failed: {response.text}")
            return False
    
    def test_get_categories(self):
        """Test getting all categories"""
        print("\n🧪 Testing Get Categories...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}/categories", headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            categories = result['data']['categories']
            print(f"✅ Retrieved {len(categories)} categories")
            return True
        else:
            print(f"❌ Get categories failed: {response.text}")
            return False
    
    def test_create_expense(self):
        """Test creating an expense"""
        print("\n🧪 Testing Expense Creation...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "amount": 45.50,
            "note": "Weekly grocery shopping",
            "expense_date": datetime.now().isoformat(),
            "category_id": self.category_id
        }
        
        response = requests.post(f"{self.base_url}/expenses", json=data, headers=headers)
        
        if response.status_code == 201:
            result = response.json()
            self.expense_id = result['data']['expense']['_id']
            print("✅ Expense creation successful")
            print(f"   Expense ID: {self.expense_id}")
            print(f"   Amount: ${result['data']['expense']['amount']}")
            return True
        else:
            print(f"❌ Expense creation failed: {response.text}")
            return False
    
    def test_get_expenses(self):
        """Test getting expenses"""
        print("\n🧪 Testing Get Expenses...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}/expenses", headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            expenses = result['data']['expenses']
            print(f"✅ Retrieved {len(expenses)} expenses")
            return True
        else:
            print(f"❌ Get expenses failed: {response.text}")
            return False
    
    def test_expense_filtering(self):
        """Test expense filtering"""
        print("\n🧪 Testing Expense Filtering...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Test past week filter
        response = requests.get(f"{self.base_url}/expenses?filter=past_week&include_summary=true", headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            expenses = result['data']['expenses']
            summary = result['data'].get('summary')
            print(f"✅ Past week filter: {len(expenses)} expenses")
            if summary:
                print(f"   Total amount: ${summary['total_amount']}")
            return True
        else:
            print(f"❌ Expense filtering failed: {response.text}")
            return False
    
    def test_update_expense(self):
        """Test updating an expense"""
        print("\n🧪 Testing Expense Update...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "amount": 55.75,
            "note": "Updated grocery shopping expense"
        }
        
        response = requests.put(f"{self.base_url}/expenses/{self.expense_id}", json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Expense update successful")
            print(f"   New amount: ${result['data']['expense']['amount']}")
            return True
        else:
            print(f"❌ Expense update failed: {response.text}")
            return False
    
    def test_expense_summary(self):
        """Test expense summary"""
        print("\n🧪 Testing Expense Summary...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}/expenses/summary", headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            summary = result['data']['summary']
            print("✅ Expense summary retrieved")
            print(f"   Total amount: ${summary['total_amount']}")
            print(f"   Total count: {summary['total_count']}")
            return True
        else:
            print(f"❌ Expense summary failed: {response.text}")
            return False
    
    def test_delete_expense(self):
        """Test deleting an expense"""
        print("\n🧪 Testing Expense Deletion...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.delete(f"{self.base_url}/expenses/{self.expense_id}", headers=headers)
        
        if response.status_code == 200:
            print("✅ Expense deletion successful")
            return True
        else:
            print(f"❌ Expense deletion failed: {response.text}")
            return False
    
    def test_delete_category(self):
        """Test deleting a category"""
        print("\n🧪 Testing Category Deletion...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.delete(f"{self.base_url}/categories/{self.category_id}", headers=headers)
        
        if response.status_code == 200:
            print("✅ Category deletion successful")
            return True
        else:
            print(f"❌ Category deletion failed: {response.text}")
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Expense Tracker API Tests...\n")
        
        tests = [
            self.test_user_registration,
            self.test_user_login,
            self.test_create_category,
            self.test_get_categories,
            self.test_create_expense,
            self.test_get_expenses,
            self.test_expense_filtering,
            self.test_update_expense,
            self.test_expense_summary,
            self.test_delete_expense,
            self.test_delete_category
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except requests.exceptions.ConnectionError:
                print(f"❌ Connection error: Make sure the API server is running on {self.base_url}")
                failed += 1
            except Exception as e:
                print(f"❌ Unexpected error in {test.__name__}: {str(e)}")
                failed += 1
        
        print(f"\n📊 Test Results:")
        print(f"   ✅ Passed: {passed}")
        print(f"   ❌ Failed: {failed}")
        print(f"   📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        if failed == 0:
            print("\n🎉 All tests passed! The API is working correctly.")
        else:
            print(f"\n⚠️  {failed} test(s) failed. Please check the API implementation.")

def main():
    """Main function to run the tests"""
    print("Expense Tracker API Test Suite")
    print("=" * 50)
    
    tester = APITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
