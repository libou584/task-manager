# Task Manager

Web application task manager using python flask and databases


Database schema :

    CREATE TABLE Tasks(id integer, title varchar, description varchar, status varchar, date date, tag integer, priority integer);
    CREATE TABLE Tags(id integer, name varchar);