# 🔧 FIX 401 UNAUTHORIZED ERROR
## Complete Postman Testing Sequence

## 🚨 **PROBLEM: 401 UNAUTHORIZED**

You're getting 401 because you need to **register a user first** before you can login.

## ✅ **SOLUTION: Complete Testing Sequence**

### **Step 1: Health Check (No Auth Required)**
- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/health`
- **Headers:** None
- **Expected:** 200 OK with MongoDB connected

### **Step 2: Register User (Create Account)**
- **Method:** `POST`
- **URL:** `http://127.0.0.1:5000/api/users/register`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "securepass123"
}
```
- **Expected:** 201 Created with user data + JWT token
- **📌 COPY THE TOKEN** from response!

### **Step 3: Login User (Get JWT Token)**
- **Method:** `POST`
- **URL:** `http://127.0.0.1:5000/api/users/login`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "email": "john.doe@example.com",
  "password": "securepass123"
}
```
- **Expected:** 200 OK with user data + JWT token

### **Step 4: Create Category (JWT Protected)**
- **Method:** `POST`
- **URL:** `http://127.0.0.1:5000/api/categories`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer YOUR_TOKEN_HERE`
- **Body (raw JSON):**
```json
{
  "title": "Groceries",
  "description": "Food and household items"
}
```
- **Expected:** 201 Created with category data
- **📌 COPY THE CATEGORY ID** from response!

### **Step 5: Create Expense (JWT Protected)**
- **Method:** `POST`
- **URL:** `http://127.0.0.1:5000/api/expenses`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer YOUR_TOKEN_HERE`
- **Body (raw JSON):**
```json
{
  "amount": 25.50,
  "note": "Grocery shopping at Walmart",
  "expense_date": "2025-10-02T10:00:00Z",
  "category_id": "CATEGORY_ID_FROM_STEP_4"
}
```
- **Expected:** 201 Created with expense data

### **Step 6: Get Expenses (JWT Protected)**
- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/api/expenses`
- **Headers:** `Authorization: Bearer YOUR_TOKEN_HERE`
- **Expected:** 200 OK with expenses list

### **Step 7: Test Filtering (JWT Protected)**
- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/api/expenses?filter=past_week`
- **Headers:** `Authorization: Bearer YOUR_TOKEN_HERE`
- **Expected:** 200 OK with filtered expenses

## 🔍 **COMMON ISSUES & FIXES**

### **Issue 1: 401 UNAUTHORIZED on Login**
**Cause:** User doesn't exist
**Fix:** Register user first (Step 2)

### **Issue 2: 401 UNAUTHORIZED on Protected Endpoints**
**Cause:** Missing or invalid JWT token
**Fix:** 
1. Make sure you have a valid token from login/register
2. Add `Authorization: Bearer YOUR_TOKEN` header
3. Check token is not expired

### **Issue 3: 400 BAD REQUEST**
**Cause:** Invalid request body
**Fix:** 
1. Check JSON format is correct
2. Check all required fields are present
3. Check Content-Type header is `application/json`

### **Issue 4: 404 NOT FOUND**
**Cause:** Wrong URL or server not running
**Fix:** 
1. Check server is running: `curl http://127.0.0.1:5000/health`
2. Check URL is correct: `http://127.0.0.1:5000/api/users/login`

## 🎯 **QUICK TESTING CHECKLIST**

### **Before Testing:**
- [ ] Server is running: `curl http://127.0.0.1:5000/health`
- [ ] MongoDB is connected (check health response)
- [ ] Postman is configured correctly

### **Testing Sequence:**
- [ ] 1. Health check (no auth)
- [ ] 2. Register user (get token)
- [ ] 3. Login user (get token)
- [ ] 4. Create category (use token)
- [ ] 5. Create expense (use token)
- [ ] 6. Get expenses (use token)
- [ ] 7. Test filtering (use token)

### **Common Mistakes:**
- [ ] Trying to login before registering
- [ ] Missing Authorization header
- [ ] Wrong Content-Type header
- [ ] Invalid JSON format
- [ ] Using wrong URL

## 🚀 **QUICK START COMMANDS**

### **Start API Server:**
```bash
python mongodb_api.py
```

### **Test API Health:**
```bash
curl http://127.0.0.1:5000/health
```

### **Test with Docker:**
```bash
docker-compose up -d
curl http://localhost:5000/health
```

## 📝 **POSTMAN COLLECTION SETUP**

### **Create Collection:**
1. Open Postman
2. Click "Collections" → "New Collection"
3. Name: "Expense Tracker API"

### **Add Requests:**
1. **Health Check** - GET `/health`
2. **Register User** - POST `/api/users/register`
3. **Login User** - POST `/api/users/login`
4. **Create Category** - POST `/api/categories`
5. **Create Expense** - POST `/api/expenses`
6. **Get Expenses** - GET `/api/expenses`
7. **Filter Expenses** - GET `/api/expenses?filter=past_week`

### **Set Environment Variables:**
1. Click "Environments" → "New Environment"
2. Name: "Expense Tracker"
3. Add variables:
   - `base_url`: `http://127.0.0.1:5000`
   - `token`: (will be set after login)

## 🎉 **YOU'RE READY!**

Follow this sequence and you'll have a working API demonstration:

1. **Register** → Get token
2. **Login** → Verify token
3. **Create Category** → Use token
4. **Create Expense** → Use token
5. **List Expenses** → Use token
6. **Filter Expenses** → Use token

**No more 401 errors!** 🚀
