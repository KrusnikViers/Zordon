import dj_database_url
import os


# Required environment variables.
telegram_token = os.environ['TELEGRAM_TOKEN']
database_credentials = dj_database_url.parse(os.environ['DATABASE_URL'])
superuser_login = os.environ['SUPERUSER_LOGIN']

# Optional environment variables.
cooldown_time_minutes = os.getenv('COOLDOWN_TIME', 120)

commands_by_level = [
    {
        'u_status',      # Get user status and default keyboard
        'u_activate',    # Turn summon notifications on
        'u_deactivate',  # Turn summon notifications off
        'u_cancel',      # Cancel current action
        'u_report',      # Send message to superuser

        'a_list',  # List all available activities

        's_new',     # Subscribe to activity
        's_delete',  # Unsubscribe from activity

        'p_accept',        # Accept summon call
        'p_accept_later',  # Accept summon with notification about being late
        'p_decline',       # Decline summon call
    },
    {
        'a_new',     # Create new activity
        'a_delete',  # Delete activity
        'p_summon',  # Summon users for activity
    }
]

commands_for_superuser = {
    'su_promote',           # Increase user rights level
    'su_demote',            # Decrease user rights level
    'su_full_information',  # Get all information from DB
}

commands_set = commands_for_superuser
for commands_on_level in commands_by_level:
    commands_set = commands_set.union(commands_on_level)

pending_user_actions = {
    'none': 0,
    'a_new': 1,
    'u_report': 2,
}
