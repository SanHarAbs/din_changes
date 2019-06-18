from conection import connect

def savetransactionrecord(recordid,transactionhash,transactiontype,adddate):
    print('i am here')
    conx =connect()
    cursor = conx.cursor()
    print('inside')
    insertSql = """INSERT INTO transactionrecords
                    (uniqueid,transactionhash,type,Add_Date) 
                    VALUES (%s, %s,%s, %s)"""

    val = (recordid,transactionhash,transactiontype,adddate)
    cursor.execute(insertSql, val)
    conx.commit()

def validatestringlength(stringdata):
    cleanstr = stringdata.strip()
    if(len(cleanstr)<=30):
        return True,cleanstr
    else:
        return False,'string should not be greater then 30 characters'

def IsValidUniqueNumber(number,typeid):
    conx =connect()
    cursor = conx.cursor()
    selectquery = "select uniqueid  from transactionrecords where uniqueid = '"+ str(number)+"' and  type = '"+str(typeid)+"' limit 1"""
    cursor.execute(selectquery)
    myresult = cursor.fetchall()
    
    # print(myresult)
    # print(len(myresult))

    if(len(myresult)>0):        
       return True
    else:
        return False
