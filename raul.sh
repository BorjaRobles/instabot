#!/bin/sh

cd examples

echo -e " *************************************   "
echo -e " *        RAUL STUFF             *   "
echo -e " ************************************* \n\n"



echo -e " *************************************   "
echo -e " *        FOLLOWER STUFF             *   "
echo -e " ************************************* \n"

echo -e " Following clients \n"
## Follow clients
python follow_users_from_file.py -u raulcampossbd82 -p lamadrederu23 "$(realpath clients.txt)"

echo -e " Following HASTAGS \n"
## Follow users by hashtag
python follow_users_by_hashtag.py -u raulcampossbd82 -p lamadrederu23 hashtags follow4follow like4like instafollow followme followforfollow followback

echo -e " Following FOLLOWERS \n"
## Follow followers
python follow_user_following.py -u raulcampossbd82 -p lamadrederu23


echo -e " *************************************   "
echo -e " *        LIKES.  STUFF              *   "
echo -e " ************************************* \n"


echo -e " Like clients lasts media \n"
##Like clients lasts media
python like_users.py -u raulcampossbd82 -p lamadrederu23



echo -e " Like HASTAGS \n"
## Like hastags
python like_hashtags.py -u raulcampossbd82 -p lamadrederu23 hashtags follow4follow like4like instafollow followme followforfollow followback


echo -e " *************************************   "
echo -e " *        DOWNLOAD STUFSS            *   "
echo -e " ************************************* \n"


cd autopost
python download.py -q 'best images'

python auto_post.py -u raulcampossbd82 -p lamadrederu23
