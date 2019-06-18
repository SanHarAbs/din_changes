import mysql.connector
from mysql.connector import Error
from mysql.connector.errors import Error


def connect():
    """ Connect to MySQL database """
    try:
        cnxn = mysql.connector.connect(host='125.62.193.130',
                                       database='patientdata',
                                       user='root',
                                       auth_plugin='mysql_native_password',
                                       password='pa$$word')
        return cnxn
    except Error as e:
        raise Exception("Error in database connection", Error)
