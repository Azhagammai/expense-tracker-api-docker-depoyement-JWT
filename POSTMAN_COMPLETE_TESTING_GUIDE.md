# POSTMAN TESTING GUIDE - EXPENSE TRACKER API

## 🎯 Complete Testing Guide for Interview Requirements

This guide shows you exactly how to test the Expense Tracker API with Postman to meet all interview requirements.

## 📋 API Requirements Checklist

✅ **User Authentication with JWT**  
✅ **User Signup Functionality**  
✅ **JWT Token Generation & Validation**  
✅ **Expense Filtering (Past week, Last month, Last 3 months, Custom dates)**  
✅ **Expense CRUD Operations (Add, Remove, Update, List)**  
✅ **JWT Protection on ALL endpoints**  
✅ **Predefined Categories (Groceries, Leisure, Electronics, Utilities, Clothing, Health, Others)**  
✅ **MongoDB Data Persistence**  

## 🚀 Getting Started

### Step 1: Start the API Server
```bash
# In your terminal, run:
python mongodb_api.py
```

The server will start on: `http://127.0.0.1:5000`

### Step 2: Open Postman
Create a new collection called "Expense Tracker API"

---

## 📝 POSTMAN TESTING SEQUENCE

### 1. HEALTH CHECK (No Authentication Required)

**Request:**
- Method: `GET`
- URL: `http://127.0.0.1:5000/health`
- Headers: None

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "API is operational",
  "database": "MongoDB Connected",
  "data_counts": {
    "users": 0,
    "categories": 0,
    "expenses": 0
  }
}
```

---

### 2. USER REGISTRATION (Signup Functionality)

**Request:**
- Method: `POST`
- URL: `http://127.0.0.1:5000/api/users/register`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": "64f8a1b2c3d4e5f6a7b8c9d0",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com"
    },
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

**📌 IMPORTANT:** Copy the `token` from this response - you'll need it for all other requests!

---

### 3. USER LOGIN (JWT Authentication)

**Request:**
- Method: `POST`
- URL: `http://127.0.0.1:5000/api/users/login`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
```json
{
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "user": {
      "id": "64f8a1b2c3d4e5f6a7b8c9d0",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com"
    },
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

---

### 4. CREATE CATEGORY (JWT Protected)

**Request:**
- Method: `POST`
- URL: `http://127.0.0.1:5000/api/categories`
- Headers: 
  - `Content-Type: application/json`
  - `Authorization: Bearer YOUR_TOKEN_HERE`
- Body (raw JSON):
```json
{
  "title": "Groceries",
  "description": "Food and household items"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Category created successfully",
  "data": {
    "category": {
      "id": "64f8a1b2c3d4e5f6a7b8c9d1",
      "title": "Groceries",
      "description": "Food and household items",
      "user_id": "64f8a1b2c3d4e5f6a7b8c9d0",
      "created_at": "2025-10-02T10:30:00.000Z"
    }
  }
}
```

**📌 IMPORTANT:** Copy the `category.id` from this response - you'll need it for creating expenses!

**Test with all predefined categories:**
- Groceries ✅
- Leisure
- Electronics
- Utilities
- Clothing
- Health
- Others

---

### 5. GET CATEGORIES (JWT Protected)

**Request:**
- Method: `GET`
- URL: `http://127.0.0.1:5000/api/categories`
- Headers: `Authorization: Bearer YOUR_TOKEN_HERE`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "categories": [
      {
        "id": "64f8a1b2c3d4e5f6a7b8c9d1",
        "title": "Groceries",
        "description": "Food and household items",
        "user_id": "64f8a1b2c3d4e5f6a7b8c9d0",
        "created_at": "2025-10-02T10:30:00.000Z"
      }
    ],
    "available_categories": [
      "Groceries", "Leisure", "Electronics", "Utilities", 
      "Clothing", "Health", "Others"
    ]
  }
}
```

---

### 6. CREATE EXPENSE (JWT Protected)

**Request:**
- Method: `POST`
- URL: `http://127.0.0.1:5000/api/expenses`
- Headers: 
  - `Content-Type: application/json`
  - `Authorization: Bearer YOUR_TOKEN_HERE`
