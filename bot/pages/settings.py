from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown
from ..settings import api, API_TYPE, API_TYPE_CACHED

def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    lang = context._chat_data.get_lang()
    cl_notif_15m = context._chat_data.cl_notif_15m
    cl_notif_1m = context._chat_data.cl_notif_1m

    if context._chat_data.group_id is not None:
        if API_TYPE == API_TYPE_CACHED:
            group = escape_markdown(api._cache.get_group(context._chat_data.group_id)[2], version=2)
        else:
            group = context._chat_data.group_id
    else:
        group = lang['text.not_selected']

    buttons = [[
        InlineKeyboardButton(text=lang['button.select_group'], callback_data='open.select_group'),
        InlineKeyboardButton(text=lang['button.select_lang'], callback_data='open.select_lang')
    ], [
        InlineKeyboardButton(text=lang['button.settings.cl_notif_15m'], callback_data=f'set.cl_notif_15m#state={int(not cl_notif_15m)}')
    ], [
        InlineKeyboardButton(text=lang['button.settings.cl_notif_1m'], callback_data=f'set.cl_notif_1m#state={int(not cl_notif_1m)}')
    ], [
        InlineKeyboardButton(text=lang['button.back'], callback_data='open.menu')
    ]]

    def get_icon(setting: bool) -> str:
        return '✅' if setting else '❌'

    page_text = lang['page.settings'].format(
        group_id=group,
        cl_notif_15m=get_icon(cl_notif_15m),
        cl_notif_1m=get_icon(cl_notif_1m)
    )

    return {
        'text': page_text,
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
