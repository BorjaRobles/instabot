"""
    instabot example

    Workflow:
        1) unfollows users that don't follow you.
"""

import sys
import os
import argparse

sys.path.append(os.path.join(sys.path[0], '../'))

from instabot import Bot

bot = Bot()
bot.login(username='raulcampossbd82', password='lamadrederu23')
bot.unfollow_non_followers()
