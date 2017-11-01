import time, sys, os, yaml, glob, argparse, sys, random, requests, shutil
from instabot import Bot
from bs4 import BeautifulSoup

sys.path.append(os.path.join(sys.path[0], '../../'))

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
args = parser.parse_args()

random_filename = random.choice([
    x for x in os.listdir('pics')
])

photo_path = 'pics/' + random_filename

bot = Bot()
bot.login(username=args.u, password=args.p)

print("upload: " + caption)
bot.uploadPhoto(photo_path, caption=caption)
if bot.LastResponse.status_code != 200:
    print(bot.LastResponse)

shutil.rmtree('pics')
