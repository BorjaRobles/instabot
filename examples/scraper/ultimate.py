"""
    ULTIMATE SCRIPT FOR RAUL

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


def get_random(from_list):
    _random=random.choice(from_list)
    print("Random from ultimate.py script is chosen: \n" + _random + "\n")
    return _random


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
args = parser.parse_args()

f = open("setting.txt")
lines = f.readlines()
setting_0 = int(lines[0].strip())
setting_1 = int(lines[1].strip())
setting_2 = int(lines[2].strip())
setting_3 = int(lines[3].strip())
setting_4 = int(lines[4].strip())
setting_5 = int(lines[5].strip())
setting_6 = int(lines[6].strip())
setting_7 = int(lines[7].strip())
setting_8 = int(lines[8].strip())
setting_9 = int(lines[9].strip())
setting_10 = int(lines[10].strip())
setting_11 = int(lines[11].strip())
setting_12 = int(lines[12].strip())
setting_13 = int(lines[13].strip())
setting_14 = int(lines[14].strip())
setting_15 = int(lines[15].strip())
setting_16 = int(lines[16].strip())
setting_17 = int(lines[17].strip())
setting_18 = lines[18].strip()

bot = Bot(
    max_likes_per_day=setting_0,
    max_unlikes_per_day=setting_1,
    max_follows_per_day=setting_2,
    max_unfollows_per_day=setting_3,
    max_comments_per_day=setting_4,
    max_likes_to_like=setting_5,
    max_followers_to_follow=setting_6,
    min_followers_to_follow=setting_7,
    max_following_to_follow=setting_8,
    min_following_to_follow=setting_9,
    max_followers_to_following_ratio=setting_10,
    max_following_to_followers_ratio=setting_11,
    min_media_count_to_follow=setting_12,
    like_delay=setting_13,
    unlike_delay=setting_14,
    follow_delay=setting_15,
    unfollow_delay=setting_16,
    comment_delay=setting_17,
    whitelist="whitelist.txt",
    comments_file="comments.txt",
    stop_words=[
        'order',
        'shop',
        'store',
        'free',
        'doodleartindonesia',
        'doodle art indonesia',
        'fullofdoodleart',
        'commission',
        'vector',
        'karikatur',
        'jasa',
        'open'])


bot.login(username=args.u, password=args.p,
          proxy=args.proxy)


bot.logger.info("ULTIMATE SCRAPING PHOTOS BOT FOR PHOTOGRAPHER")
comments_file_name = "comments.txt"


def generate_tags():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    r = requests.get('https://top-hashtags.com/instagram/', headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    thetags = []

    for tag in soup.find_all("div", {'class': 'tht-tag'}, 'a'):
        thetags.append(tag.string.encode('ascii','ignore'))

    cut = random.sample(thetags, 20)
    same = ['#follow4follow', '#f4f', '#TagsForLikes', '#like4like', '#instafollow', '#followme']
    cut.extend(same)
    return " ".join(str(x) for x in cut)


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


def job7():
    if not os.listdir('photos'):
        try:
            bot.logger.info('--------------------------------')
            bot.logger.info('Trying to download medias by tag')
            bot.logger.info('--------------------------------')

            shutil.rmtree('photos')
            for hashtag in ['portraitpage', 'top_portrait','infinite_faces',
                            'sexywoman', 'boudoirphotography',
                            'fashionphotography', 'boudoir']:
                medias = bot.get_hashtag_medias(hashtag)
                try:
                    bot.logger.info(" --- Downloading medias --- ")
                    bot.download_photos(medias)
                except:
                    bot.logger.error(" --> Something gone wrg :( <-- ")
                    pass
        except Exception as e:
            print 'Whoops something gone wrg ....'
            print(str(e))
    else:
        try:
            random_filename = random.choice([
                x for x in os.listdir('photos')
            ])

            photo_path = 'photos/' + random_filename
            tags = generate_tags()

            print("upload: " + tags)
            bot.uploadPhoto(photo_path, caption=tags)
            if bot.LastResponse.status_code != 200:
                print bot.LastResponse
        except Exception as e:
            print str(e)
        print("Removing file ... " + photo_path)
        os.remove(photo_path)


def job8():
    try:
        bot.unfollow_non_followers()
    except Exception as e:
        bot.unfollow_non_followers()
# end of job8


''' """
    Workflow:
        Download media photos with hashtag.
"""
def download_medias():
    if not os.listdir('photos'):
        try:
            bot.logger.info('--------------------------------')
            bot.logger.info('Trying to download medias by tag')
            bot.logger.info('--------------------------------')

            shutil.rmtree('photos')
            for hashtag in ['portraitpage', 'top_portrait','infinite_faces',
                            'sexywoman', 'boudoirphotography',
                            'fashionphotography', 'boudoir']:
                medias = bot.get_hashtag_medias(hashtag)
                try:
                    bot.logger.info(" --- Downloading medias --- ")
                    bot.download_photos(medias)
                except:
                    bot.logger.error(" --> Something gone wrg :( <-- ")
                    pass
        except Exception as e:
            print 'Whoops something gone wrg ....'
            print(str(e))
    else:
        bot.logger.info('-------------------------------- ')
        bot.logger.info('DONT NEED TO DOWNLOAD IMAGES YET ')
        bot.logger.info('-------------------------------- ') '''

# function to make threads -> details here http://bit.ly/faq_schedule
def run_threaded(job_fn):
    job_thread=threading.Thread(target=job_fn)
    job_thread.start()


schedule.every(1).hour.do(run_threaded, stats)              # get stats
schedule.every(6).hours.do(run_threaded, job1)              # like hashtag
schedule.every(2).hours.do(run_threaded, job2)              # like timeline
schedule.every(8).hours.do(run_threaded, job3)              # comment timeline medias
schedule.every(3).hours.do(run_threaded, job4)              # Like users medias
schedule.every(6).hours.do(run_threaded, job5)              # Going to follow followers
schedule.every(6).hours.do(run_threaded, job6)              # Follow users
schedule.every(24).hours.do(run_threaded, job7)             # Upload pic
schedule.every(72).hours.do(run_threaded, job8)             # Unfollow non followers
# schedule.every(24).hours.do(run_threaded, download_medias)  # Renew images

while True:
    schedule.run_pending()
    time.sleep(1)
