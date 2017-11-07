from InstagramAPI import InstagramAPI
from bs4 import BeautifulSoup
import random, os, requests, shutil

user,pwd = 'cortneyrodriguizs', 'insta@123'

InstagramAPI = InstagramAPI(user,pwd)
InstagramAPI.login() # login

random_filename = random.choice([
    x for x in os.listdir('pictures')
])

photo_path = 'pictures/' + random_filename

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
r=requests.get('https://top-hashtags.com/instagram/', headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')


thetags = []

for tag in soup.find_all("div", {'class': 'tht-tag'}, 'a'):
    thetags.append(tag.string.encode('ascii','ignore'))

cut = random.sample(thetags, 24)
same = ['#follow4follow', '#f4f', '#TagsForLikes', '#like4like', '#instafollow', '#followme']
test = cut.extend(same)
caption = " ".join(str(x) for x in cut)

InstagramAPI.uploadPhoto(photo_path, caption =caption)

#shutil.rmtree('/pictures')
