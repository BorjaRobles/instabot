from pyhive import hive
from multiprocessing import Process
import os, shutil
import threading
import schedule
import time


def launch_user(user):
  os.system('python2.7 ultimate.py -u ' + str(user[0]) + ' -p ' + str( user[1]) + ' -proxy masush:masush@' + str(user[2]))


def renew_data():
    os.system('./bin/renew_data.sh')


while True:
    renew_data()

    cursor = hive.connect('sandbox.hortonworks.com').cursor()
    cursor.execute('SELECT * FROM user_data WHERE running <> "true"')
    info = cursor.fetchall()
    
    for user in info:
        p = Process(target=launch_user, args=(user,))
        p.start()
        time.sleep(60)


    time.sleep(1440)