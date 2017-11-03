"""
    ULTIMATE SCRIPT FOR RAUL

    It uses data written in files:
        * follow_followers.txt
        * follow_following.txt
        * like_hashtags.txt
        * like_users.txt
    and do the job. This bot can be run 24/7.
"""

import os
import shutil
import glob
import requests
import sys
import argparse
import random
import time
import yaml             #->added to make pics upload -> see job8
import glob             #->added to make pics upload -> see job8
from tqdm import tqdm
from random import shuffle
from bs4 import BeautifulSoup


sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot


def get_random(from_list):
    _random=random.choice(from_list)
    print("Random from ultimate.py script is chosen: \n" + _random + "\n")
    return _random


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
r=requests.get('https://top-hashtags.com/instagram/', headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

thetags = []

for tag in soup.find_all("div", {'class': 'tht-tag'}, 'a'):
    thetags.append(tag.string.encode('ascii','ignore'))

cut = random.sample(thetags, 20)
same = ['#follow4follow', '#f4f', '#TagsForLikes', '#like4like', '#instafollow', '#followme']
test = cut.extend(same)
caption = " ".join(str(x) for x in cut)






parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
args = parser.parse_args()


bot = Bot(whitelist="whitelist.txt", filter_users=False,
          comments_file="comments.txt")
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)


bot.logger.info("ULTIMATE RAUL")
comments_file_name = "comments.txt"


bot.save_user_stats(bot.user_id)
print("Current script's schedule:")

follow_followers_list = bot.read_list_from_file("follow_followers.txt")
print("Going to follow followers of:", follow_followers_list)

follow_following_list = bot.read_list_from_file("follow_following.txt")
print("Going to follow following of:", follow_following_list)


random_hashtag_file = bot.read_list_from_file("follow_hashtags.txt")
print("Going to follow users of hashtags:", random_hashtag_file)


like_hashtags_list = bot.read_list_from_file("like_hashtags.txt")
print("Going to like hashtags:", like_hashtags_list)

like_users_list = bot.read_list_from_file("like_users.txt")
print("Going to like users:", like_users_list)

print("Going to comment timeline medias")
bot.comment_medias(bot.get_timeline_medias())

tasks_list = []
for item in follow_followers_list:
    bot.follow_followers(item, nfollows=10)
for item in follow_following_list:
    bot.follow_following(item)
for item in like_hashtags_list:
    bot.like_hashtag(item, amount=int(700/24))
for item in like_users_list:
    bot.like_user(item)


bot.follow_users(bot.get_hashtag_users(get_random(random_hashtag_file)))

#bot.unfollow_non_followers()

random_filename = random.choice([
     x for x in os.listdir('pics')
 ])

photo_path = 'pics/' + random_filename

print("upload: " + caption)
bot.uploadPhoto(photo_path, caption=caption)
if bot.LastResponse.status_code != 200:
    print(bot.LastResponse)

#shutil.rmtree('pics')