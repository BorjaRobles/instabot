drop table config;

CREATE EXTERNAL TABLE config (
    bot_version INT,
    filter_users STRING,
    max_likes_per_day INT,
    max_unlikes_per_day INT,
    max_follows_per_day INT,
    max_unfollows_per_day INT,
    max_comments_per_day INT,
    max_likes_to_like INT,
    max_followers_to_follow INT,
    min_followers_to_follow INT,
    max_following_to_follow INT,
    min_following_to_follow INT,
    max_followers_to_following_ratio INT,
    max_following_to_followers_ratio INT,
    min_media_count_to_follow INT,
    like_delay INT,
    unlike_delay INT,
    follow_delay INT,
    unfollow_delay INT,
    comment_delay INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'
LOCATION '/instabot/config'
tblproperties ("skip.header.line.count"="1");

MSCK REPAIR TABLE config;
