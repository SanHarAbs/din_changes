from conection import connect
import hashlib  # for hash key
import datetime
import uuid # for UniqueID
from mysql.connector import Error
from flask import jsonify,request
from datetime import datetime as dt
import datetime
import calendar
import utility
#import Treatment_PatientTreatmentContract

def addTreatment():
    conx = connect()
    print('connection')
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:

        if not request.json:
           return 'Please send a valid Json object', 400

        uniqueId = str(datetime.datetime.utcnow()).replace("-", "").replace(":", "").replace(".", "").replace(" ", "")

        if 'treatmentName' not in request.json:
           responsemessage = "Provide treatment name"
           responsecode = 400
        else:
            treatmentName = request.json["treatmentName"]

        if 'patientid' not in request.json:
           responsemessage = "Provide patient id"
           responsecode = 400
        else:
            patientid = request.json["patientid"]

        if 'uhid' not in request.json:
           responsemessage = "Provide uhid"
           responsecode = 400
        else:
            uhid = request.json["uhid"]
        
        res,treatmentName = utility.validatestringlength(treatmentName)

        if(res == False):
            responsemessage=treatmentName
            responsecode = 400

        treatmentid = "t"+str(uniqueId)

        if(responsecode == 200):
            versionNo = 1
            addDate = datetime.datetime.now()
            hashId = hashlib.md5((
                                    uniqueId+
                                    str(treatmentid)+
                                    str(treatmentName)+
                                    str(patientid) +
                                    str(versionNo)
                                    ).encode('utf-8')).hexdigest()

        # Insert Record intot the Block chain
        # transhash,response = Treatment_PatientTreatmentContract.addTreatment(uniqueId, str(treatmentid), str(hashId))

        transhash = "xyz"
        response = 200
        if(response == 200):
            insertSql = """INSERT INTO treatment(record_id, treatment_id, treatment_name, version_no, add_date, hash_id, patient_id, uhid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (uniqueId, treatmentid, str(treatmentName), versionNo, addDate, str(hashId), str(patientid), str(uhid))

            cursor.execute(insertSql, val)
            conx.commit()
            print('Saved to Database')
            # 3 For Treatment and 4 For Paient Treatment
            utility.savetransactionrecord(str(uniqueId),str(transhash),3,addDate)
            responsemessage = "Treatment added"
            responsecode = 200
        else:
            responsecode = 400
            responsemessage = 'Error'

    except Error as e:
        print(e)
        responsemessage =e.msg
        responsecode =e.errno
    finally:
        cursor.close()
        conx.close()
        return responsemessage, responsecode

def updateTreatmentByTreatmentId():
    conx = connect()
    print('connection')
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:

        if not request.json:
           return 'Please send a valid Json object', 400

        if 'treatmentId' not in request.json:
           responsemessage = "Provide Treatment Id"
           responsecode = 400
        else:
            treatmentId = request.json["treatmentId"]

        selectQuery = "SELECT treatment_id FROM treatment WHERE treatment_id='"+treatmentId+"'"
        cursor.execute(selectQuery)
        myresult = cursor.fetchall()    
        if(len(myresult) == 0):
            responsemessage= "Invalid Treatment Id"
            responsecode =400
        
        if 'treatmentName' not in request.json:
           responsemessage = "Provide treatment name"
           responsecode = 400
        else:
            treatmentName = request.json["treatmentName"]

        uniqueId = str(datetime.datetime.utcnow()).replace("-", "").replace(":", "").replace(".", "").replace(" ", "")
        
        # res,treatmentName = utility.validatestringlength(treatmentName)

        # if(res == False):
        #     responsemessage=treatmentName
        #     responsecode = 400

        if(responsecode == 200):
            selectQuery = """SELECT MAX(version_no) AS versionNo FROM treatment WHERE treatment_id='"""+treatmentId+"'"
            cursor.execute(selectQuery)
            myresult = cursor.fetchone()       
            if(myresult[0] == None):
                versionNo = 1
            else:
                versionNo = (int(myresult[0])+1)
            
            addDate = datetime.datetime.now()
            hashId = hashlib.md5((uniqueId+
                                  str(treatmentId)+
                                  str(treatmentName)+
                                  str(versionNo)
                                ).encode('utf-8')).hexdigest()

            # Insert Record intot the Block chain
            # transhash,response = Treatment_PatientTreatmentContract.addTreatment(uniqueId, str(treatmentId), str(hashId))
            transhash = "xyz"
            response = 200
            if(response == 200):
                insertSql = """INSERT INTO treatment(record_id, treatment_id, treatment_name, version_no, add_date, hash_id) VALUES (%s, %s, %s, %s, %s, %s)"""
                val = (uniqueId, treatmentId, str(treatmentName), versionNo, addDate, str(hashId))
                cursor.execute(insertSql, val)
                conx.commit()

                print('Saved to Database')
                # 3 For Treatment and 4 For Paient Treatment
                utility.savetransactionrecord(str(uniqueId),str(transhash),3,addDate)

                responsemessage = "Treatment successfully updated"
                responsecode = 200
            else:
                responsemessage = "Error"
                responsecode = 400

    except Error as e:
        responsemessage =e.msg
        responsecode =e.errno
    finally:
        cursor.close()
        conx.close()
        return responsemessage, responsecode


