from bson import ObjectId
from models.category import Category
from services.database import db_service
from config import Config

class CategoryService:
    @staticmethod
    def create_category(title, description, user_id):
        """Create a new category for user"""
        # Validate category title
        if not Category.is_valid_category(title):
            raise ValueError(f"Invalid category. Must be one of: {', '.join(Config.EXPENSE_CATEGORIES)}")
        
        # Check if user already has this category
        existing_category = db_service.find_one('categories', {
            'title': title,
            'user_id': ObjectId(user_id)
        })
        
        if existing_category:
            raise ValueError(f"Category '{title}' already exists for this user")
        
        # Create new category
        category = Category(title, description, user_id)
        
        category_data = {
            'title': category.title,
            'description': category.description,
            'user_id': category.user_id
        }
        
        category_id = db_service.insert_one('categories', category_data)
        category._id = category_id
        
        return category
    
    @staticmethod
    def get_user_categories(user_id):
        """Get all categories for a user"""
        categories_data = db_service.find_many('categories', 
                                             {'user_id': ObjectId(user_id)},
                                             sort=[('title', 1)])
        
        categories = []
        for cat_data in categories_data:
            category = Category(
                cat_data['title'],
                cat_data['description'],
                cat_data['user_id'],
                cat_data['_id']
            )
            categories.append(category)
        
        return categories
    
    @staticmethod
    def get_category_by_id(category_id, user_id):
        """Get category by ID for specific user"""
        if not db_service.is_valid_object_id(category_id):
            return None
        
        category_data = db_service.find_one('categories', {
            '_id': ObjectId(category_id),
            'user_id': ObjectId(user_id)
        })
        
        if not category_data:
            return None
        
        category = Category(
            category_data['title'],
            category_data['description'],
            category_data['user_id'],
            category_data['_id']
        )
        
        return category
    
    @staticmethod
    def update_category(category_id, user_id, title=None, description=None):
        """Update category"""
        if not db_service.is_valid_object_id(category_id):
            raise ValueError("Invalid category ID")
        
        # Get existing category
        existing_category = CategoryService.get_category_by_id(category_id, user_id)
        if not existing_category:
            raise ValueError("Category not found")
        
        update_data = {}
        
        if title is not None:
            if not Category.is_valid_category(title):
                raise ValueError(f"Invalid category. Must be one of: {', '.join(Config.EXPENSE_CATEGORIES)}")
            
            # Check if user already has this category (excluding current one)
            existing_with_title = db_service.find_one('categories', {
                'title': title,
                'user_id': ObjectId(user_id),
                '_id': {'$ne': ObjectId(category_id)}
            })
            
            if existing_with_title:
                raise ValueError(f"Category '{title}' already exists for this user")
            
            update_data['title'] = title
        
        if description is not None:
            update_data['description'] = description
        
        if update_data:
            success = db_service.update_one('categories', 
                                          {'_id': ObjectId(category_id), 'user_id': ObjectId(user_id)},
                                          update_data)
            if not success:
                raise ValueError("Failed to update category")
        
        # Return updated category
        return CategoryService.get_category_by_id(category_id, user_id)
    
    @staticmethod
    def delete_category(category_id, user_id):
        """Delete category and all associated expenses"""
        if not db_service.is_valid_object_id(category_id):
            raise ValueError("Invalid category ID")
        
        # Check if category exists
        category = CategoryService.get_category_by_id(category_id, user_id)
        if not category:
            raise ValueError("Category not found")
        
        # Delete all expenses in this category
        db_service.delete_many('expenses', {
            'category_id': ObjectId(category_id),
            'user_id': ObjectId(user_id)
        })
        
        # Delete the category
        success = db_service.delete_one('categories', {
            '_id': ObjectId(category_id),
            'user_id': ObjectId(user_id)
        })
        
        if not success:
            raise ValueError("Failed to delete category")
        
        return True
