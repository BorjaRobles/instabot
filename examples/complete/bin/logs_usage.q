drop table tmp_logs;
drop table logs;

SET parquet.compression=SNAPPY;
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;

CREATE EXTERNAL TABLE logs (
  seguidores int,
  siguiendo int,
  medias int,
  username string)
PARTITIONED BY (dt STRING)
LOCATION '/instabot/logs';


create external table tmp_logs (
  dt string,
  seguidores int,
  siguiendo int,
  medias int,
  username string
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n'
STORED AS TEXTFILE LOCATION '/instabot/tmp_logs'
tblproperties('skip.header.line.count'='1');

INSERT OVERWRITE TABLE logs PARTITION (dt)
SELECT seguidores, siguiendo, medias, username, dt FROM tmp_logs;

MSCK REPAIR TABLE logs;
