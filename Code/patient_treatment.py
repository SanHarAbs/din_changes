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
import json
#import Treatment_PatientTreatmentContract
from urllib import parse

def addPatientTreatment():
    conx = connect()
    print('connection')
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:

        if not request.json:
            return 'Please send a valid Json object', 400

        uniqueId = str(datetime.datetime.utcnow()).replace("-", "").replace(":", "").replace(".", "").replace(" ", "")

        if 'ptPfNo' not in request.json:
           responsemessage= "Provide patient pfNo"
           responsecode =400
        else:
            ptPfNo = request.json["ptPfNo"]

        if 'patientid' not in request.json:
           responsemessage= "Provide patient id"
           responsecode =400
        else:
            patientid = request.json["patientid"]

        if 'uhid' not in request.json:
           responsemessage= "Provide uhid"
           responsecode =400
        else:
            uhid = request.json["uhid"]

        selectQuery = "SELECT pfno FROM Patientdetails WHERE pfno='"+ptPfNo+"'"
        cursor.execute(selectQuery)
        myresult = cursor.fetchall()    
        if(len(myresult) == 0):
            responsemessage= "Invalid patient pfNo"
            responsecode =400

        if 'treatmentId' not in request.json:
            responsemessage = "Provide treatment Id"
            responsecode = 400
        else:
            treatmentId = request.json["treatmentId"]

        selectQuery = "SELECT treatment_id FROM treatment WHERE treatment_id = '"+ treatmentId+ "'"
        cursor.execute(selectQuery)
        myresult = cursor.fetchall()       
        if(len(myresult) == 0):
            responsemessage= "Invalid Treatment Id"
            responsecode =400

        if 'isTest' not in request.json:
           responsemessage = "Provide isTest details"
           responsecode = 400
        else:
            isTest = request.json["isTest"]

        if 'patientDetails' not in request.json:
           responsemessage = "Provide patient details"
           responsecode = 400
        else:
            patientDetails = request.json["patientDetails"]

        patienttreatmentid = "pt"+str(uniqueId)
       
        
        if(responsecode == 200):
            versionNo = 1
            addDate = datetime.datetime.now()
            hashId = hashlib.md5((uniqueId+
                                    str(ptPfNo)+
                                    str(treatmentId)+
                                    str(patientid) +
                                    str(isTest)+
                                    str(patientDetails)+
                                    str(patienttreatmentid)+
                                    str(versionNo)
                                    ).encode('utf-8')).hexdigest()
            
             # Insert Record intot the Block chain
            # transhash,response = Treatment_PatientTreatmentContract.addPatientTreatment(uniqueId,patienttreatmentid,ptPfNo, treatmentId, hashId)
            
            transhash = "xyz"
            response = 200

            if(response == 200):
                insertQuery = """INSERT INTO patient_treatment(record_id, patient_treatment_id, pt_pf_no, treatment_id, is_test, pt_details, version_no, add_date, hash_id, patient_id, uhid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                val = (uniqueId, patienttreatmentid, ptPfNo, treatmentId, isTest, json.dumps(patientDetails), versionNo, addDate, str(hashId), str(patientid), str(uhid))
                cursor.execute(insertQuery, val)
                conx.commit()
                
                print('Saved to Database')
                # 3 For Treatment and 4 For Paient Treatment
                utility.savetransactionrecord(str(uniqueId),str(transhash),4,addDate)
                print('Transaction record saved')

                responsemessage = "{'message':'Patient treatment successfully added','treatId':'"+patienttreatmentid+"'}"
                responsecode = 200
            else:
                responsemessage = "Error"
                responsecode = 400
        
    except Error as e:
        print(e)
        responsemessage =e.msg
        responsecode =e.errno
    finally:
        cursor.close()
        conx.close()
        return responsemessage, responsecode

def updatePatientTreatmentByPatientTreatmentId():
    conx = connect()
    print('connection')
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:
        
        if not request.json:
            return 'Please send a valid Json object', 400

        if 'patientTreatmentId' not in request.json:
           responsemessage= "Provide Patient treatment ID"
           responsecode =400
        else:
            patientTreatmentId = request.json["patientTreatmentId"]

        selectQuery = "SELECT patient_treatment_id, pt_pf_no, treatment_id, is_test FROM patient_treatment WHERE patient_treatment_id='"+patientTreatmentId+"' ORDER BY version_no DESC LIMIT 1"
        cursor.execute(selectQuery)
        myresult = cursor.fetchone()    
        if(myresult != None):
            ptPfNo = myresult[1]
            treatmentId = myresult[2]
            isTest =  myresult[3]
        else:
            responsemessage = "Invalid Patient Treatment Id"
            responsecode = 400
        
        uniqueId = str(datetime.datetime.utcnow()).replace("-", "").replace(":", "").replace(".", "").replace(" ", "")
        print(uniqueId)
        # print(request.json["ptPfNo"])
        # if 'ptPfNo' not in request.json:
        #    responsemessage= "Provide patient pfNo"
        #    responsecode =400
        # else:
        #     ptPfNo = request.json["ptPfNo"]

        # selectQuery = "SELECT pfno FROM Patientdetails WHERE pfno='"+ptPfNo+"'"
        # cursor.execute(selectQuery)
        # myresult = cursor.fetchall()    
        # if(len(myresult) == 0):
        #     responsemessage= "Invalid patient pfNo"
        #     responsecode =400

        # if 'treatmentId' not in request.json:
        #    responsemessage = "Provide treatment Id"
        #    responsecode = 400
        # else:
        #     treatmentId = request.json["treatmentId"]

        # selectQuery = "SELECT treatment_id FROM treatment WHERE treatment_id = '"+ treatmentId+ "'"
        # cursor.execute(selectQuery)
        # myresult = cursor.fetchall()       
        # if(len(myresult) == 0):
        #     responsemessage= "Invalid Treatment Id"
        #     responsecode =400

        # if 'isTest' not in request.json:
        #    responsemessage = "Provide isTest details"
        #    responsecode = 400
        # else:
        #     isTest = request.json["isTest"]

        if 'patientDetails' not in request.json:
            if isTest == 0:
                responsemessage = "Provide Patient's Treatment Details"
            elif  isTest == 1:
                responsemessage = "Provide Patient's Test Details"
            else:
                responsemessage = "Provide Patient's Details"
            responsecode = 400
        else:
            patientDetails = request.json["patientDetails"]
       
        if(responsecode == 200):
        
            selectQuery = "SELECT MAX(version_no) AS versionNo FROM patient_treatment WHERE patient_treatment_id = '"+ patientTreatmentId+"'"
            cursor.execute(selectQuery)
            myresult = cursor.fetchone()       
            if(myresult[0] == None):
                versionNo = 1
            else:
                versionNo = (int(myresult[0])+1)

            addDate = datetime.datetime.now()
            hashId = hashlib.md5((uniqueId+
                                    str(ptPfNo)+
                                    str(treatmentId)+
                                    str(isTest)+
                                    str(patientDetails)+
                                    str(patientTreatmentId)+
                                    str(versionNo)
                                    ).encode('utf-8')).hexdigest()
             # Insert Record intot the Block chain
            # transhash,response = Treatment_PatientTreatmentContract.addPatientTreatment(uniqueId,patientTreatmentId,ptPfNo, treatmentId, hashId)
            
            transhash = "xyz"
            response = 200

            if(response == 200):
                insertQuery = """INSERT INTO patient_treatment(record_id, patient_treatment_id, pt_pf_no, treatment_id, is_test, pt_details, version_no, add_date, hash_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                val = (uniqueId, patientTreatmentId, ptPfNo, treatmentId, isTest, json.dumps(patientDetails), versionNo, addDate, str(hashId))
                cursor.execute(insertQuery, val)
                conx.commit()

                print('Saved to Database')
                # 3 For Treatment and 4 For Paient Treatment
                utility.savetransactionrecord(str(uniqueId),str(transhash),4,addDate)
                print('Transaction record saved')
                responsemessage = "Patient treatment successfully updated"
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

def getPatientTreatmentByPatientPfNo(ptPfNo):
    conx = connect()
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:        
        if(responsecode == 200):
            # selectquery = "SELECT record_id AS recordId, patient_treatment_id AS patientTreatmentId, pt_pf_no AS ptPfNo, treatment_id AS treatmentId, pt_details AS ptDetails, version_no AS versionNo, add_date AS addDate, hash_id AS hashId FROM patient_treatment WHERE pt_pf_no = '"+ str(ptPfNo)+"' ORDER BY version_no DESC LIMIT 1"
            selectquery = "WITH pt_treatment AS (SELECT ROW_NUMBER() OVER (PARTITION BY patient_treatment_id ORDER BY version_no desc) rowNo, record_id AS recordId, patient_treatment_id AS patientTreatmentId, pt_pf_no AS ptPfNo, treatment_id AS treatmentId, is_test AS isTest, pt_details AS ptDetails, version_no AS versionNo, add_date AS addDate, hash_id AS hashId FROM patient_treatment WHERE pt_pf_no='"+ptPfNo+"') SELECT recordId, patientTreatmentId, ptPfNo, treatmentId, isTest, ptDetails, versionNo, addDate, hashId FROM pt_treatment WHERE rowNo = 1"
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

def getPatientTreatmentByTreatmentId(treatmentId):
    conx = connect()
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:        
        if(responsecode == 200):
            selectquery = "SELECT record_id AS recordId, patient_treatment_id AS patientTreatmentId, pt_pf_no AS ptPfNo, treatment_id AS treatmentId, is_test AS isTest, pt_details AS ptDetails, version_no AS versionNo, add_date AS addDate, hash_id AS hashId FROM patient_treatment WHERE treatment_id = '"+treatmentId+"' ORDER BY version_no DESC LIMIT 1"
            # selectquery = "WITH pt_treatment AS (SELECT ROW_NUMBER() OVER (PARTITION BY pt_pf_no ORDER BY version_no desc) rowNo, record_id AS recordId, patient_treatment_id AS patientTreatmentId, pt_pf_no AS ptPfNo, treatment_id AS treatmentId, pt_details AS ptDetails, version_no AS versionNo, add_date AS addDate, hash_id AS hashId FROM patient_treatment WHERE treatment_id='"+treatmentId+"') SELECT recordId, patientTreatmentId, ptPfNo, treatmentId, ptDetails, versionNo, addDate, hashId FROM pt_treatment WHERE rowNo = 1"
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

def getPatientTreatmentByPatientTreatmentId(patientTreatmentId):
    conx = connect()
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:        
        if(responsecode == 200):
            selectquery = "SELECT record_id AS recordId, patient_treatment_id AS patientTreatmentId, pt_pf_no AS ptPfNo, treatment_id AS treatmentId, is_test AS isTest, pt_details AS ptDetails, version_no AS versionNo, add_date AS addDate, hash_id AS hashId FROM patient_treatment WHERE patient_treatment_id = '"+ str(patientTreatmentId)+"' ORDER BY version_no DESC LIMIT 1"
            # selectquery = "WITH pt_treatment AS (SELECT ROW_NUMBER() OVER (PARTITION BY pt_pf_no ORDER BY version_no desc) rowNo, record_id AS recordId, patient_treatment_id AS patientTreatmentId, pt_pf_no AS ptPfNo, treatment_id AS treatmentId, pt_details AS ptDetails, version_no AS versionNo, add_date AS addDate, hash_id AS hashId FROM patient_treatment WHERE patient_treatment_id='"+patientTreatmentId+"') SELECT recordId, patientTreatmentId, ptPfNo, treatmentId, ptDetails, versionNo, addDate, hashId FROM pt_treatment WHERE rowNo = 1"
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

def getPatientTreatmentByRecordId(recordId):
    conx = connect()
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:        
        if(responsecode == 200):
            selectquery = "SELECT record_id AS recordId, patient_treatment_id AS patientTreatmentId, pt_pf_no AS ptPfNo, treatment_id AS treatmentId, pt_details AS ptDetails, is_test AS isTest, version_no AS versionNo, add_date AS addDate, hash_id AS hashId FROM patient_treatment WHERE record_id = '"+ str(recordId)+"'"
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

def getPatientTreatments():
    conx = connect()
    responsemessage = ""
    responsecode = 200
    cursor = conx.cursor()
    try:        
        if(responsecode == 200):
            pageNo = 1
            pageSize = 2000
            queryParams = parse.parse_qs(parse.urlsplit(request.url).query)
            if 'pageNo' in queryParams:
                pageNo = int(queryParams['pageNo'][0])
                if pageNo <= 0:
                    print("Negative")
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
                selectQuery = "WITH pt_treatment AS (SELECT ROW_NUMBER() OVER (PARTITION BY patient_treatment_id ORDER BY version_no desc) rowNo, record_id AS recordId, patient_treatment_id AS patientTreatmentId, pt_pf_no AS ptPfNo, treatment_id AS treatmentId, is_test AS isTest, pt_details AS ptDetails, version_no AS versionNo, add_date AS addDate, hash_id AS hashId FROM patient_treatment) SELECT recordId, patientTreatmentId, ptPfNo, treatmentId, isTest, ptDetails, versionNo, addDate, hashId FROM pt_treatment WHERE rowNo = 1 LIMIT "+str(offset)+", "+str(limit)
                cursor.execute(selectQuery)
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

def getpatienttreatmentfromblockchain(recordid):
    
    if(utility.IsValidUniqueNumber(recordid,4) == True):
        data,respose=  Treatment_PatientTreatmentContract.getPatientTreatment(recordid)
        return data,respose
    else:
        return [],400
