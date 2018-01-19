drop table comments;

CREATE EXTERNAL TABLE IF NOT EXISTS comments (
	comment STRING,
	comment_type STRING
)
COMMENT 'Comments' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION '/instabot/comments';

MSCK REPAIR TABLE comments;
