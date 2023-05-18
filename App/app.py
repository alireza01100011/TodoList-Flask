from flask import Flask , render_template , redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Database.db"

db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html' , title='Home')


if __name__ == '__main__':
    app.run(debug=True)