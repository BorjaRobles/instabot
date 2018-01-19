import os, shutil, glob, requests
import sys, argparse, random, time
import yaml, glob
from tqdm import tqdm
from random import shuffle
from bs4 import BeautifulSoup
import threading
import schedule
from pyhive import hive
from TCLIService.ttypes import TOperationState
import MySQLdb

def launch_bots():
    os.system('python ~/instabot/examples/complete/bin/bot_launcher.py')


def renew_data():
    for file in os.listdir("~/instabot/examples/complete/bin/renew"):
        if file.endswith(".sh"):
            os.system('%s') % os.path.join('~/instabot/examples/complete/bin/renew/', file)
        elif file.endswith(".py"):
            os.system('python %s') % os.path.join('~/instabot/examples/complete/bin/renew/', file)


def data_processing():
    for file in os.listdir("~/instabot/examples/complete/bin/data_processing"):
        if file.endswith(".sh"):
            os.system('%s') % os.path.join('~/instabot/examples/complete/bin/data_processing/', file)
        elif file.endswith(".py"):
            os.system('python %s') % os.path.join('~/instabot/examples/complete/bin/data_processing/', file)

def run_threaded(job_fn):
    job_thread=threading.Thread(target=job_fn)
    job_thread.start()

schedule.every(1).hour.do(run_threaded, launch_bots)
schedule.every(2).hours.do(run_threaded, renew_data)
schedule.every(24).hours.do(run_threaded, data_processing)


while True:
    schedule.run_pending()
    time.sleep(1)
