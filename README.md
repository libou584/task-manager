# Task Manager

Web application task manager using python flask and databases

Requirements : sqlite3

#### Python virtual environment initialization:

	$ python3 -m env env
	$ echo "env/" >> .gitignore
	$ source env/bin/activate
	$ python3 -m pip install -r requirements.txt
	$ deactivate

#### SQLite database initialization:

	$ touch tasks.db
	$ echo "tasks.db" >> .gitignore
	$ sqlite3 tasks.db
	sqlite> CREATE TABLE Tasks(id integer, title varchar, description varchar, status varchar, date date, tag varchar, priority integer);
	sqlite> .quit

#### Usage (after both python virtual environment and sqlite database initiallizations) :

	$ source env/bin/activate
	$ flask run	

Do what you do

	Ctrl+C
	$ deactivate
