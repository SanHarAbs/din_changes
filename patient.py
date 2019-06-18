from conection import connect
import hashlib  # for hash key
import datetime
import uuid # for UniqueID
from mysql.connector import Error
from flask import jsonify,request


# Importing Blockchain code
import patientcontract
from datetime import datetime as dt
import datetime
import calendar

import utility


def getallpatients():
    conx =connect()
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:        
        if(responsecode==200):
            selectquery = """WITH patient as (select ROW_NUMBER() OVER (
                                                        PARTITION BY pfno
                                                        ORDER BY duplicateno desc     ) rowno,
                                                        ID,pfno,patientName,contact,DOB,HashID, duplicateno,
                                                        Isdead,DOD, ReasonOfDeath 
                                                        from Patientdetails  )
                                                        select ID,
                                                        pfno,patientName,contact,DOB,HashID, duplicateno,
                                                        Isdead,DOD, ReasonOfDeath 
                                                        from patient  where rowno = 1"""
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

def getpatientbypfno(pfno):
    conx =connect()
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:        
        if(responsecode==200):
            selectquery = "select ID, pfno,patientName,contact,DOB,HashID, duplicateno, Isdead,DOD, ReasonOfDeath from Patientdetails where pfno = '"+ str(pfno)+"' order by duplicateNo desc limit 1"
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

def AddPatient():
    conx =connect()
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:
        
        if not request.json:
           return 'Please send a valid Json object', 400
       

        uniqueid= int(str(datetime.datetime.utcnow()).replace("-", "").replace(":", "").replace(".", "").replace(" ", ""))

        if 'patientname' not in request.json:
           responsemessage= "Provide patient name"
           responsecode =400
        else:
            patientname = request.json["patientname"]

        if 'pfno' not in request.json:
           responsemessage= "Provide pfno"
           responsecode =400
        else:
            pfno = request.json["pfno"]
      
        if 'dob' not in request.json:
           responsemessage= "Provide DOB"
           responsecode =400
        else:
            try:
                dob = datetime.datetime.strptime(request.json["dob"], '%Y-%m-%d')
            except Exception as e:
                responsemessage= "Please provide a valid date"
                responsecode =400
     
        if 'contact' not in request.json:
            responsemessage= "Provide contact"
            responsecode =400
        else:
            contact = request.json["contact"]
            try:
                contact = int(contact)
            except ValueError:
                responsemessage= "Provide contact"
                responsecode =400
        
        res,patientname= utility.validatestringlength(patientname)
      
        if(res==False):
            responsemessage=patientname
            responsecode =400

        if(responsecode==200):
            isdead = False
            dod =None
            reasonOfdeath =''
            dodtimestamp =0
           
            addadate =datetime.datetime.now()

            dobtimestamp = calendar.timegm(dob.utctimetuple())
            
            selectquery = "select max(duplicateno) as did from Patientdetails where pfno = '"+ str(pfno)+"'"
            cursor.execute(selectquery)
            myresult = cursor.fetchone()          
            maxcounter =0
            if(myresult[0] == None):
                maxcounter= 1
            else:
                maxcounter = (int(myresult[0])+1)
            if(maxcounter<=1):
                print('Here')
                print(pfno)
                hash_key = hashlib.md5((str(uniqueid)+str(pfno) +
                                        str(patientname)+str(contact)
                                        +str(dobtimestamp)
                                        +str(maxcounter)
                                        +str(isdead) +str(dodtimestamp)+str(reasonOfdeath)
                                       ).encode('utf-8')).hexdigest()
                print(patientname)
                print(contact)
                print(dobtimestamp)
                print(dodtimestamp)

                #(ID,pfNo,ptName,contactnumber,ptDOB,HashID,duplicateno,Isdead,DOD,ReasonOfDeath
                #ID,pfNo,ptName,contactnumber,ptDOB,HashID,duplicateno,Isdead,DOD,ReasonOfDeath
                transhash,response = patientcontract.addpatientrecord(uniqueid,str(pfno),str(patientname),
                                                                        int(contact),dobtimestamp,
                                                                        str(hash_key),maxcounter,isdead,dodtimestamp,reasonOfdeath)

                ##### Transaction type 1 for patient 2 for hospital

                if(response == 200):
                    insertSql = """INSERT INTO Patientdetails (ID,pfno,Patientname,
                                contact,dob,Add_Date,HashID,duplicateno,Isdead,DOD,ReasonOfDeath) 
                                VALUES (%s, %s,%s, %s,%s, %s,%s,%s,%s,%s,%s)"""

                    val = (str(uniqueid), str(pfno),str(patientname),str(contact), dobtimestamp, addadate,str(hash_key),maxcounter,isdead,dodtimestamp,reasonOfdeath)
               
                    cursor.execute(insertSql, val)
                    conx.commit()
                    print('Database')

                    utility.savetransactionrecord(str(uniqueid),str(transhash),1,addadate)

                    responsemessage="Patient registered"
                    responsecode =200
                else:
                    responsecode = 400
                    responsemessage = 'Error'
            else:
                responsemessage="PfId already exists"
                responsecode =400

    except Error as e:
        print(e)
        responsemessage =e.msg
        responsecode =e.errno
 
    finally:
        cursor.close()
        conx.close()
        print(responsecode)
        return responsemessage, responsecode

