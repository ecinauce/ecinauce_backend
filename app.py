from flask import Flask, session, request, render_template, url_for, redirect
from flask.json import jsonify
from passlib.hash import sha256_crypt
from .model.model_user import User
from .settings import project_db
from .utils import validate_user, validate_registration


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/user/<username>")
def get_user(username):
	if 'username' in session:
		if session["username"] == username:
			user = project_db["users"].find_one({"username": username})["_id"]
			return User(user).get_json()
		else:
			return 'Invalid User'
	return 'You are not logged in'
	

@app.route('/')
def index():
	if 'username' in session:
		user = project_db["users"].find_one({"username": session["username"]})["_id"]
		return User(user).get_json()
	return 'You are not logged in'


@app.route("/register", methods=['POST', 'GET'])
def register():
	if request.method == 'POST':
		if validate_registration(request.form['username'], request.form["password"], request.form["vrf_password"]):
			user_item = project_db["users"].insert_one({"username": request.form['username']})
			user_id = user_item.inserted_id

			password = request.form['password']
			project_db["accounts"].insert_one({"user_id": user_id, "password": sha256_crypt.encrypt(password)})
			return jsonify(User(user_id).get_json())
		else:
			return '''<b>Registration Error, user might already exist or there is password mismatch.</b>'''
	return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if validate_user(request.form["username"], request.form["password"]):
			session['username'] = request.form['username']
			return redirect(url_for('index'))
		else:
			return '''
				<b>Login</b>
				<b>Invalid Credentials</b>
				<form method="post">
					<label for="username">Username:</label><br>
					<p><input type=text name=username></p>
					<label for="password">Password:</label><br>
					<input type="password" name="password"><br>
					<p><input type=submit value=Login></p>
				</form>	'''	
	return '''
		<b>Login</b>
		<form method="post">
			<label for="username">Username:</label><br>
			<p><input type=text name=username></p>
			<label for="password">Password:</label><br>
			<input type="password" name="password"><br>
			<p><input type=submit value=Login></p>
		</form>	'''


@app.route('/logout')
def logout():
	# remove the username from the session if it's there
	session.pop('username', None)
	return redirect(url_for('index'))
