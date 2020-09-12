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

#count how many tests were passed
num = 0
for passed in testStatus:
	if passed == "passed":
		num += 1

print('-----------------------')
print(f'\n\nTESTS PASSED {num}/{len(testStatus)}')


