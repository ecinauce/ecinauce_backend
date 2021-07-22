from .model_institution import Institution
from ..settings import project_db
from ..utils import bson_parse


class Experience:
	def __init__(self, _id):
		self.name = ""
		self._id = _id
		self.institutions = []


	def add_institution(self, name):
		inst_item = project_db["institutions"].insert_one({"name": name})
		inst_id = inst_item.inserted_id
		
		inst_instance = Institution(institution_id)
		institution_instance.name = name
		self.institutions.add(inst_id)


	def load(self):
		item = project_db["exeriences"].find_one({"_id": self._id})
		return bson_parse(item)
	

	def get_json(self):
		item = self.load()
		item["institutions"] = [Institution(inst).load() for inst in self.institutions]
		return item
	

	def commit(self):
		project_db["exeriences"].replace_one(
			{"_id": self._id}, 
			self.__dict__, 
			upsert=True)
