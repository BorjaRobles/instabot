from pyhive import hive
from TCLIService.ttypes import TOperationState
import MySQLdb
import sys

cursor = hive.connect('localhost').cursor()
mysql_connection = MySQLdb.connect(db="INSTABOT" )

cursor.execute('select username, password, proxy from user_data')
user_data = cursor.fetchall()

def find_existing_one(username):
  mysql_cur=mysql_connection.cursor()
  query = "SELECT USERNAME FROM INSTABOT.ACCOUNTS_HIVE WHERE USERNAME='%s'" % str(username[0])
  mysql_cur.execute(query)
  result = mysql_cur.fetchone()
  try:
    if str(result[0]):
      return True
  except Exception as e:
    return False

for user in user_data:
        mysql_cur=mysql_connection.cursor()
	if find_existing_one(user):
	  query = "UPDATE INSTABOT.ACCOUNTS_HIVE SET USERNAME='%s', PASSWORD='%s', PROXY='%s' WHERE USERNAME='%s'" % (str(user[0]), str(user[1]), str(user[2]), str(user[0]))
	  mysql_cur.execute(query)
          mysql_connection.commit()
	else:
          query = "INSERT INTO INSTABOT.ACCOUNTS_HIVE (USERNAME, PASSWORD, PROXY, RUNNING) VALUES ('%s', '%s', '%s', 'FALSE') ON DUPLICATE KEY UPDATE USERNAME = '%s', PASSWORD= '%s', PROXY='%s'" % (str(user[0]), str(user[1]), str(user[2]), str(user[0]), str(user[1]), str(user[2]))
          mysql_cur.execute(query)
	  mysql_connection.commit()
