from passlib.hash import sha256_crypt
from .settings import project_db


def bson_parse(item):
	item["_id"] = str(item["_id"])
	return item


def validate_user(username, password):
	user = project_db["users"].find_one({"username": username})
	v_password = project_db["accounts"].find_one({"user_id": user["_id"]})["password"]
	
	if sha256_crypt.verify(password, v_password):
		return bson_parse(user)


def validate_registration(username, pass1, pass2):
	user = project_db["users"].find_one({"username": username})
	password = pass1 == pass2
	return True if not user and password else False
