from settings import project_db


class Field:
	def __init__(self, _id):
		self.name = ""
		self._id = _id


	def db_commit(self):
		project_db["fields"].replace_one(
			{"_id": self._id}, 
			self.__dict__, 
			upsert=True)