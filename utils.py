from .settings import project_db


def bson_parse(item):
	item["_id"] = str(item["_id"])
	return item


def validate_user(username):
	user = project_db["users"].find_one({"username": username})
	return bson_parse(user)


def validate_registration(username):
	user = project_db["users"].find_one({"username": username})
	return True if not user else False
