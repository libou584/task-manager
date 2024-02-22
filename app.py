from flask import Flask, g, render_template, request
import sqlite3
import datetime
# import os


# TEMPLATE_DIR = os.path.abspath('./templates')
# STATIC_DIR = os.path.abspath('./templates/static')


app = Flask(__name__) # template_folder = TEMPLATE_DIR, static_folder=STATIC_DIR
DATABASE = "tasks.db"



def get_db() :
	db = getattr(g, '_database', None)
	if db is None :
		db = g._database = sqlite3.connect(DATABASE)
	return db


@app.teardown_appcontext
def close_connection(exception) :
	db = getattr(g, '_database', None)
	if db is not None :
		db.close()


@app.route("/")
def display() :
	connection = get_db()
	c = connection.cursor()
	c.execute("SELECT title, description, tag FROM Tasks WHERE status = 'ndone' ORDER BY priority ;")
	task_list = c.fetchall()
	print(task_list)
	return render_template("homepage.html", task_list = task_list)


@app.route("/add_task", methods = ['GET', 'POST'])
def add_task() :
	if request.method == 'POST' :
		connection = get_db()
		c = connection.cursor()
		c.execute("SELECT MAX(id)+1 FROM Tasks ;")
		id = c.fetchall()[0][0]
		if id is None :
			id = 0
		else :
			id = int(id)
		title = request.form['title']
		description = request.form['description']
		tag = request.form['tag']
		priority = request.form['priority']
		if not priority : 
			priority = 5
		status = "ndone"
		date = str(datetime.date.today())
		c.execute(f"INSERT INTO Tasks(id, title, description, status, date, tag, priority) VALUES (?, ?, ?, ?, ?, ?, ?) ;", (id, title, description, status, date, tag, priority))
		connection.commit()
	return render_template("add_task.html")