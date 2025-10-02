from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from models.category import CategorySchema
from services.category_service import CategoryService

category_bp = Blueprint('categories', __name__)

@category_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all categories for the authenticated user"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        
        categories = CategoryService.get_user_categories(user_id)
        
        return jsonify({
            'status': 'success',
            'data': {
                'categories': [category.to_dict() for category in categories]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while fetching categories'
        }), 500

@category_bp.route('/categories/<category_id>', methods=['GET'])
@jwt_required()
def get_category(category_id):
    """Get a specific category by ID"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        
        category = CategoryService.get_category_by_id(category_id, user_id)
        
        if not category:
            return jsonify({
                'status': 'error',
                'message': 'Category not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': {
                'category': category.to_dict()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while fetching category'
        }), 500

@category_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    """Create a new category"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        
        # Validate request data
        schema = CategorySchema()
        data = schema.load(request.get_json())
        
        # Create category
        category = CategoryService.create_category(
            data['title'],
            data['description'],
            user_id
        )
        
        return jsonify({
            'status': 'success',
            'message': 'Category created successfully',
            'data': {
                'category': category.to_dict()
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
            'message': 'An error occurred while creating category'
        }), 500

@category_bp.route('/categories/<category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    """Update an existing category"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        
        # Validate request data
        schema = CategorySchema()
        data = schema.load(request.get_json())
        
        # Update category
        category = CategoryService.update_category(
            category_id,
            user_id,
            data.get('title'),
            data.get('description')
        )
        
        return jsonify({
            'status': 'success',
            'message': 'Category updated successfully',
            'data': {
                'category': category.to_dict()
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
        }), 400
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while updating category'
        }), 500

@category_bp.route('/categories/<category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    """Delete a category"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        
        CategoryService.delete_category(category_id, user_id)
        
        return jsonify({
            'status': 'success',
            'message': 'Category deleted successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while deleting category'
        }), 500
