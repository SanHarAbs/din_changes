
from flask_cors import CORS
from flask import Flask,jsonify,abort,make_response,request
import hospital
import patient
import hospital
app = Flask(__name__)
CORS(app)

############ Hospital Endpoints ##############
@app.route('/api/getallhospitals', methods=['GET'])
def getallhospitals_endpoint():
    message,code = hospital.getallhospitals()
    return make_response(jsonify({'Result': message}), code)

@app.route('/api/gethospitalbyregistrationno/<registrationno>', methods=['GET'])
def getpatientbypfno(registrationno):
    message,code = hospital.gethospitalbyregistrationno(registrationno)
    return make_response(jsonify({'Result': message}), code)

@app.route('/api/createhospital', methods=['POST'])
def addhospital():
    message,code = hospital.addhospital()
    return make_response(jsonify({'Result': message}), code)

@app.route('/api/modifyhospital', methods=['POST'])
def modifyhospital():
    message,code = hospital.modifyhospital()
    return make_response(jsonify({'Result': message}), code)


@app.route('/api/gethospitalfromchain/<recordid>', methods=['GET'])
def gethospitalfromchain(recordid):
    message,code = hospital.gethospitalfromblockchain(recordid)
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

############## End for Hospital Endpoints ########


########### Patient Endpoints ###########
@app.route('/api/getallpatients', methods=['GET'])
def getallpatients():
    message,code = patient.getallpatients()
    return make_response(jsonify({'Result': message}), code)

@app.route('/api/getpatientbypfno/<pfno>', methods=['GET'])
def patientbypfno(pfno):
    message,code = patient.getpatientbypfno(pfno)
    return make_response(jsonify({'Result': message}), code)

@app.route('/api/getpatientfromchain/<recordid>', methods=['GET'])
def getpatientfromchain(recordid):
    message,code = patient.getpatientfromblockchain(recordid)
    
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

@app.route('/api/ispatientdead/<recordid>', methods=['GET'])
def ispatientdead(recordid):
    message,code = patient.isdeadpatient(recordid)
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


@app.route('/api/createPatient', methods=['POST'])
def AddPatient():
    message,code = patient.AddPatient()
    return make_response(jsonify({'Result': message}), code)

@app.route('/api/modifypatient', methods=['POST'])
def modifypatient():
    message,code = patient.modifypatient()
    return make_response(jsonify({'Result': message}), code)


#############End for patient end points ########33
if __name__ == '__main__':
    app.run( debug=True)