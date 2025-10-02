# 🎯 POSTMAN TESTING GUIDE - PROJECT REQUIREMENTS
## Complete Data Examples for Expense Tracker API

## 📋 **PROJECT REQUIREMENTS CHECKLIST**

✅ **User Authentication with JWT**  
✅ **User Signup Functionality**  
✅ **JWT Generation & Validation**  
✅ **Expense Filtering** (Past week, Last month, Last 3 months, Custom dates)  
✅ **Complete Expense CRUD** (Add, Remove, Update)  
✅ **JWT Protection on ALL endpoints**  
✅ **Predefined Categories** (Groceries, Leisure, Electronics, Utilities, Clothing, Health, Others)  
✅ **MongoDB Data Management**  

## 🚀 **STEP-BY-STEP POSTMAN TESTING**

### **STEP 1: Start Your API**
```bash
python simple_working_api.py
```

---

## 🔐 **1. USER AUTHENTICATION**

### **1.1 User Signup (Create New Account)**
**Method:** `POST`  
**URL:** `http://127.0.0.1:5000/api/users/register`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "first_name": "Alice",
  "last_name": "Johnson",
  "email": "alice.johnson@example.com",
  "password": "mySecurePassword123"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": "671234567890abcdef123456",
      "first_name": "Alice",
      "last_name": "Johnson",
      "email": "alice.johnson@example.com"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**📌 COPY THE TOKEN** - You'll need it for all other requests!

### **1.2 User Login (Existing Account)**
**Method:** `POST`  
**URL:** `http://127.0.0.1:5000/api/users/login`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "email": "alice.johnson@example.com",
  "password": "mySecurePassword123"
}
```

---

## 📂 **2. CATEGORY MANAGEMENT**

### **2.1 Create Categories (All Required Categories)**

**Method:** `POST`  
**URL:** `http://127.0.0.1:5000/api/categories`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

**Create Each Category (7 requests):**

**Category 1 - Groceries:**
```json
{
  "title": "Groceries",
  "description": "Food and household essentials"
}
```

**Category 2 - Leisure:**
```json
{
  "title": "Leisure",
  "description": "Entertainment and recreational activities"
}
```

**Category 3 - Electronics:**
```json
{
  "title": "Electronics",
  "description": "Electronic devices and gadgets"
}
```

**Category 4 - Utilities:**
```json
{
  "title": "Utilities",
  "description": "Electricity, water, gas, internet bills"
}
```

**Category 5 - Clothing:**
```json
{
  "title": "Clothing",
  "description": "Clothes, shoes, and accessories"
}
```

**Category 6 - Health:**
```json
{
  "title": "Health",
  "description": "Medical expenses and healthcare"
}
```

**Category 7 - Others:**
```json
{
  "title": "Others",
  "description": "Miscellaneous expenses"
}
```

### **2.2 Get All Categories**
**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/api/categories`

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

---

## 💰 **3. INCOME MANAGEMENT**

### **3.1 Set Monthly Income**
**Method:** `POST`  
**URL:** `http://127.0.0.1:5000/api/income`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

**Body (JSON):**
```json
{
  "amount": 6500.00
}
```

### **3.2 Get Monthly Income**
**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/api/income`

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

---

## 📊 **4. EXPENSE MANAGEMENT (COMPLETE CRUD)**

### **4.1 ADD NEW EXPENSES**

**Method:** `POST`  
**URL:** `http://127.0.0.1:5000/api/expenses`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

**Expense Examples (Use Category IDs from Step 2):**

**Expense 1 - Groceries:**
```json
{
  "amount": 125.50,
  "note": "Weekly grocery shopping at supermarket",
  "expense_date": "2025-10-01T10:30:00Z",
  "category_id": "GROCERIES_CATEGORY_ID_FROM_STEP_2"
}
```

**Expense 2 - Leisure:**
```json
{
  "amount": 45.00,
  "note": "Movie tickets for weekend",
  "expense_date": "2025-10-02T19:00:00Z",
  "category_id": "LEISURE_CATEGORY_ID_FROM_STEP_2"
}
```

**Expense 3 - Electronics:**
```json
{
  "amount": 299.99,
  "note": "New wireless headphones",
  "expense_date": "2025-09-28T14:15:00Z",
  "category_id": "ELECTRONICS_CATEGORY_ID_FROM_STEP_2"
}
```

**Expense 4 - Utilities:**
```json
{
  "amount": 180.75,
  "note": "Monthly electricity bill",
  "expense_date": "2025-09-25T00:00:00Z",
  "category_id": "UTILITIES_CATEGORY_ID_FROM_STEP_2"
}
```

**Expense 5 - Clothing:**
```json
{
  "amount": 89.99,
  "note": "New work shirt",
  "expense_date": "2025-09-20T16:45:00Z",
  "category_id": "CLOTHING_CATEGORY_ID_FROM_STEP_2"
}
```

