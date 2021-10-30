from flask import Flask, g, render_template, request

import sqlite3

app = Flask(__name__)

def get_message_db():
	if "message_db" not in g:
		g.message_db = sqlite3.connect("messages_db.sqlite")

	cursor = g.message_db.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS \
					messages(id INT, handle TEXT, message TEXT)")

	return g.message_db

def insert_message(request):
	if request.method == "POST":
		message = request.form["message"]
		handle = request.form["handle"]

		db = get_message_db()
		cursor = db.cursor()
		cursor.execute("SELECT COUNT(*) FROM messages")
		row = cursor.fetchone() # get the current number of rows
		cursor.execute("INSERT INTO messages(id, handle, message)\
						VALUES(" + str(row[0] + 1) + ", \""+ handle + "\", \"" + message + "\")")

		db.commit()
		db.close()

def random_messages(n):
	
	db = get_message_db()
	cursor = db.cursor()
	cursor.execute("SELECT * FROM messages ORDER BY RANDOM() LIMIT " + str(n))
	random_messages = cursor.fetchall()
	db.close()
	return random_messages


@app.route("/")
def main():
	return render_template("base.html")

@app.route("/submit/", methods = ["POST", "GET"])
def submit():

	# the case of transmitting data
	if request.method == "GET":
		return render_template("submit.html")

	# the case of receiving data
	else: 
		try:
			insert_message(request)
			return render_template("submit.html", thanks = True)
		except:
			return render_template("submit.html", error = True)

@app.route("/view/")
def view():
	# call random_messages() and pass the random messages to the "view" html template
	return render_template("view.html", random_messages = random_messages(5))















