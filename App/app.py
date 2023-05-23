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
    ReminderTime = db.Column(db.Text , unique=False , nullable=False)
    Done = db.Column(db.Integer , default=0 , unique=False , nullable=False)
    
    def __repr__(self):
        return f'Todo({self.Id} , {self.Title} , {self.Content} , {self.ReminderTime} , {self.Done})'
# Create DataBase
with app.app_context() :
    db.create_all()

# HomePage
@app.route('/')
def home():
    items = Todo.query.all()
    tasks = [None for i in range(len(items))]
    SortDeata = sorted([task.ReminderTime for task in items])
    for task in items:
        tasks.insert(SortDeata.index(task.ReminderTime) , task)
    
    for task in tasks : 
        if task == None : tasks.remove(task)

    return render_template('home.html' , title='Home' , tasks=tasks)


@app.route('/about')
def about():
    return redirect('https://github.com/alireza536')

@app.route('/Delete/<ID>')
def Delete(ID):
    task = Todo.query.get(ID)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/Done/<ID>')
def Done(ID):
    task = Todo.query.get(ID)
    task.Done = 1
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/AddTodo')
def AddTodo():
    return render_template('from.html' , title='Add Todo' , value_content='' , value_title='' , value_time='' , URL_Action='AddTask' , ID='')


@app.route('/AddTask/', methods=('GET', 'POST'))
def CreateTodo():
    if request.method == 'POST':
        try :
            newtask = Todo(
                Title=request.form['title'],
                Content= request.form['content'] ,
                ReminderTime =request.form['time'])
        except KeyError:
            return redirect(url_for('AddTodo'))
        
        db.session.add(newtask)
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/Edite/<int:ID>')
def Edite(ID):
    task = Todo.query.get(ID)
    return render_template('from.html' , title=f'Edite {task.Title}' , value_content=f'{task.Content}' , value_title=f'{task.Title}' , value_time='05:02' , URL_Action='-Edite' , ID=f'{int(ID)}')

@app.route('/-Edite/<ID>' , methods=('GET', 'POST'))
def edite(ID):
    if request.method == 'POST':
        task = Todo.query.get(ID)
        task.Id = int(ID)
        task.Title  = request.form['title']
        task.Content = request.form['content']
        task.ReminderTime = request.form['time']
        db.session.commit()
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True , host='192.168.1.9')