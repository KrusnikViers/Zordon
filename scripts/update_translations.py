from app.core.info import APP_DIR
from app.i18n.updater import TranslationsUpdater


updater = TranslationsUpdater(APP_DIR.joinpath('i18n'), APP_DIR)
updater.regenerate_all()
