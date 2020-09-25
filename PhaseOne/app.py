from flask import Flask, request
from flask_api import status
from store import Store
import requests
import json
import os

app = Flask(__name__)
myStore = Store()

@app.route('/kv-store/<key>', methods=['GET', 'PUT', 'DELETE'])
def store(key):
	forwarding = os.environ.get('FORWARDING_ADDRESS')

	# if the clients request was sent to the 
	# main instance, then main instance directly
	# responds to client
	# else, if the clients request was sent to the 
	# follower instance, then the follower forwards 
	# the request to main and main responds to follower
	# who then forwards it to the client
	if forwarding == 'not_set': 
		if request.method == 'PUT':
			return putRequest(key)
		elif request.method == 'GET':
			return getRequest(key)
		elif request.method == 'DELETE':
			return deleteRequest(key)
	else: 
		#main instance url
		main_url = "http://" + forwarding + "/kv-store/" + key

		#forward the request to the main instance
		try:
			resp = requests.request(method=request.method,
									url=main_url, 
									headers=request.headers,
									data=request.data, timeout=1)
		except requests.exceptions.Timeout:
			if request.method == 'GET':
				err = json.dumps({"error":"Main instance is down","message":"Error in GET"})
			elif request.method == 'PUT':
				err = json.dumps({"error":"Main instance is down","message":"Error in PUT"})
			elif request.method == 'DELETE':
				err = json.dumps({"error":"Main instance is down","message":"Error in DELETE"})

			return err + '\n', status.HTTP_503_SERVICE_UNAVAILABLE
		else:
			return resp.content, resp.status_code
		
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
	app.run(host='0.0.0.0', port=13800)