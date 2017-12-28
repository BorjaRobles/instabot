
rm -rf tmp
mkdir -p tmp

hadoop fs -rm -r /trash/users
hadoop fs -rm -r /trash/tags
hadoop fs -rm -r /trash/users_to_like
hadoop fs -rm -r /trash/comments

hadoop fs -mkdir -p /trash/users
hadoop fs -mkdir -p /trash/tags
hadoop fs -mkdir -p /trash/users_to_like
hadoop fs -mkdir -p /trash/comments

cd tmp
wget -O users.csv "https://docs.google.com/spreadsheets/d/1SSoHDNQhXH84ewAF0FrwW6Q8I_BSFVij0qQxAkLMagQ/export?gid=0&format=csv"
wget -O tags.csv "https://docs.google.com/spreadsheets/d/1G1sKyz7pazCesqej8xsxLfVgi8G5qm7QWTRBgyiu2zE/export?gid=0&format=csv"
wget -O users_to_like.csv "https://docs.google.com/spreadsheets/d/1aIZPJXYNI9SKhDexQNAM7Hg7XtfNSS8Hx7nDsyZEm5E/export?gid=0&format=csv"
wget -O comments.csv "https://docs.google.com/spreadsheets/d/1HRQQ0Wxf7OhXkzrkm5LwfdtcuV5IURlO0hx7GOTCKwQ/export?gid=0&format=csv"

hadoop fs -put users.csv /trash/users
hadoop fs -put tags.csv /trash/tags
hadoop fs -put users_to_like.csv /trash/users_to_like
hadoop fs -put comments.csv /trash/comments

hive -e "drop table tmp_user_data"
hive -e "drop table tmp_comments"
hive -e "drop table tmp_users_to_like"
hive -e "drop table tmp_tags"

#hive -e "drop table user_data"
#hive -e "drop table comments"
#hive -e "drop table users_to_like"
#hive -e "drop table tags"


hive -e "CREATE TABLE IF NOT EXISTS user_data (username STRING, password STRING, proxy STRING, account_type STRING, running STRING) STORED AS ORC;"
hive -e "CREATE TABLE IF NOT EXISTS comments (comment STRING, comment_type STRING) STORED AS ORC;"
hive -e "CREATE TABLE IF NOT EXISTS users_to_like (username STRING) STORED AS ORC;"
hive -e "CREATE TABLE IF NOT EXISTS tags (tagname STRING, tagtype STRING) STORED AS ORC;"


hive -e "CREATE EXTERNAL TABLE IF NOT EXISTS tmp_user_data(username STRING, password STRING, proxy STRING, account_type STRING, running STRING) COMMENT 'Users temporal data' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION '/trash/users'"
hive -e "CREATE EXTERNAL TABLE IF NOT EXISTS tmp_comments(comment STRING, comment_type STRING) COMMENT 'Comments' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION '/trash/comments'"
hive -e "CREATE EXTERNAL TABLE IF NOT EXISTS tmp_users_to_like(username STRING) COMMENT 'Users to like' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION '/trash/users_to_like'"
hive -e "CREATE EXTERNAL TABLE IF NOT EXISTS tmp_tags(tagname STRING, tagtype STRING) COMMENT 'List of tags' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION '/trash/tags'"


hive -e "INSERT OVERWRITE TABLE comments SELECT A.comment, A.comment_type FROM tmp_comments as A LEFT JOIN comments as B ON A.comment = B.comment"
hive -e "INSERT OVERWRITE TABLE comments SELECT A.comment, A.comment_type FROM tmp_comments as A LEFT JOIN comments as B WHERE A.comment = B.comment"
hive -e "INSERT OVERWRITE TABLE users_to_like SELECT A.username FROM tmp_users_to_like as A LEFT JOIN users_to_like as B ON A.username = B.username"
hive -e "INSERT OVERWRITE TABLE tags SELECT A.tagname, A.tagtype FROM tmp_tags as A LEFT JOIN tags as B ON A.tagname = B.tagname"



