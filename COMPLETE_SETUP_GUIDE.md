# 🚀 Complete Setup Guide - Expense Tracker API

## 📋 **Prerequisites Checklist**

### ✅ **Step 1: Install MongoDB**

#### **Option A: MongoDB Community Server (Local)**
1. Download MongoDB from: https://www.mongodb.com/try/download/community
2. Install MongoDB Community Server
3. Start MongoDB service:
   - **Windows:** MongoDB should start automatically as a service
   - **Manual start:** Run `mongod` in command prompt

#### **Option B: MongoDB Atlas (Cloud - Recommended)**
1. Go to: https://www.mongodb.com/atlas
2. Create a free account
3. Create a new cluster
4. Get your connection string

### ✅ **Step 2: Verify Python Installation**
```bash
python --version
# Should show Python 3.8 or higher
```

### ✅ **Step 3: Install Dependencies**
```bash
cd "C:\Users\ADMIN\Downloads\expense-tracker-api-main (1)"
pip install -r requirements.txt
```

## 🔧 **MongoDB Configuration**

### **For Local MongoDB:**
Your MongoDB URI should be:
```
mongodb://localhost:27017/expense_tracker
```

### **For MongoDB with Authentication:**
If you have MongoDB with username/password:
```
mongodb://username:password@localhost:27017/expense_tracker?authSource=admin
```

### **For MongoDB Atlas (Cloud):**
```
mongodb+srv://username:password@cluster.mongodb.net/expense_tracker?retryWrites=true&w=majority
```

## 🚀 **Starting the API Server**

### **Method 1: Using the Main App**
```bash
cd "C:\Users\ADMIN\Downloads\expense-tracker-api-main (1)"
python app.py
```

### **Method 2: Using the Run Script**
```bash
python run.py --mode dev
```

### **Method 3: Using the Minimal API (for testing)**
```bash
python minimal_api.py
```

## 📮 **Testing with Postman**

### **Base URL:**
```
http://localhost:5000
```

### **Test Endpoints (Minimal API):**

#### 1. **Health Check**
- **Method:** GET
- **URL:** `http://localhost:5000/health`
- **Expected Response:**
```json
{
  "status": "healthy",
  "message": "API is operational"
}
```

#### 2. **Home Endpoint**
- **Method:** GET
- **URL:** `http://localhost:5000/`
- **Expected Response:**
```json
{
  "message": "Expense Tracker API is running!",
  "status": "success"
}
```

#### 3. **Test GET**
- **Method:** GET
- **URL:** `http://localhost:5000/api/test`

#### 4. **Test POST**
- **Method:** POST
- **URL:** `http://localhost:5000/api/test`
- **Headers:** `Content-Type: application/json`
- **Body:**
```json
{
  "name": "Azhagammai",
  "message": "Testing from Postman"
}
```

## 🔐 **Full API Testing (with MongoDB)**

Once MongoDB is running, test the full API:

### **1. User Registration**
- **Method:** POST
- **URL:** `http://localhost:5000/api/users/register`
- **Headers:** `Content-Type: application/json`
- **Body:**
```json
{
  "first_name": "Azhagammai",
  "last_name": "Test",
  "email": "azhagammai@example.com",
  "password": "Azhagammai@25879865"
}
```

### **2. User Login**
- **Method:** POST
- **URL:** `http://localhost:5000/api/users/login`
- **Headers:** `Content-Type: application/json`
- **Body:**
```json
{
  "email": "azhagammai@example.com",
  "password": "Azhagammai@25879865"
}
```

**📝 Important:** Copy the `token` from the login response!

### **3. Create Category**
- **Method:** POST
- **URL:** `http://localhost:5000/api/categories`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer YOUR_TOKEN_HERE`
- **Body:**
```json
{
  "title": "Groceries",
  "description": "Food and household items"
}
```

### **4. Create Expense**
- **Method:** POST
- **URL:** `http://localhost:5000/api/expenses`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer YOUR_TOKEN_HERE`
- **Body:**
```json
{
  "amount": 45.50,
  "note": "Weekly grocery shopping",
  "expense_date": "2024-10-02T10:30:00",
  "category_id": "YOUR_CATEGORY_ID_HERE"
}
```

### **5. Get Expenses with Filters**
- **Method:** GET
- **URL:** `http://localhost:5000/api/expenses?filter=past_week&include_summary=true`
- **Headers:** `Authorization: Bearer YOUR_TOKEN_HERE`

## 🔧 **Troubleshooting**

### **Issue: "Unable to connect to the remote server"**
**Solutions:**
1. Check if the server is actually running
2. Try different ports: 5000, 5001, 8000
3. Check Windows Firewall settings
4. Try `127.0.0.1` instead of `localhost`

### **Issue: "MongoDB connection failed"**
**Solutions:**
1. Make sure MongoDB is running:
   ```bash
   # Check if MongoDB is running
   tasklist | findstr mongod
   ```
2. For MongoDB Atlas, check your connection string
3. Check network connectivity

### **Issue: "Import errors"**
**Solution:**
```bash
pip install -r requirements.txt
```

### **Issue: "JWT token errors"**
**Solution:**
Make sure you're including the Authorization header:
```
Authorization: Bearer your_actual_token_here
```

## 🎯 **Quick Start Commands**

```bash
# 1. Navigate to project
cd "C:\Users\ADMIN\Downloads\expense-tracker-api-main (1)"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start minimal API (for testing)
python minimal_api.py

# 4. Test in another terminal/Postman
# GET http://localhost:5000/health
```

## 🌐 **MongoDB Atlas Setup (Recommended)**

1. **Create Account:** https://www.mongodb.com/atlas
2. **Create Cluster:** Choose free tier
3. **Create Database User:**
   - Username: `azhagammai`
   - Password: `Azhagammai@25879865`
4. **Whitelist IP:** Add `0.0.0.0/0` for testing
5. **Get Connection String:** 
   ```
   mongodb+srv://azhagammai:Azhagammai%4025879865@cluster0.xxxxx.mongodb.net/expense_tracker?retryWrites=true&w=majority
   ```

## 📞 **Next Steps**

1. ✅ **Test minimal API** with Postman first
2. ✅ **Set up MongoDB** (local or Atlas)
3. ✅ **Test full API** with authentication
4. ✅ **Create expenses** and test filtering

**Your API is ready for the interview! 🎉**
