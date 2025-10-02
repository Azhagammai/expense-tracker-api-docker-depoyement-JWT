from bson import ObjectId
from marshmallow import Schema, fields, validate
from datetime import datetime

class Expense:
    def __init__(self, amount, note, expense_date, category_id, user_id, _id=None):
        self._id = _id
        self.amount = float(amount)
        self.note = note
        self.expense_date = expense_date if isinstance(expense_date, datetime) else datetime.fromisoformat(expense_date.replace('Z', '+00:00'))
        self.category_id = ObjectId(category_id) if isinstance(category_id, str) else category_id
        self.user_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            '_id': str(self._id) if self._id else None,
            'amount': self.amount,
            'note': self.note,
            'expense_date': self.expense_date.isoformat(),
            'category_id': str(self.category_id),
            'user_id': str(self.user_id),
            'created_at': self.created_at.isoformat()
        }

class ExpenseSchema(Schema):
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    note = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    expense_date = fields.DateTime(required=True)
    category_id = fields.Str(required=True)

class ExpenseUpdateSchema(Schema):
    amount = fields.Float(validate=validate.Range(min=0.01))
    note = fields.Str(validate=validate.Length(min=1, max=500))
    expense_date = fields.DateTime()
    category_id = fields.Str()