- Body (raw JSON):
```json
{
  "amount": 25.50,
  "note": "Grocery shopping at Walmart",
  "expense_date": "2025-10-02T10:00:00Z",
  "category_id": "64f8a1b2c3d4e5f6a7b8c9d1"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Expense created successfully",
  "data": {
    "expense": {
      "id": "64f8a1b2c3d4e5f6a7b8c9d2",
      "amount": 25.50,
      "note": "Grocery shopping at Walmart",
      "expense_date": "2025-10-02T10:00:00.000Z",
      "category_id": "64f8a1b2c3d4e5f6a7b8c9d1",
      "user_id": "64f8a1b2c3d4e5f6a7b8c9d0",
      "created_at": "2025-10-02T10:30:00.000Z"
    }
  }
}
```

**Create multiple expenses for testing:**
```json
// Expense 2
{
  "amount": 15.99,
  "note": "Movie tickets",
  "expense_date": "2025-10-01T19:00:00Z",
  "category_id": "CATEGORY_ID_FOR_LEISURE"
}

// Expense 3
{
  "amount": 299.99,
  "note": "New laptop",
  "expense_date": "2025-09-30T14:00:00Z",
  "category_id": "CATEGORY_ID_FOR_ELECTRONICS"
}
```

---

### 7. GET EXPENSES (JWT Protected)

**Request:**
- Method: `GET`
- URL: `http://127.0.0.1:5000/api/expenses`
- Headers: `Authorization: Bearer YOUR_TOKEN_HERE`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "expenses": [
      {
        "id": "64f8a1b2c3d4e5f6a7b8c9d2",
        "amount": 25.50,
        "note": "Grocery shopping at Walmart",
        "expense_date": "2025-10-02T10:00:00.000Z",
        "category_id": "64f8a1b2c3d4e5f6a7b8c9d1",
        "user_id": "64f8a1b2c3d4e5f6a7b8c9d0",
        "created_at": "2025-10-02T10:30:00.000Z"
      }
    ]
  }
}
```

---

### 8. EXPENSE FILTERING (JWT Protected)

#### 8.1 Past Week Filter
**Request:**
- Method: `GET`
- URL: `http://127.0.0.1:5000/api/expenses?filter=past_week`
- Headers: `Authorization: Bearer YOUR_TOKEN_HERE`

#### 8.2 Last Month Filter
**Request:**
- Method: `GET`
- URL: `http://127.0.0.1:5000/api/expenses?filter=last_month`
- Headers: `Authorization: Bearer YOUR_TOKEN_HERE`

#### 8.3 Last 3 Months Filter
**Request:**
- Method: `GET`
- URL: `http://127.0.0.1:5000/api/expenses?filter=last_3_months`
- Headers: `Authorization: Bearer YOUR_TOKEN_HERE`

#### 8.4 Custom Date Range Filter
**Request:**
- Method: `GET`
- URL: `http://127.0.0.1:5000/api/expenses?filter=custom&start_date=2025-09-01T00:00:00Z&end_date=2025-09-30T23:59:59Z`
- Headers: `Authorization: Bearer YOUR_TOKEN_HERE`

#### 8.5 With Summary
**Request:**
- Method: `GET`
- URL: `http://127.0.0.1:5000/api/expenses?include_summary=true`
- Headers: `Authorization: Bearer YOUR_TOKEN_HERE`

**Expected Response with Summary:**
```json
{
  "status": "success",
  "data": {
    "expenses": [...],
    "summary": {
      "total_amount": 341.48,
      "total_count": 3,
      "category_breakdown": {
        "64f8a1b2c3d4e5f6a7b8c9d1": {
          "amount": 25.50,
          "count": 1
        }
      }
    }
  }
}
```

---

### 9. UPDATE EXPENSE (JWT Protected)

**Request:**
- Method: `PUT`
- URL: `http://127.0.0.1:5000/api/expenses/EXPENSE_ID_HERE`
- Headers: 
  - `Content-Type: application/json`
  - `Authorization: Bearer YOUR_TOKEN_HERE`
- Body (raw JSON):
```json
{
  "amount": 30.00,
  "note": "Updated grocery shopping",
  "expense_date": "2025-10-02T10:00:00Z"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Expense updated successfully",
  "data": {
    "expense": {
      "id": "64f8a1b2c3d4e5f6a7b8c9d2",
      "amount": 30.00,
      "note": "Updated grocery shopping",
      "expense_date": "2025-10-02T10:00:00.000Z",
      "category_id": "64f8a1b2c3d4e5f6a7b8c9d1",
      "user_id": "64f8a1b2c3d4e5f6a7b8c9d0",
      "created_at": "2025-10-02T10:30:00.000Z",
      "updated_at": "2025-10-02T10:35:00.000Z"
    }
  }
}
```

