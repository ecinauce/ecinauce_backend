class Contact:
	def __init__(self, _id):
		self._id = _id # exsting mongoId
		self.details = {} # import from mongo