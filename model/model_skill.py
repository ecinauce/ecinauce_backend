from .model_category import Category
from ..settings import project_db
from ..utils import bson_parse


class Skill:
	def __init__(self, _id):
		self.name = ""
		self._id = _id
		self.categories = []


	def add_category(self, name):
		cat_item = project_db["categories"].insert_one({"name": name})
		cat_id = cat_item.inserted_id
		
		cat_instance = Category(cat_id)
		cat_instance.name = name
		self.categories.add(cat_id)


	def load(self):
		item = project_db["skills"].find_one({"_id": self._id})
		return bson_parse(item)
	

	def get_json(self):
		item = self.load()
		item["categories"] = [Category(cat).load() for cat in self.categories]
		return item
	

	def commit(self):
		project_db["skills"].replace_one(
			{"_id": self._id}, 
			self.__dict__, 
			upsert=True)
