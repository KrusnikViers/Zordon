# Zordon Telegram Bot
[![Build Status](https://travis-ci.org/KrusnikViers/Zordon.svg?branch=master&style=flat)](https://travis-ci.org/KrusnikViers/Zordon)
[![Build Status](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](https://opensource.org/licenses/MIT)

_Gathers together the most powerful kittens, pandas and capybaras in this Universe. And your friends, also._

Allow to register set of activities. Users, subscribed on Bot and specific activity, may call other subscribers to start new session. Mainly, written to gather party for Overwatch :3

### Deployment:

**Dependencies:**
* Python 2.7
* PostgreSQL DB

**Environment variables:**

* `TELEGRAM_TOKEN`\
Access token for Telegram Bot.\
Should be received from @BotFather during bot registration.
* `DATABASE_URL`\
DSN-formatted complete URL of PostgreSQL database.\
DSN-format: `postgres://<user>:<password>@<host>:<port>/<database_name>`.
* `SUPERUSER_LOGIN`\
Username (without @) of only user with unlimited access 
* `COOLDOWN_TIME` (optional)\
Duration (in minutes) of time period, while user considered as participant of activity.
* `WEBHOOK_URL` (optional)\
URL of the Zordon server.\
If set, bot will run in webhook mode, instead of usual polling.
