from flask import Flask, request
from flask_api import status
import json
from store import Store

app = Flask(__name__)
myStore = Store()

@app.route('/kv-store/<key>', methods=['GET', 'PUT', 'DELETE'])
def store(key):

	if request.method == 'PUT':
		json_data = request.get_json()

		if json_data:
			val = json_data['value']
			if len(val) >= 50:
				return json.dumps({"error":"Key is too long","message":"Error in PUT"}) +'\n', status.HTTP_400_BAD_REQUEST
			else:
				return str(val) + '\n'#myStore.insert(key, val)
		else:
			return json.dumps({"error":"Value is missing","message":"Error in PUT"}) + '\n', status.HTTP_400_BAD_REQUEST

	#if PUT request
		#if key exists, update value
		#else insert key/value into store
	#else if GET request
		#if key exists, return value to client
		#else return 404 error code to client
	#else if DELETE request
		#if key exists, delete key and value from store, return 200 status code
		#else return 404 error code

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8081)