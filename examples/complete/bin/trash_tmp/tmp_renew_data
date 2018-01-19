
# Renew temporal local folder
rm -rf tmp_downloads
mkdir -p tmp_downloads

# Delete folders
hadoop fs -rm -r /instabot/users
hadoop fs -rm -r /instabot/tags
hadoop fs -rm -r /instabot/users_to_like
hadoop fs -rm -r /instabot/comments
hadoop fs -rm -r /instabot/config

# Create new blank folders
hadoop fs -mkdir -p /instabot/users
hadoop fs -mkdir -p /instabot/tags
hadoop fs -mkdir -p /instabot/users_to_like
hadoop fs -mkdir -p /instabot/comments
hadoop fs -mkdir -p /instabot/config

# Download data
cd tmp_downloads

wget -O users.csv "https://docs.google.com/spreadsheets/d/1SSoHDNQhXH84ewAF0FrwW6Q8I_BSFVij0qQxAkLMagQ/export?gid=0&format=csv"
wget -O tags.csv "https://docs.google.com/spreadsheets/d/1G1sKyz7pazCesqej8xsxLfVgi8G5qm7QWTRBgyiu2zE/export?gid=0&format=csv"
wget -O users_to_like.csv "https://docs.google.com/spreadsheets/d/1aIZPJXYNI9SKhDexQNAM7Hg7XtfNSS8Hx7nDsyZEm5E/export?gid=0&format=csv"
wget -O comments.csv "https://docs.google.com/spreadsheets/d/1HRQQ0Wxf7OhXkzrkm5LwfdtcuV5IURlO0hx7GOTCKwQ/export?gid=0&format=csv"
wget -O config.csv "https://docs.google.com/spreadsheets/d/1aYrsrOautRvRYLRbBidDElkV1PsCXOa9z-7RVEOlsIk/export?gid=0&format=csv"

# Upload data to the cluster
hadoop fs -put users.csv /instabot/users
hadoop fs -put tags.csv /instabot/tags
hadoop fs -put users_to_like.csv /instabot/users_to_like
hadoop fs -put comments.csv /instabot/comments
hadoop fs -put config.csv /instabot/config

# Create the tables
#hive -e "CREATE EXTERNAL TABLE IF NOT EXISTS user_data(username STRING, password STRING, proxy STRING, account_type STRING, running STRING) COMMENT 'Users temporal data' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION '/instabot/users'"
#hive -e "CREATE EXTERNAL TABLE IF NOT EXISTS comments(comment STRING, comment_type STRING) COMMENT 'Comments' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION '/instabot/comments'"
#hive -e "CREATE EXTERNAL TABLE IF NOT EXISTS users_to_like(username STRING, active STRING) COMMENT 'Users to like' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION '/instabot/users_to_like'"
#hive -e "CREATE EXTERNAL TABLE IF NOT EXISTS tags(tagname STRING, tagtype STRING) COMMENT 'List of tags' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION '/instabot/tags'"

cd ..

hive -f bin/table_config.q
hive -f bin/table_user_data.q
hive -f bin/table_comments.q
hive -f bin/table_users_to_like.q
hive -f bin/table_tags.q

