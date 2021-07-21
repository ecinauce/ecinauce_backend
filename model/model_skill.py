from model_category import Category
from settings import project_db


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


	def db_commit(self):
		project_db["skills"].replace_one(
			{"_id": self._id}, 
			self.__dict__, 
			upsert=True)
