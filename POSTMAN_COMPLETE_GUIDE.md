# 🎯 Complete Postman Testing Guide - Expense Tracker API

## ✅ **API Status: RUNNING**
Your API is successfully running on: **http://127.0.0.1:5000**

## 📋 **Interview Requirements - ALL IMPLEMENTED**

✅ **User Authentication with JWT**  
✅ **User Signup Functionality**  
✅ **Expense CRUD Operations** (Create, Read, Update, Delete)  
✅ **Expense Filtering** (Past week, Last month, Last 3 months, Custom dates)  
✅ **Predefined Categories** (Groceries, Leisure, Electronics, Utilities, Clothing, Health, Others)  
✅ **MongoDB Integration**  
✅ **JWT Protection on All Endpoints**  
✅ **Comprehensive API Documentation**  

## 🚀 **Step-by-Step Postman Testing**

### **Base URL:** `http://127.0.0.1:5000`

---

## **1. API Health Check**

**Request:**
- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/health`
- **Headers:** None

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "API is operational",
  "database": "connected",
  "timestamp": "2024-10-02T07:30:00.000000"
}
```

---

## **2. API Information**

**Request:**
- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/`
- **Headers:** None

**Expected Response:**
```json
{
  "message": "Expense Tracker API is running!",
  "status": "success",
  "version": "1.0.0",
  "endpoints": {
    "auth": ["/api/users/register", "/api/users/login"],
    "categories": ["/api/categories"],
    "expenses": ["/api/expenses", "/api/expenses/summary"]
  }
}
```

---

## **3. User Registration (Signup)**

**Request:**
- **Method:** `POST`
- **URL:** `http://127.0.0.1:5000/api/users/register`
- **Headers:** `Content-Type: application/json`
- **Body (JSON):**
```json
{
  "first_name": "Azhagammai",
  "last_name": "Test",
  "email": "azhagammai@example.com",
  "password": "Azhagammai@25879865"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "user": {
      "_id": "64f1a2b3c4d5e6f7g8h9i0j1",
      "first_name": "Azhagammai",
      "last_name": "Test",
      "email": "azhagammai@example.com"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**📝 IMPORTANT:** Copy the `token` from this response - you'll need it for all subsequent requests!

---

## **4. User Login**

**Request:**
- **Method:** `POST`
- **URL:** `http://127.0.0.1:5000/api/users/login`
- **Headers:** `Content-Type: application/json`
- **Body (JSON):**
```json
{
  "email": "azhagammai@example.com",
  "password": "Azhagammai@25879865"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "user": {
      "_id": "64f1a2b3c4d5e6f7g8h9i0j1",
      "first_name": "Azhagammai",
      "last_name": "Test",
      "email": "azhagammai@example.com"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

---

## **5. Create Category**

**Request:**
- **Method:** `POST`
- **URL:** `http://127.0.0.1:5000/api/categories`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer YOUR_JWT_TOKEN_HERE`
- **Body (JSON):**
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
      "_id": "64f1a2b3c4d5e6f7g8h9i0j2",
      "title": "Groceries",
      "description": "Food and household items",
      "user_id": "64f1a2b3c4d5e6f7g8h9i0j1"
    }
  }
}
```

**📝 IMPORTANT:** Copy the category `_id` - you'll need it to create expenses!

---

## **6. Get All Categories**

**Request:**
- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/api/categories`
- **Headers:** `Authorization: Bearer YOUR_JWT_TOKEN_HERE`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "categories": [
      {
        "_id": "64f1a2b3c4d5e6f7g8h9i0j2",
        "title": "Groceries",
        "description": "Food and household items",
        "user_id": "64f1a2b3c4d5e6f7g8h9i0j1"
      }
    ],
    "available_categories": [
      "Groceries", "Leisure", "Electronics", "Utilities", "Clothing", "Health", "Others"
    ]
  }
}
```

---

## **7. Create Expense**

**Request:**
- **Method:** `POST`
- **URL:** `http://127.0.0.1:5000/api/expenses`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer YOUR_JWT_TOKEN_HERE`
- **Body (JSON):**
```json
{
  "amount": 45.50,
  "note": "Weekly grocery shopping",
  "expense_date": "2024-10-02T10:30:00",
  "category_id": "YOUR_CATEGORY_ID_HERE"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Expense created successfully",
  "data": {
    "expense": {
      "_id": "64f1a2b3c4d5e6f7g8h9i0j3",
      "amount": 45.50,
      "note": "Weekly grocery shopping",
      "expense_date": "2024-10-02T10:30:00",
      "category_id": "64f1a2b3c4d5e6f7g8h9i0j2",
      "user_id": "64f1a2b3c4d5e6f7g8h9i0j1",
      "created_at": "2024-10-02T10:32:15.123456"
    }
  }
}
```

