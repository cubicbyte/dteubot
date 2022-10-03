import requests.exceptions

from datetime import datetime, timedelta
from telebot import types
from .get_schedule import get_schedule
from .load_langs import load_langs
from .get_remaining_time import get_remaining_time
from .get_structures.src.get_structures import get_structures
from .get_faculties.src.get_faculties import get_faculties
from .get_courses.src.get_courses import get_courses
from .get_groups.src.get_groups import get_groups

raise Exception('Calling create_message.py file')

langs = load_langs('langs')

def create_api_unavaliable_message(message):
    message_text = message.lang['text']['api_unavaliable']
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_menu'], callback_data='open.menu'),
        types.InlineKeyboardButton(text=message.lang['text']['button_write_me'], url='https://t.me/Bogdan4igg')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg

def create_invalid_group_message(message):
    message_text = message.lang['text']['group_incorrect']
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_select_group'], callback_data='open.select_group'),
        types.InlineKeyboardButton(text=message.lang['text']['button_more'], callback_data='open.more')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg

def create_info_message(message):
    message_text = message.lang['command']['info']
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_back'], callback_data='open.more'),
        types.InlineKeyboardButton(text=message.lang['text']['button_menu'], callback_data='open.menu')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg

def create_more_message(message):
    message_text = message.lang['command']['more']
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_info'], callback_data='open.info')
    )

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_back'], callback_data='open.menu')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg

def create_lang_select_message(message):
    markup = types.InlineKeyboardMarkup()

    if message.config['lang'] == None:
        chat_lang = message.lang['text']['not_selected']
    else:
        chat_lang = langs[message.config['lang']]['lang_name']

    message_text = message.lang['command']['lang_select'].format(lang=chat_lang)

    for lang in langs:
        markup.add(
            types.InlineKeyboardButton(text=langs[lang]['lang_name'], callback_data=f'select.lang={lang}')
        )

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_back'], callback_data='open.settings'),
        types.InlineKeyboardButton(text=message.lang['text']['button_menu'], callback_data='open.menu')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg

def create_menu_message(message):
    remaining_time = get_remaining_time(message, datetime.now())

    if remaining_time['to'] == None:
        left = message.lang['text']['subjects_missing_today']

    else:
        remaining = str(remaining_time['remaining'])

        if '.' in remaining:
            remaining = remaining[:remaining.index('.')]

        if remaining_time['to'] == 0:
            left = message.lang['text']['ring_left_start'].format(left=remaining)
        
        elif remaining_time['to'] == 1:
            left = message.lang['text']['ring_left_end'].format(left=remaining)

    message_text = message.lang['command']['menu'].format(left=left)
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_schedule_today'], callback_data='open.schedule.today'),
        types.InlineKeyboardButton(text=message.lang['text']['button_schedule_tomorrow'], callback_data='open.schedule.tomorrow')
    )

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_schedule_week'], callback_data='open.schedule.week'),
        types.InlineKeyboardButton(text=message.lang['text']['button_schedule_next_week'], callback_data='open.schedule.next_week')
    )

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_schedule_full'], callback_data='open.schedule.full')
    )

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_settings'], callback_data='open.settings'),
        types.InlineKeyboardButton(text=message.lang['text']['button_refresh'], callback_data='open.menu'),
        types.InlineKeyboardButton(text=message.lang['text']['button_more'], callback_data='open.more')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg

def create_select_structure_message(message):
    structures = get_structures()

    if not structures:
        return create_select_faculty_message(message)

    markup = types.InlineKeyboardMarkup()
    message_text = message.lang['command']['structure']

    for structure in structures:
        markup.add(
            types.InlineKeyboardButton(text=structures[structure], callback_data=f'select.schedule.structure_id={structure}')
        )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg

def create_select_faculty_message(message):
    markup = types.InlineKeyboardMarkup()
    message_text = message.lang['command']['faculty']
    faculties = get_faculties(message.config['schedule']['structure_id'])

    for faculty in faculties:
        markup.add(
            types.InlineKeyboardButton(text=faculties[faculty], callback_data=f'select.schedule.faculty_id={faculty}')
        )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg

