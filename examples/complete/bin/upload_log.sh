#!/bin/bash

hadoop fs -put -f $1/*.tsv /instabot/logs