def getTreatments():
    conx = connect()
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:        
        if(responsecode == 200):
            selectquery = """WITH treatmnt AS (SELECT ROW_NUMBER() OVER (PARTITION BY treatment_id ORDER BY version_no DESC) rowNo, record_id AS recordId, treatment_id AS treatmentId, treatment_name AS treatmentName, version_no AS versionNo, add_date AS addDate, hash_id AS hashId FROM treatment) SELECT recordId, treatmentId, treatmentName, versionNo, addDate, hashId FROM treatmnt WHERE rowNo = 1"""
            cursor.execute(selectquery)
            myresult = cursor.fetchall() 
            if(len(myresult) != 0):        
                responsemessage = myresult
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

def getTreatmentByTreatmentId(treatmentId):
    conx = connect()
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:        
        if(responsecode == 200):
            selectquery = "SELECT record_id AS recordId, treatment_id AS treatmentId, treatment_name AS treatmentName, version_no AS versionNo, add_date AS addDate, hash_id AS hashId FROM treatment WHERE treatment_id = '"+ str(treatmentId)+"' ORDER BY version_no DESC LIMIT 1"
            cursor.execute(selectquery)
            myresult = cursor.fetchall() 
            if(len(myresult) != 0):        
                responsemessage = myresult
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

def getTreatmentByRecordId(recordId):
    conx = connect()
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:        
        if(responsecode == 200):
            selectquery = "SELECT record_id AS recordId, treatment_id AS treatmentId, treatment_name AS treatmentName, version_no AS versionNo, add_date AS addDate, hash_id AS hashId FROM treatment WHERE record_id = " + recordId
            cursor.execute(selectquery)
            myresult = cursor.fetchall() 
            if(len(myresult) != 0):        
                responsemessage = myresult
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

def gettreatmentfromblockchain(recordid):
    
    if(utility.IsValidUniqueNumber(recordid,3) == True):
        data,respose=  Treatment_PatientTreatmentContract.getTreatmentByRecordId(recordid)
        return data,respose
    else:
        return [],400


def getTreatmentByPatientId(patientId):
    conx = connect()
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:
        if (responsecode == 200):
            selectquery = "SELECT record_id AS recordId, treatment_id AS treatmentId, treatment_name AS treatmentName, version_no AS versionNo, add_date AS addDate, hash_id AS hashId FROM treatment WHERE patient_id = '" + str(
                patientId) + "' ORDER BY version_no DESC LIMIT 1"
            cursor.execute(selectquery)
            myresult = cursor.fetchall()
            if (len(myresult) != 0):
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

def getTreatmentsByUhid(uhid):
    conx = connect()
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:
        if (responsecode == 200):
            selectquery = "SELECT record_id AS recordId, treatment_id AS treatmentId, treatment_name AS treatmentName, version_no AS versionNo, add_date AS addDate, hash_id AS hashId,patient_id AS patientid,uhid AS uhId  FROM treatment WHERE uhid = '" + str(
                uhid) + "' ORDER BY version_no DESC"
            cursor.execute(selectquery)
            myresult = cursor.fetchall()
            if (len(myresult) != 0):
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
