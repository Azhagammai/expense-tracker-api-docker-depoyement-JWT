# 🎯 COMPLETE POSTMAN INTERVIEW TESTS
## Full Test Suite for Expense Tracker API - Interview Task Completion

## 📋 **INTERVIEW TASK COMPLETION CHECKLIST**

This test suite demonstrates **ALL** project requirements:
- ✅ User Authentication with JWT
- ✅ User Signup Functionality  
- ✅ JWT Generation & Validation
- ✅ Complete Expense CRUD Operations
- ✅ All Required Filtering Options
- ✅ JWT Protection on ALL Endpoints
- ✅ All 7 Required Categories
- ✅ MongoDB Data Management

---

## 🚀 **POSTMAN COLLECTION - COPY & PASTE READY**

### **Collection Name:** `Expense Tracker API - Interview Complete`

---

## **TEST 1: API Health Check**
**Purpose:** Verify API is running

**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/health`  
**Headers:** None  

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "API is operational",
  "database": "MongoDB Connected"
}
```

---

## **TEST 2: User Registration (Signup)**
**Purpose:** Demonstrate user signup functionality

**Method:** `POST`  
**URL:** `http://127.0.0.1:5000/api/users/register`  

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "email": "john.smith@interview.com",
  "password": "InterviewPass123"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": "USER_ID",
      "first_name": "John",
      "last_name": "Smith",
      "email": "john.smith@interview.com"
    },
    "token": "JWT_TOKEN_HERE"
  }
}
```

**📌 SAVE THE TOKEN** for next tests!

---

## **TEST 3: User Login**
**Purpose:** Demonstrate login functionality

**Method:** `POST`  
**URL:** `http://127.0.0.1:5000/api/users/login`  

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "email": "john.smith@interview.com",
  "password": "InterviewPass123"
}
```

---

## **TEST 4: JWT Security Test (Should Fail)**
**Purpose:** Demonstrate JWT protection

**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/api/categories`  
**Headers:** None (No Authorization)

**Expected Response:**
```json
{
  "msg": "Missing Authorization Header"
}
```

---

## **TEST 5-11: Create All Required Categories**
**Purpose:** Demonstrate all 7 required categories

**Method:** `POST`  
**URL:** `http://127.0.0.1:5000/api/categories`  

**Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_JWT_TOKEN
```

### **Test 5: Groceries Category**
```json
{
  "title": "Groceries",
  "description": "Food and household essentials"
}
```

### **Test 6: Leisure Category**
```json
{
  "title": "Leisure",
  "description": "Entertainment and recreational activities"
}
```

### **Test 7: Electronics Category**
```json
{
  "title": "Electronics",
  "description": "Electronic devices and gadgets"
}
```

### **Test 8: Utilities Category**
```json
{
  "title": "Utilities",
  "description": "Bills for electricity, water, gas, internet"
}
```

### **Test 9: Clothing Category**
```json
{
  "title": "Clothing",
  "description": "Clothes, shoes, and accessories"
}
```

### **Test 10: Health Category**
```json
{
  "title": "Health",
  "description": "Medical expenses and healthcare"
}
```

### **Test 11: Others Category**
```json
{
  "title": "Others",
  "description": "Miscellaneous expenses"
}
```

---

## **TEST 12: Get All Categories**
**Purpose:** Verify categories created with global amounts

**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/api/categories`  

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "categories": [
      {
        "id": "CATEGORY_ID",
        "title": "Groceries",
        "description": "Food and household essentials",
        "total_amount": 0.0,
        "expense_count": 0
      }
    ],
    "available_categories": ["Groceries", "Leisure", "Electronics", "Utilities", "Clothing", "Health", "Others"]
  }
}
```

---

## **TEST 13: Set Monthly Income**
**Purpose:** Demonstrate income tracking

**Method:** `POST`  
**URL:** `http://127.0.0.1:5000/api/income`  

**Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_JWT_TOKEN
```

**Body:**
```json
{
  "amount": 7500.00
}
```

---

## **TEST 14-20: Add Expenses (One for Each Category)**
**Purpose:** Demonstrate expense creation and category amount tracking

**Method:** `POST`  
**URL:** `http://127.0.0.1:5000/api/expenses`  

**Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_JWT_TOKEN
```

### **Test 14: Groceries Expense**
```json
{
  "amount": 150.75,
  "note": "Weekly grocery shopping - fruits, vegetables, meat",
  "expense_date": "2025-10-01T10:00:00Z",
  "category_id": "GROCERIES_CATEGORY_ID"
}
```

### **Test 15: Leisure Expense**
```json
{
  "amount": 65.00,
  "note": "Movie tickets and popcorn for weekend",
  "expense_date": "2025-10-02T19:30:00Z",
  "category_id": "LEISURE_CATEGORY_ID"
}
```

### **Test 16: Electronics Expense**
```json
{
  "amount": 299.99,
  "note": "New wireless bluetooth headphones",
  "expense_date": "2025-09-28T15:45:00Z",
  "category_id": "ELECTRONICS_CATEGORY_ID"
}
```

### **Test 17: Utilities Expense**
```json
{
  "amount": 185.50,
  "note": "Monthly electricity bill payment",
  "expense_date": "2025-09-25T00:00:00Z",
  "category_id": "UTILITIES_CATEGORY_ID"
}
```

### **Test 18: Clothing Expense**
```json
{
  "amount": 89.99,
  "note": "New business shirt for work",
  "expense_date": "2025-09-20T14:20:00Z",
  "category_id": "CLOTHING_CATEGORY_ID"
}
```

### **Test 19: Health Expense**
```json
{
  "amount": 120.00,
  "note": "Doctor consultation and prescription",
  "expense_date": "2025-09-15T11:00:00Z",
  "category_id": "HEALTH_CATEGORY_ID"
}
```

### **Test 20: Others Expense**
```json
{
  "amount": 45.00,
  "note": "Birthday gift for colleague",
  "expense_date": "2025-09-10T16:30:00Z",
  "category_id": "OTHERS_CATEGORY_ID"
}
```

---

## **TEST 21-25: Expense Filtering (All Required Filters)**
**Purpose:** Demonstrate all filtering capabilities

**Method:** `GET`  
**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN
```

