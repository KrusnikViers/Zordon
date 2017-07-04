import os

token = os.environ['ZRD_TELEGRAM_TOKEN']

db_name = os.getenv('ZRD_DB_NAME', 'zordon_db')
db_host = os.getenv('ZRD_DB_HOST', '127.0.0.1')
db_user = os.getenv('ZRD_DB_USER', 'zordon_user')
db_pass = os.getenv('ZRD_DB_PASS', '')

is_hook_on = os.getenv('ZRD_HOOK_ENABLED', False)
if is_hook_on:
    hook_host = os.getenv('ZRD_HOOK_HOST', '127.0.0.1')
    hook_path = os.getenv('ZRD_HOOK_PATH', '')
    hook_port = int(os.getenv('ZRD_HOOK_PORT', 80))
