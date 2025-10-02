#!/usr/bin/env python3
"""
Complete Expense Tracker API - Single File Implementation
Meets all interview requirements:
- User authentication with JWT
- Expense CRUD operations
- Predefined categories
- Date filtering (past week, month, 3 months, custom)
- MongoDB integration
"""

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import datetime, timedelta
from bson import ObjectId
from bson.errors import InvalidId
import calendar
import re
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/expense_tracker')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'KdQ8MBny_gA-Rt7pdVTP69wnzxvJxnelYqBx8VaXQBY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

# Initialize extensions
mongo = PyMongo(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)

# Predefined expense categories
EXPENSE_CATEGORIES = [
    'Groceries', 'Leisure', 'Electronics', 'Utilities', 'Clothing', 'Health', 'Others'
]

# Utility functions
def is_valid_object_id(object_id):
    """Check if string is a valid ObjectId"""
    try:
        ObjectId(object_id)
        return True
    except (InvalidId, TypeError):
        return False

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Routes

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Expense Tracker API is running!',
        'status': 'success',
        'version': '1.0.0',
        'endpoints': {
            'auth': ['/api/users/register', '/api/users/login'],
            'categories': ['/api/categories'],
            'expenses': ['/api/expenses', '/api/expenses/summary']
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        # Test MongoDB connection
        mongo.db.command('ping')
        db_status = 'connected'
    except Exception:
        db_status = 'disconnected'
    
    return jsonify({
        'status': 'healthy',
        'message': 'API is operational',
        'database': db_status,
        'timestamp': datetime.utcnow().isoformat()
    })

# Authentication Routes

@app.route('/api/users/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'status': 'error',
                    'message': f'{field} is required'
                }), 400
        
        # Validate email format
        if not validate_email(data['email']):
            return jsonify({
                'status': 'error',
                'message': 'Invalid email format'
            }), 400
        
        # Validate password length
        if len(data['password']) < 6:
            return jsonify({
                'status': 'error',
                'message': 'Password must be at least 6 characters long'
            }), 400
        
        # Check if user already exists
        if mongo.db.users.find_one({'email': data['email'].lower()}):
            return jsonify({
                'status': 'error',
                'message': 'User with this email already exists'
            }), 400
        
        # Hash password
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        
        # Create user
        user_data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'].lower(),
            'password': hashed_password,
            'created_at': datetime.utcnow()
        }
        
        result = mongo.db.users.insert_one(user_data)
        user_id = str(result.inserted_id)
        
        # Generate JWT token
        token_data = {
            'user_id': user_id,
            'email': data['email'].lower(),
            'first_name': data['first_name'],
            'last_name': data['last_name']
        }
        token = create_access_token(identity=token_data)
        
        return jsonify({
            'status': 'success',
            'message': 'User registered successfully',
            'data': {
                'user': {
                    '_id': user_id,
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'].lower()
                },
                'token': token
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred during registration'
        }), 500

@app.route('/api/users/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'status': 'error',
                'message': 'Email and password are required'
            }), 400
        
        # Find user
        user = mongo.db.users.find_one({'email': data['email'].lower()})
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'Invalid email or password'
            }), 401
        
        # Check password
        if not bcrypt.check_password_hash(user['password'], data['password']):
            return jsonify({
                'status': 'error',
                'message': 'Invalid email or password'
            }), 401
        
        # Generate JWT token
        token_data = {
            'user_id': str(user['_id']),
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name']
        }
        token = create_access_token(identity=token_data)
        
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'data': {
                'user': {
                    '_id': str(user['_id']),
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'email': user['email']
                },
                'token': token
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred during login'
        }), 500

# Category Routes

