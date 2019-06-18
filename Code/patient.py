from conection import connect
import hashlib  # for hash key
import datetime
import uuid # for UniqueID
from mysql.connector import Error
from flask import jsonify,request


# Importing Blockchain code
#import patientcontract
from datetime import datetime as dt, timedelta
import datetime
import calendar

import utility
from urllib import parse

def getallpatients():
    conx =connect()
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:        
        if(responsecode==200):
            pageNo = 1
            pageSize = 5000
            queryParams = parse.parse_qs(parse.urlsplit(request.url).query)
            if 'pageNo' in queryParams:
                pageNo = int(queryParams['pageNo'][0])
                if pageNo <= 0:
                    responsemessage = "Please Provide Non-Zero Positive Page No"
                    responsecode = 400

            if 'pageSize' in queryParams:
                pageSize = int(queryParams["pageSize"][0])
                if pageSize <= 0:
                    responsemessage="Please Provide Non-Zero Positive Page Size"
                    responsecode = 400

            if(responsecode == 200):
                offset = (pageNo-1)*pageSize
                limit = pageSize
                selectQuery = "WITH patient as (select ROW_NUMBER() OVER (PARTITION BY pfno ORDER BY duplicateno desc) rowno, ID,pfno,patientName,contact,DOB,HashID, duplicateno, Isdead,DOD, ReasonOfDeath from Patientdetails  ) select ID, pfno,patientName,contact, DATE_FORMAT(DATE_ADD('1970-01-01 00:00:00', INTERVAL DOB SECOND), '%d-%y-%Y'), HashID, duplicateno, Isdead, CASE WHEN DOD=0 THEN '00-00-0000' ELSE DATE_FORMAT(DATE_ADD('1970-01-01 00:00:00', INTERVAL DOD SECOND), '%d-%m-%Y') END, ReasonOfDeath from patient  where rowno = 1 LIMIT "+str(offset)+", "+str(limit)
                cursor.execute(selectQuery)
                myresult = cursor.fetchall() 
                if(len(myresult) != 0 and myresult[0][0] != None):        
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
            selectquery = "select ID, pfno,patientName,contact, DATE_FORMAT(DATE_ADD('1970-01-01 00:00:00', INTERVAL DOB SECOND), '%d-%m-%Y'),HashID, duplicateno, Isdead, CASE WHEN DOD=0 THEN '00-00-0000' ELSE DATE_FORMAT(DATE_ADD('1970-01-01 00:00:00', INTERVAL DOD SECOND), '%d-%m-%Y') END, ReasonOfDeath from Patientdetails where pfno = '"+ str(pfno)+"' order by duplicateNo desc limit 1"
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

        if 'patientId' not in request.json:
           responsemessage= "Provide patient id"
           responsecode =400
        else:
            patientId = request.json["patientId"]

        if 'uhid' not in request.json:
           responsemessage= "Provide uhid"
           responsecode =400
        else:
            uhid = request.json["uhid"]

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
                # transhash,response = patientcontract.addpatientrecord(uniqueid,str(pfno),str(patientname),
                #                                                         int(contact),dobtimestamp,
                #                                                         str(hash_key),maxcounter,isdead,dodtimestamp,reasonOfdeath)

                transhash = "xyz"
                response = 200
                ##### Transaction type 1 for patient 2 for hospital.
                print("transhash")
                if(response == 200):
                    insertSql = """INSERT INTO Patientdetails (ID,pfno,Patientname,
                                contact,dob,Add_Date,HashID,duplicateno,Isdead,DOD,ReasonOfDeath,patient_id,uhid) 
                                VALUES (%s, %s,%s, %s,%s, %s,%s,%s,%s,%s,%s,%s,%s)"""

                    val = (str(uniqueid), str(pfno),str(patientname),str(contact), dobtimestamp, addadate,str(hash_key),maxcounter,isdead,dodtimestamp,reasonOfdeath,str(patientId),str(uhid))
               
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

                
                # transhash,response = patientcontract.addpatientrecord(uniqueid,str(pfno),str(patientname),
                #                                                         int(contact),dobtimestamp,
                #                                                         str(hash_key),maxcounter,bool(isdead),dodtimestamp,reasonOfdeath)
                transhash = "xyz"
                response = 200
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
        data,respose = patientcontract.getPatientbyrecordid(recordid)
        dob = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds = data[2])
        data[2] = dob.strftime('%d-%m-%Y')
        return data,respose
    else:
        return [],400

def isdeadpatient(recordid):
    if((utility.IsValidUniqueNumber(recordid,1)) == True):
        data,respose =  patientcontract.isdeadpatient(recordid)
        dod = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds = data[2])
        data[2] = dod.strftime('%d-%m-%Y')
        return data,respose
    else:
        return [],400


def getpatientsbyuhid(uhid):
    conx = connect()
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:
        if (responsecode == 200):
            pageNo = 1
            pageSize = 5000
            queryParams = parse.parse_qs(parse.urlsplit(request.url).query)
            if 'pageNo' in queryParams:
                pageNo = int(queryParams['pageNo'][0])
                if pageNo <= 0:
                    responsemessage = "Please Provide Non-Zero Positive Page No"
                    responsecode = 400

            if 'pageSize' in queryParams:
                pageSize = int(queryParams["pageSize"][0])
                if pageSize <= 0:
                    responsemessage = "Please Provide Non-Zero Positive Page Size"
                    responsecode = 400

            if (responsecode == 200):
                offset = (pageNo - 1) * pageSize
                limit = pageSize
                print(uhid);
                print(offset);
                print(limit);
                selectQuery = "select ID, pfno,patientName,contact, DATE_FORMAT(DATE_ADD('1970-01-01 00:00:00', INTERVAL DOB SECOND), '%d-%m-%Y'),HashID, duplicateno, Isdead, CASE WHEN DOD=0 THEN '00-00-0000' ELSE DATE_FORMAT(DATE_ADD('1970-01-01 00:00:00', INTERVAL DOD SECOND), '%d-%m-%Y') END, ReasonOfDeath,patient_id,uhid from Patientdetails where uhid = '" + str(
                uhid) + "' order by duplicateNo desc LIMIT " + str(offset) + ", " + str(limit)
                cursor.execute(selectQuery)
                myresult = cursor.fetchall()
                print(myresult)
                if (len(myresult) != 0 and myresult[0][0] != None):
                    responsemessage = myresult
                else:
                    responsemessage = "No record"
                    responsecode = 400

    except Error as e:
        responsemessage = e.msg
        responsecode = e.errno

    finally:
        cursor.close()
        conx.close()

    return responsemessage, responsecode