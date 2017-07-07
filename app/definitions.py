import os
import dj_database_url


# Required environment variables.
telegram_token = os.environ['TELEGRAM_TOKEN']
database_credentials = dj_database_url.parse(os.environ['DATABASE_URL'])
superuser_login = os.environ['SUPERUSER_LOGIN']

# Optional environment variables.
cooldown_time_minutes = os.getenv('COOLDOWN_TIME', 120)