@app.route('/api/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all categories for the authenticated user"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        
        categories = list(mongo.db.categories.find(
            {'user_id': ObjectId(user_id)},
            {'_id': 1, 'title': 1, 'description': 1, 'user_id': 1}
        ).sort('title', 1))
        
        # Convert ObjectId to string
        for category in categories:
            category['_id'] = str(category['_id'])
            category['user_id'] = str(category['user_id'])
        
        return jsonify({
            'status': 'success',
            'data': {
                'categories': categories,
                'available_categories': EXPENSE_CATEGORIES
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while fetching categories'
        }), 500

@app.route('/api/categories', methods=['POST'])
@jwt_required()
def create_category():
    """Create a new category"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        data = request.get_json()
        
        # Validate required fields
        if not data.get('title') or not data.get('description'):
            return jsonify({
                'status': 'error',
                'message': 'Title and description are required'
            }), 400
        
        # Validate category title
        if data['title'] not in EXPENSE_CATEGORIES:
            return jsonify({
                'status': 'error',
                'message': f'Invalid category. Must be one of: {", ".join(EXPENSE_CATEGORIES)}'
            }), 400
        
        # Check if user already has this category
        existing = mongo.db.categories.find_one({
            'title': data['title'],
            'user_id': ObjectId(user_id)
        })
        
        if existing:
            return jsonify({
                'status': 'error',
                'message': f'Category "{data["title"]}" already exists for this user'
            }), 400
        
        # Create category
        category_data = {
            'title': data['title'],
            'description': data['description'],
            'user_id': ObjectId(user_id),
            'created_at': datetime.utcnow()
        }
        
        result = mongo.db.categories.insert_one(category_data)
        category_id = str(result.inserted_id)
        
        return jsonify({
            'status': 'success',
            'message': 'Category created successfully',
            'data': {
                'category': {
                    '_id': category_id,
                    'title': data['title'],
                    'description': data['description'],
                    'user_id': user_id
                }
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while creating category'
        }), 500

# Expense Routes

@app.route('/api/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    """Get expenses with optional filtering"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        
        # Get query parameters
        category_id = request.args.get('category_id')
        filter_type = request.args.get('filter')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        limit = request.args.get('limit', type=int)
        include_summary = request.args.get('include_summary', 'false').lower() == 'true'
        
        # Build query
        query = {'user_id': ObjectId(user_id)}
        
        if category_id:
            if not is_valid_object_id(category_id):
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid category ID'
                }), 400
            query['category_id'] = ObjectId(category_id)
        
        # Handle date filtering
        now = datetime.utcnow()
        start_date = None
        end_date = None
        
        if filter_type:
            if filter_type == 'past_week':
                start_date = now - timedelta(days=7)
                end_date = now
            elif filter_type == 'last_month':
                first_day_current_month = now.replace(day=1)
                last_month = first_day_current_month - timedelta(days=1)
                start_date = last_month.replace(day=1)
                end_date = last_month.replace(day=calendar.monthrange(last_month.year, last_month.month)[1])
            elif filter_type == 'last_3_months':
                start_date = now - timedelta(days=90)
                end_date = now
            elif filter_type == 'custom':
                if not start_date_str or not end_date_str:
                    return jsonify({
                        'status': 'error',
                        'message': 'Custom filter requires both start_date and end_date'
                    }), 400
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid filter type. Must be one of: past_week, last_month, last_3_months, custom'
                }), 400
        
        # Parse custom dates
        if start_date_str:
            try:
                start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid start_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
                }), 400
        
        if end_date_str:
            try:
                end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid end_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
                }), 400
        
        # Add date range to query
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query['$gte'] = start_date
            if end_date:
                date_query['$lte'] = end_date
            query['expense_date'] = date_query
        
        # Execute query
        cursor = mongo.db.expenses.find(query).sort('expense_date', -1)
        if limit:
            cursor = cursor.limit(limit)
        
        expenses = list(cursor)
        
        # Convert ObjectId to string
        for expense in expenses:
            expense['_id'] = str(expense['_id'])
            expense['user_id'] = str(expense['user_id'])
            expense['category_id'] = str(expense['category_id'])
            expense['expense_date'] = expense['expense_date'].isoformat()
            if 'created_at' in expense:
                expense['created_at'] = expense['created_at'].isoformat()
        
        response_data = {'expenses': expenses}
        
        # Add summary if requested
        if include_summary:
            total_amount = sum(expense['amount'] for expense in expenses)
            total_count = len(expenses)
            
            category_breakdown = {}
            for expense in expenses:
                cat_id = expense['category_id']
                if cat_id not in category_breakdown:
                    category_breakdown[cat_id] = {'amount': 0, 'count': 0}
                category_breakdown[cat_id]['amount'] += expense['amount']
                category_breakdown[cat_id]['count'] += 1
            
            response_data['summary'] = {
                'total_amount': total_amount,
                'total_count': total_count,
                'category_breakdown': category_breakdown
            }
        
        return jsonify({
            'status': 'success',
            'data': response_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while fetching expenses'
        }), 500

