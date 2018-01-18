#!/bin/bash

hadoop fs -put -f user_logs/$1/*.tsv /instabot/tmp_logs
#hive -f bin/logs_usage.q
