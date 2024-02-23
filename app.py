from flask import Flask, g, render_template, request, redirect, url_for
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


@app.route("/", methods = ['GET', 'POST'])
def homepage() :
	connection = get_db()
	c = connection.cursor()
	c.execute("SELECT id, title, description, tag FROM Tasks WHERE status = 'ndone' ORDER BY priority ;")
	task_list = c.fetchall()
	if request.method == 'POST' :
		if 'modify' in request.form :
			id = request.form['modify']
			return redirect(url_for("modify", id = id))
		if 'done' in request.form :
			id = request.form['done']
			c.execute("UPDATE Tasks SET status = 'done' WHERE id = (?)", id)
			connection.commit()
			return redirect(url_for("homepage"))
	return render_template("homepage.html", task_list = task_list)


@app.route("/<int:id>/modify")
def modify(id : int) :
	connection = get_db()
	c = connection.cursor()
	c.execute('SELECT title, description, tag, priority FROM Tasks WHERE id = (?) ;', (id, ))
	title, description, tag, priority = c.fetchall()[0]
	if request.method == 'POST' :
		title = request.form['title']
		description = request.form['description']
		tag = request.form['tag']
		priority = request.form['priority']
		if priority is None :
			priority = 5
		c.execute("UPDATE Tasks SET title = (?), description = (?), tag = (?), priority = (?) WHERE id = (?)", (title, description, tag, priority, id))
		connection.commit()
	return render_template("modify.html", title = title)


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
		if priority is None :
			priority = 5
		status = "ndone"
		date = str(datetime.date.today())
		c.execute("INSERT INTO Tasks(id, title, description, status, date, tag, priority) VALUES (?, ?, ?, ?, ?, ?, ?) ;", (id, title, description, status, date, tag, priority))
		connection.commit()
	return render_template("add_task.html")


@app.route("/done_tasks", methods = ['GET', 'POST'])
def done_tasks() :
	connection = get_db()
	c = connection.cursor()
	c.execute("SELECT id, title, description, tag FROM Tasks WHERE status = 'done' ORDER BY priority ;")
	done_task_list = c.fetchall()
	if request.method == 'POST' :
		id = request.form['undo']
		c.execute("UPDATE Tasks SET status = 'ndone' WHERE id = (?)", id)
		connection.commit()
		return redirect(url_for("homepage"))
	return render_template("done_tasks.html", done_task_list = done_task_list)