def create_select_course_message(message):
    markup = types.InlineKeyboardMarkup()
    message_text = message.lang['command']['course']
    courses = get_courses(message.config['schedule']['faculty_id'], message.config['schedule']['structure_id'])

    for course in courses:
        markup.add(
            types.InlineKeyboardButton(text=courses[course], callback_data=f'select.schedule.course={course}')
        )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg

def create_select_group_message(message):
    markup = types.InlineKeyboardMarkup()
    message_text = message.lang['command']['group']
    groups = get_groups(message.config['schedule']['faculty_id'], message.config['schedule']['course'], message.config['schedule']['structure_id'])

    for group in groups:
        markup.add(
            types.InlineKeyboardButton(text=groups[group], callback_data=f'select.schedule.group_id={group}')
        )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg

def create_settings_message(message):
    structure_id = message.config['schedule']['structure_id'] or '?'
    faculty_id = message.config['schedule']['faculty_id'] or '?'
    course = message.config['schedule']['course'] or '?'
    group_id = message.config['schedule']['group_id'] or '?'

    structures = get_structures()

    if not structures:
        structure_id = ''
    else:
        structure_id += '-'

    group = f'{structure_id}{faculty_id}-{course}-{group_id}'

    markup = types.InlineKeyboardMarkup()
    message_text = message.lang['command']['settings'].format(group=group)

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_select_lang'], callback_data='open.select_lang'),
        types.InlineKeyboardButton(text=message.lang['text']['button_select_group'], callback_data='open.select_group')
    )

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_back'], callback_data='open.menu')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg

def create_schedule_message(message, date: datetime | str):
    if isinstance(date, datetime):
        date_str = date.strftime('%d.%m.%Y')
    else:
        date_str = date
        date = datetime.strptime(date, '%d.%m.%Y')

    try:
        schedule_cache = get_schedule(message)
    except requests.exceptions.HTTPError:
        return create_invalid_group_message(message)
    except requests.exceptions.ConnectionError:
        return create_api_unavaliable_message(message)

    received = schedule_cache['received']
    schedule_text = ''
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_day_previous'], callback_data='open.schedule.day=' + (date - timedelta(days=1)).strftime('%d.%m.%Y')),
        types.InlineKeyboardButton(text=message.lang['text']['button_menu'], callback_data='open.menu'),
        types.InlineKeyboardButton(text=message.lang['text']['button_day_next'], callback_data='open.schedule.day=' + (date + timedelta(days=1)).strftime('%d.%m.%Y'))
    )

    if not date_str in schedule_cache['schedule']:
        received = message.lang['text']['just_now']
        schedule_text += message.lang['text']['no_info']
        day_name = '?'

    else:
        schedule = schedule_cache['schedule'][date_str]
        day_name = schedule['day']
        lessons = []

        for lesson in schedule['lessons']:
            lesson_name = lesson['content']['name'].replace('`', '\'')
            lesson_type = lesson['content']['type'].replace('`', '\'')
            lesson_audience = lesson['content']['audience'].replace('`', '\'')
            lesson_lecturer = lesson['content']['lecturer'].replace('`', '\'')
            lesson_number = lesson['lesson'][:lesson['lesson'].index(' ')].replace('`', '\'')

            lesson_str = '`  `*{0}*`{1}`\n`{2} `{3}\n`  `{4}'.format(lesson_name, lesson_type, lesson_number, lesson_audience, lesson_lecturer)

            lessons.append(lesson_str)

        schedule_text += '`—————————————————————————`\n'
        schedule_text += '\n`—————————————————————————`\n'.join(lessons)
        schedule_text += '\n`—————————————————————————`'

    msg = {
        'chat_id': message.chat.id,
        'text': message.lang['command']['schedule'].format(date=date_str + ' - ' + day_name, schedule=schedule_text, received=received),
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg