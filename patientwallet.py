
from conection import connect
import hashlib  # for hash key
import datetime
import uuid # for UniqueID
from mysql.connector import Error
from flask import jsonify,request

def GetallTransactions():
    conx =connect()
    responsemessage = "";
    responsecode = 200;
    cursor = conx.cursor()
    try:        
        if(responsecode==200):
            selectquery = """WITH hospital as (select ROW_NUMBER() OVER (
						PARTITION BY RegistrationNo
                        ORDER BY duplicateno desc    ) rowno,
                        ID, HospitalName , RegistrationNo,
                        Address,   Bedcount,  Hospitaltype,	HashID, duplicateno 
                        from Hospitaldetails  ) 
                        select    ID,   HospitalName , RegistrationNo,
                        Address,   Bedcount,
                        Hospitaltype,	HashID,     duplicateno 
                        from hospital  where rowno = 1"""
            cursor.execute(selectquery)
            myresult = cursor.fetchall() 
            if(myresult[0][0] != None):        
                responsemessage=myresult
            else:
                responsemessage="No record"
                responsecode = 400

    except Error as e:
        responsemessage =e.msg
        responsecode = e.errno
 
    finally:
        cursor.close()
        conx.close()

    return responsemessage, responsecode

def getrecordbypfno(pfno):
    return ""
    
def getrecordsByTransactionId(registrationno):
    conx =connect()
    responsemessage = "";
    responsecode = 200;
    cursor = conx.cursor()
    try:        
        if(responsecode==200):
            selectquery = "select ID,  HospitalName , RegistrationNo,  Address,   Bedcount,  Hospitaltype,	HashID, duplicateno  from Hospitaldetails where RegistrationNo = '"+ str(registrationno)+"'  order by duplicateNo desc limit 1"""
            cursor.execute(selectquery)
            myresult = cursor.fetchall() 
            print(myresult)
            if(myresult[0][0] != None):        
                responsemessage=myresult
            else:
                responsemessage="No record"
                responsecode = 400

    except Error as e:
        responsemessage =e.msg
        responsecode = e.errno
 
    finally:
        cursor.close()
        conx.close()

    return responsemessage, responsecode

def addtransaction():
    conx =connect()
    responsemessage = "";
    responsecode = 200;
    cursor = conx.cursor()
    try:
      
        if not request.json:
           return make_response(jsonify({'message':'Please send a valid Json object'}), 400)

        uniqueid =  uuid.uuid4()

        if 'hospitalname' not in request.json:
           responsemessage= "Provide Hospital name"
           responsecode =400
        else:
            hospitalname = request.json["hospitalname"]

        if 'registrationNo' not in request.json:
           responsemessage= "Provide Registration No"
           responsecode =400
        else:
            regisstrationno = request.json["registrationNo"]     
        
        if 'address' not in request.json:
            responsemessage= "Provide Address"
            responsecode =400
        else:
            address = request.json["address"]

        if 'bedcount' not in request.json:
            responsemessage= "Provide bed count"
            responsecode =400
        else:
            bedcount = request.json["bedcount"]

        if 'hospitaltype' not in request.json:
            responsemessage= "Provide hospital type"
            responsecode =400
        else:
            hospitaltype = request.json["hospitaltype"]
        
        if(responsecode==200):
            addadate = datetime.datetime.now()   
            
            hash_key = hashlib.md5((str(bedcount)+str(hospitaltype)+str(uniqueid)+str(hospitalname)+str(regisstrationno)+str(address)+str(addadate)).encode('utf-8')).hexdigest()
            selectquery = "select max(duplicateno) as did from Hospitaldetails where registrationNo = '"+ str(regisstrationno)+"'"
            cursor.execute(selectquery)
            myresult = cursor.fetchone()      
            maxcounter =0
            if(myresult[0] == None):
                maxcounter= 1
            else:
                maxcounter = (int(myresult[0])+1)
            print(maxcounter)
            if(maxcounter<=1):
                insertSql = "INSERT INTO Hospitaldetails (ID,HospitalName,RegistrationNo,Address,Add_Date,HashID,duplicateno,bedcount,hospitaltype) VALUES (%s, %s,%s, %s,%s, %s,%s,%s,%s)"
                val = (str(uniqueid),str(hospitalname), str(regisstrationno),str(address), addadate,str(hash_key),maxcounter,bedcount,hospitaltype)
                cursor.execute(insertSql, val)
                conx.commit()
                responsemessage="Hospital registered"
                responsecode =200
            else:
                responsemessage="Registration No. already exists"
                responsecode =400

    except Error as e:
        responsemessage =e.msg
 
    finally:
        cursor.close()
        conx.close()
        return responsemessage, responsecode