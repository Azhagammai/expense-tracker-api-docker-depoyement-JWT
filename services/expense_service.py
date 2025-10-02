from bson import ObjectId
from models.expense import Expense
from services.database import db_service
from services.category_service import CategoryService
from datetime import datetime, timedelta
import calendar

class ExpenseService:
    @staticmethod
    def create_expense(amount, note, expense_date, category_id, user_id):
        """Create a new expense"""
        # Validate category belongs to user
        category = CategoryService.get_category_by_id(category_id, user_id)
        if not category:
            raise ValueError("Category not found or doesn't belong to user")
        
        # Create expense
        expense = Expense(amount, note, expense_date, category_id, user_id)
        
        expense_data = {
            'amount': expense.amount,
            'note': expense.note,
            'expense_date': expense.expense_date,
            'category_id': expense.category_id,
            'user_id': expense.user_id,
            'created_at': expense.created_at
        }
        
        expense_id = db_service.insert_one('expenses', expense_data)
        expense._id = expense_id
        
        return expense
    
    @staticmethod
    def get_user_expenses(user_id, category_id=None, start_date=None, end_date=None, limit=None):
        """Get expenses for user with optional filtering"""
        query = {'user_id': ObjectId(user_id)}
        
        if category_id:
            if not db_service.is_valid_object_id(category_id):
                raise ValueError("Invalid category ID")
            query['category_id'] = ObjectId(category_id)
        
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query['$gte'] = start_date
            if end_date:
                date_query['$lte'] = end_date
            query['expense_date'] = date_query
        
        expenses_data = db_service.find_many('expenses', 
                                           query,
                                           sort=[('expense_date', -1)],
                                           limit=limit)
        
        expenses = []
        for exp_data in expenses_data:
            expense = Expense(
                exp_data['amount'],
                exp_data['note'],
                exp_data['expense_date'],
                exp_data['category_id'],
                exp_data['user_id'],
                exp_data['_id']
            )
            expenses.append(expense)
        
        return expenses
    
    @staticmethod
    def get_expense_by_id(expense_id, user_id):
        """Get expense by ID for specific user"""
        if not db_service.is_valid_object_id(expense_id):
            return None
        
        expense_data = db_service.find_one('expenses', {
            '_id': ObjectId(expense_id),
            'user_id': ObjectId(user_id)
        })
        
        if not expense_data:
            return None
        
        expense = Expense(
            expense_data['amount'],
            expense_data['note'],
            expense_data['expense_date'],
            expense_data['category_id'],
            expense_data['user_id'],
            expense_data['_id']
        )
        
        return expense
    
    @staticmethod
    def update_expense(expense_id, user_id, amount=None, note=None, expense_date=None, category_id=None):
        """Update expense"""
        if not db_service.is_valid_object_id(expense_id):
            raise ValueError("Invalid expense ID")
        
        # Get existing expense
        existing_expense = ExpenseService.get_expense_by_id(expense_id, user_id)
        if not existing_expense:
            raise ValueError("Expense not found")
        
        update_data = {}
        
        if amount is not None:
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
            update_data['amount'] = float(amount)
        
        if note is not None:
            if not note.strip():
                raise ValueError("Note cannot be empty")
            update_data['note'] = note.strip()
        
        if expense_date is not None:
            update_data['expense_date'] = expense_date
        
        if category_id is not None:
            # Validate category belongs to user
            category = CategoryService.get_category_by_id(category_id, user_id)
            if not category:
                raise ValueError("Category not found or doesn't belong to user")
            update_data['category_id'] = ObjectId(category_id)
        
        if update_data:
            success = db_service.update_one('expenses',
                                          {'_id': ObjectId(expense_id), 'user_id': ObjectId(user_id)},
                                          update_data)
            if not success:
                raise ValueError("Failed to update expense")
        
        # Return updated expense
        return ExpenseService.get_expense_by_id(expense_id, user_id)
    
    @staticmethod
    def delete_expense(expense_id, user_id):
        """Delete expense"""
        if not db_service.is_valid_object_id(expense_id):
            raise ValueError("Invalid expense ID")
        
        # Check if expense exists
        expense = ExpenseService.get_expense_by_id(expense_id, user_id)
        if not expense:
            raise ValueError("Expense not found")
        
        success = db_service.delete_one('expenses', {
            '_id': ObjectId(expense_id),
            'user_id': ObjectId(user_id)
        })
        
        if not success:
            raise ValueError("Failed to delete expense")
        
        return True
    
    @staticmethod
    def get_expenses_by_filter(user_id, filter_type, start_date=None, end_date=None):
        """Get expenses by predefined filters or custom date range"""
        now = datetime.utcnow()
        
        if filter_type == 'past_week':
            start_date = now - timedelta(days=7)
            end_date = now
        elif filter_type == 'last_month':
            # Get first day of last month
            first_day_current_month = now.replace(day=1)
            last_month = first_day_current_month - timedelta(days=1)
            start_date = last_month.replace(day=1)
            end_date = last_month.replace(day=calendar.monthrange(last_month.year, last_month.month)[1])
        elif filter_type == 'last_3_months':
            start_date = now - timedelta(days=90)
            end_date = now
        elif filter_type == 'custom':
            if not start_date or not end_date:
                raise ValueError("Custom filter requires both start_date and end_date")
        else:
            raise ValueError("Invalid filter type. Must be one of: past_week, last_month, last_3_months, custom")
        
        return ExpenseService.get_user_expenses(user_id, start_date=start_date, end_date=end_date)
    
    @staticmethod
    def get_expense_summary(user_id, start_date=None, end_date=None):
        """Get expense summary with total amount and count"""
        expenses = ExpenseService.get_user_expenses(user_id, start_date=start_date, end_date=end_date)
        
        total_amount = sum(expense.amount for expense in expenses)
        total_count = len(expenses)
        
        # Group by category
        category_summary = {}
        for expense in expenses:
            cat_id = str(expense.category_id)
            if cat_id not in category_summary:
                category_summary[cat_id] = {'amount': 0, 'count': 0}
            category_summary[cat_id]['amount'] += expense.amount
            category_summary[cat_id]['count'] += 1
        
        return {
            'total_amount': total_amount,
            'total_count': total_count,
            'category_breakdown': category_summary
        }
