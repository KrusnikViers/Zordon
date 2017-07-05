import os
import dj_database_url
import urlparse

telegram_token = os.environ['TELEGRAM_TOKEN']

database_credentials = dj_database_url.parse(os.environ['DATABASE_URL'])

cooldown_time_minutes = os.getenv('COOLDOWN_TIME', 120)

superuser_login = os.getenv('SUPERUSER_LOGIN')

is_web_hook_mode = 'WEB_HOOK_URL' in os.environ
if is_web_hook_mode:
    web_hook_params = urlparse(os.environ['WEB_HOOK_URL'])
