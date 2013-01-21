from __future__ import with_statement
from contextlib import closing
import sqlite3 # Using sqlite3 as a database
from flask import Flask, render_template, g, request, flash, redirect, url_for, session, escape

# Configutraion - most of this would need to change before being pushed to a server. Going to experiment with moving config to a seperate file soon.
DATABASE = '/tmp/dothis.db'
DEBUG = True
SECRET_KEY = 'dev key'
USERNAME = 'Admin'
PASSWORD = 'dev'

# Create the app
app = Flask(__name__)
# Pulls config settings from the Caps settings above.
app.config.from_object(__name__)

# Database fun

# Creates the database using schema.sql
def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()


def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	g.db.close()


@app.route('/')
def home():
	# Makes sure user is logged in before writing to db.
	if session.get('logged_in'):
		c = g.db.execute('select id, task from entries order by id desc')
		entries = [dict(id=row[0], task=row[1]) for row in c.fetchall()]
		# Passes the entries to a variable that is used in the template.
		return render_template('index.html', entries=entries)
	else:
		return render_template('index.html')

# Logging in and out
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		# This is like the least secure way to handle passwords.
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid Username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid Password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('home'))
	else:
		return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('home'))

# Add and Remove Items - /add doesn't have to be a rendered page, the form just calls it.
@app.route('/add', methods=['POST'])
def add_task():
	g.db.execute('INSERT INTO entries (task) VALUES (?)', [request.form['task']])
	g.db.commit() 
	flash('New task was added succesfully')
	return redirect(url_for('home'))

@app.route('/remove', methods=['POST'])
def remove_task():
	g.db.execute('DELETE FROM entries WHERE id=(?)', [request.form['id']])
	g.db.commit()
	flash('Task removed successfully')
	return redirect(url_for('home'))

# app.run() should always be in an if __name__ = '__main__' to work well when deploying to servers.
if __name__ == '__main__':
	app.run()
