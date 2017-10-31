"""
    instabot example

    Workflow:
        Like last medias by users list like_users.txt
"""

import argparse
import sys
import os

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)

like_users_list = bot.read_list_from_file("like_users.txt")
print("Going to like users:", like_users_list)


for item in like_users_list:
    bot.like_user, {'user_id': item, 'amount': None}
