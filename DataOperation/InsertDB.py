import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
def InsertData(name,phonenumber,latitude,longitude):
    status="Entry should not be empty"
    try:
        connection = mysql.connector.connect(host='localhost',
                                         database='thesisdb',
                                         user='root',
                                         password='root')
        mySql_insert_query = """INSERT INTO emservice (ServiceName, PhoneNumber, Latitude, Longitude) 
                           VALUES 
                           (%s,%s,%s,%s) """
        cursor = connection.cursor()
        recordTuple=(name,phonenumber,latitude,longitude)
        result = cursor.execute(mySql_insert_query,recordTuple)
        connection.commit()
        print("Record inserted successfully into Service table")
        status="Record inserted successfully into Service table"
        cursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))
    finally:
        if (connection.is_connected()):
            connection.close()
        print("MySQL connection is closed")
    return status;
    
