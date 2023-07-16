from flask import render_template, url_for, flash, redirect
from budgetwebapp import app, db
from flask_login import login_user, logout_user, login_required, current_user
from budgetwebapp.forms import RegistrationForm, LoginForm, ResetPasswordForm, ExpenseForm, BudgetForm,AccountForm,IncomeForm 
from budgetwebapp.models import User, Expense, Income, Budget
from werkzeug.security import generate_password_hash as hasher, check_password_hash as verfy

# Importing necessary modules and dependencies

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

# Route for the "About" page
@app.route("/about")
def about():
    return render_template('about.html', title="About")

# Route for the user registration page
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #hashing the password so as to store it in a database as hash and not text for security
        password_hash = hasher(form.password.data)
        # Create a new User instance with the form data
        new_user = User(username=form.username.data, email=form.email.data, password=password_hash)
         # Add the user to the database
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Route for the user login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and verfy(user.password, form.password.data):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', title='Login', form=form)

# Dashboard route accessible only for authenticated users
@app.route("/dashboard")
@login_required
def dashboard():
    user = current_user.username
    return render_template('dashboard.html', title='Account', user=user)

# Logout route for the user
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

# Route for the password reset page
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        flash('Password reset successful', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form, messages=flash.get_flashed_messages())

#route for expenses page
@app.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    recent_expenses = Expense.query.order_by(Expense.date.desc()).limit(10).all()
    form = ExpenseForm()
    if form.validate_on_submit():
        amount = form.amount.data
        description = form.description.data
        date = form.date.data
        expense = Expense(amount=amount, description=description, date=date)
        #adding the income to the database
        try:
            db.session.add(expense)
            db.session.commit()
            return redirect(url_for("expense"))
        except:
            return 'Error adding an ecpense in'
    else:
        table = Expense.query.order_by(Income.date_in)

        flash('Expense Recorded Sucessfully!', 'success')
    return render_template('expense.html', expenses=recent_expenses, form=form,table=table)

@app.route('/income', methods=['GET', 'POST'])
@login_required
def income():
    recent_transactions = Income.query.order_by(Income.date_in.desc()).limit(10).all()
    form = IncomeForm()
    if form.validate_on_submit():
        amount = form.amount.data
        amount = form.amount.data
        date_in = form.date_in.data
        account_id = form.account_in.data
        income = Income(amount=amount, date_in=date_in, account_id=account_id)
        #adding the income to the database
        try:
            db.session.add(income)
            db.session.commit()
            return redirect(url_for("income"))
        except:
            return 'Error adding an income in'
    else:
        table = Income.query.order_by(Income.date_in)
        return render_template('income.html', recent_transactions=recent_transactions, form=form, table=table)

@app.route('/budget', methods=['GET', 'POST'])
@login_required
def budget():
    recent_expenses = Expense.query.order_by(Expense.date.desc()).limit(10).all()
    form = BudgetForm()
    
    if form.validate_on_submit():
        amount = form.amount.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        
        # Create a new budget object
        budget = Budget(amount=amount, start_date=start_date, end_date=end_date)
        
        try:
            db.session.add(budget)
            db.session.commit()
            flash('Budget Recorded Successfully!', 'success')
        except:
            flash('Failed to add budget', 'danger')
        
        return redirect(url_for('budget'))
    
    table = Budget.query.order_by(Budget.start_date.desc()).all()
    return render_template('budget.html', expenses=recent_expenses, form=form, table=table)
