from .model_field import Field
from ..settings import project_db
from ..utils import bson_parse


class Institution:
	def __init__(self, _id):
		self.name = ""
		self._id = _id
		self.fields = []


	def add_field(self, name):
		field_item = project_db["fields"].insert_one({"name": name})
		field_id = field_item.inserted_id
		
		field_instance = Field(field_id)
		field_instance.name = name
		self.fields.add(field_id)


	def load(self):
		item = project_db["institutions"].find_one({"_id": self._id})
		return bson_parse(item)
	

	def get_json(self):
		item = self.load()
		item["fields"] = [Field(field).load() for field in self.fields]
		return item
	

	def commit(self):
		project_db["institutions"].replace_one(
			{"_id": self._id}, 
			self.__dict__, 
			upsert=True)