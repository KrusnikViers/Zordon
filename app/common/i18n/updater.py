from babel.messages import catalog, extract, mofile, pofile
import logging

from app.common import project_info

supported_languages = ['ru', 'en']
locale_dir = project_info.application_dir.joinpath('common', 'i18n')


def is_translations_compiled() -> bool:
    for lang in supported_languages:
        if not locale_dir.joinpath(lang, 'LC_MESSAGES', 'zordon.mo').is_file():
            return False
    return True


def regenerate_translations() -> bool:
    extracted = _extract_catalog_from_sources()
    # Update all supported languages .po and .mo files.
    without_errors = True
    for language in supported_languages:
        locale_dir.joinpath(language, 'LC_MESSAGES').mkdir(parents=True, exist_ok=True)
        translations, without_errors_lang = _update_existing_translations(language, extracted)
        without_errors = without_errors and without_errors_lang
        with open(str(locale_dir.joinpath(language, 'zordon.po')), 'wb') as file:
            pofile.write_po(file, translations, sort_output=True, width=None, omit_header=True)
            file.close()
        with open(str(locale_dir.joinpath(language, 'LC_MESSAGES', 'zordon.mo')), 'wb') as file:
            mofile.write_mo(file, translations)
            file.close()
    return without_errors


def _extract_catalog_from_sources() -> catalog.Catalog:
    # Extract translatable strings from project. It is a list of (filename, line_number, message, comments, context).
    translatable_strings_list = extract.extract_from_dir(dirname=str(project_info.application_dir))

    # Form dictionary of translatable strings, accumulating locations for each message.
    translatable_strings = {}
    for filename, line_num, msg, _, context in translatable_strings_list:
        if msg in translatable_strings:
            translatable_strings[msg].append((filename, line_num))
        else:
            translatable_strings[msg] = [(filename, line_num)]

    # Form babel catalog with extracted strings.
    translatable = catalog.Catalog()
    for msg, locations in translatable_strings.items():
        translatable.add(msg, locations=locations,)

    return translatable


def _update_existing_translations(language: str, extracted: catalog.Catalog) -> (catalog.Catalog, bool):
    try:
        with open(str(locale_dir.joinpath(language, 'zordon.po')), 'rb') as file:
            translations = pofile.read_po(file, locale=language, domain='zordon')
            file.close()
    except FileNotFoundError:
        translations = catalog.Catalog()

    # Validate translations
    translations.update(extracted)
    without_errors = True
    for msg in translations:
        if not msg.string:
            logging.error('Translation for {msg}({lang}) is missing!'. format(msg=msg.id, lang=language))
            without_errors = False
        elif msg.check():
            errors = ', '.join(map(str, msg.check()))
            logging.error('{msg}({lang}) has errors: {errors}'.format(msg=msg.id, lang=language, errors=errors))
            without_errors = False

    if translations.obsolete:
        logging.error('Obsolete lines found in {lang}: {lines}'.format(lang=language,
                                                                       lines=', '.join(translations.obsolete.keys())))

    translations.fuzzy = False
    return translations, without_errors
