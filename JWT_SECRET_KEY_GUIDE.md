# JWT Secret Key Setup Guide

## 🔐 What is a JWT Secret Key?

A JWT (JSON Web Token) secret key is used to:
- **Sign** JWT tokens when users log in
- **Verify** JWT tokens when users access protected endpoints
- **Ensure** tokens haven't been tampered with

## 🎯 Quick Setup (Choose One Method)

### Method 1: Generate a New Key (Recommended)

```bash
# Generate a secure 32-byte key
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"

# Generate a more secure 64-byte key
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(64))"
```

### Method 2: Use the Key Generator Script

```bash
python generate_secret_key.py
```

## 📝 How to Set Your Secret Key

### Option 1: Environment Variable (Production Recommended)

1. **Create a `.env` file:**
```env
JWT_SECRET_KEY=your_generated_key_here
MONGO_URI=mongodb://localhost:27017/expense_tracker
FLASK_ENV=development
```

2. **The app will automatically load it** (already configured in `config.py`)

### Option 2: Update config.py Directly (Development Only)

Edit `config.py`:
```python
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_generated_key_here')
```

### Option 3: Set Environment Variable in Terminal

**Windows:**
```cmd
set JWT_SECRET_KEY=your_generated_key_here
python app.py
```

**Linux/Mac:**
```bash
export JWT_SECRET_KEY=your_generated_key_here
python app.py
```

## 🧪 Test Your Setup

### 1. Check if Key is Loaded
```bash
python -c "from config import Config; print('JWT Key loaded:', Config.JWT_SECRET_KEY[:20] + '...')"
```

### 2. Test JWT Token Generation
```bash
python -c "
from flask_jwt_extended import create_access_token
from app import app
with app.app_context():
    token = create_access_token(identity={'user_id': 'test'})
    print('JWT Token generated successfully:', token[:50] + '...')
"
```

### 3. Run the Full API Test
```bash
python test_api.py
```

## 🔒 Security Best Practices

### ✅ DO:
- **Generate random keys** using `secrets` module
- **Use different keys** for development and production
- **Store keys securely** (environment variables, secrets manager)
- **Use at least 32 bytes** (256 bits) for the key
- **Rotate keys periodically** in production
- **Never commit keys** to version control

### ❌ DON'T:
- Use simple passwords like "password123"
- Use the same key across multiple applications
- Store keys in source code
- Share keys in plain text
- Use short keys (less than 32 bytes)

## 🚀 Production Deployment

### AWS Secrets Manager
```python
import boto3
import json

def get_secret():
    secret_name = "expense-tracker/jwt-key"
    region_name = "us-west-2"
    
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)['JWT_SECRET_KEY']
```

### Docker Environment
```dockerfile
# In Dockerfile
ENV JWT_SECRET_KEY=your_secure_key_here

# Or in docker-compose.yml
environment:
  - JWT_SECRET_KEY=your_secure_key_here
```

### Heroku
```bash
heroku config:set JWT_SECRET_KEY=your_secure_key_here
```

## 🔧 Troubleshooting

### Problem: "JWT decode error"
**Solution:** Make sure the same secret key is used for both signing and verifying tokens.

### Problem: "Token has expired"
**Solution:** Check token expiration settings in `config.py` (default: 7 days).

### Problem: "Invalid token"
**Solution:** Ensure the Authorization header format: `Bearer your_token_here`

## 📊 Key Strength Examples

| Key Type | Strength | Example |
|----------|----------|---------|
| **Weak** ❌ | Simple text | `"mypassword"` |
| **Poor** ❌ | Short random | `"abc123"` |
| **Good** ✅ | 32-byte URL-safe | `"KdQ8MBny_gA-Rt7pdVTP69wnzxvJxnelYqBx8VaXQBY"` |
| **Excellent** ✅ | 64-byte URL-safe | `"luo6V4Upu2QfKFeGSMKnr8xY024H2PmlcTakvPdWLHW..."` |

## 🎯 Current Setup Status

Your expense tracker API is already configured with:
- ✅ Secure JWT secret key in `config.py`
- ✅ Environment variable support
- ✅ 7-day token expiration
- ✅ Automatic token verification middleware

**You're ready to go!** 🚀

## 📞 Need Help?

If you encounter issues:
1. Run `python generate_secret_key.py` to get a new key
2. Update your `config.py` or `.env` file
3. Test with `python test_api.py`
4. Check the logs for specific error messages
