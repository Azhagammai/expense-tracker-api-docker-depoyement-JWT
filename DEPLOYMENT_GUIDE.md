# Expense Tracker API - Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB (local or cloud)
- pip (Python package manager)

### Installation Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   Create a `.env` file (optional, has defaults):
   ```env
   MONGO_URI=mongodb://localhost:27017/expense_tracker
   JWT_SECRET_KEY=your_secure_secret_key_here
   FLASK_ENV=development
   ```

3. **Start MongoDB**
   - Local: Start your MongoDB service
   - Cloud: Use MongoDB Atlas connection string

4. **Run the Application**
   ```bash
   python run.py --mode dev
   ```
   
   Or simply:
   ```bash
   python app.py
   ```

5. **Test the API**
   ```bash
   python test_api.py
   ```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

1. **Start the full stack**
   ```bash
   docker-compose up -d
   ```

This will start:
- MongoDB on port 27017
- API on port 5000

### Using Docker Only

1. **Build the image**
   ```bash
   docker build -t expense-tracker-api .
   ```

2. **Run with external MongoDB**
   ```bash
   docker run -p 5000:5000 \
     -e MONGO_URI=mongodb://your-mongo-host:27017/expense_tracker \
     -e JWT_SECRET_KEY=your-secret-key \
     expense-tracker-api
   ```

## 🌐 Production Deployment

### Environment Variables for Production
```env
MONGO_URI=mongodb://username:password@host:port/expense_tracker
JWT_SECRET_KEY=your-very-secure-secret-key-here
FLASK_ENV=production
```

### Using Gunicorn (Recommended for Production)

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
   ```

### Using systemd (Linux)

Create `/etc/systemd/system/expense-tracker.service`:
```ini
[Unit]
Description=Expense Tracker API
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/expense-tracker-api
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable expense-tracker
sudo systemctl start expense-tracker
```

## ☁️ Cloud Deployment Options

### Heroku
1. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### AWS EC2
1. Launch EC2 instance
2. Install Python, pip, MongoDB (or use MongoDB Atlas)
3. Clone repository and follow installation steps
4. Use systemd or supervisor for process management

### Digital Ocean App Platform
1. Connect your repository
2. Set environment variables
3. Deploy automatically

## 🔒 Security Considerations

### Production Security Checklist
- [ ] Use strong JWT secret key (256-bit minimum)
- [ ] Enable MongoDB authentication
- [ ] Use HTTPS in production
- [ ] Set up proper firewall rules
- [ ] Use environment variables for sensitive data
- [ ] Enable rate limiting (consider using Flask-Limiter)
- [ ] Set up monitoring and logging
- [ ] Regular security updates

### MongoDB Security
```javascript
// Create database user
use expense_tracker
db.createUser({
  user: "expense_api",
  pwd: "secure_password_here",
  roles: [{ role: "readWrite", db: "expense_tracker" }]
})
```

## 📊 Monitoring and Logging

### Application Logging
The API includes basic error handling. For production, consider:
- Structured logging with JSON format
- Log aggregation (ELK stack, Splunk)
- Application monitoring (New Relic, DataDog)

### Health Checks
- Health endpoint: `GET /health`
- Docker health check included
- Monitor MongoDB connection

## 🔧 Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   - Check MongoDB service status
   - Verify connection string
   - Check network connectivity

2. **JWT Token Issues**
   - Ensure JWT_SECRET_KEY is set
   - Check token expiration (7 days default)
   - Verify Authorization header format

3. **Import Errors**
   - Ensure all dependencies installed: `pip install -r requirements.txt`
   - Check Python version compatibility

4. **Permission Errors**
   - Ensure proper file permissions
   - Check user has write access to log directories

### Debug Mode
Run with debug enabled:
```bash
python run.py --mode dev
```

### Checking Dependencies
```bash
python run.py --mode check
```

## 📈 Performance Optimization

### Database Optimization
- Create indexes on frequently queried fields
- Use MongoDB aggregation for complex queries
- Consider connection pooling

### Application Optimization
- Use connection pooling for MongoDB
- Implement caching for frequently accessed data
- Consider using Redis for session storage

### Example MongoDB Indexes
```javascript
// Create indexes for better performance
db.users.createIndex({ "email": 1 }, { unique: true })
db.categories.createIndex({ "user_id": 1, "title": 1 })
db.expenses.createIndex({ "user_id": 1, "expense_date": -1 })
db.expenses.createIndex({ "user_id": 1, "category_id": 1 })
```

## 🔄 Updates and Maintenance

### Regular Maintenance Tasks
- Update dependencies regularly
- Monitor disk space (especially for logs)
- Backup MongoDB data
- Review and rotate JWT secrets
- Monitor API performance and errors

### Backup Strategy
```bash
# MongoDB backup
mongodump --db expense_tracker --out /path/to/backup/

# Restore
mongorestore --db expense_tracker /path/to/backup/expense_tracker/
```

---

For additional support, refer to the main README.md or create an issue in the repository.
