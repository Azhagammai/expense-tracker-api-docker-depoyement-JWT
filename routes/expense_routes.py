from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from models.expense import ExpenseSchema, ExpenseUpdateSchema
from services.expense_service import ExpenseService
from datetime import datetime

expense_bp = Blueprint('expenses', __name__)

@expense_bp.route('/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    """Get expenses with optional filtering"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        
        # Get query parameters
        category_id = request.args.get('category_id')
        filter_type = request.args.get('filter')  # past_week, last_month, last_3_months, custom
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        limit = request.args.get('limit', type=int)
        
        # Parse dates if provided
        start_date = None
        end_date = None
        
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
        
        # Get expenses based on filter type
        if filter_type:
            expenses = ExpenseService.get_expenses_by_filter(
                user_id, filter_type, start_date, end_date
            )
        else:
            expenses = ExpenseService.get_user_expenses(
                user_id, category_id, start_date, end_date, limit
            )
        
        # Get summary if requested
        include_summary = request.args.get('include_summary', 'false').lower() == 'true'
        response_data = {
            'expenses': [expense.to_dict() for expense in expenses]
        }
        
        if include_summary:
            summary = ExpenseService.get_expense_summary(user_id, start_date, end_date)
            response_data['summary'] = summary
        
        return jsonify({
            'status': 'success',
            'data': response_data
        }), 200
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while fetching expenses'
        }), 500

@expense_bp.route('/expenses/<expense_id>', methods=['GET'])
@jwt_required()
def get_expense(expense_id):
    """Get a specific expense by ID"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        
        expense = ExpenseService.get_expense_by_id(expense_id, user_id)
        
        if not expense:
            return jsonify({
                'status': 'error',
                'message': 'Expense not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': {
                'expense': expense.to_dict()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while fetching expense'
        }), 500

@expense_bp.route('/expenses', methods=['POST'])
@jwt_required()
def create_expense():
    """Create a new expense"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        
        # Validate request data
        schema = ExpenseSchema()
        data = schema.load(request.get_json())
        
        # Create expense
        expense = ExpenseService.create_expense(
            data['amount'],
            data['note'],
            data['expense_date'],
            data['category_id'],
            user_id
        )
        
        return jsonify({
            'status': 'success',
            'message': 'Expense created successfully',
            'data': {
                'expense': expense.to_dict()
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
            'message': 'An error occurred while creating expense'
        }), 500

@expense_bp.route('/expenses/<expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    """Update an existing expense"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        
        # Validate request data
        schema = ExpenseUpdateSchema()
        data = schema.load(request.get_json())
        
        # Update expense
        expense = ExpenseService.update_expense(
            expense_id,
            user_id,
            data.get('amount'),
            data.get('note'),
            data.get('expense_date'),
            data.get('category_id')
        )
        
        return jsonify({
            'status': 'success',
            'message': 'Expense updated successfully',
            'data': {
                'expense': expense.to_dict()
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
            'message': 'An error occurred while updating expense'
        }), 500

@expense_bp.route('/expenses/<expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    """Delete an expense"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        
        ExpenseService.delete_expense(expense_id, user_id)
        
        return jsonify({
            'status': 'success',
            'message': 'Expense deleted successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while deleting expense'
        }), 500

@expense_bp.route('/expenses/summary', methods=['GET'])
@jwt_required()
def get_expense_summary():
    """Get expense summary with totals and breakdowns"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        
        # Get date filters
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        filter_type = request.args.get('filter')
        
        start_date = None
        end_date = None
        
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
        
        # Apply filter if specified
        if filter_type:
            expenses = ExpenseService.get_expenses_by_filter(
                user_id, filter_type, start_date, end_date
            )
            # Calculate dates for summary
            if expenses:
                start_date = min(expense.expense_date for expense in expenses)
                end_date = max(expense.expense_date for expense in expenses)
        
        summary = ExpenseService.get_expense_summary(user_id, start_date, end_date)
        
        return jsonify({
            'status': 'success',
            'data': {
                'summary': summary,
                'period': {
                    'start_date': start_date.isoformat() if start_date else None,
                    'end_date': end_date.isoformat() if end_date else None
                }
            }
        }), 200
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while generating summary'
        }), 500