@app.route('/api/expenses', methods=['POST'])
@jwt_required()
def create_expense():
    """Create a new expense"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['amount', 'note', 'expense_date', 'category_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'{field} is required'
                }), 400
        
        # Validate amount
        try:
            amount = float(data['amount'])
            if amount <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            return jsonify({
                'status': 'error',
                'message': 'Amount must be a positive number'
            }), 400
        
        # Validate category
        if not is_valid_object_id(data['category_id']):
            return jsonify({
                'status': 'error',
                'message': 'Invalid category ID'
            }), 400
        
        # Check if category belongs to user
        category = mongo.db.categories.find_one({
            '_id': ObjectId(data['category_id']),
            'user_id': ObjectId(user_id)
        })
        
        if not category:
            return jsonify({
                'status': 'error',
                'message': 'Category not found or doesn\'t belong to user'
            }), 400
        
        # Parse expense date
        try:
            expense_date = datetime.fromisoformat(data['expense_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': 'Invalid expense_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
            }), 400
        
        # Create expense
        expense_data = {
            'amount': amount,
            'note': data['note'],
            'expense_date': expense_date,
            'category_id': ObjectId(data['category_id']),
            'user_id': ObjectId(user_id),
            'created_at': datetime.utcnow()
        }
        
        result = mongo.db.expenses.insert_one(expense_data)
        expense_id = str(result.inserted_id)
        
        return jsonify({
            'status': 'success',
            'message': 'Expense created successfully',
            'data': {
                'expense': {
                    '_id': expense_id,
                    'amount': amount,
                    'note': data['note'],
                    'expense_date': expense_date.isoformat(),
                    'category_id': data['category_id'],
                    'user_id': user_id,
                    'created_at': datetime.utcnow().isoformat()
                }
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while creating expense'
        }), 500

@app.route('/api/expenses/<expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    """Update an existing expense"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        data = request.get_json()
        
        # Validate expense ID
        if not is_valid_object_id(expense_id):
            return jsonify({
                'status': 'error',
                'message': 'Invalid expense ID'
            }), 400
        
        # Check if expense exists and belongs to user
        expense = mongo.db.expenses.find_one({
            '_id': ObjectId(expense_id),
            'user_id': ObjectId(user_id)
        })
        
        if not expense:
            return jsonify({
                'status': 'error',
                'message': 'Expense not found'
            }), 404
        
        # Build update data
        update_data = {}
        
        if 'amount' in data:
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    raise ValueError()
                update_data['amount'] = amount
            except (ValueError, TypeError):
                return jsonify({
                    'status': 'error',
                    'message': 'Amount must be a positive number'
                }), 400
        
        if 'note' in data:
            if not data['note'].strip():
                return jsonify({
                    'status': 'error',
                    'message': 'Note cannot be empty'
                }), 400
            update_data['note'] = data['note'].strip()
        
        if 'expense_date' in data:
            try:
                expense_date = datetime.fromisoformat(data['expense_date'].replace('Z', '+00:00'))
                update_data['expense_date'] = expense_date
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid expense_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
                }), 400
        
        if 'category_id' in data:
            if not is_valid_object_id(data['category_id']):
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid category ID'
                }), 400
            
            # Check if category belongs to user
            category = mongo.db.categories.find_one({
                '_id': ObjectId(data['category_id']),
                'user_id': ObjectId(user_id)
            })
            
            if not category:
                return jsonify({
                    'status': 'error',
                    'message': 'Category not found or doesn\'t belong to user'
                }), 400
            
            update_data['category_id'] = ObjectId(data['category_id'])
        
        if not update_data:
            return jsonify({
                'status': 'error',
                'message': 'No valid fields to update'
            }), 400
        
        # Update expense
        update_data['updated_at'] = datetime.utcnow()
        mongo.db.expenses.update_one(
            {'_id': ObjectId(expense_id)},
            {'$set': update_data}
        )
        
        # Get updated expense
        updated_expense = mongo.db.expenses.find_one({'_id': ObjectId(expense_id)})
        updated_expense['_id'] = str(updated_expense['_id'])
        updated_expense['user_id'] = str(updated_expense['user_id'])
        updated_expense['category_id'] = str(updated_expense['category_id'])
        updated_expense['expense_date'] = updated_expense['expense_date'].isoformat()
        if 'created_at' in updated_expense:
            updated_expense['created_at'] = updated_expense['created_at'].isoformat()
        if 'updated_at' in updated_expense:
            updated_expense['updated_at'] = updated_expense['updated_at'].isoformat()
        
        return jsonify({
            'status': 'success',
            'message': 'Expense updated successfully',
            'data': {
                'expense': updated_expense
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while updating expense'
        }), 500

@app.route('/api/expenses/<expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    """Delete an expense"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        
        # Validate expense ID
        if not is_valid_object_id(expense_id):
            return jsonify({
                'status': 'error',
                'message': 'Invalid expense ID'
            }), 400
        
        # Delete expense
        result = mongo.db.expenses.delete_one({
            '_id': ObjectId(expense_id),
            'user_id': ObjectId(user_id)
        })
        
        if result.deleted_count == 0:
            return jsonify({
                'status': 'error',
                'message': 'Expense not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'message': 'Expense deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while deleting expense'
        }), 500

@app.route('/api/expenses/summary', methods=['GET'])
@jwt_required()
def get_expense_summary():
    """Get expense summary with totals and breakdowns"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        
        # Get date filters
        filter_type = request.args.get('filter')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        # Build query
        query = {'user_id': ObjectId(user_id)}
        
        # Handle date filtering (same logic as get_expenses)
        now = datetime.utcnow()
        start_date = None
        end_date = None
        
        if filter_type:
            if filter_type == 'past_week':
                start_date = now - timedelta(days=7)
                end_date = now
            elif filter_type == 'last_month':
                first_day_current_month = now.replace(day=1)
                last_month = first_day_current_month - timedelta(days=1)
                start_date = last_month.replace(day=1)
                end_date = last_month.replace(day=calendar.monthrange(last_month.year, last_month.month)[1])
            elif filter_type == 'last_3_months':
                start_date = now - timedelta(days=90)
                end_date = now
            elif filter_type == 'custom':
                if not start_date_str or not end_date_str:
                    return jsonify({
                        'status': 'error',
                        'message': 'Custom filter requires both start_date and end_date'
                    }), 400
        
        # Parse custom dates
        if start_date_str:
            try:
                start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid start_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
                }), 400
        
        if end_date_str:
            try:
                end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid end_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
                }), 400
        
        # Add date range to query
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query['$gte'] = start_date
            if end_date:
                date_query['$lte'] = end_date
            query['expense_date'] = date_query
        
        # Get expenses
        expenses = list(mongo.db.expenses.find(query))
        
        # Calculate summary
        total_amount = sum(expense['amount'] for expense in expenses)
        total_count = len(expenses)
        
        # Category breakdown
        category_breakdown = {}
        for expense in expenses:
            cat_id = str(expense['category_id'])
            if cat_id not in category_breakdown:
                category_breakdown[cat_id] = {'amount': 0, 'count': 0}
            category_breakdown[cat_id]['amount'] += expense['amount']
            category_breakdown[cat_id]['count'] += 1
        
        return jsonify({
            'status': 'success',
            'data': {
                'summary': {
                    'total_amount': total_amount,
                    'total_count': total_count,
                    'category_breakdown': category_breakdown
                },
                'period': {
                    'start_date': start_date.isoformat() if start_date else None,
                    'end_date': end_date.isoformat() if end_date else None
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while generating summary'
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'status': 'error',
        'message': 'Method not allowed'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 EXPENSE TRACKER API - INTERVIEW READY")
    print("=" * 60)
    print("✅ Features implemented:")
    print("   - User authentication with JWT")
    print("   - Expense CRUD operations")
    print("   - Predefined categories:", ", ".join(EXPENSE_CATEGORIES))
    print("   - Date filtering (past week, month, 3 months, custom)")
    print("   - MongoDB integration")
    print("   - Comprehensive validation")
    print()
    print("🌐 Server starting on: http://127.0.0.1:5000")
    print("📋 Test endpoints:")
    print("   GET  /health")
    print("   POST /api/users/register")
    print("   POST /api/users/login")
    print("   GET  /api/categories")
    print("   POST /api/categories")
    print("   GET  /api/expenses")
    print("   POST /api/expenses")
    print("   PUT  /api/expenses/<id>")
    print("   DELETE /api/expenses/<id>")
    print()
    print("⚠️  MongoDB connection:", app.config['MONGO_URI'])
    print("🔑 JWT Secret configured")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='127.0.0.1', port=5000)
