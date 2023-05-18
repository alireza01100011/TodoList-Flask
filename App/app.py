from flask import Flask , render_template , redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Database.db"

db.init_app(app)

class Todo(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100) , unique=True, nullable=False)
    Content = db.Column(db.Text , unique=False , nullable=False)
    CreationTime = db.Column(db.DateTime , default=datetime.now , unique=False , nullable=False)
    ReminderTime = db.Column(db.DateTime , unique=False , nullable=False)


@app.route('/')
def home():
    return render_template('home.html' , title='Home')


if __name__ == '__main__':
    app.run(debug=True)