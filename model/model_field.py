from ..settings import project_db
from ..utils import bson_parse


class Field:
	def __init__(self, _id):
		self.name = ""
		self._id = _id


	def load(self):
		item = project_db["fields"].find_one({"_id": self._id})
		return bson_parse(item)
	

	def get_json(self):
		return self.load()
	

	def commit(self):
		project_db["fields"].replace_one(
			{"_id": self._id}, 
			self.__dict__, 
			upsert=True)
