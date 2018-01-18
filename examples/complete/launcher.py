from pyhive import hive
from multiprocessing import Process
import os, shutil
import threading
import schedule
import time
from TCLIService.ttypes import TOperationState
import MySQLdb

def launch_user(user):
  os.system('python ultimate.py -u ' + str(user[0]) + ' -p ' + str( user[1]) + ' -proxy masush:masush@' + str(user[2]))


def renew_data():
    shutil.rmtree('bin/tmp', ignore_errors=True)
    #os.system('./bin/renew_data.sh')
    
    os.system('hadoop fs -rm -r /instabot/users')
    os.system('hadoop fs -rm -r /instabot/tags')
    os.system('hadoop fs -rm -r /instabot/users_to_like')
    os.system('hadoop fs -rm -r /instabot/comments')
    os.system('hadoop fs -mkdir -p /instabot/users')
    os.system('hadoop fs -mkdir -p /instabot/tags')
    os.system('hadoop fs -mkdir -p /instabot/users_to_like')
    os.system('hadoop fs -mkdir -p /instabot/comments')
    os.system('cd tmp')
    os.system('wget -O users.csv "https://docs.google.com/spreadsheets/d/1SSoHDNQhXH84ewAF0FrwW6Q8I_BSFVij0qQxAkLMagQ/export?gid=0&format=csv"')
    os.system('wget -O tags.csv "https://docs.google.com/spreadsheets/d/1G1sKyz7pazCesqej8xsxLfVgi8G5qm7QWTRBgyiu2zE/export?gid=0&format=csv"')
    os.system('wget -O users_to_like.csv "https://docs.google.com/spreadsheets/d/1aIZPJXYNI9SKhDexQNAM7Hg7XtfNSS8Hx7nDsyZEm5E/export?gid=0&format=csv"')
    os.system('wget -O comments.csv "https://docs.google.com/spreadsheets/d/1HRQQ0Wxf7OhXkzrkm5LwfdtcuV5IURlO0hx7GOTCKwQ/export?gid=0&format=csv"')

# Upload data to the cluster
    os.system('hadoop fs -put users.csv /instabot/users')
    os.system('hadoop fs -put tags.csv /instabot/tags')
    os.system('hadoop fs -put users_to_like.csv /instabot/users_to_like')
    os.system('hadoop fs -put comments.csv /instabot/comments')

    os.system('python bin/from_hive_to_mysql.py')

while True:
    renew_data()
    
    mysql_connection = MySQLdb.connect(db="INSTABOT")
    mysql_cur=mysql_connection.cursor()
    query = "select USERNAME, PASSWORD, PROXY from INSTABOT.ACCOUNTS_HIVE where running = 'FALSE'"
    mysql_cur.execute(query)
    info = mysql_cur.fetchall()
    
    for user in info:
        p = Process(target=launch_user, args=(user,))
        p.start()
        time.sleep(60)


    time.sleep(900)
