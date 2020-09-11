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

	# def get(key):


	# def delete(key):