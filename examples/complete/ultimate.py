import os, shutil, glob, requests
import sys, argparse, random, time
import yaml, glob
from tqdm import tqdm
from random import shuffle
from bs4 import BeautifulSoup
import threading
import schedule
from pyhive import hive


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
    filter_users=False,
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



bot.login(username=args.u, password=args.p, proxy=args.proxy)

print "ULTIMATE SCRAPING BOT FOR %s" % (args.u)

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


def like_user_list():
    try:
        like_users_list = bot.read_list_from_file("like_users.txt")
        print("Going to like users:", like_users_list)

        for item in like_users_list:
            bot.like_user(item)
    except Exception as e:
        print(str(e))


def follow_users_by_hashtag():
    hashtag_list = bot.read_list_from_file("follow_hashtags.txt")

    for hashtag in hashtag_list:
        users = bot.get_hashtag_users(hashtag)
        bot.follow_users(users)



def stats():
    bot.save_user_stats(username=bot.user_id, path=args.u)
    # Logic for add the info to hadoop


def comment_medias():
    try:
        print("Going to comment timeline medias")
        bot.comment_medias(bot.get_timeline_medias())
    except Exception as e:
        print(str(e))


def upload_media():
    if not os.listdir('photos'):
        try:
            bot.logger.info('--------------------------------')
            bot.logger.info('Trying to download medias by tag')
            bot.logger.info('--------------------------------')

            shutil.rmtree('photos')
            for hashtag in ['portraitpage', 'top_portrait','infinite_faces','fashionphotography']:
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


def unfollow():
    try:
        bot.unfollow_non_followers()
    except Exception as e:
        bot.unfollow_non_followers()
# end of job8

# function to make threads -> details here http://bit.ly/faq_schedule
def run_threaded(job_fn):
    job_thread=threading.Thread(target=job_fn)
    job_thread.start()



schedule.every(1).hour.do(run_threaded, stats)                                 # get stats
schedule.every(3).hours.do(run_threaded, like_user_list)              # Like users medias
schedule.every(6).hours.do(run_threaded, follow_users_by_hashtag)              # like hashtag
schedule.every(8).hours.do(run_threaded, comment_medias)              # comment timeline medias
schedule.every(24).hours.do(run_threaded, upload_media)             # Upload pic
schedule.every(72).hours.do(run_threaded, unfollow)                            # Unfollow non followers

while True:
    schedule.run_pending()
    time.sleep(1)