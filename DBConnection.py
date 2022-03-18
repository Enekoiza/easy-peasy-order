import mysql.connector

def databaseConnection():
  conn = mysql.connector.connect(user='root', password='argider_12',
                              host='127.0.0.1', port=3306, database='EASYPEASY',
                              auth_plugin='mysql_native_password')

  return conn
