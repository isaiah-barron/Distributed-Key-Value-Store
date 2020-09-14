from flask_api import status
import json

class Store():

	#dictionary for kv store
	kv_store = {}

	def insert(self, key, val):
		update = False
		if key in Store.kv_store:
			update = True

		#insert key/value parir into store
		#will create a new entry or update existing key
		Store.kv_store[key] = val

		#to indicate which response to return to client 
		if update:
			return json.dumps({"message":"Updated successfully","replaced":True}) + '\n', status.HTTP_200_OK
		else:
			return json.dumps({"message":"Added successfully","replaced":False}) + '\n', status.HTTP_201_CREATED

	def get(key):
		if key in Store.kv_store:
			val = Store.kv_store[key]
			return json.dumps({"doesExist":True,"message":"Retrieved successfully","value": val}) + '\n', status.HTTP_200_OK
		else:
			return json.dumps({"doesExist":False,"error":"Key does not exist","message":"Error in GET"}) + '\n', status.HTTP_404_NOT_FOUND

	# def delete(key):