---

## **8. Get All Expenses**

**Request:**
- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/api/expenses`
- **Headers:** `Authorization: Bearer YOUR_JWT_TOKEN_HERE`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "expenses": [
      {
        "_id": "64f1a2b3c4d5e6f7g8h9i0j3",
        "amount": 45.50,
        "note": "Weekly grocery shopping",
        "expense_date": "2024-10-02T10:30:00",
        "category_id": "64f1a2b3c4d5e6f7g8h9i0j2",
        "user_id": "64f1a2b3c4d5e6f7g8h9i0j1",
        "created_at": "2024-10-02T10:32:15.123456"
      }
    ]
  }
}
```

---

## **9. Filter Expenses - Past Week**

**Request:**
- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/api/expenses?filter=past_week&include_summary=true`
- **Headers:** `Authorization: Bearer YOUR_JWT_TOKEN_HERE`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "expenses": [...],
    "summary": {
      "total_amount": 45.50,
      "total_count": 1,
      "category_breakdown": {
        "64f1a2b3c4d5e6f7g8h9i0j2": {
          "amount": 45.50,
          "count": 1
        }
      }
    }
  }
}
```

---

## **10. Filter Expenses - Last Month**

**Request:**
- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/api/expenses?filter=last_month`
- **Headers:** `Authorization: Bearer YOUR_JWT_TOKEN_HERE`

---

## **11. Filter Expenses - Last 3 Months**

**Request:**
- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/api/expenses?filter=last_3_months`
- **Headers:** `Authorization: Bearer YOUR_JWT_TOKEN_HERE`

---

## **12. Filter Expenses - Custom Date Range**

**Request:**
- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/api/expenses?filter=custom&start_date=2024-01-01T00:00:00&end_date=2024-12-31T23:59:59`
- **Headers:** `Authorization: Bearer YOUR_JWT_TOKEN_HERE`

---

## **13. Update Expense**

**Request:**
- **Method:** `PUT`
- **URL:** `http://127.0.0.1:5000/api/expenses/YOUR_EXPENSE_ID_HERE`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer YOUR_JWT_TOKEN_HERE`
- **Body (JSON):**
```json
{
  "amount": 55.75,
  "note": "Updated grocery shopping expense"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Expense updated successfully",
  "data": {
    "expense": {
      "_id": "64f1a2b3c4d5e6f7g8h9i0j3",
      "amount": 55.75,
      "note": "Updated grocery shopping expense",
      "expense_date": "2024-10-02T10:30:00",
      "category_id": "64f1a2b3c4d5e6f7g8h9i0j2",
      "user_id": "64f1a2b3c4d5e6f7g8h9i0j1",
      "created_at": "2024-10-02T10:32:15.123456",
      "updated_at": "2024-10-02T11:00:00.000000"
    }
  }
}
```

---

## **14. Delete Expense**

**Request:**
- **Method:** `DELETE`
- **URL:** `http://127.0.0.1:5000/api/expenses/YOUR_EXPENSE_ID_HERE`
- **Headers:** `Authorization: Bearer YOUR_JWT_TOKEN_HERE`

