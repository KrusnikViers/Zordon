# Zordon Telegram Bot 3.1.3

Telegram bot for group broadcasts and gathering people together.

[![Build Status](https://travis-ci.org/KrusnikViers/Zordon.svg)](https://travis-ci.org/KrusnikViers/Zordon)
[![Build status](https://ci.appveyor.com/api/projects/status/5ek9c42yy2usr23h?svg=true)](https://ci.appveyor.com/project/KrusnikViers/zordon)
[![Coverage - Codecov](https://codecov.io/gh/KrusnikViers/Zordon/branch/master/graph/badge.svg)](https://codecov.io/gh/KrusnikViers/Zordon)
[![Code Climate](https://codeclimate.com/github/KrusnikViers/Zordon/badges/gpa.svg)](https://codeclimate.com/github/KrusnikViers/Zordon)

[![Docker Build Status](https://img.shields.io/docker/build/viers/zordon.svg)](https://hub.docker.com/r/viers/zordon/)
[![Docker Pulls](https://img.shields.io/docker/pulls/viers/zordon.svg)](https://hub.docker.com/r/viers/zordon/)
[![MicroBadger Size](https://images.microbadger.com/badges/image/viers/zordon.svg)](https://hub.docker.com/r/viers/zordon/)

## Before the start
To be launched, bot needs token from @BotFather and PostgreSQL database. Also check token settings:
* Group mode should be enabled
* Inline mode should be disabled
* Group privacy mode should be disabled

At the moment, webhook mode is not available.

Bot could be configured by configuration json file or via command line (`-param_name=value`). Configuration example is in the `configuration.json.example` file, database url and Telegram API token are only required parameters.

You may specify path to the configuration file by `config=path` command line parameter. If path was not specified, bot will be looking for `configuration.json` file in the root folder.

## How to run via Docker

It is recommended to run PostgreSQL as another container and unite both containers in one internal network. Otherwise, additional `net` param is not required. To run bot as a Docker container (with docker installed) use command below: 

`docker run --restart always --net=<internal network with postgresql> --name zordon -v <path to configuration>:/configuration.json -d viers/zordon`

## Run as a developer

Project root directory should be added to `PYTHONPATH` for correct work. There are few scripts in `/scripts` directory, that are necessary for development:
* `make_migrations.py`: autogenerate migrations from updated models. Requires only `-d` parameter.
* `update_translations.py`: regenerate translations from code.
* `run_tests.py`: launch python tests. Requires only `-d` parameter, **everything in this database will be erased**
* `run_bot.py`: launch bot itself. Requires full configuration. 

### Dependencies:

* Python 3.6 or newer
* PostgreSQL database
* Packages from `requirements.txt`
