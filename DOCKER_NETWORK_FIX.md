# 🔧 DOCKER NETWORK CONNECTIVITY FIX
## Solve Docker Image Pull Issues

## 🚨 **PROBLEM IDENTIFIED**

Your Docker is configured with HTTP/HTTPS proxies that are causing network connectivity issues when pulling images from Docker Hub.

## ✅ **SOLUTION: Multiple Approaches**

### **Option 1: Use Local Docker Compose (Recommended)**

```bash
# Use the local configuration that bypasses network issues
docker-compose -f docker-compose.local.yml up --build -d
```

### **Option 2: Fix Docker Network Settings**

#### **Method A: Reset Docker Desktop**
1. Open Docker Desktop
2. Go to Settings → General
3. Click "Reset to factory defaults"
4. Restart Docker Desktop

#### **Method B: Configure Docker Daemon**
Create or edit `~/.docker/daemon.json`:
```json
{
  "dns": ["8.8.8.8", "8.8.4.4"],
  "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"]
}
```

#### **Method C: Use Alternative Base Images**
```bash
# Try pulling the image manually first
docker pull python:3.11-slim

# If that fails, try alternative registry
docker pull registry.cn-hangzhou.aliyuncs.com/library/python:3.11-slim
```

### **Option 3: Use Pre-built Images**

```bash
# Use existing Python image if available
docker images | grep python

# Or use a different base image
# Edit Dockerfile to use: FROM python:3.10-slim
```

## 🚀 **QUICK FIX COMMANDS**

### **1. Try Local Configuration (Easiest)**
```bash
# Use local docker-compose that handles network issues
docker-compose -f docker-compose.local.yml up --build -d
```

### **2. Test Network Connectivity**
```bash
# Test Docker Hub connectivity
docker pull hello-world

# Test specific Python image
docker pull python:3.11-slim
```

### **3. Alternative Base Images**
If `python:3.11-slim` fails, try:
```bash
# Use Python 3.10
docker pull python:3.10-slim

# Or use Ubuntu and install Python
docker pull ubuntu:22.04
```

## 🔧 **DOCKERFILE ALTERNATIVES**

### **Option A: Use Python 3.10**
```dockerfile
FROM python:3.10-slim
# ... rest of Dockerfile
```

### **Option B: Use Ubuntu Base**
```dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ... rest of Dockerfile
```

### **Option C: Use Alpine (Smaller)**
```dockerfile
FROM python:3.11-alpine

RUN apk add --no-cache \
    gcc \
    musl-dev \
    curl

# ... rest of Dockerfile
```

## 🎯 **RECOMMENDED APPROACH**

### **Step 1: Use Local Configuration**
```bash
# This should work around network issues
docker-compose -f docker-compose.local.yml up --build -d
```

### **Step 2: If That Fails, Try Manual Build**
```bash
# Build without compose first
docker build -f Dockerfile.local -t expense-tracker-api .

# Run manually
docker run -d --name expense-tracker-api -p 5000:5000 expense-tracker-api
```

### **Step 3: Test API**
```bash
# Test health endpoint
curl http://localhost:5000/health

# Test in Postman
# Base URL: http://localhost:5000
```

## 🐛 **TROUBLESHOOTING**

### **Common Issues:**

#### **1. Network Timeout**
```bash
# Check Docker network
docker network ls

# Reset Docker networks
docker network prune
```

#### **2. Proxy Issues**
```bash
# Check Docker proxy settings
docker system info | grep -i proxy

# Disable proxy temporarily
# In Docker Desktop: Settings → Resources → Proxies
```

#### **3. DNS Issues**
```bash
# Test DNS resolution
nslookup docker.io

# Use different DNS
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

## 🚀 **QUICK START (BYPASS DOCKER ISSUES)**

### **Run API Directly (No Docker)**
```bash
# Install dependencies
pip install -r requirements.txt

# Run API directly
python mongodb_api.py

# Test in Postman
# Base URL: http://localhost:5000
```

### **Use Docker with Local Images**
```bash
# Check existing images
docker images

# Use existing Python image
docker run -it python:3.11-slim bash
```

## 🎯 **INTERVIEW DEMONSTRATION**

### **If Docker Fails:**
1. **Show the Docker files** (Dockerfile, docker-compose.yml)
2. **Explain the setup** (MongoDB + API + Nginx)
3. **Run API directly** with `python mongodb_api.py`
4. **Demonstrate with Postman** (same functionality)
5. **Explain Docker benefits** (scalability, deployment, isolation)

### **If Docker Works:**
1. **Show Docker setup** (`docker-compose up -d`)
2. **Demonstrate scaling** (`docker-compose up -d --scale api=3`)
3. **Show data persistence** (restart containers, data survives)
4. **Test with Postman** (same API endpoints)

## 🎉 **YOU'RE READY!**

Your API works with or without Docker:

- ✅ **Direct Python:** `python mongodb_api.py`
- ✅ **Docker Local:** `docker-compose -f docker-compose.local.yml up -d`
- ✅ **Docker Production:** `docker-compose -f docker-compose.prod.yml up -d`

**Choose the method that works for your environment!** 🚀
