from flask import Flask , render_template , redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Intensification Of Database Manager 
db = SQLAlchemy()
# Intensification Of Flask App
app = Flask(__name__)
# Set DataBase
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Database.db"
# Set Flask App in DBMS
db.init_app(app)

# Database Structure 
class Todo(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100) , unique=True, nullable=False)
    Content = db.Column(db.Text , unique=False , nullable=False)
    CreationTime = db.Column(db.DateTime , default=datetime.now , unique=False , nullable=False)
    ReminderTime = db.Column(db.DateTime , unique=False , nullable=False)

# Create DataBase
with app.app_context() :
    db.create_all()

# HomePage
@app.route('/')
def home():
    return render_template('home.html' , title='Home')


if __name__ == '__main__':
    app.run(debug=True)