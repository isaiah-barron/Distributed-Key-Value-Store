from flask import Flask, request
from flask_api import status
from store import Store
import json

app = Flask(__name__)
myStore = Store()

@app.route('/kv-store/<key>', methods=['GET', 'PUT', 'DELETE'])
def store(key):

	if request.method == 'PUT':
		return putRequest(key)
	elif request.mehtod == 'GET':
		return getRequest(key)
	elif request.mehtod == 'DELETE':
		return deleteRequest(key)


def putRequest(key):
	json_data = request.get_json()
	if json_data:
		val = json_data['value']
		if len(key) > 16:
			return json.dumps({"error":"Key is too long","message":"Error in PUT"}) +'\n', status.HTTP_400_BAD_REQUEST
		else:
			return myStore.insert(key, val)
	else:
		return json.dumps({"error":"Value is missing","message":"Error in PUT"}) + '\n', status.HTTP_400_BAD_REQUEST

def getRequest(key):
	return myStore.get(key)

def deleteRequest(key):
	return myStore.delete(key)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8081)