from model_user import User

class Contact:
	def __init__(self, user):
		self.user = user # exsting mongoId
		self.details = {} # import from mongo