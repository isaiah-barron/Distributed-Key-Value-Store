import requests
import json

url = 'http://127.0.0.1:8081/kv-store/'
key = 'sampleKey'
val = 'sampleValue'
header = {"Content-Type" : "application/json"}
testStatus = []

############### PUT request tests #########################

print("\nTESTING PUT REQUESTS...\n")

#insert new key/value pair into store
print("--------Test1---------- \nTesting inserting new key/value pair into store...\n\n")
response = requests.put(url+key, headers=header, data=json.dumps({"value": val}))
expected = json.dumps({"message":"Added successfully","replaced":"False"})

for k,v in response.json().items():
	if v == "Added successfully":
		testStatus.append("passed")
		break
	else:
		testStatus.append("failed")
		print(f'Test failed......\nExpected response from server: \n{expected}\n')
		print(f'Actual response from server: \n{response.json()}\n')
		break

#update existing key with new value
val = 'dogcat'
print("--------Test2---------- \nTesting updating existing key with new value...\n\n")
response = requests.put(url+key, headers=header, data=json.dumps({"value": val}))
expected = json.dumps({"message":"Updated successfully","replaced":"True"})

for k,v in response.json().items():
	if v == "Updated successfully":
		testStatus.append("passed")
		break
	else:
		testStatus.append("failed")
		print(f'Test failed......\nExpected response from server: \n{expected}\n')
		print(f'Actual response from server: \n{response.json()}\n')
		break

# #test key is too long edge case
key = 'dogwatermelonfood'
print("--------Test3---------- \nTesting long key...\n\n")
response = requests.put(url+key, headers=header, data=json.dumps({"value": val}))
expected = json.dumps({"error":"Key is too long","message":"Error in PUT"})

for k,v in response.json().items():
	if v == "Key is too long":
		testStatus.append("passed")
		break
	else:
		testStatus.append("failed")
		print(f'Test failed......\nExpected response from server: \n{expected}\n')
		print(f'Actual response from server: \n{response.json()}\n')
		break

# #test missing value for key
key = 'sampleKey'
print("--------Test4---------- \nTesting missing value for key...\n\n")
response = requests.put(url+key, headers=header, data=json.dumps({})) ##send request with no data
expected = json.dumps({"error":"Value is missing","message":"Error in PUT"})

for k,v in response.json().items():
	if v == "Value is missing":
		testStatus.append("passed")
		break
	else:
		testStatus.append("failed")
		print(f'Test failed......\nExpected response from server: \n{expected}\n')
		print(f'Actual response from server: \n{response.json()}\n')
		break

############### DELETE request tests #########################

print("\nTESTING DELETE REQUESTS...\n")

#deleting an existing key/val pair
print("--------Test5---------- \nTesting deleting an existing key/value pair in the store...\n\n")
response = requests.delete(url+key, headers=header)
expected = json.dumps({"doesExist":True,"message":"Deleted successfully"})

for k,v in response.json().items():
	if v:
		testStatus.append("passed")
		break
	else:
		testStatus.append("failed")
		print(f'Test failed......\nExpected response from server: \n{expected}\n')
		print(f'Actual response from server: \n{response.json()}\n')
		break

#delete a non-existing key/value pair
print("--------Test6---------- \nTesting deleting a non-existing key/value pair in the store...\n\n")
response = requests.delete(url+key, headers=header)
expected = json.dumps({"doesExist":False,"error":"Key does not exist","message":"Error in DELETE"})

for k,v in response.json().items():
	if v == False:
		testStatus.append("passed")
		break
	else:
		testStatus.append("failed")
		print(f'Test failed......\nExpected response from server: \n{expected}\n')
		print(f'Actual response from server: \n{response.json()}\n')
		break

############### GET request tests #########################

# print("\nTESTING GET REQUESTS...\n")

# #get existing key/value pair
# print("--------Test7---------- \nTesting grabbing a existing key/value pair in the store...\n\n")
# val = 'breathCat'
# requests.put(url+key, headers=header, data=json.dumps({"value": val}))
# response = requests.get(url+key, headers=header)
# expected = json.dumps({"doesExist":True,"message":"Retrieved successfully","value":val})

# for k,v in response.json().items():
# 	if v:
# 		testStatus.append("passed")
# 		break
# 	else:
# 		testStatus.append("failed")
# 		print(f'Test failed......\nExpected response from server: \n{expected}\n')
# 		print(f'Actual response from server: \n{response.json()}\n')
# 		break

# #get existing key/value pair
# print("--------Test8---------- \nTesting grabbing a existing key/value pair in the store...\n\n")
# val = 'manbrainslice'
# requests.put(url+key, headers=header, data=json.dumps({"value": val}))
# response = requests.get(url+key, headers=header)
# expected = json.dumps({"doesExist":True,"message":"Retrieved successfully","value":val})
# response_data = response.json()
# for k,v in response.json().items():
# 	if v:
# 		testStatus.append("passed")
# 		break
# 	else:
# 		testStatus.append("failed")
# 		print(f'Test failed......\nExpected response from server: \n{expected}\n')
# 		print(f'Actual response from server: \n{response.json()}\n')
# 		break

#count how many tests were passed
num = 0
for passed in testStatus:
	if passed == "passed":
		num += 1

print('-----------------------')
print(f'\n\nTESTS PASSED {num}/{len(testStatus)}')


