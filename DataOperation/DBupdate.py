import mysql.connector
from mysql.connector import Error
def UpdateData(btnid, servicename,phonenumber,lat,long):
    status="Update Fail!"
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='thesisdb',
                                             user='root',
                                             password='root')
        cursor = connection.cursor()
        sql_update_query = """Update emservice set ServiceName = %s,PhoneNumber=%s,Latitude=%s,Longitude=%s where Id = %s"""
        inputData = (servicename,phonenumber,lat,long,btnid)
        cursor.execute(sql_update_query, inputData)
        connection.commit()
        print("Record Updated successfully ")
        status="Record Updated successfully "
    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return status;

