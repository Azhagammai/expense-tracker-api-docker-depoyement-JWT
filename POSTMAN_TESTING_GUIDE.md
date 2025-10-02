# 📮 Postman Testing Guide - Expense Tracker API

## 🌐 **API Base URL**
```
http://localhost:5000
```

## 🧪 **Step-by-Step Testing with Postman**

### **Step 1: Test API Health**

**Request:**
- **Method:** `GET`
- **URL:** `http://localhost:5000/health`
- **Headers:** None required

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "API is operational"
}
```

---

### **Step 2: User Registration**

**Request:**
- **Method:** `POST`
- **URL:** `http://localhost:5000/api/users/register`
- **Headers:** 
  - `Content-Type: application/json`
- **Body (JSON):**
```json
{
  "first_name": "Azhagammai",
  "last_name": "User",
  "email": "azhagammai@example.com",
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
      "_id": "64f1a2b3c4d5e6f7g8h9i0j1",
      "first_name": "Azhagammai",
      "last_name": "User",
      "email": "azhagammai@example.com"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**📝 Important:** Copy the `token` from the response - you'll need it for all subsequent requests!

---

### **Step 3: User Login**

**Request:**
- **Method:** `POST`
- **URL:** `http://localhost:5000/api/users/login`
- **Headers:** 
  - `Content-Type: application/json`
- **Body (JSON):**
```json
{
  "email": "azhagammai@example.com",
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
      "_id": "64f1a2b3c4d5e6f7g8h9i0j1",
      "first_name": "Azhagammai",
      "last_name": "User",
      "email": "azhagammai@example.com"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

---

### **Step 4: Create a Category**

**Request:**
- **Method:** `POST`
- **URL:** `http://localhost:5000/api/categories`
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

**📝 Important:** Copy the category `_id` - you'll need it to create expenses!

---

### **Step 5: Get All Categories**

**Request:**
- **Method:** `GET`
- **URL:** `http://localhost:5000/api/categories`
- **Headers:** 
  - `Authorization: Bearer YOUR_JWT_TOKEN_HERE`

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
    ]
  }
}
```

---

### **Step 6: Create an Expense**

**Request:**
- **Method:** `POST`
- **URL:** `http://localhost:5000/api/expenses`
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

### **Step 7: Get All Expenses**

**Request:**
- **Method:** `GET`
- **URL:** `http://localhost:5000/api/expenses`
- **Headers:** 
  - `Authorization: Bearer YOUR_JWT_TOKEN_HERE`

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

### **Step 8: Filter Expenses (Past Week)**

**Request:**
- **Method:** `GET`
- **URL:** `http://localhost:5000/api/expenses?filter=past_week&include_summary=true`
- **Headers:** 
  - `Authorization: Bearer YOUR_JWT_TOKEN_HERE`

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

### **Step 9: Update an Expense**

**Request:**
- **Method:** `PUT`
- **URL:** `http://localhost:5000/api/expenses/YOUR_EXPENSE_ID_HERE`
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

---

### **Step 10: Delete an Expense**

**Request:**
- **Method:** `DELETE`
- **URL:** `http://localhost:5000/api/expenses/YOUR_EXPENSE_ID_HERE`
- **Headers:** 
  - `Authorization: Bearer YOUR_JWT_TOKEN_HERE`

**Expected Response:**
```json
{
  "status": "success",
  "message": "Expense deleted successfully"
}
```

---

## 🔍 **Advanced Filtering Examples**

### **Filter by Last Month**
```
GET http://localhost:5000/api/expenses?filter=last_month
```

### **Filter by Last 3 Months**
```
GET http://localhost:5000/api/expenses?filter=last_3_months
```

### **Custom Date Range Filter**
```
GET http://localhost:5000/api/expenses?filter=custom&start_date=2024-01-01T00:00:00&end_date=2024-01-31T23:59:59
```

### **Filter by Category**
```
GET http://localhost:5000/api/expenses?category_id=YOUR_CATEGORY_ID
```

### **Get Expense Summary**
```
GET http://localhost:5000/api/expenses/summary
```

---

## 📋 **Available Expense Categories**

When creating categories, use one of these predefined titles:
- `Groceries`
- `Leisure`
- `Electronics`
- `Utilities`
- `Clothing`
- `Health`
- `Others`

---

## 🚨 **Common Error Responses**

### **401 Unauthorized (Missing/Invalid Token)**
```json
{
  "status": "error",
  "message": "Missing Authorization Header"
}
```

### **400 Bad Request (Validation Error)**
```json
{
  "status": "error",
  "message": "Validation failed",
  "errors": {
    "email": ["Not a valid email address."]
  }
}
```

### **404 Not Found**
```json
{
  "status": "error",
  "message": "Resource not found"
}
```

---

## 🔧 **Postman Setup Tips**

### **1. Set up Environment Variables in Postman:**
- `base_url`: `http://localhost:5000`
- `jwt_token`: (copy from login response)
- `category_id`: (copy from category creation)
- `expense_id`: (copy from expense creation)

### **2. Use Variables in Requests:**
- URL: `{{base_url}}/api/users/login`
- Authorization: `Bearer {{jwt_token}}`

### **3. Auto-extract Token with Test Script:**
Add this to the "Tests" tab in your login request:
```javascript
if (pm.response.code === 200) {
    const response = pm.response.json();
    pm.environment.set("jwt_token", response.data.token);
}
```

---

## 🎯 **Quick Test Sequence**

1. ✅ Health Check
2. ✅ Register User
3. ✅ Login User (save token)
4. ✅ Create Category (save category_id)
5. ✅ Create Expense
6. ✅ Get All Expenses
7. ✅ Filter Expenses (past_week)
8. ✅ Update Expense
9. ✅ Delete Expense

**Your API is ready for testing! 🚀**
