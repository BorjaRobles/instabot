import time
import sys
import os
import yaml
import glob
from instabot import Bot
import argparse
import sys

sys.path.append(os.path.join(sys.path[0], '../../'))

from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
args = parser.parse_args()

posted_pic_list = []
try:
    with open('pics.txt', 'r') as f:
        posted_pic_list = f.read().splitlines()
except:
    posted_pic_list = []

bot = Bot()
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)


pics = glob.glob("./pics/*.jpg")
pics = sorted(pics)

try:
    for pic in pics:
        if pic in posted_pic_list:
            continue

            caption = pic[:-4].split(" ")
            caption = " ".join(caption[1:])

            print("upload: " + caption)
            bot.uploadPhoto(pic, caption=caption)
            if bot.LastResponse.status_code != 200:
                print(bot.LastResponse)
                # snd msg
                break

            if not pic in posted_pic_list:
                posted_pic_list.append(pic)
                with open('pics.txt', 'a') as f:
                    f.write(pic + "\n")

except Exception as e:
    print(str(e))
