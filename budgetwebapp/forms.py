from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DecimalField,FloatField, SelectField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=4,max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confrim_password = PasswordField('Confrim Password', validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=4,max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit= SubmitField('Login')

class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit= SubmitField('Login')


class ExpenseForm(FlaskForm):
    category_id = SelectField('Expense Category', coerce=int, validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    description = TextAreaField('Description')
    date = DateField('Date', validators=[DataRequired()])
    submit= SubmitField('Record Expense')

class BudgetForm(FlaskForm):
    category_id = SelectField('Budget Category', choices=[('DEVELOPMENT_BUDGET', 'Development'), ('Expenditure_Budget', 'Expenditure')], validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit= SubmitField('Add Budget')

class AccountForm(FlaskForm):
    account_type = SelectField('Account Type', choices=[('MOBILE_MONEY', 'Mobile Money'), ('CASH', 'Cash'), ('BANK', 'Bank')], validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(max=30)])
    account = StringField('Account', validators=[DataRequired(), Length(max=255)])
    submit= SubmitField('Add Account')

class IncomeForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    date_in = DateField('Date', validators=[DataRequired()])
    account_in =SelectField('Account Type', choices=[('MOBILE_MONEY', 'Mobile Money'), ('CASH', 'Cash'), ('BANK', 'Bank')] , validators=[DataRequired()])
    submit= SubmitField('Add Income')