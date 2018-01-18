drop table user_data;

SET parquet.compression=SNAPPY;
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;


CREATE EXTERNAL TABLE IF NOT EXISTS user_data (
	username STRING,
	password STRING,
	proxy STRING,
	account_type STRING,
	running STRING
)
COMMENT 'Users temporal data' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION '/instabot/users';

MSCK REPAIR TABLE user_data;
