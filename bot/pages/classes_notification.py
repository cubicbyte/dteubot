from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.helpers import escape_markdown
from lib.api.schemas import TimeTableDate
from bot.data import ChatData


def get_notification_schedule_section(day: TimeTableDate) -> str:
    f = '`{0})` *{1}*`[{2}]`\n'
    section = ''

    for l in day.lessons:
        for p in l.periods:
            section += f.format(
                l.number,
                escape_markdown(p.disciplineShortName, version=2),
                escape_markdown(p.typeStr, version=2))

    return section[:-1]


def create_message(chat_data: ChatData, day: TimeTableDate, remaining: str) -> dict:
    buttons = [[
        InlineKeyboardButton(text=chat_data.get_lang()['button.open_schedule'],
                             callback_data=f'open.schedule.day#date={day.date}'),
        InlineKeyboardButton(text=chat_data.get_lang()['button.settings'],
                             callback_data='open.settings')
    ]]

    return {
        'text': chat_data.get_lang()['page.classes_notification'].format(
            remaining=remaining,
            schedule=get_notification_schedule_section(day)),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
