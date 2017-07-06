import os
import dj_database_url
import urlparse

# Required environment variables.
telegram_token = os.environ['TELEGRAM_TOKEN']
database_credentials = dj_database_url.parse(os.environ['DATABASE_URL'])
superuser_login = os.environ['SUPERUSER_LOGIN']

# Optional environment variables.
cooldown_time_minutes = os.getenv('COOLDOWN_TIME', 120)
web_hook_params = urlparse(os.environ['WEB_HOOK_URL']) if 'WEB_HOOK_URL' in os.environ else None
