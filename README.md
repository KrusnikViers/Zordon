# Zordon Telegram Bot
_Gathers together the most powerful kittens, pandas and capybaras in the Universe to fight against evil and boredom. Or, at least, to play Overwatch._

[![Build Status](https://travis-ci.org/KrusnikViers/Zordon.svg?branch=wp-2.0)](https://travis-ci.org/KrusnikViers/Zordon)
[![Build status](https://ci.appveyor.com/api/projects/status/5ek9c42yy2usr23h?branch=wp-2.0&svg=true)](https://ci.appveyor.com/project/KrusnikViers/zordon)
[![Code Climate](https://codeclimate.com/github/KrusnikViers/Zordon/badges/gpa.svg?branch=wp-2.0)](https://codeclimate.com/github/KrusnikViers/Zordon)
[![Coverage - Coveralls](https://coveralls.io/repos/github/KrusnikViers/Zordon/badge.svg?branch=wp-2.0)](https://coveralls.io/github/KrusnikViers/Zordon?branch=master)
[![Coverage - CodeCov](https://codecov.io/gh/KrusnikViers/Zordon/branch/master/graph/badge.svg?branch=wp-2.0)](https://codecov.io/gh/KrusnikViers/Zordon)

### Dependencies:

* Python 3.5 or newer
* PostgreSQL 9.2 or newer
* Packages from `requirements.txt`

### Environment variables:

* `ZORDON_DATABASE` - DSN-formatted complete URL of PostgreSQL database. DSN-format: _postgres://user:password@host:port/database_name_.
* `ZORDON_TOKEN` - Access token for Telegram Bot. Should be received from @BotFather during bot registration.
* `ZORDON_SUPERUSER` - Username of only user with unlimited access.
* `ZORDON_VERBOSITY` (optional) - logging verbosity level. Possible values are `SILENT`, `INFO`, `DEBUG` and `FULL`.

### How to run

All scripts should be executed from root directory of the project.
* Run bot: `python scripts/run_bot.py`. All required environment variables must be set and valid.
* Run tests: `python -m unittests`. All required environment variables must be set, database must exist.
* Create DB migrations: `python scripts/make_migrations.py`. Database variable must be set and valid.

### How to translate

Project uses usual `gettext` internationalization mechanism. Common way to work with translations is via `babel` package: `pip install babel`.

* Template file generation: `pybabel extract -o app/locale/<lang>/LC_MESSAGES/common.po --input-dirs=app`
* Template file compilation: `pybabel compile -o app/locale/<lang>/LC_MESSAGES/common.mo -i app/locale/<lang>/LC_MESSAGES/common.po`
