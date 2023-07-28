from budgetwebapp import app
from budgetwebapp import db

if __name__ == '__main__':
    with app.app_context():
        # Create the tables
        db.create_all()

    app.run(debug=True)