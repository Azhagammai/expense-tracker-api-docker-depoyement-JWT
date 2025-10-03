# 🐳 DOCKER DEPLOYMENT GUIDE
## Expense Tracker API - Production Ready

This guide shows you how to deploy your Expense Tracker API using Docker and Docker Compose.


## 🚀 DEPLOYMENT COMMANDS

### Development Commands

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build

# Build Image
docker build -t expense-tracker-api .

# Run Continer
docker run -d -p 5000:5000 expense-tracker-api


# Access API Docker Deploy
 http://localhost:5000
```

## 📋 PREREQUISITES

- Docker installed on your system
- Docker Compose installed
- Git (to clone the repository)

## 🚀 QUICK START

### 1. Development Deployment (Local Testing)

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

**Services will be available at:**
- API: `http://localhost:5000`
- MongoDB: `localhost:27017`
- Nginx: `http://localhost:80`

### 2. Production Deployment

```bash
# Copy environment file
cp env.example .env

# Edit .env with your production values
nano .env

# Start production services
docker-compose -f docker-compose.prod.yml up -d --build
```

## 📁 DOCKER FILES EXPLAINED

### `Dockerfile`
- **Base Image:** Python 3.11 slim
- **Security:** Non-root user
- **Health Check:** Built-in health monitoring
- **Optimized:** Multi-stage build for smaller images

### `docker-compose.yml` (Development)
- **MongoDB:** Database with your credentials
- **API:** Your Flask application
- **Nginx:** Reverse proxy for load balancing
- **Networking:** Isolated network for services

### `docker-compose.prod.yml` (Production)
- **Scaling:** Multiple API replicas
- **Resource Limits:** Memory and CPU limits
- **Security:** Enhanced nginx configuration
- **Monitoring:** Health checks and logging

## 🔧 CONFIGURATION

### Environment Variables

Create a `.env` file:

```bash
# MongoDB Configuration
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=your_secure_password

# JWT Configuration
JWT_SECRET_KEY=your_jwt_secret_key

# Flask Configuration
FLASK_ENV=production
```

### MongoDB Configuration

The MongoDB container is configured with:
- **Username:** admin
- **Password:** Your specified password
- **Database:** expense_tracker
- **Port:** 27017
- **Persistence:** Data stored in Docker volume


```

### Production Commands

```bash
# Start production services
docker-compose -f docker-compose.prod.yml up -d

# Scale API replicas
docker-compose -f docker-compose.prod.yml up -d --scale api=3

# View production logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop production services
docker-compose -f docker-compose.prod.yml down
```

## 📊 MONITORING & HEALTH CHECKS

### Health Check Endpoints

```bash
# API Health
curl http://localhost:5000/health

# Through Nginx
curl http://localhost/health
```

### Container Health

```bash
# Check container status
docker-compose ps

# Check specific service logs
docker-compose logs api
docker-compose logs mongodb
docker-compose logs nginx

# Check resource usage
docker stats
```

## 🔒 SECURITY FEATURES

### Production Security

1. **Non-root User:** API runs as non-root user
2. **Network Isolation:** Services in isolated network
3. **Resource Limits:** Memory and CPU limits
4. **Rate Limiting:** Nginx rate limiting (10 req/s)
5. **Security Headers:** XSS protection, frame options
6. **Environment Variables:** Sensitive data in .env

### MongoDB Security

- Authentication enabled
- Root user with strong password
- Network access restricted to API container

## 📈 SCALING

### Horizontal Scaling

```bash
# Scale API to 3 replicas
docker-compose -f docker-compose.prod.yml up -d --scale api=3

# Scale with load balancer
docker-compose -f docker-compose.prod.yml up -d --scale api=5
```

### Vertical Scaling

Edit `docker-compose.prod.yml`:

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 512M
          cpus: '0.25'
```

## 🗄️ DATA PERSISTENCE

### MongoDB Data

```bash
# Data is stored in Docker volume
docker volume ls

# Backup MongoDB data
docker exec expense_tracker_mongodb mongodump --out /backup

# Restore MongoDB data
docker exec expense_tracker_mongodb mongorestore /backup
```

### Volume Management

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect expense-tracker-api-main-1_mongodb_data

# Remove volume (WARNING: Data loss)
docker volume rm expense-tracker-api-main-1_mongodb_data
```

## 🐛 TROUBLESHOOTING

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using port 5000
netstat -tulpn | grep :5000

# Kill process
sudo kill -9 <PID>
```

#### 2. MongoDB Connection Failed
```bash
# Check MongoDB logs
docker-compose logs mongodb

# Check MongoDB status
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"
```

#### 3. API Not Starting
```bash
# Check API logs
docker-compose logs api

# Check environment variables
docker-compose exec api env | grep MONGO
```

#### 4. Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Rebuild containers
docker-compose down
docker-compose up --build
```

### Debug Commands

```bash
# Enter API container
docker-compose exec api bash

# Enter MongoDB container
docker-compose exec mongodb mongosh

# Check network connectivity
docker-compose exec api ping mongodb

# Test API from inside container
docker-compose exec api curl http://localhost:5000/health
```

## 📝 POSTMAN TESTING WITH DOCKER

### Test Local Docker Deployment

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

### Test Production Deployment

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
