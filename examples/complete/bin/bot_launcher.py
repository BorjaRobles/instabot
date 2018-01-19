from multiprocessing import Process
import os, shutil
import threading
import schedule
import time
from pyhive import hive
from TCLIService.ttypes import TOperationState
import MySQLdb

BOT_PATH = '~/instabot/examples/complete/'

def launch_user(user):
    hive_cursor = hive.connect('localhost').cursor()
    bot_version_q = "SELECT bot_version FROM config"
    hive_cursor = hive.connect('localhost').cursor()
    hive_cursor.execute(bot_version_q)
    bot_v = hive_cursor.fetchone()

    mysql_connection = MySQLdb.connect(db="INSTABOT")
    mysql_cur=mysql_connection.cursor()
    query = "SELECT RUNNING FROM INSTABOT.ACCOUNTS_HIVE WHERE USERNAME = '%s'" % str(user[0])
    mysql_cur.execute(query)
    result = mysql_cur.fetchone()

    if str(result[0]) == 'FALSE':
        os.system('python %sultimate.py -u ' + 
        	str(user[0]) + ' -p ' + str( user[1]) + ' -proxy masush:masush@' + str(user[2]) + ' -version ' + str(bot_v[0])) % BOT_PATH


mysql_connection = MySQLdb.connect(db="INSTABOT")
mysql_cur=mysql_connection.cursor()
query = "select USERNAME, PASSWORD, PROXY from INSTABOT.ACCOUNTS_HIVE where running = 'FALSE'"
mysql_cur.execute(query)
info = mysql_cur.fetchall()

for user in info:
    p = Process(target=launch_user, args=(user,))
    p.start()
    time.sleep(5)
