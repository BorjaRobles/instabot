"""
    SCRIPT FOR NOT UPLOAD PHOTOS

    It uses data written in files:
        * follow_followers.txt
        * follow_following.txt
        * like_hashtags.txt
        * like_users.txt
    and do the job. This bot can be run 24/7.
"""

import os, shutil, glob, requests
import sys, argparse, random, time
import yaml, glob
from tqdm import tqdm
from random import shuffle
from bs4 import BeautifulSoup
import threading
import schedule

sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
args = parser.parse_args()

bot = Bot(whitelist="whitelist.txt", filter_users=False,
          comments_file="comments.txt")
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)


bot.logger.info("ULTIMATE NOT UPLOAD PHOTOS")
comments_file_name = "comments.txt"


def stats(): bot.save_user_stats(bot.user_id)


def job1():
    try:
        like_hashtags_list = bot.read_list_from_file("like_hashtags.txt")
        print("Going to like hashtags:", like_hashtags_list)

        for item in like_hashtags_list:
            bot.like_hashtag(item, amount=int(700/24))
    except Exception as e:
        print(str(e))


def job2():
    try:
        bot.like_timeline(amount=int(300/24))
    except Exception as e:
        print(str(e))


def job3():
    try:
        print("Going to comment timeline medias")
        bot.comment_medias(bot.get_timeline_medias())
    except Exception as e:
        print(str(e))


def job4():
    try:
        like_users_list = bot.read_list_from_file("like_users.txt")
        print("Going to like users:", like_users_list)

        for item in like_users_list:
            bot.like_user(item)
    except Exception as e:
        print(str(e))


def job5():
    try:
        follow_followers_list = bot.read_list_from_file("follow_followers.txt")
        print("Going to follow followers of:", follow_followers_list)

        for item in follow_followers_list:
            bot.follow_followers(item)
    except Exception as e:
        print(str(e))


def job6():
    try:
        follow_following_list = bot.read_list_from_file("follow_following.txt")
        print("Going to follow:", follow_following_list)

        for item in follow_following_list:
            bot.follow_users(item)
    except Exception as e:
        print(str(e))


def job8():
    try:
        print("Going to unfollow non followers")
        bot.unfollow_non_followers()
    except Exception as e:
        print("Something not worked trying again")
        bot.unfollow_non_followers()


# function to make threads -> details here http://bit.ly/faq_schedule
def run_threaded(job_fn):
    job_thread=threading.Thread(target=job_fn)
    job_thread.start()

schedule.every(1).hour.do(run_threaded, stats)              # get stats
schedule.every(6).hours.do(run_threaded, job1)              # like hashtag
schedule.every(2).hours.do(run_threaded, job2)              # like timeline
schedule.every(8).hours.do(run_threaded, job3)              # comment timeline medias
schedule.every(1).days.at("16:00").do(run_threaded, job4)   # Like users medias
schedule.every(6).hours.do(run_threaded, job5)              # Going to follow followers
schedule.every(6).hours.do(run_threaded, job6)              # Follow users
schedule.every(5).days.at("10:00").do(run_threaded, job8)   # Unfollow non followers


while True:
    schedule.run_pending()
    time.sleep(1)
