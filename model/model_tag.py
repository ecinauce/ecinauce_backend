from settings import project_db


class Tag:
	def __init__(self, _id):
		self.name = ""
		self._id = _id # mongo generated


	def db_commit(self):
		project_db["tags"].replace_one(
			{"_id": self._id}, 
			self.__dict__, 
			upsert=True)