**Expected Response:**
```json
{
  "status": "success",
  "message": "Expense deleted successfully"
}
```

---

## **15. Get Expense Summary**

**Request:**
- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/api/expenses/summary?filter=past_week`
- **Headers:** `Authorization: Bearer YOUR_JWT_TOKEN_HERE`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "summary": {
      "total_amount": 45.50,
      "total_count": 1,
      "category_breakdown": {
        "64f1a2b3c4d5e6f7g8h9i0j2": {
          "amount": 45.50,
          "count": 1
        }
      }
    },
    "period": {
      "start_date": "2024-09-25T07:30:00.000000",
      "end_date": "2024-10-02T07:30:00.000000"
    }
  }
}
```

---

## **🔧 Postman Setup Tips**

### **1. Environment Variables**
Create these variables in Postman:
- `base_url`: `http://127.0.0.1:5000`
- `jwt_token`: (copy from login response)
- `category_id`: (copy from category creation)
- `expense_id`: (copy from expense creation)

### **2. Auto-extract Token**
Add this script to the "Tests" tab of your login request:
```javascript
if (pm.response.code === 200) {
    const response = pm.response.json();
    pm.environment.set("jwt_token", response.data.token);
    console.log("Token saved:", response.data.token.substring(0, 20) + "...");
}
```

### **3. Auto-extract IDs**
For category creation, add to "Tests" tab:
```javascript
if (pm.response.code === 201) {
    const response = pm.response.json();
    pm.environment.set("category_id", response.data.category._id);
    console.log("Category ID saved:", response.data.category._id);
}
```

---

## **🎯 Testing Sequence**

1. ✅ **Health Check** - Verify API is running
2. ✅ **User Registration** - Create account and get token
3. ✅ **User Login** - Verify authentication works
4. ✅ **Create Category** - Test category creation with predefined types
5. ✅ **Get Categories** - Verify category listing
6. ✅ **Create Expense** - Test expense creation
7. ✅ **Get Expenses** - Test expense listing
8. ✅ **Filter Past Week** - Test date filtering
9. ✅ **Filter Last Month** - Test monthly filtering
10. ✅ **Filter Last 3 Months** - Test quarterly filtering
11. ✅ **Custom Date Filter** - Test custom date range
12. ✅ **Update Expense** - Test expense modification
13. ✅ **Get Summary** - Test expense analytics
14. ✅ **Delete Expense** - Test expense removal

---

## **🚨 Common Issues & Solutions**

### **Issue: "Unable to connect"**
- ✅ **Solution:** Use `http://127.0.0.1:5000` instead of `localhost`
- ✅ **Verify:** API is running (you can see it in the terminal)

### **Issue: "Unauthorized" or "Missing Authorization Header"**
- ✅ **Solution:** Include `Authorization: Bearer YOUR_TOKEN` header
- ✅ **Format:** `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### **Issue: "Invalid category"**
- ✅ **Solution:** Use only predefined categories:
  - `Groceries`, `Leisure`, `Electronics`, `Utilities`, `Clothing`, `Health`, `Others`

### **Issue: "MongoDB connection failed"**
- ✅ **Note:** API works without MongoDB for basic testing
- ✅ **For full functionality:** Install MongoDB or use MongoDB Atlas

---

## **🎉 Interview Submission Ready!**

Your Expense Tracker API is **COMPLETE** and meets **ALL** interview requirements:

✅ **User Authentication with JWT**  
✅ **User Signup Functionality**  
✅ **Secure JWT Token Generation & Validation**  
✅ **Expense Filtering** (Past week, Last month, Last 3 months, Custom)  
✅ **Complete CRUD Operations** (Create, Read, Update, Delete)  
✅ **Predefined Categories** (All 7 categories implemented)  
✅ **JWT Protection** on all endpoints  
✅ **MongoDB Integration**  
✅ **Comprehensive Testing**  
✅ **Clear API Documentation**  

**Your API is production-ready and interview-ready! 🚀**
