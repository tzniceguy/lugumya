from budgetwebapp import db, UserMixin
from enum import Enum

# Creating a class that contains a list of account types a user can add: Mobile Money, Bank, and Cash
class AccountType(Enum):
    MOBILE_MONEY = 'Mobile Money'
    CASH = 'Cash'
    BANK = 'Bank'


'''
Creating the tables to use in our database.
Using SQLite3 database for this project, but planning to migrate to either MySQL or PostgreSQL.
'''
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    profile = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(30), nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy=True, foreign_keys='Expense.user_id')  # Add foreign_keys argument
    budgets = db.relationship('Budget', backref='user', lazy=True)

    @property
    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile}')"


# Enum class for expense categories
class expense_category(Enum):
    FOOD = 'Food'
    RENT = 'Rent'
    DRINKS_BEVERAGES = 'Drinks and Beverages'
    NEW_PROPERTY = 'New Property'
    OTHER_1 = 'Other 1'
    OTHER_2 = 'Other 2'
    OTHER_3 = 'Other 3'
    OTHER_4 = 'Other 4'

# Model for expense categories
class ExpenseCategory(db.Model):
    __tablename__ = 'expense_category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(expense_category), nullable=False)

    def __init__(self, name):
        self.name = name

# Model for expenses
class Expense(db.Model):
    __tablename__ = 'expense'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Add foreign key constraint
    category_id = db.Column(db.Integer, db.ForeignKey('expense_category.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    date = db.Column(db.Date, nullable=False)

    def __init__(self, user_id, category_id, amount, description, date):
        self.user_id = user_id
        self.category_id = category_id
        self.amount = amount
        self.description = description
        self.date = date


# Model for budget categories
class BudgetCategory(db.Model):
    __tablename__ = 'budget_category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, name):
        self.name = name

# Model for budgets
class Budget(db.Model):
    __tablename__ = 'budget'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('budget_category.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    def __init__(self, user_id, category_id, amount, start_date, end_date):
        self.user_id = user_id
        self.category_id = category_id
        self.amount = amount
        self.start_date = start_date
        self.end_date = end_date

# Model for user accounts
class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.Enum(AccountType), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    account = db.Column(db.String(255), nullable=False)

    def __init__(self, name, account_type, account):
        self.name = name
        self.account_type = account_type
        self.account = account

#Model for Income table
class Income(db.Model):
    __tablename__ = 'income'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date_in = db.Column(db.Date, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    account = db.relationship('Account', backref=db.backref('income', lazy=True))

    def __init__(self, amount, date_in, account_id):
        self.amount = amount
        self.date_in = date_in
        self.account_id = account_id





        