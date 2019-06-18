from flask_cors import CORS
from flask import Flask,jsonify,abort,make_response,request
import os.path
import hospital
import patient
import treatment
import patient_treatment

app = Flask(__name__)
CORS(app)


############ Hospital Endpoints ##############
@app.route('/api/getallhospitals', methods=['GET'])
def getallhospitals_endpoint():
    message, code = hospital.getallhospitals()
    return make_response(jsonify({'Result': message}), code)


@app.route('/api/gethospitalbyregistrationno/<registrationno>', methods=['GET'])
def getpatientbypfno(registrationno):
    message, code = hospital.gethospitalbyregistrationno(registrationno)
    return make_response(jsonify({'Result': message}), code)


@app.route('/api/createhospital', methods=['POST'])
def addhospital():
    message, code = hospital.addhospital()
    return make_response(jsonify({'Result': message}), code)


@app.route('/api/modifyhospital', methods=['POST'])
def modifyhospital():
    message, code = hospital.modifyhospital()
    return make_response(jsonify({'Result': message}), code)


@app.route('/api/gethospitalfromchain/<recordid>', methods=['GET'])
def gethospitalfromchain(recordid):
    message, code = hospital.gethospitalfromblockchain(recordid)
    thislist = []
    for p in message:
        try:
            t = p.decode()
            thislist.append(t)
        except AttributeError:
            thislist.append(p)
            pass
    # return jsonify('',code)
    return make_response(jsonify({'Result': thislist}), code)


############## End for Hospital Endpoints ########


########### Patient Endpoints ###########
@app.route('/api/getallpatients', methods=['GET'])
def getallpatients():
    message, code = patient.getallpatients()
    return make_response(jsonify({'Result': message}), code)


@app.route('/api/getpatientbypfno/<pfno>', methods=['GET'])
def patientbypfno(pfno):
    message, code = patient.getpatientbypfno(pfno)
    return make_response(jsonify({'Result': message}), code)

@app.route('/api/getpatientsbyuhid/<uhid>', methods=['GET'])
def patientsbyuhid(uhid):
    message, code = patient.getpatientsbyuhid(uhid)
    return make_response(jsonify({'Result': message}), code)


@app.route('/api/getpatientfromchain/<recordid>', methods=['GET'])
def getpatientfromchain(recordid):
    message, code = patient.getpatientfromblockchain(recordid)

    thislist = []
    for p in message:
        try:
            t = p.decode()

            thislist.append(t)
        except AttributeError:

            thislist.append(p)
            pass
    # return jsonify('',code)
    return make_response(jsonify({'Result': thislist}), code)


@app.route('/api/ispatientdead/<recordid>', methods=['GET'])
def ispatientdead(recordid):
    message, code = patient.isdeadpatient(recordid)
    thislist = []
    for p in message:
        try:
            t = p.decode()
            thislist.append(t)
        except AttributeError:
            thislist.append(p)
            pass
    # return jsonify('',code)
    return make_response(jsonify({'Result': thislist}), code)


@app.route('/api/createPatient', methods=['POST'])
def AddPatient():
    message, code = patient.AddPatient()
    return make_response(jsonify({'Result': message}), code)


@app.route('/api/modifypatient', methods=['POST'])
def modifypatient():
    message, code = patient.modifypatient()
    return make_response(jsonify({'Result': message}), code)


########### Patient Treatment Endpoints ###########
@app.route('/api/addPatientTreatment', methods=['POST'])
def addPatientTreatment():
    message,code = patient_treatment.addPatientTreatment()
    return make_response(jsonify({'Result': message}), code)

@app.route('/api/updatePatientTreatmentByPatientTreatmentId', methods=['POST'])
def updatePatientTreatmentByPatientTreatmentId():
    message,code = patient_treatment.updatePatientTreatmentByPatientTreatmentId()
    return make_response(jsonify({'Result': message}), code)

@app.route('/api/getPatientTreatmentByRecordId/<recordId>', methods=['GET'])
def getPatientTreatmentByRecordId(recordId):
    message,code = patient_treatment.getPatientTreatmentByRecordId(recordId)
    return make_response(jsonify({'Result': message}), code)

@app.route('/api/getPatientTreatmentByPatientPfNo/<patientPfNo>', methods=['GET'])
def getPatientTreatmentByPatientPfNo(patientPfNo):
    message,code = patient_treatment.getPatientTreatmentByPatientPfNo(patientPfNo)
    return make_response(jsonify({'Result': message}), code)

@app.route('/api/getPatientTreatmentByTreatmentId/<treatmentId>', methods=['GET'])
def getPatientTreatmentByTreatmentId(treatmentId):
    message,code = patient_treatment.getPatientTreatmentByTreatmentId(treatmentId)
    return make_response(jsonify({'Result': message}), code)

@app.route('/api/getTreatmentByPatientId/<patientId>', methods=['GET'])
def getTreatmentByPatientId(patientId):
    message,code = treatment.getTreatmentByPatientId(patientId)
    return make_response(jsonify({'Result': message}), code)

@app.route('/api/getTreatmentsByUhid/<uhid>', methods=['GET'])
def getTreatmentsByUhid(uhid):
    message,code = treatment.getTreatmentsByUhid(uhid)
    return make_response(jsonify({'Result': message}), code)

@app.route('/api/getPatientTreatmentByPatientTreatmentId/<patientTreatmentId>', methods=['GET'])
def getPatientTreatmentByPatientTreatmentId(patientTreatmentId):
    print(os.path.split("="))
    message,code = patient_treatment.getPatientTreatmentByPatientTreatmentId(patientTreatmentId)
    return make_response(jsonify({'Result': message}), code)

@app.route('/api/getPatientTreatments', methods=['GET'])
def getPatientTreatments():
    message,code = patient_treatment.getPatientTreatments()
    return make_response(jsonify({'Result': message}), code)

@app.route('/api/getpatienttreatmentfromblockchain/<recordid>', methods=['GET'])
def getpatienttreatmentfromblockchain(recordid):
    
    message,code = patient_treatment.getpatienttreatmentfromblockchain(recordid)

    thislist =[]
    for p in message:   
        try:
            t= p.decode()
            thislist.append(t)
        except AttributeError:
            thislist.append(p)
            pass
    #return jsonify('',code)
    return make_response(jsonify({'Result': thislist}), code)

#############End for patient treatment end points ########33
if __name__ == '__main__':
    app.run( host='0.0.0.0', port=5000,debug=True)