#!/usr/bin/env python3
"""
MONGODB-CONNECTED EXPENSE TRACKER API
All data will be stored in MongoDB - perfect for Postman testing!
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import os
from bson import ObjectId
import json

app = Flask(__name__)
CORS(app)

# MongoDB Configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/expense_tracker'
app.config['JWT_SECRET_KEY'] = 'KdQ8MBny_gA-Rt7pdVTP69wnzxvJxnelYqBx8VaXQBY'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

# Initialize extensions
mongo = PyMongo(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Predefined expense categories as required
EXPENSE_CATEGORIES = ['Groceries', 'Leisure', 'Electronics', 'Utilities', 'Clothing', 'Health', 'Others']

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

# ROUTES

@app.route('/')
def home():
    return jsonify({
        'message': 'Expense Tracker API is running!',
        'status': 'success',
        'version': '1.0.0',
        'database': 'MongoDB Connected',
        'endpoints': {
            'auth': [
                '/api/users/register',
                '/api/users/login'
            ],
            'categories': [
                '/api/categories'
            ],
            'expenses': [
                '/api/expenses',
                '/api/expenses/summary'
            ]
        },
        'features': [
            'User Authentication with JWT',
            'Expense CRUD Operations',
            'Predefined Categories',
            'Date Filtering (Past week, Last month, Last 3 months, Custom)',
            'MongoDB Data Persistence'
        ]
    })

@app.route('/health')
def health():
    try:
        # Test MongoDB connection
        users_count = mongo.db.users.count_documents({})
        categories_count = mongo.db.categories.count_documents({})
        expenses_count = mongo.db.expenses.count_documents({})
        
        return jsonify({
            'status': 'healthy',
            'message': 'API is operational',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'MongoDB Connected',
            'data_counts': {
                'users': users_count,
                'categories': categories_count,
                'expenses': expenses_count
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Database connection failed: {str(e)}',
            'database': 'MongoDB Connection Error'
        }), 500

# USER AUTHENTICATION ENDPOINTS

@app.route('/api/users/register', methods=['POST'])
def register():
    """User signup functionality - stores in MongoDB"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['first_name', 'last_name', 'email', 'password']
        for field in required:
            if not data.get(field):
                return jsonify({'status': 'error', 'message': f'{field} is required'}), 400
        
        email = data['email'].lower()
        
        # Check if user exists in MongoDB
        existing_user = mongo.db.users.find_one({'email': email})
        if existing_user:
            return jsonify({'status': 'error', 'message': 'User already exists'}), 400
        
        # Hash password
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        
        # Create user document for MongoDB
        user_doc = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': email,
            'password': hashed_password,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        # Insert into MongoDB
        result = mongo.db.users.insert_one(user_doc)
        user_id = str(result.inserted_id)
        
        # Generate JWT token
        token_data = {
            'user_id': user_id,
            'email': email,
            'first_name': data['first_name'],
            'last_name': data['last_name']
        }
        token = create_access_token(identity=token_data)
        
        return jsonify({
            'status': 'success',
            'message': 'User registered successfully',
            'data': {
                'user': {
                    'id': user_id,
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': email
                },
                'token': token
            }
        }), 201
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Registration failed: {str(e)}'}), 500

