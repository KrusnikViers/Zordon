# Telegram Bot Template 1.0.0

[![Build Status](https://travis-ci.org/KrusnikViers/TgBotTemplate.svg)](https://travis-ci.org/KrusnikViers/TgBotTemplate)
[![Build status](https://ci.appveyor.com/api/projects/status/6uaw3t0aevq62ydp?svg=true)](https://ci.appveyor.com/project/KrusnikViers/tgbottemplate)
[![Coverage - Codecov](https://codecov.io/gh/KrusnikViers/TgBotTemplate/branch/master/graph/badge.svg)](https://codecov.io/gh/KrusnikViers/TgBotTemplate)
[![Maintainability](https://api.codeclimate.com/v1/badges/11bbbf9259251bdcada3/maintainability)](https://codeclimate.com/github/KrusnikViers/TgBotTemplate/maintainability)

This project is intended to be used as a base for other Telegram bots. Current template has next features/requirements:
* Requires Python 3.6 or newer
* Requires Python packages from `requirements.txt`
* Contains lightweight database, that could be used to store your bot information
* Has localization support using Babel library.
* Has templates for tests and CI services for open source projects.

_If any changes made to this file, check all places with RELEASE-UPDATE comment in code to be updated accordingly_

## Before the start
Every Telegram bot needs token from the @BotFather. When registering a token, keep in mind:
* For participating in groups, Group mode should be enabled;
* To see group message history, Group privacy mode should be disabled.

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
