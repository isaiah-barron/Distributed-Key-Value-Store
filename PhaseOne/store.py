from flask_api import status
import json

class Store():

	#dictionary for kv store
	kv_store = {}

	def insert(self, key, val):
		Store.kv_store['key'] = val
		return json.dumps({"message":"Added successfully","replaced":False}) + '\n', status.HTTP_201_CREATED

	# def get(key):


	# def delete(key):