@app.route('/api/users/login', methods=['POST'])
def login():
    """User login with JWT generation - authenticates against MongoDB"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'status': 'error', 'message': 'Email and password required'}), 400
        
        email = data['email'].lower()
        
        # Find user in MongoDB
        user = mongo.db.users.find_one({'email': email})
        if not user:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
        
        # Verify password
        if not bcrypt.check_password_hash(user['password'], data['password']):
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
        
        # Generate token
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
                    'id': str(user['_id']),
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'email': user['email']
                },
                'token': token
            }
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Login failed: {str(e)}'}), 500

# CATEGORY ENDPOINTS

@app.route('/api/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all categories for authenticated user from MongoDB"""
    try:
        user_id = get_jwt_identity()['user_id']
        
        # Get user categories from MongoDB
        user_categories = list(mongo.db.categories.find({'user_id': user_id}))
        
        # Convert ObjectId to string for JSON serialization
        for cat in user_categories:
            cat['id'] = str(cat['_id'])
            del cat['_id']
            cat['created_at'] = cat['created_at'].isoformat() if 'created_at' in cat else None
        
        return jsonify({
            'status': 'success',
            'data': {
                'categories': user_categories,
                'available_categories': EXPENSE_CATEGORIES
            }
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to fetch categories: {str(e)}'}), 500

@app.route('/api/categories', methods=['POST'])
@jwt_required()
def create_category():
    """Create new category with predefined constraints - stores in MongoDB"""
    try:
        user_id = get_jwt_identity()['user_id']
        data = request.get_json()
        
        if not data.get('title') or not data.get('description'):
            return jsonify({'status': 'error', 'message': 'Title and description required'}), 400
        
        # Validate predefined categories
        if data['title'] not in EXPENSE_CATEGORIES:
            return jsonify({
                'status': 'error', 
                'message': f'Invalid category. Must be one of: {", ".join(EXPENSE_CATEGORIES)}'
            }), 400
        
        # Check if user already has this category
        existing_category = mongo.db.categories.find_one({
            'user_id': user_id, 
            'title': data['title']
        })
        if existing_category:
            return jsonify({'status': 'error', 'message': 'Category already exists'}), 400
        
        # Create category document for MongoDB
        category_doc = {
            'title': data['title'],
            'description': data['description'],
            'user_id': user_id,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        # Insert into MongoDB
        result = mongo.db.categories.insert_one(category_doc)
        category_id = str(result.inserted_id)
        
        # Prepare response
        category = {
            'id': category_id,
            'title': data['title'],
            'description': data['description'],
            'user_id': user_id,
            'created_at': category_doc['created_at'].isoformat()
        }
        
        return jsonify({
            'status': 'success',
            'message': 'Category created successfully',
            'data': {'category': category}
        }), 201
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Category creation failed: {str(e)}'}), 500

# EXPENSE ENDPOINTS

@app.route('/api/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    """List and filter expenses with all required filters - from MongoDB"""
    try:
        user_id = get_jwt_identity()['user_id']
        
        # Get query parameters
        category_id = request.args.get('category_id')
        filter_type = request.args.get('filter')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        include_summary = request.args.get('include_summary', 'false').lower() == 'true'
        
        # Build MongoDB query
        query = {'user_id': user_id}
        
        # Apply category filter
        if category_id:
            query['category_id'] = category_id
        
        # Apply date filtering
        now = datetime.utcnow()
        
        if filter_type == 'past_week':
            query['expense_date'] = {'$gte': now - timedelta(days=7)}
        elif filter_type == 'last_month':
            first_day_current = now.replace(day=1)
            last_month = first_day_current - timedelta(days=1)
            first_day_last_month = last_month.replace(day=1)
            query['expense_date'] = {
                '$gte': first_day_last_month,
                '$lte': last_month
            }
        elif filter_type == 'last_3_months':
            query['expense_date'] = {'$gte': now - timedelta(days=90)}
        elif filter_type == 'custom':
            if start_date_str and end_date_str:
                try:
                    start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
                    end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
                    query['expense_date'] = {'$gte': start_date, '$lte': end_date}
                except ValueError:
                    return jsonify({'status': 'error', 'message': 'Invalid date format'}), 400
        
        # Get expenses from MongoDB
        expenses_cursor = mongo.db.expenses.find(query).sort('expense_date', -1)
        expenses = list(expenses_cursor)
        
        # Convert ObjectId to string for JSON serialization
        for expense in expenses:
            expense['id'] = str(expense['_id'])
            del expense['_id']
            expense['expense_date'] = expense['expense_date'].isoformat()
            expense['created_at'] = expense['created_at'].isoformat() if 'created_at' in expense else None
        
        response_data = {'expenses': expenses}
        
        # Add summary if requested
        if include_summary:
            total_amount = sum(exp['amount'] for exp in expenses)
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
        
        return jsonify({'status': 'success', 'data': response_data})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to fetch expenses: {str(e)}'}), 500

@app.route('/api/expenses', methods=['POST'])
@jwt_required()
def create_expense():
    """Add new expense - stores in MongoDB"""
    try:
        user_id = get_jwt_identity()['user_id']
        data = request.get_json()
        
        # Validate required fields
        required = ['amount', 'note', 'expense_date', 'category_id']
        for field in required:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'{field} is required'}), 400
        
        # Validate amount
        try:
            amount = float(data['amount'])
            if amount <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            return jsonify({'status': 'error', 'message': 'Amount must be positive number'}), 400
        
        # Validate category exists and belongs to user
        category_id = data['category_id']
        category = mongo.db.categories.find_one({
            '_id': ObjectId(category_id),
            'user_id': user_id
        })
        if not category:
            return jsonify({'status': 'error', 'message': 'Invalid category'}), 400
        
        # Parse date
        try:
            expense_date = datetime.fromisoformat(data['expense_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid date format'}), 400
        
        # Create expense document for MongoDB
        expense_doc = {
            'amount': amount,
            'note': data['note'],
            'expense_date': expense_date,
            'category_id': category_id,
            'user_id': user_id,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        # Insert into MongoDB
        result = mongo.db.expenses.insert_one(expense_doc)
        expense_id = str(result.inserted_id)
        
        # Prepare response
        expense = {
            'id': expense_id,
            'amount': amount,
            'note': data['note'],
            'expense_date': expense_date.isoformat(),
            'category_id': category_id,
            'user_id': user_id,
            'created_at': expense_doc['created_at'].isoformat()
        }
        
        return jsonify({
            'status': 'success',
            'message': 'Expense created successfully',
            'data': {'expense': expense}
        }), 201
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Expense creation failed: {str(e)}'}), 500

@app.route('/api/expenses/<expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    """Update existing expense - updates in MongoDB"""
    try:
        user_id = get_jwt_identity()['user_id']
        data = request.get_json()
        
        # Check if expense exists and belongs to user
        expense = mongo.db.expenses.find_one({
            '_id': ObjectId(expense_id),
            'user_id': user_id
        })
        if not expense:
            return jsonify({'status': 'error', 'message': 'Expense not found'}), 404
        
        # Prepare update document
        update_doc = {'updated_at': datetime.utcnow()}
        
        # Update fields if provided
        if 'amount' in data:
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    raise ValueError()
                update_doc['amount'] = amount
            except (ValueError, TypeError):
                return jsonify({'status': 'error', 'message': 'Invalid amount'}), 400
        
        if 'note' in data:
            if not data['note'].strip():
                return jsonify({'status': 'error', 'message': 'Note cannot be empty'}), 400
            update_doc['note'] = data['note'].strip()
        
        if 'expense_date' in data:
            try:
                expense_date = datetime.fromisoformat(data['expense_date'].replace('Z', '+00:00'))
                update_doc['expense_date'] = expense_date
            except ValueError:
                return jsonify({'status': 'error', 'message': 'Invalid date format'}), 400
        
        if 'category_id' in data:
            category_id = data['category_id']
            category = mongo.db.categories.find_one({
                '_id': ObjectId(category_id),
                'user_id': user_id
            })
            if not category:
                return jsonify({'status': 'error', 'message': 'Invalid category'}), 400
            update_doc['category_id'] = category_id
        
        # Update in MongoDB
        mongo.db.expenses.update_one(
            {'_id': ObjectId(expense_id)},
            {'$set': update_doc}
        )
        
        # Get updated expense
        updated_expense = mongo.db.expenses.find_one({'_id': ObjectId(expense_id)})
        updated_expense['id'] = str(updated_expense['_id'])
        del updated_expense['_id']
        updated_expense['expense_date'] = updated_expense['expense_date'].isoformat()
        updated_expense['created_at'] = updated_expense['created_at'].isoformat()
        updated_expense['updated_at'] = updated_expense['updated_at'].isoformat()
        
        return jsonify({
            'status': 'success',
            'message': 'Expense updated successfully',
            'data': {'expense': updated_expense}
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Update failed: {str(e)}'}), 500

@app.route('/api/expenses/<expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    """Remove existing expense - deletes from MongoDB"""
    try:
        user_id = get_jwt_identity()['user_id']
        
        # Check if expense exists and belongs to user
        expense = mongo.db.expenses.find_one({
            '_id': ObjectId(expense_id),
            'user_id': user_id
        })
        if not expense:
            return jsonify({'status': 'error', 'message': 'Expense not found'}), 404
        
        # Delete from MongoDB
        mongo.db.expenses.delete_one({'_id': ObjectId(expense_id)})
        
        return jsonify({
            'status': 'success',
            'message': 'Expense deleted successfully'
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Delete failed: {str(e)}'}), 500

@app.route('/api/expenses/summary', methods=['GET'])
@jwt_required()
def get_expense_summary():
    """Get expense summary with filtering - from MongoDB"""
    try:
        user_id = get_jwt_identity()['user_id']
        filter_type = request.args.get('filter')
        
        # Build MongoDB query
        query = {'user_id': user_id}
        
        # Apply date filtering if specified
        if filter_type:
            now = datetime.utcnow()
            
            if filter_type == 'past_week':
                query['expense_date'] = {'$gte': now - timedelta(days=7)}
            elif filter_type == 'last_month':
                first_day_current = now.replace(day=1)
                last_month = first_day_current - timedelta(days=1)
                first_day_last_month = last_month.replace(day=1)
                query['expense_date'] = {
                    '$gte': first_day_last_month,
                    '$lte': last_month
                }
            elif filter_type == 'last_3_months':
                query['expense_date'] = {'$gte': now - timedelta(days=90)}
        
        # Get expenses from MongoDB
        expenses = list(mongo.db.expenses.find(query))
        
        # Calculate summary
        total_amount = sum(exp['amount'] for exp in expenses)
        total_count = len(expenses)
        
        category_breakdown = {}
        for expense in expenses:
            cat_id = expense['category_id']
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
                }
            }
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Summary failed: {str(e)}'}), 500

# ERROR HANDLERS
@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'status': 'error', 'message': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    print("=" * 80)
    print("MONGODB EXPENSE TRACKER API - READY FOR POSTMAN!")
    print("=" * 80)
    print("ALL REQUIREMENTS IMPLEMENTED:")
    print("   - User Authentication with JWT")
    print("   - User Signup Functionality")
    print("   - JWT Token Generation & Validation")
    print("   - Expense Filtering:")
    print("     - Past week")
    print("     - Last month")
    print("     - Last 3 months") 
    print("     - Custom date range")
    print("   - Expense CRUD Operations:")
    print("     - Add new expenses")
    print("     - Remove existing expenses")
    print("     - Update existing expenses")
    print("     - List expenses")
    print("   - JWT Protection on ALL endpoints")
    print("   - Predefined Categories:", ", ".join(EXPENSE_CATEGORIES))
    print("   - Data Model with efficient category handling")
    print("   - MONGODB DATA PERSISTENCE - All data saved to MongoDB!")
    print()
    print("SERVER STARTING ON: http://127.0.0.1:5000")
    print("TEST ENDPOINTS:")
    print("   GET  /health")
    print("   POST /api/users/register")
    print("   POST /api/users/login")
    print("   GET  /api/categories")
    print("   POST /api/categories")
    print("   GET  /api/expenses")
    print("   POST /api/expenses")
    print("   PUT  /api/expenses/<id>")
    print("   DELETE /api/expenses/<id>")
    print("   GET  /api/expenses/summary")
    print("=" * 80)
    print("READY FOR POSTMAN TESTING - DATA WILL BE SAVED TO MONGODB!")
    print("=" * 80)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
