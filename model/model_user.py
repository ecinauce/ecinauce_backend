from .model_skill import Skill
from .model_experience import Experience
from .model_contact import Contact
from ..settings import project_db
from ..utils import bson_parse


class User:
	def __init__(self, _id):
		self.name = ""
		self._id = _id
		self.objective = ""
		self.skills = []
		self.experiences = []
		self.contacts = []


	def add_skills(self, name):
		skill_item = project_db["skills"].insert_one({"name": name})
		skill_id = skill_item.inserted_id
		
		skill_instance = Skill(skill_id)
		skill_instance.name = name
		self.skills.add(skill_id)


	def add_experience(self, name):
		exp_item = project_db["experiences"].insert_one({"name": name})
		exp_id = exp_item.inserted_id
		
		exp_instance = Experience(exp_id)
		exp_instance.name = name
		self.experiences.add(cat_id)


	def add_contacts(self, name):
		con_item = project_db["contacts"].insert_one({"name": name})
		con_id = con_item.inserted_id
		
		con_instance = Contact(con_id)
		con_instance.name = name
		self.contacts.add(con_id)


	def load(self):
		item = project_db["users"].find_one({"_id": self._id})
		return bson_parse(item)
	

	def get_json(self):
		item = self.load()
		item["skills"] = [Skill(skill).load() for skill in self.skills]
		item["experiences"] = [Experience(exp).load() for exp in self.experiences]
		item["contacts"] = [Contact(cont).load() for cont in self.contacts]
		return item
	

	def commit(self):
		project_db["users"].replace_one(
			{"_id": self._id}, 
			self.__dict__, 
			upsert=True)