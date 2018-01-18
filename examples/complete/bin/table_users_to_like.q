drop table users_to_like;

CREATE EXTERNAL TABLE IF NOT EXISTS users_to_like (
	username STRING,
	active STRING
)
COMMENT 'Users to like' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION '/instabot/users_to_like';

MSCK REPAIR TABLE users_to_like;
