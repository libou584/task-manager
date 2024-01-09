from flask import Flask, g, render_template
import sqlite3


app = Flask(__name__)
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
	content += "<table><tr><td><h3>Tasks</h3></td><td><h3>Today</h3></td></tr>"
	c.execute("SELECT * FROM Tasks ;")
	content += "<tr><td><table>"
	content += "<tr><td>Title</td><td>Description</td><td>Status</td><td>Date</td></tr>"
	for tpl in c.fetchall() :
		content += render_template("line_temp.html", title = tpl[1], description = tpl[2], status = tpl[3], date = tpl[4])
	content += "</table></td>"
	content += "<td><table>"
	c.execute("SELECT * FROM Tasks ;")
	content += "<tr><td>Title</td><td>Description</td><td>Status</td><td>Date</td></tr>"
	for tpl in c.fetchall() :
		content += render_template("line_temp.html", title = tpl[1], description = tpl[2], status = tpl[3], date = tpl[4])
	content += "</table></td></tr>"
	return content
