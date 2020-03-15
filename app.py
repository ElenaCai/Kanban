from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
if __name__!="__main__":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class Todo(db.Model): #each task has id, text, complete and doing status
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)
    doing = db.Column(db.Boolean)

@app.route('/') #diract to main page of the website
def index():
    incomplete = Todo.query.filter_by(complete=False, doing=False).all()  # filter by incomplete items
    doing = Todo.query.filter_by(complete=False, doing=True).all()
    complete = Todo.query.filter_by(complete=True, doing=False).all()
    return render_template('index.html', incomplete=incomplete, doing=doing,
                           complete=complete)  # links to the html file

@app.route('/add', methods=['POST'])  #add a task
def add():
    todo = Todo(text=request.form['todoitem'], complete=False, doing=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/doing/<id>')  #start doing a task
def doing(id):
    todo = Todo.query.filter_by(id=int(id)).first()  #query for the todo
    todo.complete = False
    todo.doing = True
    db.session.commit()  #commit the update
    return redirect(url_for('index'))


@app.route('/complete/<id>')  #complete a task
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()  #query for the todo
    todo.complete = True
    todo.doing = False
    db.session.commit()  #commit the update
    return redirect(url_for('index'))


@app.route('/incomplete/<id>')  #incomplete a task
def incomplete(id):
    todo = Todo.query.filter_by(id=int(id)).first()  #query for the todo
    todo.complete = False
    todo.doing = False
    db.session.commit()  #commit the update
    return redirect(url_for('index'))


@app.route('/delete/<id>')  #delete a task
def delete(id):
    todo = Todo.query.filter_by(id=int(id)).first()  # query for the todo
    db.session.delete(todo)  # delete the task
    db.session.commit()  # commit the update
    return redirect(url_for('index'))


@app.route('/random_select')  #randomly select a task for the procrastinators that don't know where to start
def random_select():
    choices = Todo.query.filter_by(complete=False).all() #filter by non-complete tasks
    id = random.choice(choices)
    id.complete = False
    id.doing = True
    db.session.commit()  #commit the update
    return redirect(url_for('selected_task', task_id=str(id.text)))


@app.route('/selected_task/<task_id>') #use for magic dice selected task
def selected_task(task_id):
    incomplete = Todo.query.filter_by(complete=False, doing=False).all()
    doing = Todo.query.filter_by(complete=False, doing=True).all()
    complete = Todo.query.filter_by(complete=True, doing=False).all()
    select = True
    return render_template('index.html', incomplete=incomplete, doing=doing, complete=complete, select=select,
                           task_id=task_id)


if __name__ == '__main__':
    app.run(debug=True)  #use debug
