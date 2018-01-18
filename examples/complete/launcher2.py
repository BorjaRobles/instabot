from multiprocessing import Process
import os, shutil
import threading
import schedule
import time
from pyhive import hive
from TCLIService.ttypes import TOperationState
import MySQLdb


def launch_user(user):
    hive_cursor = hive.connect('localhost').cursor()
    bot_version_q = "SELECT bot_version FROM config"
    hive_cursor = hive.connect('localhost').cursor()
    hive_cursor.execute(bot_version_q)
    bot_v = hive_cursor.fetchone()    

    os.system('python ultimate.py -u ' + str(user[0]) + ' -p ' + str( user[1]) + ' -proxy masush:masush@' + str(user[2]) + ' -version ' + str(bot_v[0]))

def renew_data():
    os.system('./bin/renew_data.sh')
    os.system('./bin/from_hive_to_mysql.py')

def transform():
    os.system('hive -f bin/logs_usage.q')

def launch_bots():
    print 'Starting new bot accounts'
    renew_data()

    mysql_connection = MySQLdb.connect(db="INSTABOT")
    mysql_cur=mysql_connection.cursor()
    query = "select USERNAME, PASSWORD, PROXY from INSTABOT.ACCOUNTS_HIVE where running = 'FALSE'"
    mysql_cur.execute(query)
    info = mysql_cur.fetchall()

    for user in info:
        p = Process(target=launch_user, args=(user,))
        p.start()
        time.sleep(5)



while True:
  launch_bots()
  time.sleep(86400)
  transform()
