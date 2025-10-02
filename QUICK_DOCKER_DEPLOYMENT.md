# 🐳 QUICK DOCKER DEPLOYMENT GUIDE
## Expense Tracker API - Ready to Deploy!

## 🚀 ONE-COMMAND DEPLOYMENT

### Development (Local Testing)
```bash
# Start everything with one command
docker-compose up --build -d
```

### Production (Scalable)
```bash
# Start production with scaling
docker-compose -f docker-compose.prod.yml up --build -d
```

---

## 📋 WHAT YOU GET

### Services Included:
- ✅ **Expense Tracker API** - Your Flask application
- ✅ **MongoDB Database** - With your credentials
- ✅ **Nginx Load Balancer** - For production scaling
- ✅ **Health Monitoring** - Built-in health checks
- ✅ **Data Persistence** - MongoDB data survives restarts

### Ports:
- **API:** `http://localhost:5000`
- **MongoDB:** `localhost:27017`
- **Nginx:** `http://localhost:80`

---

## 🎯 DEPLOYMENT COMMANDS

### 1. Start Development Environment
```bash
# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 2. Start Production Environment
```bash
# Start production with scaling
docker-compose -f docker-compose.prod.yml up --build -d

# Scale API to 3 replicas
docker-compose -f docker-compose.prod.yml up -d --scale api=3

# View production logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 3. Test Your Deployment
```bash
# Test API health
curl http://localhost:5000/health

# Test through Nginx
curl http://localhost/health

# Test with Postman
# Base URL: http://localhost:5000
```

---

## 📊 MONITORING COMMANDS

### Check Service Status
```bash
# View running containers
docker-compose ps

# Check resource usage
docker stats

# View specific service logs
docker-compose logs api
docker-compose logs mongodb
docker-compose logs nginx
```

### Health Checks
```bash
# API health
curl http://localhost:5000/health

# MongoDB health
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"

# Nginx health
curl -I http://localhost/health
```

---

## 🔧 CONFIGURATION

### Environment Variables
Create `.env` file:
```bash
# MongoDB
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=Azhagammai@25879865

# JWT
JWT_SECRET_KEY=KdQ8MBny_gA-Rt7pdVTP69wnzxvJxnelYqBx8VaXQBY

# Flask
FLASK_ENV=production
```

### Scaling
```bash
# Scale API to 5 replicas
docker-compose -f docker-compose.prod.yml up -d --scale api=5

# Check scaled services
docker-compose -f docker-compose.prod.yml ps
```

---

## 🗄️ DATA MANAGEMENT

### Backup Data
```bash
# Backup MongoDB
docker-compose exec mongodb mongodump --out /backup

# Copy backup from container
docker cp expense_tracker_mongodb:/backup ./mongodb_backup
```

### Restore Data
```bash
# Copy backup to container
docker cp ./mongodb_backup expense_tracker_mongodb:/backup

# Restore MongoDB
docker-compose exec mongodb mongorestore /backup
```

### Reset Everything
```bash
# Stop and remove everything (WARNING: Data loss)
docker-compose down -v

# Remove all images
docker-compose down --rmi all
```

---

## 🐛 TROUBLESHOOTING

### Common Issues

#### Port Already in Use
```bash
# Check what's using port 5000
netstat -tulpn | grep :5000

# Kill process
sudo kill -9 <PID>
```

#### Services Not Starting
```bash
# Check logs
docker-compose logs

# Rebuild containers
docker-compose down
docker-compose up --build
```

#### MongoDB Connection Issues
```bash
# Check MongoDB logs
docker-compose logs mongodb

# Test MongoDB connection
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"
```

#### Permission Issues
```bash
# Fix permissions
sudo chown -R $USER:$USER .

# Rebuild
docker-compose down
docker-compose up --build
```

---

## 🌐 PRODUCTION DEPLOYMENT

### Cloud Deployment Options

#### AWS ECS
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker build -t expense-tracker-api .
docker tag expense-tracker-api:latest <account>.dkr.ecr.us-east-1.amazonaws.com/expense-tracker-api:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/expense-tracker-api:latest
```

#### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/expense-tracker-api
gcloud run deploy --image gcr.io/PROJECT-ID/expense-tracker-api --platform managed
```

#### Azure Container Instances
```bash
# Build and push to ACR
az acr build --registry myregistry --image expense-tracker-api .
az container create --resource-group myResourceGroup --name expense-tracker --image myregistry.azurecr.io/expense-tracker-api
```

---

## 📝 POSTMAN TESTING WITH DOCKER

### Test Your Deployed API

1. **Start Services:**
   ```bash
   docker-compose up -d
   ```

2. **Test Health:**
   ```bash
   curl http://localhost:5000/health
   ```

3. **Use Postman:**
   - Base URL: `http://localhost:5000`
   - Follow the same testing guide as before
   - All endpoints work the same way

### Production Testing

1. **Start Production Services:**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Test Through Nginx:**
   ```bash
   curl http://localhost/health
   ```

3. **Use Postman:**
   - Base URL: `http://localhost` (through Nginx)
   - Or direct: `http://localhost:5000`

---

## 🎯 INTERVIEW DEMONSTRATION

### Docker Deployment Demo

1. **Show Docker Setup:**
   ```bash
   # Show files
   ls -la Dockerfile docker-compose.yml

   # Start services
   docker-compose up -d

   # Show running containers
   docker-compose ps
   ```

2. **Demonstrate Scaling:**
   ```bash
   # Scale API
   docker-compose up -d --scale api=3

   # Show load balancing
   curl http://localhost/health
   ```

3. **Show Data Persistence:**
   ```bash
   # Create data via Postman
   # Stop containers
   docker-compose down

   # Start again
   docker-compose up -d

   # Data is still there!
   curl http://localhost:5000/health
   ```

---

## 🎉 QUICK START CHECKLIST

### Before Deployment:
- [ ] Docker installed
- [ ] Docker Compose installed
- [ ] All files present (Dockerfile, docker-compose.yml, mongodb_api.py)

### Deployment:
- [ ] Run `docker-compose up --build -d`
- [ ] Check `docker-compose ps`
- [ ] Test `curl http://localhost:5000/health`

### Testing:
- [ ] Use Postman with base URL `http://localhost:5000`
- [ ] Test all endpoints (register, login, categories, expenses)
- [ ] Verify data persistence

### Production:
- [ ] Use `docker-compose.prod.yml`
- [ ] Set environment variables
- [ ] Scale with `--scale api=3`
- [ ] Monitor with `docker-compose logs`

---

## 🚀 YOU'RE READY!

Your Expense Tracker API is now:
- ✅ **Containerized** with Docker
- ✅ **Scalable** with Docker Compose
- ✅ **Production-ready** with security features
- ✅ **Load balanced** with Nginx
- ✅ **Persistent** with MongoDB volumes
- ✅ **Monitored** with health checks

**Deploy anywhere with Docker!** 🐳
