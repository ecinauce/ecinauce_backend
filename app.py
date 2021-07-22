from flask import Flask
from flask import session
from flask import request
from flask import render_template, url_for
from flask.json import jsonify

from .model.model_user import User
from .settings import project_db


app = Flask(__name__)
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/user/<username>")
def get_user(username):
	user = project_db["users"].find_one({"name": username})["_id"]
	return User(user).get_json()


@app.route("/reg_user/", methods=['POST', 'GET'])
def reg_user():
	if request.method == 'POST':
		user_item = project_db["users"].insert_one({"name": request.form['username']})
		user_id = user_item.inserted_id
		return jsonify(User(user_id).get_json())
	return render_template('register.html')


### Logins are a problem for another day
# @app.route('/', user=user)
# def index():
#     if 'username' in session:
#         return f'Logged in as {session["username"]}'
#     return 'You are not logged in'

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('index'))
#     return '''
#         <form method="post">
#             <p><input type=text name=username>
#             <p><input type=submit value=Login>
#         </form>
#     '''

# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('index'))
