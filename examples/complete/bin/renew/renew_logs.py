from multiprocessing import Process
import os, shutil
import threading
import schedule
import time
from pyhive import hive
from TCLIService.ttypes import TOperationState
import MySQLdb

mysql_connection = MySQLdb.connect(db="INSTABOT")
mysql_cur=mysql_connection.cursor()
query = "select USERNAME from INSTABOT.ACCOUNTS_HIVE where running = 'TRUE'"
mysql_cur.execute(query)
info = mysql_cur.fetchall()

for user in info:
  os.system('hadoop fs -put -f ~/instabot/examples/complete/user_logs/%s/%s.tsv /instabot/tmp_logs' % (str(user[0]),str(user[0]))
