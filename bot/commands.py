import os
from datetime import date as _date
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot import pages
from bot.data import ContextManager
from settings import langs

handlers = list[CommandHandler]()


def register_command(command, filters=None, block=None):
    def decorator(func):
        def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            ctx = ContextManager(update, context)
            return func(ctx)

        handlers.append(CommandHandler(command=command, callback=wrapper, filters=filters, block=block))
        return wrapper

    return decorator


@register_command('calls')
async def calls(ctx: ContextManager):
    msg = await ctx.update.message.chat.send_message(
        **pages.calls(ctx))
    ctx.chat_data.save_message('calls', msg)


@register_command(['empty_1', 'empty_2'])
async def empty(ctx: ContextManager):
    msg = await ctx.update.message.chat.send_message(
        **pages.statistic(ctx))
    ctx.chat_data.save_message('statistic', msg)


@register_command('lang')
async def lang(ctx: ContextManager):
    # /lang
    if len(ctx.args) == 0:
        msg = await ctx.update.message.chat.send_message(
            **pages.lang_selection(ctx))
        ctx.chat_data.save_message('lang_selection', msg)
        return

    # /lang <lang_code>
    lang_code = ctx.args[0].lower()

    if not lang_code in langs:
        lang_code = os.getenv('DEFAULT_LANG')

    ctx.chat_data.set('lang_code', lang_code)

    msg = await ctx.update.message.chat.send_message(
        **pages.menu(ctx))
    ctx.chat_data.save_message('menu', msg)


@register_command('left')
async def left(ctx: ContextManager):
    msg = await ctx.update.message.chat.send_message(
        **pages.left(ctx))
    ctx.chat_data.save_message('left', msg)


@register_command('menu')
async def menu(ctx: ContextManager):
    msg = await ctx.update.message.chat.send_message(
        **pages.menu(ctx))
    ctx.chat_data.save_message('menu', msg)


@register_command('select')
async def select(ctx: ContextManager):
    # /select
    if len(ctx.context.args) == 0:
        msg = await ctx.update.message.chat.send_message(
            **pages.structure_list(ctx))
        ctx.chat_data.save_message('structure_list', msg)
        return

    # /select <group_id>
    group_id = ctx.context.args[0]

    # Check if group_id is number
    if group_id.isnumeric():
        group_id = int(group_id)
        ctx.chat_data.set('group_id', group_id)
    else:
        # TODO: send error message
        pass

    msg = await ctx.update.message.chat.send_message(
        **pages.menu(ctx))
    ctx.chat_data.save_message('menu', msg)


@register_command('settings')
async def settings(ctx: ContextManager):
    msg = await ctx.update.message.chat.send_message(
        **pages.settings(ctx))
    ctx.chat_data.save_message('settings', msg)


@register_command('start')
async def start(ctx: ContextManager):
    # Get referral code
    if len(ctx.context.args) == 0:
        ref = None
    else:
        ref = ctx.context.args[0]

    # Set referral code
    if ctx.user_data.get('ref') is None:
        ctx.user_data.set('ref', ref)

    # Send greeting message
    msg = await ctx.update.message.chat.send_message(
        **pages.greeting(ctx))
    ctx.chat_data.save_message('greeting', msg)

    # Send main message
    msg = await ctx.update.message.chat.send_message(
        **pages.structure_list(ctx))
    ctx.chat_data.save_message('structure_list', msg)


@register_command('today')
async def today(ctx: ContextManager):
    # Send message
    date = _date.today()
    msg = await ctx.update.message.chat.send_message(
        **pages.schedule(ctx, date))

    # Save message
    data = {'date': date.isoformat()}
    ctx.chat_data.save_message('schedule', msg, data)


@register_command('tomorrow')
async def tomorrow(ctx: ContextManager):
    # Send message
    date = _date.today() + pages.timedelta(days=1)
    msg = await ctx.update.message.chat.send_message(
        **pages.schedule(ctx, date))

    # Save message
    data = {'date': date.isoformat()}
    ctx.chat_data.save_message('schedule', msg, data)
