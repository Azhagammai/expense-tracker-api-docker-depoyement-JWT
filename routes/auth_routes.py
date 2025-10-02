from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models.user import UserRegistrationSchema, UserLoginSchema
from services.user_service import UserService
from services.database import db_service

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/users/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        # Validate request data
        schema = UserRegistrationSchema()
        data = schema.load(request.get_json())
        
        # Create user
        user = UserService.create_user(
            data['first_name'],
            data['last_name'],
            data['email'],
            data['password']
        )
        
        # Generate JWT token
        token = UserService.generate_token(user)
        
        return jsonify({
            'status': 'success',
            'message': 'User registered successfully',
            'data': {
                'user': user.to_dict(),
                'token': token
            }
        }), 201
        
    except ValidationError as e:
        return jsonify({
            'status': 'error',
            'message': 'Validation failed',
            'errors': e.messages
        }), 400
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred during registration'
        }), 500

@auth_bp.route('/users/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        # Validate request data
        schema = UserLoginSchema()
        data = schema.load(request.get_json())
        
        # Authenticate user
        user = UserService.authenticate_user(
            data['email'],
            data['password']
        )
        
        # Generate JWT token
        token = UserService.generate_token(user)
        
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'data': {
                'user': user.to_dict(),
                'token': token
            }
        }), 200
        
    except ValidationError as e:
        return jsonify({
            'status': 'error',
            'message': 'Validation failed',
            'errors': e.messages
        }), 400
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 401
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred during login'
        }), 500

@auth_bp.route('/users/profile', methods=['GET'])
def get_profile():
    """Get user profile (requires authentication)"""
    from flask_jwt_extended import jwt_required, get_jwt_identity
    
    try:
        # This will be protected by JWT middleware
        current_user = get_jwt_identity()
        
        user = UserService.get_user_by_id(current_user['user_id'])
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': {
                'user': user.to_dict()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while fetching profile'
        }), 500