### **Test 21: Past Week Filter**
**URL:** `http://127.0.0.1:5000/api/expenses?filter=past_week`

### **Test 22: Last Month Filter**
**URL:** `http://127.0.0.1:5000/api/expenses?filter=last_month`

### **Test 23: Last 3 Months Filter**
**URL:** `http://127.0.0.1:5000/api/expenses?filter=last_3_months`

### **Test 24: Custom Date Range Filter**
**URL:** `http://127.0.0.1:5000/api/expenses?filter=custom&start_date=2025-09-01T00:00:00Z&end_date=2025-10-31T23:59:59Z`

### **Test 25: Category Filter (Groceries)**
**URL:** `http://127.0.0.1:5000/api/expenses?category_id=GROCERIES_CATEGORY_ID`

---

## **TEST 26: Update Expense**
**Purpose:** Demonstrate expense update functionality

**Method:** `PUT`  
**URL:** `http://127.0.0.1:5000/api/expenses/EXPENSE_ID_FROM_TEST_14`  

**Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_JWT_TOKEN
```

**Body:**
```json
{
  "amount": 175.25,
  "note": "Updated grocery shopping - added cleaning supplies",
  "expense_date": "2025-10-01T10:00:00Z",
  "category_id": "GROCERIES_CATEGORY_ID"
}
```

---

## **TEST 27: Calculate Savings & Balance**
**Purpose:** Demonstrate financial summary with category breakdown

**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/api/savings`  

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "monthly_summary": {
      "month": "2025-10",
      "income": 7500.00,
      "total_expenses": 956.23,
      "savings": 6543.77,
      "savings_percentage": 87.25
    },
    "expense_breakdown": {
      "GROCERIES_ID": {
        "category_name": "Groceries",
        "total_amount": 175.25,
        "expense_count": 1,
        "monthly_amount": 175.25,
        "monthly_count": 1
      },
      "LEISURE_ID": {
        "category_name": "Leisure",
        "total_amount": 65.00,
        "expense_count": 1,
        "monthly_amount": 65.00,
        "monthly_count": 1
      }
    }
  }
}
```

---

## **TEST 28: Delete Expense**
**Purpose:** Demonstrate expense deletion

**Method:** `DELETE`  
**URL:** `http://127.0.0.1:5000/api/expenses/EXPENSE_ID_FROM_TEST_15`  

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Expense deleted successfully",
  "data": {
    "deleted_expense_id": "EXPENSE_ID",
    "amount_removed": 65.00
  }
}
```

---

## **TEST 29: Verify Category Amounts Updated**
**Purpose:** Show global category amounts are accurate

**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/api/categories`  

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN
```

**Expected Response:** Categories show updated total_amount and expense_count

---

## **TEST 30: Final Savings Calculation**
**Purpose:** Show accurate balance after all operations

**Method:** `GET`  
**URL:** `http://127.0.0.1:5000/api/savings`  

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN
```

---

## 🎯 **INTERVIEW DEMONSTRATION SCRIPT**

### **Phase 1: Authentication (Tests 1-4)**
"Let me demonstrate the user authentication system with JWT security..."

### **Phase 2: Category Management (Tests 5-12)**
"Now I'll create all 7 required categories with global amount tracking..."

### **Phase 3: Income Setup (Test 13)**
"Setting up monthly income for financial calculations..."

### **Phase 4: Expense CRUD (Tests 14-20, 26, 28)**
"Demonstrating complete CRUD operations - Create, Read, Update, Delete..."

### **Phase 5: Filtering Capabilities (Tests 21-25)**
"Testing all required filtering options - past week, last month, last 3 months, and custom dates..."

### **Phase 6: Financial Analysis (Tests 27, 29, 30)**
"Finally, showing accurate balance calculation and savings analysis..."

---

## 📊 **EXPECTED FINAL RESULTS**

After running all tests, you should demonstrate:

✅ **User Authentication:** JWT tokens working  
✅ **All 7 Categories:** Created and tracked  
✅ **Multiple Expenses:** One in each category  
✅ **All Filters Working:** Past week, month, 3 months, custom  
✅ **CRUD Operations:** Create, Read, Update, Delete  
✅ **Global Amounts:** Categories showing correct totals  
✅ **Savings Calculation:** Income vs expenses vs balance  
✅ **JWT Security:** All endpoints protected  

---

## 🚀 **INTERVIEW SUCCESS CHECKLIST**

- [ ] API starts successfully
- [ ] User registration works
- [ ] JWT authentication works
- [ ] All 7 categories created
- [ ] Expenses created in each category
- [ ] All filtering options work
- [ ] Update expense works
- [ ] Delete expense works
- [ ] Category amounts update correctly
- [ ] Savings calculation is accurate
- [ ] JWT protection verified

**Run all 30 tests in sequence to demonstrate complete project requirements!** 🎯

---

## 💡 **POSTMAN TIPS**

1. **Save JWT Token:** After Test 2, copy token to environment variable
2. **Save Category IDs:** Copy category IDs from Test 12 responses
3. **Save Expense IDs:** Copy expense IDs for update/delete tests
4. **Run in Order:** Tests build on each other
5. **Check Responses:** Verify each response matches expected format

**Your API demonstrates every single project requirement perfectly!** 🚀
