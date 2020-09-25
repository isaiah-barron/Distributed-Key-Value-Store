import requests
from requests.packages.urllib3.connectionpool import HTTPConnectionPool
import json

url = 'http://127.0.0.1:13800/kv-store/'
header = {"Content-Type" : "application/json"}
testStatus = []

############### PUT request tests #########################

print("\nTESTING PUT REQUESTS...\n")

#insert new key/value pair into store
print("--------Test1---------- \nTesting inserting new key/value pair into store...\n\n")

key = 'sampleKey'
val = 'sampleValue'
response = requests.put(url+key, headers=header, data=json.dumps({"value": val}))
expected = json.dumps({"message":"Added successfully","replaced":"False"})
actual = response.json()

if actual['message'] == "Added successfully":
	testStatus.append("passed")
else:
	testStatus.append("failed")
	print(f'Test failed......\nExpected response from server: \n{expected}\n')
	print(f'Actual response from server: \n{response.json()}\n')

#update existing key with new value
print("--------Test2---------- \nTesting updating existing key with new value...\n\n")

val = 'dogcat'
response = requests.put(url+key, headers=header, data=json.dumps({"value": val}))
expected = json.dumps({"message":"Updated successfully","replaced":"True"})
actual = response.json()

if actual['message'] == "Updated successfully":
	testStatus.append("passed")
else:
	testStatus.append("failed")
	print(f'Test failed......\nExpected response from server: \n{expected}\n')
	print(f'Actual response from server: \n{response.json()}\n')

# #test key is too long edge case
print("--------Test3---------- \nTesting long key...\n\n")

key = 'dogwatermelonfood'
response = requests.put(url+key, headers=header, data=json.dumps({"value": val}))
expected = json.dumps({"error":"Key is too long","message":"Error in PUT"})
actual = response.json()

if actual['error'] == "Key is too long":
	testStatus.append("passed")
else:
	testStatus.append("failed")
	print(f'Test failed......\nExpected response from server: \n{expected}\n')
	print(f'Actual response from server: \n{response.json()}\n')

# #test missing value for key
print("--------Test4---------- \nTesting missing value for key...\n\n")

key = 'sampleKey'
response = requests.put(url+key, headers=header, data=json.dumps({})) ##send request with no data
expected = json.dumps({"error":"Value is missing","message":"Error in PUT"})
actual = response.json()

if actual['error'] == "Value is missing":
	testStatus.append("passed")
else:
	testStatus.append("failed")
	print(f'Test failed......\nExpected response from server: \n{expected}\n')
	print(f'Actual response from server: \n{response.json()}\n')

############### DELETE request tests #########################

print("\nTESTING DELETE REQUESTS...\n")

#deleting an existing key/val pair
print("--------Test5---------- \nTesting deleting an existing key/value pair in the store...\n\n")

response = requests.delete(url+key, headers=header)
expected = json.dumps({"doesExist":"True","message":"Deleted successfully"})
actual = response.json()

if actual['doesExist']:
	testStatus.append("passed")
else:
	testStatus.append("failed")
	print(f'Test failed......\nExpected response from server: \n{expected}\n')
	print(f'Actual response from server: \n{response.json()}\n')

#delete a non-existing key/value pair
print("--------Test6---------- \nTesting deleting a non-existing key/value pair in the store...\n\n")

response = requests.delete(url+key, headers=header)
expected = json.dumps({"doesExist":"False","error":"Key does not exist","message":"Error in DELETE"})
actual = response.json()

if actual['doesExist'] == False:
	testStatus.append("passed")
else:
	testStatus.append("failed")
	print(f'Test failed......\nExpected response from server: \n{expected}\n')
	print(f'Actual response from server: \n{response.json()}\n')

############### GET request tests #########################

print("\nTESTING GET REQUESTS...\n")

#get existing key/value pair
print("--------Test7---------- \nTesting grabbing a existing key/value pair in the store...\n\n")

val = 'breathCat'
requests.put(url+key, headers=header, data=json.dumps({"value": val}))
response = requests.get(url+key, headers=header)
expected = json.dumps({"doesExist":"True","message":"Retrieved successfully","value":val})
actual = response.json()

if actual['doesExist'] and actual['value'] == val:
	testStatus.append('passed')
else:
	print(f'Test failed......\nExpected response from server: \n{expected}\n')
	print(f'Actual response from server: \n{actual}\n')
	testStatus.append('failed')
	
#get updated existing key/value pair
print("--------Test8---------- \nTesting grabbing a updated existing key/value pair in the store...\n\n")
val = 'manbrainslice'
requests.put(url+key, headers=header, data=json.dumps({"value": val}))
response = requests.get(url+key, headers=header)
expected = json.dumps({"doesExist":"True","message":"Retrieved successfully","value":val})
actual = response.json()

if actual['doesExist'] and  actual['value'] == val:
	testStatus.append('passed')
else:
	testStatus.append('failed')
	print(f'Test failed......\nExpected response from server: \n{expected}\n')
	print(f'Actual response from server: \n{actual}\n')

#get a non-existing key/value pair
print("--------Test9---------- \nTesting grabbing a non-existing key/value pair in the store...\n\n")

key = 'donkeytail'
response = requests.get(url+key, headers=header)
expected = json.dumps({"doesExist":"False","error":"Key does not exist","message":"Error in GET"})
actual = response.json()

if actual['doesExist'] == False:
	testStatus.append('passed')
else:
	testStatus.append('failed')
	print(f'Test failed......\nExpected response from server: \n{expected}\n')
	print(f'Actual response from server: \n{actual}\n')

############### Main/Follower tests #########################

#test main instance with put request
print("--------Test10---------- \nTesting Main instance...\n\n")

requests.delete(url+key, headers=header)

rsp = requests.put(url+key, headers=header, data=json.dumps({"value": val}), stream=True)

try:
	ip, port = rsp.raw._fp.fp.raw._sock.getpeername() #grab port of the server that responded
except AttributeError as error:
	testStatus.append('failed')
	print(f'Test failed with error {error}')
else:
	actual = rsp.json()
	expected = json.dumps({"message":"Added successfully","replaced":"False"})

	#check if key was added successfully and the main instance responded to the client
	if str(port) == '13800' and actual['message'] == "Added successfully":
		testStatus.append('passed')
	else:
		testStatus.append('failed')
		print(f'Test failed......\nExpected response from server: \n{expected}\n with port 13800' )
		print(f'Actual response from server: \n{actual}\n with port {port}')

#test follower instance with put request
print("--------Test11---------- \nTesting follower instance...\n\n")

val ='sammyhammyjammy'
url = 'http://127.0.0.1:13801/kv-store/' #send request to follower
rsp = requests.put(url+key, headers=header, data=json.dumps({"value": val}), stream=True)

try:
	ip, port = rsp.raw._fp.fp.raw._sock.getpeername() #grab port of the server that responded
except AttributeError as error:
	testStatus.append('failed')
	print(f'Test failed with error...\n {error}')
else:
	actual = rsp.json()
	expected = json.dumps({"message":"Updated successfully","replaced":"True"})

	#check if key was added successfully and the follower instance forward the response to the client
	if str(port) == '13801' and actual['message'] == "Updated successfully":
		testStatus.append('passed')
	else:
		testStatus.append('failed')
		print(f'Test failed......\nExpected response from server: \n{expected}\n with port 13801')
		print(f'Actual response from server: \n{actual}\n with port {port}')

#count how many tests were passed
num = 0
for passed in testStatus:
	if passed == "passed":
		num += 1

print(f'\nTESTS PASSED {num}/{len(testStatus)}')


