# Zordon Telegram Bot 3.0

### Current version is under development and highly unstable

[![Build Status](https://travis-ci.org/KrusnikViers/Zordon.svg)](https://travis-ci.org/KrusnikViers/Zordon)
[![Build status](https://ci.appveyor.com/api/projects/status/5ek9c42yy2usr23h?svg=true)](https://ci.appveyor.com/project/KrusnikViers/zordon)
[![Coverage - Coveralls](https://coveralls.io/repos/github/KrusnikViers/Zordon/badge.svg)](https://coveralls.io/github/KrusnikViers/Zordon?branch=master)
[![Code Climate](https://codeclimate.com/github/KrusnikViers/Zordon/badges/gpa.svg)](https://codeclimate.com/github/KrusnikViers/Zordon)

[![Docker Build Status](https://img.shields.io/docker/build/viers/zordon.svg)](https://hub.docker.com/r/viers/zordon/)
[![Docker Pulls](https://img.shields.io/docker/pulls/viers/zordon.svg)](https://hub.docker.com/r/viers/zordon/)
[![MicroBadger Size](https://images.microbadger.com/badges/image/viers/zordon.svg)](https://hub.docker.com/r/viers/zordon/)


## How to run

To run bot in Docker container, use command below: 

`docker run --restart always --net=<internal network with postgresql> --name zordon -v <path to configuration>:/configuration.json -d viers/zordon`

Bot can be started without docker by `python scripts/run_bot.py`. Parameters can be configured via the command line or in the configuration json file.

Tests can be run with `python -m unittests` in root directory.

### BotFather
Check bot settings with BotFather:
* Group mode should be enabled
* Inline mode should be disabled
* Group privacy mode should be disabled

### Dependencies:

* Python 3.7 or newer
* PostgreSQL database
* Packages from `requirements.txt`
