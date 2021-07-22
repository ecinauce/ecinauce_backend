from .model_tag import Tag
from ..settings import 
from ..utils import bson_parse


class Category:
	def __init__(self, _id):
		self.name = ""
		self._id = _id # mongo generated
		self.tags = []


	def add_tag(self, name):
		tag_item = project_db["tags"].insert_one({"name": name})
		tag_id = tag_item.inserted_id
		
		tag_instance = Tag(tag_id)
		tag_instance.name = name
		self.tags.add(tag_id)


	def load(self):
		item = project_db["categories"].find_one({"_id": self._id})
		return bson_parse(item)
	

	def get_json(self):
		item = self.load()
		item["tags"] = [Tag(tag).load() for tag in self.tags]
		return item


	def commit(self):
		project_db["categories"].replace_one(
			{"_id": self._id}, 
			self.__dict__, 
			upsert=True)
