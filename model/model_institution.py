from model_field import Field
from settings import project_db


class Institution:
	def __init__(self):
		self.name = ""
		self._id = ""
		self.fields = []


	def add_field(self, name):
		field_item = project_db["fields"].insert_one({"name": name})
		field_id = field_item.inserted_id
		
		field_instance = Field(field_id)
		field_instance.name = name
		self.fields.add(field_id)


	def db_commit(self):
		project_db["institutions"].replace_one(
			{"_id": self._id}, 
			self.__dict__, 
			upsert=True)