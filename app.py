from flask import Flask, session, request, render_template, url_for, redirect
from flask.json import jsonify

from .model.model_user import User
from .settings import project_db
from .utils import validate_user, validate_registration


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/user/<username>")
def get_user(username):
	if 'username' in session:
		user = project_db["users"].find_one({"username": username})["_id"]
		return User(user).get_json()
	return 'You are not logged in'
	

### Logins are a problem for another day
@app.route('/')
def index():
	if 'username' in session:
		user = project_db["users"].find_one({"username": session["username"]})["_id"]
		return User(user).get_json()
	return 'You are not logged in'


@app.route("/register", methods=['POST', 'GET'])
def register():
	if request.method == 'POST':
		if validate_registration(request.form['username']):
			user_item = project_db["users"].insert_one({"username": request.form['username']})
			user_id = user_item.inserted_id
			return jsonify(User(user_id).get_json())
		else:
			return '''<b>User already exists</b>'''
	return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if validate_user(request.form["username"]):
			session['username'] = request.form['username']
			return redirect(url_for('index'))
		else:
			return '''
				<b>Invalid Credentials</b>
				<form method="post">
					<p><input type=text name=username>
					<p><input type=submit value=Login>
				</form>	'''	
	return '''
		<form method="post">
			<p><input type=text name=username>
			<p><input type=submit value=Login>
		</form>	'''


@app.route('/logout')
def logout():
	# remove the username from the session if it's there
	session.pop('username', None)
	return redirect(url_for('index'))
