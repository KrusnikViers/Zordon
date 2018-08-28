from babel.messages import catalog, extract, mofile, pofile
import logging
from pathlib import Path

from app.core import config

SUPPORTED_LANGUAGES = ['ru', 'en']
LOCALE_DIR = config.APP_DIRECTORY.joinpath('i18n')


def is_translations_generated() -> bool:
    for lang in SUPPORTED_LANGUAGES:
        if not LOCALE_DIR.joinpath(lang, 'LC_MESSAGES', 'zordon.mo').is_file():
            return False
    return True


def regenerate_translations() -> bool:
    new_strings_catalog = _build_strings_catalog_from_sources()
    is_translations_complete = True
    for language in SUPPORTED_LANGUAGES:
        LOCALE_DIR.joinpath(language, 'LC_MESSAGES').mkdir(parents=True, exist_ok=True)
        current_catalog = _get_updated_existing_translations(language, new_strings_catalog)
        is_translations_complete = is_translations_complete and _is_translations_valid(current_catalog, language)
        with LOCALE_DIR.joinpath(language, 'zordon.po').open(mode='wb') as file:
            pofile.write_po(file, current_catalog, sort_output=True, width=None, omit_header=True)
        with LOCALE_DIR.joinpath(language, 'LC_MESSAGES', 'zordon.mo').open(mode='wb') as file:
            mofile.write_mo(file, current_catalog)
    return is_translations_complete


def _build_strings_catalog_from_sources() -> catalog.Catalog:
    strings_dict = _get_translatable_strings()
    result = catalog.Catalog()
    for msg, locations in strings_dict.items():
        result.add(msg, locations=locations,)
    return result


def _get_translatable_strings() -> dict:
    strings_list = extract.extract_from_dir(dirname=str(config.APP_DIRECTORY))
    strings_dict = {}
    for filename, line_num, msg, _, context in strings_list:
        if msg in strings_dict:
            strings_dict[msg].append((filename, line_num))
        else:
            strings_dict[msg] = [(filename, line_num)]
    return strings_dict


def _get_updated_existing_translations(language: str, new_strings_catalog: catalog.Catalog) -> catalog.Catalog:
    current_catalog = _read_existing_translations_for_language(language)
    current_catalog.update(new_strings_catalog)
    if current_catalog.obsolete:
        obsolete_lines = ', '.join(current_catalog.obsolete.keys())
        logging.error('Obsolete lines found in {lang}: {lines}'.format(lang=language, lines=obsolete_lines))
    catalog.fuzzy = False
    return current_catalog


def _read_existing_translations_for_language(language: str) -> catalog.Catalog:
    file_path = Path(str(LOCALE_DIR.joinpath(language, 'zordon.po')))
    if file_path.is_file():
        with file_path.open(mode='rb') as file:
            return pofile.read_po(file, locale=language, domain='zordon')
    return catalog.Catalog()


def _is_translations_valid(strings_catalog: catalog.Catalog, language: str) -> bool:
    is_translations_valid = True
    for msg in strings_catalog:
        if not msg.string:
            logging.error('Translation for {msg}({lang}) is missing!'.format(msg=msg.id, lang=language))
            is_translations_valid = False
        elif msg.check():
            errors = ', '.join(map(str, msg.check()))
            logging.error('{msg}({lang}): {errors}'.format(msg=msg.id, lang=language, errors=errors))
            is_translations_valid = False
    return is_translations_valid
