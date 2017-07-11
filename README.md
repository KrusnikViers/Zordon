# Zordon Telegram Bot
_Gathers together the most powerful kittens, pandas and capybaras in the Universe to fight against evil and boredom. Or, at least, to play Overwatch._

[![Build Status](https://travis-ci.org/KrusnikViers/Zordon.svg?branch=master)](https://travis-ci.org/KrusnikViers/Zordon)
[![Code Climate](https://codeclimate.com/github/KrusnikViers/Zordon/badges/gpa.svg)](https://codeclimate.com/github/KrusnikViers/Zordon)
[![Coverage Status](https://coveralls.io/repos/github/KrusnikViers/Zordon/badge.svg?branch=master)](https://coveralls.io/github/KrusnikViers/Zordon?branch=master)

To run bot, you have to set necessary environment variables and run `python run_bot.py`. Tests can be run via `python -m unittests` in root directory.

### Dependencies:

* Python 3.3 or newer
* PostgreSQL 9.2 or newer
* Packages from `requirements.txt`

### Environment variables:

* `TELEGRAM_TOKEN` - Access token for Telegram Bot. Should be received from @BotFather during bot registration.
* `DATABASE_URL` - DSN-formatted complete URL of PostgreSQL database. DSN-format: _postgres://user:password@host:port/database_name_.
* `SUPERUSER_LOGIN` - Username of only user with unlimited access.
* `COOLDOWN_TIME` (optional) - Duration (in minutes) of time period, while user considered as participant of activity.
