import os
from datetime import date as _date
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot import pages
from settings import langs

handlers = list[CommandHandler]()


def register_command_handler(command, filters=None, block=None):
    def decorator(func):
        handlers.append(CommandHandler(command=command, callback=func, filters=filters, block=block))
        return func

    return decorator


@register_command_handler('calls')
async def calls(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = await upd.message.chat.send_message(
        **pages.calls(ctx))
    ctx._chat_data.save_message('calls', msg)


@register_command_handler(['empty_1', 'empty_2'])
async def empty(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = await upd.message.chat.send_message(
        **pages.statistic(upd, ctx))
    ctx._chat_data.save_message('statistic', msg)


@register_command_handler('lang')
async def lang(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # /lang
    if len(ctx.args) == 0:
        msg = await upd.message.chat.send_message(
            **pages.lang_selection(ctx))
        ctx._chat_data.save_message('lang_selection', msg)
        return

    # /lang <lang_code>
    lang_code = ctx.args[0].lower()

    if not lang_code in langs:
        lang_code = os.getenv('DEFAULT_LANG')

    ctx._chat_data.set('lang_code', lang_code)

    msg = await upd.message.chat.send_message(
        **pages.menu(ctx))
    ctx._chat_data.save_message('menu', msg)


@register_command_handler('left')
async def left(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = await upd.message.chat.send_message(
        **pages.left(ctx))
    ctx._chat_data.save_message('left', msg)


@register_command_handler('menu')
async def menu(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = await upd.message.chat.send_message(
        **pages.menu(ctx))
    ctx._chat_data.save_message('menu', msg)


@register_command_handler('select')
async def select(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # /select
    if len(ctx.args) == 0:
        msg = await upd.message.chat.send_message(
            **pages.structure_list(ctx))
        ctx._chat_data.save_message('structure_list', msg)
        return

    # /select <group_id>
    group_id = ctx.args[0]

    # Check if group_id is number
    if group_id.isnumeric():
        group_id = int(group_id)
        ctx._chat_data.set('group_id', group_id)
    else:
        # TODO: send error message
        pass

    msg = await upd.message.chat.send_message(
        **pages.menu(ctx))
    ctx._chat_data.save_message('menu', msg)


@register_command_handler('settings')
async def settings(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = await upd.message.chat.send_message(
        **pages.settings(ctx))
    ctx._chat_data.save_message('settings', msg)


@register_command_handler('start')
async def start(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # Get referral code
    if len(ctx.args) == 0:
        ref = None
    else:
        ref = ctx.args[0]

    # Set referral code
    if ctx._user_data.get('ref') is None:
        ctx._user_data.set('ref', ref)

    # Send greeting message
    msg = await upd.message.chat.send_message(
        **pages.greeting(ctx))
    ctx._chat_data.save_message('greeting', msg)

    # Send main message
    msg = await upd.message.chat.send_message(
        **pages.structure_list(ctx))
    ctx._chat_data.save_message('structure_list', msg)


@register_command_handler('today')
async def today(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # Send message
    date = _date.today()
    msg = await upd.message.chat.send_message(
        **pages.schedule(ctx, date))

    # Save message
    data = {'date': date.strftime('%Y-%m-%d')}
    ctx._chat_data.save_message('schedule', msg, data)


@register_command_handler('tomorrow')
async def tomorrow(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # Send message
    date = _date.today() + pages.timedelta(days=1)
    msg = await upd.message.chat.send_message(
        **pages.schedule(ctx, date))

    # Save message
    data = {'date': date.strftime('%Y-%m-%d')}
    ctx._chat_data.save_message('schedule', msg, data)
