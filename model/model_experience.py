from model_institution import Institution
from settings import project_db


class Experience:
	def __init__(self):
		self.name = ""
		self._id = ""
		self.institutions = []


	def add_institution(self, name):
		inst_item = project_db["institutions"].insert_one({"name": name})
		inst_id = inst_item.inserted_id
		
		inst_instance = Institution(institution_id)
		institution_instance.name = name
		self.institutions.add(inst_id)


	def db_commit(self):
		project_db["exeriences"].replace_one(
			{"_id": self._id}, 
			self.__dict__, 
			upsert=True)
