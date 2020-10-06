from flask import Flask, request
from flask_api import status
from store import Store
import requests
import json
import os
import hashlib

app = Flask(__name__)
myStore = Store()

@app.route('/kv-store/keys/<key>', methods=['GET', 'PUT', 'DELETE'])
def store(key):
	#grab current view and IP address of the node that recieved the request
	get_view = os.environ.get('VIEW')
	view = get_view.split(',')
	my_ip = os.environ.get('ADDRESS')

	#hash the key and use it to determine which node the key belongs to
	hash = hashlib.md5(key.encode())
	node = int(hash.hexdigest(), 16) % len(view)

	if my_ip == view[node]: #key belongs on this node (service request)
		if request.method == 'PUT':
			return putRequest(key)
		elif request.method == 'GET':
			return getRequest(key)
		elif request.method == 'DELETE':
			return deleteRequest(key)
	else: #key belongs on a different node (forward request to correct node)

		#forward the request to the correct node
		try:
			node_url = f'http://{view[node]}/kv-store/keys/{key}'
			resp = requests.request(method=request.method,
									url=node_url,
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

@app.route('/kv-store/key-count', methods=['GET'])
def keyCouunt():
	return myStore.size()

# @app.route('/kv-store/view-change', methods=['PUT']

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=13800)