def modifypatient():
    conx =connect()
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:

        
        responsemessage = ""
        responsecode = 200
        if not request.json:
           return 'Please send a valid Json object', 400

        if 'patientname' not in request.json:
           responsemessage= "Provide patient name"
           responsecode =400
        else:
            patientname = request.json["patientname"]

        if 'pfno' not in request.json:
           responsemessage= "Provide pfno"
           responsecode =400
        else:
            pfno = request.json["pfno"]

        if 'dob' not in request.json:
           responsemessage= "Provide DOB"
           responsecode =400
        else:
            try:
                dob = datetime.datetime.strptime(request.json["dob"], '%Y-%m-%d')
                dobtimestamp = calendar.timegm(dob.utctimetuple())
            except Exception as e:
                responsemessage= "Please provide a valid date"
                responsecode =400
            

        if 'contact' not in request.json:
            responsemessage= "Provide contact number"
            responsecode =400
        else:
            contact = request.json["contact"]
            try:
                contact = int(contact)
            except ValueError:
                responsemessage= "Provide contact"
                responsecode =400

        if 'isdead' not in request.json:
            responsemessage= "Provide isdead or not"
            responsecode =400
        else:
            isdead = request.json["isdead"]
        
          ######### Check basic validatiom ##########
        if(bool(isdead)== True):
            
            if 'dod' not in request.json:
                responsemessage= "Provide dod"
                responsecode =400
            else:
                try:
                    dod = datetime.datetime.strptime(request.json["dod"], '%Y-%m-%d')
                    dodtimestamp = calendar.timegm(dod.utctimetuple())
                except Exception as e:
                    responsemessage= "Please provide a valid date."
                    responsecode =400
            
            if 'reasonOfdeath' not in request.json:
                responsemessage= "Provide reason of death"
                responsecode =400
            else:
                reasonOfdeath = request.json["reasonOfdeath"]
            if(dob> dod):
                responsemessage= "Date of birth can not be greater than Date of death."
                responsecode =400

        else:
            dod = 0
            dodtimestamp = 0
            isdead =False
            reasonOfdeath =''
        
        res,patientname= utility.validatestringlength(patientname)
   
        if(res==False):
            responsemessage=patientname
            responsecode =400

        if(res==True):
            res,reasonOfdeath= utility.validatestringlength(reasonOfdeath)
            if(res==False):
                responsemessage=reasonOfdeath
                responsecode =400
       
        if(responsecode==200):
            uniqueid= int(str(datetime.datetime.utcnow()).replace("-", "").replace(":", "").replace(".", "").replace(" ", ""))
            addadate = datetime.datetime.now()   
           
            selectquery = "select max(duplicateno) from Patientdetails where pfno = '"+ str(pfno)+"'"
            cursor.execute(selectquery)
            myresult = cursor.fetchone()          
            
            if(myresult[0] == None):
                responsemessage="PfId not exists"
                responsecode =400
            else:
                
                maxcounter = (int(myresult[0])+1)
                
                hash_key = hashlib.md5((str(uniqueid)+str(pfno) +
                                        str(patientname)+str(contact)
                                        +str(dobtimestamp)
                                        +str(maxcounter)
                                        +str(isdead) +str(dodtimestamp)+str(reasonOfdeath)
                                       ).encode('utf-8')).hexdigest()

                
                transhash,response = patientcontract.addpatientrecord(uniqueid,str(pfno),str(patientname),
                                                                        int(contact),dobtimestamp,
                                                                        str(hash_key),maxcounter,bool(isdead),dodtimestamp,reasonOfdeath)
                
                if(response==200):
                  
                    insertSql = """INSERT INTO Patientdetails (ID,pfno,Patientname,
                                    contact,dob,Add_Date,HashID,duplicateno,Isdead,DOD,ReasonOfDeath) 
                                    VALUES (%s, %s,%s, %s,%s, %s,%s,%s,%s,%s,%s)"""
                
                    val = (str(uniqueid), str(pfno),str(patientname),str(contact), 
                                    dobtimestamp, addadate,str(hash_key)
                                    ,maxcounter,isdead,dodtimestamp,reasonOfdeath)
                    cursor.execute(insertSql, val)
                    conx.commit()

                
                     #### Transaction type 1 for patient 2 for hospital

                    utility.savetransactionrecord(str(uniqueid),str(transhash),1,addadate)
                    

                    responsemessage="Patient modified"
                    responsecode =200
                else:
                    responsecode =400
                    responsemessage = 'Error'

    except Error as e:  
        responsemessage =e.msg
        responsecode =e.errno
        raise Exception(e.msg,Error)
 
    finally:
        cursor.close()
        conx.close()

        return responsemessage, responsecode


def getpatientfromblockchain(recordid):
    if(utility.IsValidUniqueNumber(recordid,1) == True):
        data,respose=  patientcontract.getPatientbyrecordid(recordid)
        return data,respose
    else:
        return [],400

def isdeadpatient(recordid):
    if((utility.IsValidUniqueNumber(recordid,1)) == True):
        data,respose=  patientcontract.isdeadpatient(recordid)
        return data,respose
    else:
        return [],400
