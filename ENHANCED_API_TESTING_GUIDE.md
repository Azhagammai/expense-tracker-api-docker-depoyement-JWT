# 🎯 ENHANCED EXPENSE TRACKER API - TESTING GUIDE
## With Monthly Income & Savings Calculation

## 🚀 **NEW FEATURES ADDED**

✅ **Monthly Income Tracking** - Set and track monthly income  
✅ **Savings Calculation** - Calculate savings based on income vs expenses  
✅ **Expense Analysis** - Breakdown by categories with amounts  
✅ **Financial Summary** - Complete monthly financial overview  

## 📋 **COMPLETE TESTING SEQUENCE**

### **Step 1: Start the Enhanced API**
```bash
python simple_working_api.py
```

### **Step 2: Health Check**
**GET** `http://127.0.0.1:5000/health`

### **Step 3: Register User**
**POST** `http://127.0.0.1:5000/api/users/register`

**Headers:**
- `Content-Type: application/json`

**Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "securepass123"
}
```

**📌 COPY THE TOKEN** from response!

### **Step 4: Create Categories**
**POST** `http://127.0.0.1:5000/api/categories`

**Headers:**
- `Content-Type: application/json`
- `Authorization: Bearer YOUR_TOKEN_HERE`

**Body:**
```json
{
  "title": "Groceries",
  "description": "Food and household items"
}
```

**Repeat for all categories:**
- Leisure
- Electronics
- Utilities
- Clothing
- Health
- Others

### **Step 5: Set Monthly Income**
**POST** `http://127.0.0.1:5000/api/income`

**Headers:**
- `Content-Type: application/json`
- `Authorization: Bearer YOUR_TOKEN_HERE`

**Body:**
```json
{
  "amount": 5000.00
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Monthly income set successfully",
  "data": {
    "income": {
      "amount": 5000.00,
      "month": "2025-10"
    }
  }
}
```

### **Step 6: Create Expenses**
**POST** `http://127.0.0.1:5000/api/expenses`

**Headers:**
- `Content-Type: application/json`
- `Authorization: Bearer YOUR_TOKEN_HERE`

**Body:**
```json
{
  "amount": 150.00,
  "note": "Weekly grocery shopping",
  "expense_date": "2025-10-01T10:00:00Z",
  "category_id": "CATEGORY_ID_FROM_STEP_4"
}
```

**Create multiple expenses:**
```json
// Expense 2
{
  "amount": 75.00,
  "note": "Movie tickets",
  "expense_date": "2025-10-02T19:00:00Z",
  "category_id": "LEISURE_CATEGORY_ID"
}

// Expense 3
{
  "amount": 200.00,
  "note": "Electricity bill",
  "expense_date": "2025-10-03T00:00:00Z",
  "category_id": "UTILITIES_CATEGORY_ID"
}

// Expense 4
{
  "amount": 300.00,
  "note": "New laptop",
  "expense_date": "2025-10-04T14:00:00Z",
  "category_id": "ELECTRONICS_CATEGORY_ID"
}
```

### **Step 7: Get Monthly Income**
**GET** `http://127.0.0.1:5000/api/income`

**Headers:**
- `Authorization: Bearer YOUR_TOKEN_HERE`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "income": {
      "amount": 5000.00,
      "month": "2025-10"
    }
  }
}
```

### **Step 8: Calculate Savings**
**GET** `http://127.0.0.1:5000/api/savings`

**Headers:**
- `Authorization: Bearer YOUR_TOKEN_HERE`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "monthly_summary": {
      "month": "2025-10",
      "income": 5000.00,
      "total_expenses": 725.00,
      "savings": 4275.00,
      "savings_percentage": 85.5
    },
    "expense_breakdown": {
      "total_count": 4,
      "categories": {
        "CATEGORY_ID_1": {
          "amount": 150.00,
          "count": 1,
          "category_name": "Groceries"
        },
        "CATEGORY_ID_2": {
          "amount": 75.00,
          "count": 1,
          "category_name": "Leisure"
        },
        "CATEGORY_ID_3": {
          "amount": 200.00,
          "count": 1,
          "category_name": "Utilities"
        },
        "CATEGORY_ID_4": {
          "amount": 300.00,
          "count": 1,
          "category_name": "Electronics"
        }
      }
    }
  }
}
```

## 🎯 **NEW API ENDPOINTS**

### **Income Management**
- **POST** `/api/income` - Set monthly income
- **GET** `/api/income` - Get current month's income

### **Savings Calculation**
- **GET** `/api/savings` - Calculate savings and financial summary

## 📊 **FEATURES DEMONSTRATED**

### **1. Monthly Income Tracking**
- Set monthly income amount
- Track income by month
- Update income as needed

### **2. Savings Calculation**
- **Formula:** `Savings = Monthly Income - Total Expenses`
- **Percentage:** `Savings % = (Savings / Income) * 100`
- **Real-time calculation** based on current month

### **3. Expense Analysis**
- **Total expenses** by month
- **Category breakdown** with amounts and counts
- **Category names** for better understanding
- **Expense count** per category

### **4. Financial Summary**
- **Monthly overview** with income, expenses, savings
- **Savings percentage** for financial health
- **Category-wise spending** analysis
- **Complete financial picture**

## 🎉 **INTERVIEW DEMONSTRATION**

### **Complete Flow:**
1. **Register User** → Get JWT token
2. **Create Categories** → Set up expense categories
3. **Set Monthly Income** → $5000/month
4. **Add Expenses** → Multiple expenses in different categories
5. **Calculate Savings** → See financial summary

### **Results Shown:**
- **Income:** $5000.00
- **Total Expenses:** $725.00
- **Savings:** $4275.00
- **Savings %:** 85.5%
- **Category Breakdown:** Groceries, Leisure, Utilities, Electronics

## 🚀 **YOU'RE READY!**

Your enhanced API now includes:
- ✅ **Monthly Income Tracking**
- ✅ **Savings Calculation**
- ✅ **Expense Analysis by Category**
- ✅ **Financial Summary Reports**
- ✅ **All Original Features** (JWT, CRUD, Filtering)

**Test the complete flow in Postman and demonstrate the financial management capabilities!** 🎯
