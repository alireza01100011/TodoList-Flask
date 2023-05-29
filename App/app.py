from flask import Flask , render_template , redirect , url_for , request
from flask_sqlalchemy import SQLAlchemy
from webbrowser import open_new_tab
from winotify import Notification , audio

from datetime import datetime
from time import sleep
from threading import Thread
from requests import get

import pickle

IP = '127.0.0.1'
PORT = '1401'

# <================================App And DataBase==================================>

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

# Returns A Sorted List Of All Tasks 
def GetTask()->list[Todo]:
    # Get All Tasks
    items = Todo.query.all()
    # Build Storage Space
    tasks = [None for i in range(len(items))]
    # Sort Data By Time
    SortDeata = sorted([task.ReminderTime for task in items])
    # Add Tasks To The List 
    for task in items:
        tasks[SortDeata.index(task.ReminderTime)] = task
    
    return tasks




# <================================Home==================================>
# HomePage
@app.route('/')
def home():
    # Get All Task
    tasks = GetTask()
    
    return render_template(
        'home.html', # Html File
        title='Todo List', # Title Web Page
        tasks=tasks, # List Tasks
        Title_From = 'Add New Task', # Title From
        URL_Action='AddTask', # Url -> Action Form
        ID='', # Defulte
        value_title='', # Defulte
        value_content='', # Defulte
        value_time='' # Defulte
        )

# <================================About==================================>
# About Page
@app.route('/about')
def about():
    return redirect('https://github.com/alireza536')

# <================================Delete Task==================================>
# Delete Task
@app.route('/Delete/<ID>')
def Delete(ID):
    task = Todo.query.get(ID)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))

# <================================Done Task==================================>
# Task Done Operation 
@app.route('/Done/<ID>')
def Done(ID):
    task = Todo.query.get(ID)
    task.Done = 1
    db.session.commit()
    return redirect(url_for('home'))

# <================================Add Task==================================>
# Add New Task
# It Receives The Information From The Form And Adds The New Task 
@app.route('/AddTask/', methods=('GET', 'POST'))
def AddNewTask():
    if request.method == 'POST':
        try :
            # Create New Task
            newtask = Todo(
                Title=request.form['title'],
                Content= request.form['content'] ,
                ReminderTime =request.form['time'])
        
        except KeyError:
            return redirect(url_for('home'))
        
        # Add New Task To Database
        db.session.add(newtask)
        db.session.commit()

        return redirect(url_for('home'))

# <================================Edite Task==================================>
# Edit Task 
# This Function Prepares The Main Page For Editing 
@app.route('/Edite/<int:ID>')
def Edite(ID):
    # Get The Selected Task For Editing 
    task = Todo.query.get(ID)
    # Get All Tasks Sorted For Display 
    tasks = GetTask()
    # Send Information To The Main Page 
    return render_template(
            'home.html', # Html File
            title='Todo List', # Title
            tasks=tasks, # All Tasks For Display 
            Title_From = f'Edite Todo : {task.Title}', # The Title Of The Form 
            URL_Action='-Edite', # The Address That Will Send The Data Form In The End {Action Url}
            ID=f'{int(ID)}', # Task Id Selected For Editing 
            value_title=f'{task.Title}' , # Task Name Or Title In The Form Field 
            value_content=f'{task.Content}', # Task Description In The Form Field 
            value_time=f'{task.ReminderTime}', # Task Reminder Time In The Form Field 
            )


# This Function Applies The Received Values To Edit The Task In The Database 
@app.route('/-Edite/<ID>' , methods=('GET', 'POST'))
def edite(ID):
    if request.method == 'POST':
        # Get Task
        task = Todo.query.get(ID)
        # Set Id - [ To Not Change The ID ]
        task.Id = int(ID)
        # Set New Title
        task.Title  = request.form['title']
        # Set New Description
        task.Content = request.form['content']
        # Set New Reminder Time
        task.ReminderTime = request.form['time']
        # Seve
        db.session.commit()
        # Refresh The Page To Show The Changes 
        return redirect(url_for('home'))

@app.route('/GetAllData')
def ReturnAllTask():
    return pickle.dumps(GetTask())
# <================================Mian(Run)==================================>
def Send_Notification(Url=f'http://{IP}:{PORT}' , *args , **kwargs ):
    Noti = Notification(*args , **kwargs , icon=r'F:\Alireza\Python\TodoList-Flask\App\static\icon.ico' , app_id='Todo List' , duration='short')
    Noti.set_audio(audio.Reminder , True)
    Noti.add_actions(label='Todo List' , launch=Url)
    Noti.add_actions(label='Done' , launch=f'{Url}')
    Noti.show()

def Reminder():
    sleep(5)
    Ids = []
    while True:
        sleep(10)
        try : 
            Tasks = get(f'http://{IP}:{PORT}/GetAllData').content
        except OSError : pass
        for task in pickle.loads(Tasks):
            if task.Done == 1 : continue
            if f"{task.ReminderTime}" == f"{datetime.now().strftime('%H:%M')}" and task.Id not in Ids:
                Send_Notification(title=task.Title,msg=task.Content)
                Ids.append(task.Id)

if __name__ == '__main__':
    
    open_new_tab(f'http://{IP}:{PORT}')
    Thread(target=Reminder).start()
    app.run(debug=False , host=IP , port=int(PORT))