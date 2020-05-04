# Zordon Telegram Bot 4.0.0

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

Options could be passed via configuration json file or command line (`-param_name=value`), configuration example is
in the `configuration.json.example` file. By default, bot will be looking for `configuration.json` file in the root
directory (same level with this README file). Telegram API token is the only required parameter to have bot started.

## How to run via Docker

```
docker run --restart always --name <instance name> -d <docker image name> \
 -v <path to configuration>:/instance/configuration.json \
 -v <path to the db directory>:/instance/storage
```

## How to run as a developer

Project root directory should be added to `PYTHONPATH`. There are few scripts in `/scripts` directory, that are
useful for the development:
* `make_migrations.py`: autogenerate migrations from the updated models.
* `update_translations.py`: regenerate translations from the code.
* `run_tests.py`: launch python tests.
* `run_bot.py`: launch bot itself. Requires full configuration. 