---

### 10. DELETE EXPENSE (JWT Protected)

**Request:**
- Method: `DELETE`
- URL: `http://127.0.0.1:5000/api/expenses/EXPENSE_ID_HERE`
- Headers: `Authorization: Bearer YOUR_TOKEN_HERE`

**Expected Response:**
```json
{
  "status": "success",
  "message": "Expense deleted successfully"
}
```

---

### 11. EXPENSE SUMMARY (JWT Protected)

**Request:**
- Method: `GET`
- URL: `http://127.0.0.1:5000/api/expenses/summary`
- Headers: `Authorization: Bearer YOUR_TOKEN_HERE`

**With Filter:**
- URL: `http://127.0.0.1:5000/api/expenses/summary?filter=past_week`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "summary": {
      "total_amount": 341.48,
      "total_count": 3,
      "category_breakdown": {
        "64f8a1b2c3d4e5f6a7b8c9d1": {
          "amount": 25.50,
          "count": 1
        }
      }
    }
  }
}
```

---

## 🔒 JWT PROTECTION TESTING

### Test 1: Access Protected Endpoint Without Token
**Request:**
- Method: `GET`
- URL: `http://127.0.0.1:5000/api/expenses`
- Headers: None

**Expected Response:**
```json
{
  "msg": "Missing Authorization Header"
}
```

### Test 2: Access Protected Endpoint With Invalid Token
**Request:**
- Method: `GET`
- URL: `http://127.0.0.1:5000/api/expenses`
- Headers: `Authorization: Bearer invalid_token`

**Expected Response:**
```json
{
  "msg": "Token has expired"
}
```

---

## 📊 MONGODB DATA PERSISTENCE VERIFICATION

### Check Data in MongoDB
After creating users, categories, and expenses, you can verify the data is stored in MongoDB:

1. **Check Health Endpoint:**
   - GET `http://127.0.0.1:5000/health`
   - Look for `data_counts` showing your created data

2. **Data Persistence Test:**
   - Create some data
   - Restart the API server
   - Check that data still exists

---

## 🎯 INTERVIEW DEMONSTRATION CHECKLIST

### ✅ User Authentication with JWT
- [ ] User registration works
- [ ] User login generates JWT token
- [ ] JWT token is required for protected endpoints
- [ ] Invalid tokens are rejected

### ✅ User Signup Functionality
- [ ] New users can register
- [ ] Duplicate emails are rejected
- [ ] All required fields are validated

### ✅ JWT Token Generation & Validation
- [ ] Tokens are generated on login/register
- [ ] Tokens are validated on protected endpoints
- [ ] Expired tokens are rejected

### ✅ Expense Filtering
- [ ] Past week filter works
- [ ] Last month filter works
- [ ] Last 3 months filter works
- [ ] Custom date range filter works

### ✅ Expense CRUD Operations
- [ ] Add new expenses
- [ ] List expenses
- [ ] Update existing expenses
- [ ] Remove existing expenses

### ✅ JWT Protection on ALL Endpoints
- [ ] All protected endpoints require valid JWT
- [ ] Unprotected endpoints (health, register, login) work without JWT

### ✅ Predefined Categories
- [ ] Categories must be from predefined list
- [ ] All 7 categories are available: Groceries, Leisure, Electronics, Utilities, Clothing, Health, Others

### ✅ MongoDB Data Persistence
- [ ] Data is stored in MongoDB
- [ ] Data persists after server restart
- [ ] Health endpoint shows data counts

---

## 🚀 QUICK START COMMANDS

### Start the API:
```bash
python mongodb_api.py
```

### Test with curl (alternative to Postman):
```bash
# Health check
curl http://127.0.0.1:5000/health

# Register user
curl -X POST http://127.0.0.1:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john@example.com","password":"pass123"}'

# Login
curl -X POST http://127.0.0.1:5000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"pass123"}'
```

---

## 📝 NOTES FOR INTERVIEW

1. **All endpoints are JWT protected** except `/health`, `/api/users/register`, and `/api/users/login`
2. **Data is stored in MongoDB** - you can verify this by checking the health endpoint
3. **All 7 predefined categories** are enforced in the API
4. **Comprehensive filtering** supports all required date ranges
5. **Full CRUD operations** for expenses with proper validation
6. **Secure authentication** with JWT tokens
7. **Data persistence** - all data survives server restarts

This API meets all the interview requirements and demonstrates professional-level API development with proper security, data modeling, and MongoDB integration.
