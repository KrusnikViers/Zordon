#!/usr/bin/env bash

export PYTHONPATH="$PYTHONPATH:/zordon"
python3 /zordon/scripts/run_bot.py --configuration-file=/configuration.json
