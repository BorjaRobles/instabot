"""
    instabot example

    Workflow:
        Take users from input file and follow them.
        The file should contain one username per line!
"""

import sys
import os
import argparse

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
args = parser.parse_args()

bot = Bot(filter_users=False)
users_to_follow = bot.read_list_from_file("clients.txt")
if not users_to_follow:
    exit()
else:
    print("Found %d users in file." % len(users_to_follow))

bot.login(username=args.u, password=args.p,
          proxy=args.proxy)

bot.follow_users(users_to_follow)