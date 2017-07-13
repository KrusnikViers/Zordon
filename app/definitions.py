import dj_database_url
import os


# Required environment variables.
telegram_token = os.environ['TELEGRAM_TOKEN']
database_credentials = dj_database_url.parse(os.environ['DATABASE_URL'])
superuser_login = os.environ['SUPERUSER_LOGIN']

# Optional environment variables.
cooldown_time_minutes = os.getenv('COOLDOWN_TIME', 120)

commands_set = {
    # User-related commands
    'u_status',
    'u_activate',
    'u_deactivate',
    'u_cancel',

    # Activity commands
    'a_list',
    'a_new',
    'a_delete',

    # Subscription commands
    's_new',
    's_delete',

    # Participation commands
    'p_summon',
    'p_accept_now',
    'p_accept_later',
    'p_decline',

    # Superuser commands
    'su_promote',
    'su_demote',
    'su_full_information',
}


pending_user_actions = {
    'none': 0,
    'a_new': 1,
}
