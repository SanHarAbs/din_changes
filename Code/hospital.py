
from conection import connect
import hashlib  # for hash key
import datetime
import uuid # for UniqueID
from mysql.connector import Error
from flask import jsonify,request



#import hospitalcontract
from datetime import datetime as dt
import datetime
import calendar
import utility

def getallhospitals():
    conx =connect()
    responsemessage = ""
    responsecode = 200
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

def gethospitalbyregistrationno(registrationno):
    conx =connect()
    responsemessage = "";
    responsecode = 200;
    cursor = conx.cursor()
    try:        
        if(responsecode==200):
            selectquery = "select ID,  HospitalName , RegistrationNo,  Address,   Bedcount,  Hospitaltype,	HashID, duplicateno  from Hospitaldetails where RegistrationNo = '"+ str(registrationno)+"'  order by duplicateNo desc limit 1"""
            cursor.execute(selectquery)
            myresult = cursor.fetchall() 
            #print(myresult)
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

def addhospital():
    conx =connect()
    responsemessage = "";
    responsecode = 200;
    cursor = conx.cursor()
    print('Here')
    
    try:
      
        if not request.json:
           return 'Please send a valid Json object', 400

        uniqueid= int(str(datetime.datetime.utcnow()).replace("-", "").replace(":", "").replace(".", "").replace(" ", ""))

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
            try:
                bedcount = int(bedcount)
            except ValueError:
                responsemessage= "Provide bed count"
                responsecode =400

        if 'hospitaltype' not in request.json:
            responsemessage= "Provide hospital type"
            responsecode =400
        else:
            hospitaltype = request.json["hospitaltype"]
            try:
                hospitaltype = int(hospitaltype)
            except ValueError:
                responsemessage= "Provide hospital type"
                responsecode =400
        
        
        res,hospitalname= utility.validatestringlength(hospitalname)
       
        if(res==False):
            responsemessage=hospitalname
            responsecode =400
        

        if(res==True):
            res,address= utility.validatestringlength(address)
            if(res==False):
                responsemessage=address
                responsecode =400
        

        if(responsecode==200):
            addadate = datetime.datetime.now()            
            
            selectquery = "select max(duplicateno) as did from Hospitaldetails where registrationNo = '"+ str(regisstrationno)+"'"
            cursor.execute(selectquery)
            myresult = cursor.fetchone()      
            maxcounter =0
            if(myresult[0] == None):
                maxcounter= 1
            else:
                maxcounter = (int(myresult[0])+1)
          
            if(maxcounter<=1):
                
                hash_key = hashlib.md5((str(uniqueid)+str(hospitalname)
                                        +str(regisstrationno)
                                        +str(address)+ str(maxcounter)
                                        +str(bedcount)
                                        +str(hospitaltype)).encode('utf-8')).hexdigest()
             
                #ID,hospitalname,regisstrationno,address,HashID,duplicateno,bedcount,hospitaltype
                # transhash,response = hospitalcontract.addhospital(uniqueid,hospitalname,regisstrationno,address,
                #                                                         hash_key,maxcounter,
                #                                                       bedcount,hospitaltype)
                
                transhash = "xyz"
                response = 200

                ##### Transaction type 1 for patient 2 for hospital
                if(response == 200):

                    insertSql = """INSERT INTO Hospitaldetails (ID,HospitalName,RegistrationNo,Address,Add_Date,HashID,
                                        duplicateno,bedcount,hospitaltype) VALUES (%s, %s,%s, %s,%s, %s,%s,%s,%s)"""
                    
                    val = (str(uniqueid),str(hospitalname), str(regisstrationno),str(address), addadate,str(hash_key),maxcounter,bedcount,hospitaltype)
                    cursor.execute(insertSql, val)
                    conx.commit()
                   
                    #### Transaction type 1 for patient 2 for hospital
                    
                    utility.savetransactionrecord(str(uniqueid),str(transhash),2,addadate)


                    responsemessage="Hospital registered"
                    responsecode =200

                else:
                    responsecode = 400
                    responsemessage = 'Error'
               
                
            else:
                responsemessage="Registration No. already exists"
                responsecode =400

    except Error as e:
        responsemessage =e.msg
 
    finally:
        cursor.close()
        conx.close()

        return responsemessage, responsecode

def modifyhospital():
    conx =connect()
    responsemessage = "";
    responsecode = 200;
    cursor = conx.cursor()
    try:
      
        if not request.json:
           return 'Please send a valid Json object', 400

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
            try:
                bedcount = int(bedcount)
            except ValueError:
                responsemessage= "Provide bed count"
                responsecode =400

        if 'hospitaltype' not in request.json:
            responsemessage= "Provide hospital type"
            responsecode =400
        else:
            hospitaltype = request.json["hospitaltype"]
            try:
                hospitaltype = int(hospitaltype)
            except ValueError:
                responsemessage= "Provide hospital type"
                responsecode =400

        
        res,hospitalname= utility.validatestringlength(hospitalname)
        print(res)
        if(res==False):
            responsemessage=hospitalname
            responsecode =400
        

        if(res==True):
            res,address= utility.validatestringlength(address)
            if(res==False):
                responsemessage=address
                responsecode =400

        
        if(responsecode==200):
            uniqueid= int(str(datetime.datetime.utcnow()).replace("-", "").replace(":", "").replace(".", "").replace(" ", ""))

            addadate = datetime.datetime.now()   
            selectquery = "select max(duplicateno) as did from Hospitaldetails where registrationNo = '"+ str(regisstrationno)+"'"
            
            cursor.execute(selectquery)
            myresult = cursor.fetchone()          

            if(myresult[0] == None):
                responsemessage="Registration no. not exists"
                responsecode =400
            else:
                maxcounter = (int(myresult[0])+1)
                
                hash_key = hashlib.md5((str(uniqueid)+str(hospitalname)+str(regisstrationno)
                                    +str(address)+ str(maxcounter)
                                    + str(bedcount)+ str(hospitaltype)).encode('utf-8')).hexdigest()
                
                
                 
                #ID,hospitalname,regisstrationno,address,HashID,duplicateno,bedcount,hospitaltype
                # transhash,response = hospitalcontract.addhospital(uniqueid,hospitalname,regisstrationno,address,
                #                                                         hash_key,maxcounter,
                #                                                       bedcount,hospitaltype)
                
                transhash = "xyz"
                response = 200

                ##### Transaction type 1 for patient 2 for hospital
                if(response == 200):
                
                    insertSql = "INSERT INTO Hospitaldetails (ID,HospitalName,RegistrationNo,Address,Add_Date,HashID,duplicateno,bedcount,hospitaltype) VALUES (%s, %s,%s, %s,%s, %s,%s,%s,%s)"
                    val = (str(uniqueid),str(hospitalname), str(regisstrationno),str(address), addadate,str(hash_key),maxcounter,bedcount,hospitaltype)
                    cursor.execute(insertSql, val)
                    
                    conx.commit()

                    #### Transaction type 1 for patient 2 for hospital

                    utility.savetransactionrecord(str(uniqueid),str(transhash),2,addadate)

                    responsemessage="Record Modified."
                    responsecode =200
                else:
                    responsemessage="Error"
                    responsecode =400


    except Error as e:
        responsemessage =e.msg
 
    finally:
        cursor.close()
        conx.close()

        return responsemessage, responsecode

def gethospitalfromblockchain(recordid):
    if((utility.IsValidUniqueNumber(recordid,2)) == True):
        data,respose=  hospitalcontract.getHospitalbyrecordid(recordid)
        return data,respose
    else:
        print('else')
        return [],400
