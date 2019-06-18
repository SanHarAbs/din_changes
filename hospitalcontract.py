
from web3 import Web3, HTTPProvider, IPCProvider


w3 = Web3(HTTPProvider('http://219.91.253.103:8003'))

w3.eth.defaultAccount = w3.toChecksumAddress('0x9a5c064a5b519e2b116e51ad6b4629ccc35f4f22')
#w3.eth.defaultAccount = w3.eth.accounts[0]

contractAddress = w3.toChecksumAddress("0x342de7fce990c6861115e5323ec4350f784eea7e")
#contractAddress = w3.toChecksumAddress("0xeabebcc1245a6a091f37144de4083fd0c2cf2e6e")

contractAbi = """[
	{
		"constant": false,
		"inputs": [
			{
				"name": "id",
				"type": "uint256"
			},
			{
				"name": "name",
				"type": "bytes32"
			},
			{
				"name": "regNo",
				"type": "bytes32"
			},
			{
				"name": "hospitalAddress",
				"type": "bytes32"
			},
			{
				"name": "hashid",
				"type": "bytes32"
			},
			{
				"name": "duplicateno",
				"type": "int256"
			},
			{
				"name": "noOfBeds",
				"type": "int256"
			},
			{
				"name": "hospitalType",
				"type": "int256"
			}
		],
		"name": "addHospital",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "id",
				"type": "uint256"
			}
		],
		"name": "getHospitalbyrecordid",
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
			},
			{
				"name": "",
				"type": "int256"
			},
			{
				"name": "",
				"type": "int256"
			},
			{
				"name": "",
				"type": "int256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
]
"""


hospitalinterface = w3.eth.contract(
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
#val = (str(uniqueid),str(hospitalname), str(regisstrationno),str(address), addadate,str(hash_key),maxcounter,bedcount,hospitaltype)
        #
        # ID,HospitalName,RegistrationNo,Address,HashID,  duplicateno,bedcount,hospitaltype



def addhospital(ID,hospitalname,regisstrationno,hospitaladdress,HashID,duplicateno,bedcount,hospitaltype):
    responsecode =400
    tx_hash=''
    # print('aa')
    # print(ID)
    try:
        #print('Block')
        w3.personal.unlockAccount(w3.eth.accounts[0], 'This_Is_Strong_Password')

        hexregisstrationno = Web3.toHex(text=regisstrationno)
        hexaddress = Web3.toHex(text=hospitaladdress)
        hexhashid = Web3.toHex(text=HashID)
        hexhospitalName = Web3.toHex(text=hospitalname)

        tx_hash = hospitalinterface.functions.addHospital(int(ID),hexhospitalName,
                                                            hexregisstrationno,
                                                            hexaddress,   hexhashid,
                                                            int(duplicateno),int(bedcount),
                                                            int(hospitaltype)
                                                            ).transact()
        # print(tx_hash)
        # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        responsecode =200
        #print(tx_receipt)
    except e:
        tx_hash = 'Error'
        responsecode =400
    return tx_hash,responsecode


def getHospitalbyrecordid(id):
    try:
        w3.personal.unlockAccount(w3.eth.accounts[0], 'This_Is_Strong_Password')
        result = hospitalinterface.functions.getHospitalbyrecordid(int(id)).call()
        # print('Here')
        # print(result)
        return result,200
    except Error as e:
        print(e)
        return [],400

#getPatientbyrecordid("ea07b075-5d84-4d30-9d28-db3e41bef559")
