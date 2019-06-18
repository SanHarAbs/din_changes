
from web3 import Web3, HTTPProvider, IPCProvider


w3 = Web3(HTTPProvider('http://219.91.253.103:8003'))

w3.eth.defaultAccount = w3.toChecksumAddress('0x9a5c064a5b519e2b116e51ad6b4629ccc35f4f22')
#w3.eth.defaultAccount = w3.eth.accounts[0]

#contractAddress = w3.toChecksumAddress("0x5100f89ef8246175cd0c8b5dda40fe51ae3d202d")
contractAddress = w3.toChecksumAddress("0xba086ff9c542e484fae7aad3a63f4be0eca9bbf6")


contractAbi = """
[
	{
		"constant": false,
		"inputs": [
			{
				"name": "recordId",
				"type": "uint256"
			},
			{
				"name": "treatmentId",
				"type": "bytes32"
			},
			{
				"name": "hashId",
				"type": "bytes32"
			}
		],
		"name": "addTreatment",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "recordId",
				"type": "uint256"
			}
		],
		"name": "getPatientTreatment",
		"outputs": [
			{
				"name": "",
				"type": "bytes32"
			},
			{
				"name": "",
				"type": "bytes32"
			},
			{
				"name": "",
				"type": "bytes32"
			},
			{
				"name": "",
				"type": "bytes32"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "recordId",
				"type": "uint256"
			},
			{
				"name": "patientTreatmentId",
				"type": "bytes32"
			},
			{
				"name": "ptPfNo",
				"type": "bytes32"
			},
			{
				"name": "treatmentId",
				"type": "bytes32"
			},
			{
				"name": "hashId",
				"type": "bytes32"
			}
		],
		"name": "addPatientTreatment",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "recordId",
				"type": "uint256"
			}
		],
		"name": "getTreatmentByRecordId",
		"outputs": [
			{
				"name": "treatmentId",
				"type": "bytes32"
			},
			{
				"name": "hashId",
				"type": "bytes32"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
]
"""

interface = w3.eth.contract(
					address=contractAddress,
					abi=contractAbi
					)

# import re
# myString = re.sub(r"[\n\t\s]*", "", contractAbi)
# print(myString)


# Display the default greeting from the contract

# w3.personal.unlockAccount(w3.eth.accounts[0], 'seed')
# tx_hash = patientinterface.functions.addPatient(12345,'0x68656c6c6f0000000000000000000000',

#                                                     '0x68656c6c6f0000000000000000000000',
#                                                     123,123,1,False,123456,
#                                                     '0x68656c6c6f0000000000000000000000',
#                                                     '0x68656c6c6f0000000000000000000000'
#                                                     ).transact()
# print(tx_hash)
# tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# print(tx_receipt)

# print("Reteriving data")
# print(patientinterface.functions.getPatientbyrecordid(12345).call())

# number = Web3.toHex(text='mohit')
# print(number)
# print(len(number))

# xxxxxxx= "0x68656c6c6f20486f772041726520797075"
# print(len(xxxxxxx))

def addTreatment(recordId, treatmentId, hashId):
	responsecode =400
	tx_hash=''
	

	try:
		#print(treatmentId)
		w3.personal.unlockAccount(w3.eth.accounts[0], 'This_Is_Strong_Password')
		hextreatmentid=Web3.toHex(text=treatmentId)
		hexhashid=Web3.toHex(text=hashId)
		# print(recordId)
		# print(hextreatmentid)
		# print(hexhashid)
		tx_hash = interface.functions.addTreatment(int(recordId),hextreatmentid,hexhashid).transact()
		#print(tx_hash)
		# tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
		responsecode =200
		#print(tx_receipt)
	except e:
		tx_hash = 'Error'
		responsecode =400
	return tx_hash, responsecode


def getTreatmentByRecordId(id):
	try:

		w3.personal.unlockAccount(w3.eth.accounts[0], 'This_Is_Strong_Password')
		result = interface.functions.getTreatmentByRecordId(int(id)).call()
		print(result)
		return result, 200
	except Error as e:
		print(e)
		return [], 400



def addPatientTreatment(recordId, patientTreatmentId,  ptPfNo,  treatmentId,  hashId):
	responsecode =400
	tx_hash=''
	# print(recordId)
	# print('Inside')
	try:
		w3.personal.unlockAccount(w3.eth.accounts[0], 'This_Is_Strong_Password')
		hexpfno=Web3.toHex(text=ptPfNo)
		hexhashid=Web3.toHex(text=hashId)
		hexpatientTreatmentId=Web3.toHex(text=patientTreatmentId)
		hexhashid=Web3.toHex(text=hashId)
		
		tx_hash = interface.functions.addPatientTreatment(int(recordId), hexpatientTreatmentId, hexpfno, hexpatientTreatmentId, hexhashid).transact()
		
		#tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
		responsecode =200
		#print(tx_receipt)
	except e:
		print(e)
		tx_hash = 'Error'
		responsecode =400
	return tx_hash, responsecode


def getPatientTreatment(id):
	try:

		w3.personal.unlockAccount(w3.eth.accounts[0], 'This_Is_Strong_Password')
		result = interface.functions.getPatientTreatment(int(id)).call()
		#print(result)
		return result, 200
	except Error as e:
		print(e)
		return [], 400
