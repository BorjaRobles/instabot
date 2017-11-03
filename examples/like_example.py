"""
    instabot example

    Workflow:
    1) likes your timeline feed
    2) likes user's feed

    Notes:
    1) You should pass user_id, not username
"""

import argparse
import time
import sys
import os

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
args = parser.parse_args()



bot = Bot(filter_users=False)
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)

# like media by a single user_id
like_users_list = bot.read_list_from_file("like_users.txt")

for item in like_users_list:
    bot.like_user(item)

#bot.like_user('kekukybarcelona')

# likes all media from timeline
#bot.like_timeline()

# likes all media from timeline
#bot.like_medias(bot.get_timeline_medias())

# likes media by hashtag(s)
tags = ["l4l"]

for t in tags:
    bot.like_hashtag(t)
