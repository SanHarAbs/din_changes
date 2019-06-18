
from web3 import Web3, HTTPProvider, IPCProvider


w3 = Web3(HTTPProvider('http://219.91.253.103:8003'))

w3.eth.defaultAccount = w3.toChecksumAddress('0x9a5c064a5b519e2b116e51ad6b4629ccc35f4f22')
#w3.eth.defaultAccount = w3.eth.accounts[0]

contractAddress = w3.toChecksumAddress("0x3305d46ab20556d045819e93c2b64a6bf182935d")
#contractAddress = w3.toChecksumAddress("0xeabebcc1245a6a091f37144de4083fd0c2cf2e6e")


contractAbi = """[
	{
		"constant": false,
		"inputs": [
			{
				"name": "recid",
				"type": "uint256"
			},
			{
				"name": "pfNo",
				"type": "bytes32"
			},
			{
				"name": "ptName",
				"type": "bytes32"
			},
			{
				"name": "dob",
				"type": "uint256"
			},
			{
				"name": "dod",
				"type": "uint256"
			},
			{
				"name": "duplicateno",
				"type": "int256"
			},
			{
				"name": "Isdead",
				"type": "bool"
			},
			{
				"name": "contact",
				"type": "uint256"
			},
			{
				"name": "HashID",
				"type": "bytes32"
			},
			{
				"name": "deathreason",
				"type": "bytes32"
			}
		],
		"name": "addPatient",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "recid",
				"type": "uint256"
			}
		],
		"name": "getPatientbyrecordid",
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
				"type": "uint256"
			},
			{
				"name": "",
				"type": "int256"
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
		"constant": true,
		"inputs": [
			{
				"name": "recid",
				"type": "uint256"
			}
		],
		"name": "getPatientdetails",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "bool"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "bytes32"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
]
"""

patientinterface = w3.eth.contract(
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

def addpatientrecord(ID,pfNo,ptName,contactnumber,ptDOB,HashID,duplicateno,Isdead,DOD,deadreason):
    responsecode =400
    tx_hash=''
    print(ID)

    try:
        w3.personal.unlockAccount(w3.eth.accounts[0], 'This_Is_Strong_Password')
        hexpfno=Web3.toHex(text=pfNo)
        hexName=Web3.toHex(text=ptName)
        hexhashid=Web3.toHex(text=HashID)
        dreason=Web3.toHex(text=deadreason)
        # print('aaaaaa')
        tx_hash = patientinterface.functions.addPatient(ID,hexpfno,
                                                            hexName,
                                                            ptDOB,DOD,duplicateno,Isdead,contactnumber,
                                                            hexhashid,dreason).transact()
        # print(tx_hash)
        # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        responsecode =200
        # print(tx_receipt)
    except e:
        tx_hash = 'Error'
        responsecode =400
    return tx_hash,responsecode


def getPatientbyrecordid(id):
    try:

        w3.personal.unlockAccount(w3.eth.accounts[0], 'This_Is_Strong_Password')
        result = patientinterface.functions.getPatientbyrecordid(int(id)).call()
        # print(result)
        return result,200
    except Error as e:
        print(e)
        return [],400



def isdeadpatient(id):
    try:
        # print(id)
        w3.personal.unlockAccount(w3.eth.accounts[0], 'This_Is_Strong_Password')
        result = patientinterface.functions.getPatientdetails(int(id)).call()
        # print('done')
        return result,200
    except Error as e:
        print(e)
        return [],400

#getPatientbyrecordid("ea07b075-5d84-4d30-9d28-db3e41bef559")
