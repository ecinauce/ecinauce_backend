import jwt, os
from traceback import print_exc
from flask import Flask, session, request, render_template, url_for, redirect
from flask_cors import CORS
from flask.json import jsonify
from passlib.hash import sha256_crypt
from .model.model_user import User
from .settings import project_db
from .utils import validate_user, validate_registration, bson_parse
from functools import wraps


app = Flask(__name__)
app.secret_key = os.urandom(16)
CORS(app)

# CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/register", methods=['POST', 'GET'])
def register():
	if request.method == 'POST':
		output = dict(request.get_json())
		if validate_registration(output["username"], output["password"], output["vrf_password"]):
			user_item = project_db["users"].insert_one({"username": output['username']})
			user_id = user_item.inserted_id

			password = output['password']
			project_db["accounts"].insert_one({"user_id": user_id, "password": sha256_crypt.encrypt(password)})
			return jsonify(User(user_id).get_json())
		else:
			return {"message":"Registration Error, user might already exist or there is password mismatch."}
	return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		output = dict(request.get_json())
		if validate_user(output["username"], output["password"]):
			session['username'] = output['username']
			return {"message": "Logged in"}
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


@app.route('/')
def index():
	if 'username' in session:
		user = project_db["users"].find_one({"username": session["username"]})["_id"]
		output = {
			"status": "ok",
			"payload": User(user).get_json(),
			"session": session
		}
		return output
	# return session
	return {
		"status": "Not logged in"
	}


@app.route("/user/<username>")
def get_user(username):
	if 'username' in session:
		if session["username"] == username:
			user = project_db["users"].find_one({"username": username})["_id"]
			return User(user).get_json()
		else:
			return {
				"status": 'Invalid User'
			}
	return {
		"status": "Not logged in"
		}
	

@app.route("/update_user", methods=['POST'])
def update():
	if 'username' in session:
		if request.method == "POST":
			user_id = project_db["users"].find_one({"username": session['username']})["_id"]
			user = User(user_id).get_json()
			form = output.to_dict()
			user.update(form)
			return user
		return redirect(url_for('index'))
	return redirect(url_for('index'))


# @app.route("/update_experience", methods=['POST'])
# def update():
# 	if 'username' in session:
# 		if request.method == "POST":
# 			user_id = project_db["users"].find_one({"username": session['username']})["_id"]
# 			user = User(user_id).get_json()
# 			form = output.to_dict()
# 			user.update(form)
# 			return user
# 		return redirect(url_for('index'))
# 	return redirect(url_for('index'))


@app.route("/render_html")
def rendering():
	return render_template('form_user.html')


@app.route("/users")
def get_users():
	users = [bson_parse(i) for i in project_db["users"].find()]
	return {
		"status": "ok",
		"payload": users
	}