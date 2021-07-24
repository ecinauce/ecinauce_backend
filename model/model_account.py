from ..settings import project_db
from ..utils import bson_parse


class Account:
	def __init__(self, username):
		self._id = ""
		self.username = username
		self.password = ""


	def load(self):
		item = project_db["accounts"].find_one({"username": self.username})
		return bson_parse(item)
	

	def commit(self):
		project_db["accounts"].replace_one(
			{"_id": self._id}, 
			self.__dict__, 
			upsert=True)