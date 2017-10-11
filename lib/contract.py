import urllib
import json
import time

url = "https://api.hyperchain.cn/v1/"
path = {
	"get_token": "token/gtoken",
	"payload": "dev/payload",
	"invoke":"dev/contract/invoke",
	"invokesync":"dev/contract/invokesync"
	}
auth_data = {
	'phone': '13056961943',
	'password': '123456',
	'client_id': '4909d978-fb21-45e2-974d-c7b6a9c17067',
	'client_secret': '868v4oq14w1DvGt6Bft19rQ3091t2589'
	}

FROM = '738fdc2553b5cdcae43952539dcb04b3ae621ee1'
CONTRACT_ADDRESS = '0x52735ea369e07185bf852c4f9758a79bd63a9d8f'

ABI = '[{"constant":false,"inputs":[],"name":"getUsers","outputs":[{"name":"users","type":"address[]"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"fileHash","type":"bytes"}],"name":"getEvidence","outputs":[{"name":"code","type":"uint256"},{"name":"fHash","type":"bytes"},{"name":"fUpLoadTime","type":"uint256"},{"name":"saverAddress","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"fileHash","type":"bytes"},{"name":"fileUploadTime","type":"uint256"}],"name":"saveEvidence","outputs":[{"name":"code","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'

AUTH_TOKEN = ''

IS_AUTH_REQUEST = True
NOT_AUTH_REQUEST = True

def post(is_auth_request, url, data, headers={}):
	global AUTH_TOKEN
	if AUTH_TOKEN != '':
		headers['Authorization'] = AUTH_TOKEN
	if is_auth_request:
		req = urllib.request.Request(method = "POST",url = url, headers = headers, data = data)
	else:
		req = urllib.request.Request(method = "POST",url = url, headers = headers, json = data)
	response = urllib.request.urlopen(req).read()
	return response


def get_token():
	global AUTH_TOKEN
	requrl = url + path["get_token"]
	data = urllib.parse.urlencode(auth_data).encode('utf-8')
	res = post(IS_AUTH_REQUEST, requrl, data,{'Content-Type': r'application/x-www-form-urlencoded'})
	result = eval(res)
	print(result['access_token'])
	AUTH_TOKEN = result['access_token']
	return result['access_token']

def get_payload(func, args=[]):
	global AUTH_TOKEN
	if AUTH_TOKEN == '':
		raise Exception("token is " , AUTH_TOKEN)
	requrl = url + path['payload']
	data = {
		"abi": ABI,
		"func": func,
		"args": args
	}
	response = post(NOT_AUTH_REQUEST,requrl, bytes(json.dumps(data), 'utf-8'),{'Content-Type':r'application/json'})
	res = response.decode('ascii')
	print ("payload", res)
	return res[1:-1]

def save_evidence(hash):
	global AUTH_TOKEN
	if AUTH_TOKEN == '':
		raise Exception("token is " , AUTH_TOKEN)
	requrl = url + path['invokesync']
	timestamp = str(time.time())
	payload = get_payload('saveEvidence', [hash, '2'])
	data = {
		"Const":False,
		"From": FROM,
		"To": CONTRACT_ADDRESS,
		"Payload": payload
	}
	response = post(NOT_AUTH_REQUEST,requrl, bytes(json.dumps(data), 'utf-8'),{'Content-Type':r'application/json'})
	res = response.decode('ascii')
	print ("get_evidence", res)
	return res

def get_evidence(hash):
	global AUTH_TOKEN
	if AUTH_TOKEN == '':
		raise Exception("token is " , AUTH_TOKEN)
	requrl = url + path['invokesync']
	timestamp = str(time.time())
	payload = get_payload('getEvidence', [hash])
	data = {
		"Const":False,
		"From": FROM,
		"To": CONTRACT_ADDRESS,
		"Payload": payload
	}
	response = post(NOT_AUTH_REQUEST,requrl, bytes(json.dumps(data), 'utf-8'),{'Content-Type':r'application/json'})
	res = response.decode('ascii')
	print ("save_evidence", res)
	return res

def get_users():
	global AUTH_TOKEN
	if AUTH_TOKEN == '':
		raise Exception("token is " , AUTH_TOKEN)
	requrl = url + path['invokesync']
	timestamp = str(time.time())
	payload = get_payload('getUsers')
	data = {
		"Const":False,
		"From": FROM,
		"To": CONTRACT_ADDRESS,
		"Payload": payload
	}
	response = post(NOT_AUTH_REQUEST,requrl, bytes(json.dumps(data), 'utf-8'),{'Content-Type':r'application/json'})
	res = response.decode('utf-8')
	json_result = json.loads(res)
	print ("getusers", unpack_ret(json_result["Ret"], 'getUsers'))

def unpack_ret(ret,method):
	url = "http://127.0.0.1:8080/unpack"
	data = {
	"AbiString":ABI,
	"Ret":ret,
	"Method":method
	}
	data_dumped = bytes(json.dumps(data), 'ascii')
	print(data_dumped)
	req = urllib.request.Request(method = "POST",url = url, headers = {'Content-Type':r'application/json'}, data = data_dumped)
	response = urllib.request.urlopen(req).read()
	res = response.decode('utf-8')
	json_result = json.loads(res)
	return json_result