**Expense 6 - Health:**
```json
{
  "amount": 65.00,
  "note": "Doctor consultation fee",
  "expense_date": "2025-09-15T11:00:00Z",
  "category_id": "HEALTH_CATEGORY_ID_FROM_STEP_2"
}
```

**Expense 7 - Others:**
```json
{
  "amount": 25.00,
  "note": "Gift for friend's birthday",
  "expense_date": "2025-09-10T00:00:00Z",
  "category_id": "OTHERS_CATEGORY_ID_FROM_STEP_2"
}
```

### **4.2 UPDATE EXISTING EXPENSE**

**Method:** `PUT`  
**URL:** `http://127.0.0.1:5000/api/expenses/EXPENSE_ID_FROM_STEP_4.1`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

**Body (JSON):**
```json
{
  "amount": 135.75,
  "note": "Updated grocery shopping amount - added extra items",
  "expense_date": "2025-10-01T10:30:00Z",
  "category_id": "GROCERIES_CATEGORY_ID_FROM_STEP_2"
}
```

### **4.3 REMOVE EXISTING EXPENSE**

**Method:** `DELETE`  
**URL:** `http://127.0.0.1:5000/api/expenses/EXPENSE_ID_FROM_STEP_4.1`

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

---

## 🔍 **5. EXPENSE FILTERING (ALL REQUIRED FILTERS)**

### **5.1 Past Week Filter**
**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/api/expenses?filter=past_week`

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

### **5.2 Last Month Filter**
**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/api/expenses?filter=last_month`

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

### **5.3 Last 3 Months Filter**
**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/api/expenses?filter=last_3_months`

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

### **5.4 Custom Date Range Filter**
**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/api/expenses?filter=custom&start_date=2025-09-01T00:00:00Z&end_date=2025-10-31T23:59:59Z`

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

### **5.5 Filter by Category**
**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/api/expenses?category_id=GROCERIES_CATEGORY_ID`

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

### **5.6 Get All Expenses (No Filter)**
**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/api/expenses`

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

---

## 📈 **6. SAVINGS & BALANCE CALCULATION**

### **6.1 Calculate Savings**
**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/api/savings`

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "monthly_summary": {
      "month": "2025-10",
      "income": 6500.00,
      "total_expenses": 831.23,
      "savings": 5668.77,
      "savings_percentage": 87.2
    },
    "expense_breakdown": {
      "category_id_1": {
        "category_name": "Groceries",
        "total_amount": 135.75,
        "expense_count": 1,
        "monthly_amount": 135.75,
        "monthly_count": 1
      }
    }
  }
}
```

---

## 🔒 **7. JWT SECURITY TESTING**

### **7.1 Test Protected Endpoint Without Token**
**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/api/expenses`

**Headers:** *(No Authorization header)*

**Expected Response:**
```json
{
  "msg": "Missing Authorization Header"
}
```

### **7.2 Test with Invalid Token**
**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/api/expenses`

**Headers:**
```
Authorization: Bearer invalid_token_here
```

**Expected Response:**
```json
{
  "msg": "Invalid token"
}
```

---

## 📋 **8. HEALTH CHECK & API INFO**

### **8.1 API Health Check**
**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/health`

### **8.2 API Information**
**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/`

---

## 🎯 **PROJECT REQUIREMENTS VERIFICATION**

### ✅ **User Authentication & JWT**
- [x] User signup functionality *(Step 1.1)*
- [x] JWT generation *(Step 1.1 & 1.2)*
- [x] JWT validation *(All protected endpoints)*
- [x] Secure session management *(Token-based)*

### ✅ **Expense Filtering**
- [x] Past week filter *(Step 5.1)*
- [x] Last month filter *(Step 5.2)*
- [x] Last 3 months filter *(Step 5.3)*
- [x] Custom date range filter *(Step 5.4)*

### ✅ **Expense CRUD Operations**
- [x] Add new expenses *(Step 4.1)*
- [x] Remove existing expenses *(Step 4.3)*
- [x] Update existing expenses *(Step 4.2)*

### ✅ **JWT Protection**
- [x] All endpoints protected *(Authorization header required)*
- [x] JWT identifies requester *(User-specific data)*

### ✅ **Required Categories**
- [x] Groceries *(Step 2.1)*
- [x] Leisure *(Step 2.1)*
- [x] Electronics *(Step 2.1)*
- [x] Utilities *(Step 2.1)*
- [x] Clothing *(Step 2.1)*
- [x] Health *(Step 2.1)*
- [x] Others *(Step 2.1)*

### ✅ **Data Management**
- [x] MongoDB integration *(All data persisted)*
- [x] Efficient category handling *(Global amount tracking)*

## 🚀 **READY FOR DEMONSTRATION!**

Follow this guide step-by-step in Postman to demonstrate all project requirements. Your API meets every specification:

- ✅ **Complete User Authentication System**
- ✅ **All Required Filtering Options**
- ✅ **Full CRUD Operations**
- ✅ **JWT Security on All Endpoints**
- ✅ **All Required Categories**
- ✅ **MongoDB Data Persistence**

**Your Expense Tracker API is production-ready!** 🎯
