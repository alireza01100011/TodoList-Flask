from flask import Flask , render_template , redirect , url_for , request
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
    ReminderTime = db.Column(db.Text , unique=False , nullable=False)


# Create DataBase
with app.app_context() :
    db.create_all()

# HomePage
@app.route('/')
def home():
    tasks = Todo.query.all()
    return render_template('home.html' , title='Home' , tasks=tasks)

@app.route('/Delete/<ID>')
def Delete(ID):
    task = Todo.query.get(ID)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/AddTodo')
def AddTodo():
    return render_template('addtodo.html' , title='Add Todo')

@app.route('/AddTask/', methods=('GET', 'POST'))
def CreateTodo():
    if request.method == 'POST':
        try:
            newtask = Todo(
            Title=request.form['title'],
            Content= request.form['content'] ,
            ReminderTime =request.form['time'])
        except KeyError:
            return redirect(url_for('AddTodo'))
        
        db.session.add(newtask)
        db.session.commit()
        return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)