from flask import Flask, g, render_template, request

import sqlite3

app = Flask(__name__)

def get_message_db():
	if 'message_db' not in g:
        g.message_db = sqlite3.connect('messages_db.sqlite')

    cursor = g.message_db.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS messages(id INT, handle TEXT, message TEXT)')

    return g.message_db

def insert_message(request):
	if request.method == 'POST':
		message = request.form['message']
		handle = request.form['handle']

		db = get_message_db()
		cursor = db.cursor()
		cursor.execute('SELECT COUNT(*) FROM messages')
		row = cursor.fetchone() # get the current number of rows
		cursor.execute('INSERT INTO messages(id, handle, message) VALUES ("str(row[0] + 1", \
						handle, message)')
		
		db.commit()
		db.close()

