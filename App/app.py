from flask import Flask , render_template , redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html' , title='Home')


if __name__ == '__main__':
    app.run(debug=True)