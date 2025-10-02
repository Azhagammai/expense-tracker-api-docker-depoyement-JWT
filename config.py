import os
from datetime import timedelta

class Config:
    # MongoDB Configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/expense_tracker')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'KdQ8MBny_gA-Rt7pdVTP69wnzxvJxnelYqBx8VaXQBY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    
    # Flask Configuration
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # Predefined expense categories
    EXPENSE_CATEGORIES = [
        'Groceries',
        'Leisure', 
        'Electronics',
        'Utilities',
        'Clothing',
        'Health',
        'Others'
    ]
