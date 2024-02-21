from flask import Flask, g, render_template, request
import sqlite3
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
	c = get_db().cursor()
	content = "<!DOCTYPE html><title>&#x1F5D2; Task Manager</title>"
	# content += "<h1>Task Manager</h1>"
	content += "<a href = '/add_tag'>Add a tag</a>"
	content += "<h2>Tasks</h2>"
	c.execute("SELECT * FROM Tasks ;")
	content += "<table><tr><td>Title</td><td>Description</td><td>Status</td><td>Date</td></tr>"
	for tpl in c.fetchall() :
		content += render_template("line_temp.html", title = tpl[1], description = tpl[2], status = tpl[3], date = tpl[4])
	content += "</table>"
	return content


@app.route("/tags/")
def tags() :
	c = get_db().cursor()
	c.execute("SELECT name FROM Tags;")
	tag_list = c.fetchall()
	return render_template("tags.html", tag_list = tag_list)


@app.route("/add_tag/", methods = ['POST'])
def add_tag() :
	c = get_db().cursor()
	name = request.form["name"]
	c.execute(f"INSERT INTO Tags (id, name) VALUES (SELECT MAX(id) FROM Tags, {name})")
	return render_template("tag_form.html")