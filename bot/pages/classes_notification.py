from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.helpers import escape_markdown
from lib.api.schemas import TimeTableDate
from ..data import ChatData

def get_notification_schedule_section(day: TimeTableDate) -> str:
    f = '`{0})` *{1}*`[{2}]`\n'
    section = ''

    for l in day.lessons:
        for p in l.periods:
            section += f.format(l.number, escape_markdown(p.disciplineShortName, version=2), escape_markdown(p.typeStr, version=2))

    return section[:-1]

def create_message_15m(chat_data: ChatData, day: TimeTableDate) -> dict:
    buttons = [[
        InlineKeyboardButton(text=chat_data.get_lang()['button.close_page'], callback_data='close_page'),
        InlineKeyboardButton(text=chat_data.get_lang()['button.settings'], callback_data='open.settings')
    ]]

    return {
        'text': chat_data.get_lang()['page.classes_notification'].format(remaining='15', schedule=get_notification_schedule_section(day)),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }

def create_message_1m(chat_data: ChatData, day: TimeTableDate) -> dict:
    buttons = [[
        InlineKeyboardButton(text=chat_data.get_lang()['button.close_page'], callback_data='close_page'),
        InlineKeyboardButton(text=chat_data.get_lang()['button.settings'], callback_data='open.settings')
    ]]

    return {
        'text': chat_data.get_lang()['page.classes_notification'].format(remaining='1', schedule=get_notification_schedule_section(day)),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
