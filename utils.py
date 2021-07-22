def bson_parse(item):
	item["_id"] = str(item["_id"])
	return item