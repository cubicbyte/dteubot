"""
This file contains all bot buttons handlers
"""

import os
import re
from datetime import date, timedelta
from telegram.ext import CallbackQueryHandler

from telegram import Update
from telegram.ext import CallbackContext

from bot import pages, utils
from bot.data import ContextManager
from settings import api, langs

handlers = list[CallbackQueryHandler]()


def register_button(pattern=None, block=None):
    """Register button handler"""

    def decorator(func):
        def wrapper(update: Update, context: CallbackContext):
            ctx = ContextManager(update, context)
            return func(ctx)

        handlers.append(CallbackQueryHandler(callback=wrapper, pattern=pattern, block=block))
        return wrapper

    return decorator


def validate_admin(func):
    """Validate user admin permissions"""

    async def wrapper(context):
        if not context.user_data.get('admin'):
            if not context.update.callback_query:
                return
            await context.update.callback_query.answer(
                text=context.lang.get('alert.no_permissions'),
                show_alert=True)
            return
        return await func(context)

    return wrapper


@register_button('^admin.clear_cache')
@validate_admin
async def clear_cache(ctx: ContextManager):
    """Clear all the API cache"""

    api.clear_cache()

    await ctx.update.callback_query.answer(
        text=ctx.lang.get('alert.done'),
        show_alert=True
    )


@register_button('^admin.clear_logs')
@validate_admin
async def clear_logs(ctx: ContextManager):
    """Clear bot logs"""

    # pylint: disable=consider-using-with
    open(os.path.join(os.getenv('LOGS_PATH'), 'debug.log'), 'w', encoding='utf-8').close()

    await ctx.update.callback_query.answer(
        text=ctx.lang.get('alert.done'),
        show_alert=True
    )


@register_button('^admin.get_logs')
@validate_admin
async def get_logs(ctx: ContextManager):
    """Send bot logs to user"""

    # Show user that bot is sending file
    await ctx.context.bot.send_chat_action(
        ctx.update.callback_query.message.chat.id, 'upload_document')

    # Read and send logs file
    filepath = os.path.join(os.getenv('LOGS_PATH'), 'debug.log')
    with open(filepath, 'rb') as file:
        await ctx.context.bot.send_document(ctx.update.callback_query.message.chat.id, file)


@register_button('^admin.open_panel')
@validate_admin
async def open_admin_panel(ctx: ContextManager):
    """Open admin panel"""
    msg = await ctx.update.callback_query.edit_message_text(**pages.admin_panel(ctx))
    ctx.chat_data.save_message('admin_panel', msg)


@register_button('^close_page')
async def close_page(ctx: ContextManager):
    """Delete page message"""
    await ctx.update.callback_query.delete_message()
    ctx.chat_data.remove_message(ctx.update.callback_query.message.message_id)


@register_button('^open.calls')
async def open_calls(ctx: ContextManager):
    """Open calls schedule"""
    msg = await ctx.update.callback_query.edit_message_text(
        **pages.calls(ctx, back_btn='open.more')
    )
    ctx.chat_data.save_message('calls', msg)


@register_button('^open.info')
async def open_info(ctx: ContextManager):
    """Open info page"""
    msg = await ctx.update.callback_query.edit_message_text(**pages.info(ctx))
    ctx.chat_data.save_message('info', msg)


@register_button('^open.left')
async def open_left(ctx: ContextManager):
    """Open page with time left to the start/end of the lesson"""
    msg = await ctx.update.callback_query.edit_message_text(
        **pages.left(ctx, back_btn='open.more'))
    ctx.chat_data.save_message('left', msg)


@register_button('^open.menu')
async def open_menu(ctx: ContextManager):
    """Open menu page"""
    msg = await ctx.update.callback_query.edit_message_text(**pages.menu(ctx))
    ctx.chat_data.save_message('menu', msg)


@register_button('^open.more')
async def open_more(ctx: ContextManager):
    """Open more page"""
    msg = await ctx.update.callback_query.edit_message_text(**pages.more(ctx))
    ctx.chat_data.save_message('more', msg)


@register_button('^open.schedule.day')
async def open_schedule(ctx: ContextManager):
    """Open schedule page"""

    _date = utils.parse_callback_query(ctx.update.callback_query.data)['args']['date']
    msg = await ctx.update.callback_query.edit_message_text(
        **pages.schedule(ctx, date=_date))
    ctx.chat_data.save_message('schedule', msg)


@register_button('^open.schedule.extra')
async def open_schedule_extra(ctx: ContextManager):
    """Open schedule extra info page"""

    # TODO: message can be longer than 4096 characters

    _date = utils.parse_callback_query(ctx.update.callback_query.data)['args']['date']
    msg = await ctx.update.callback_query.edit_message_text(
        **pages.schedule_extra(ctx, date=_date))
    ctx.chat_data.save_message('schedule_extra', msg)


@register_button('^open.schedule.today')
async def open_today(ctx: ContextManager):
    """Open schedule page for today"""

    # Send message
    _date = date.today()
    msg = await ctx.update.callback_query.edit_message_text(
        **pages.schedule(ctx, date=_date))

    # Save message to database
    data = {'date': _date.isoformat()}
    ctx.chat_data.save_message('schedule', msg, data)


@register_button('^open.schedule.tomorrow')
async def open_tomorrow(ctx: ContextManager):
    """Open schedule page for tomorrow"""

    # Send message
    _date = date.today() + timedelta(days=1)
    msg = await ctx.update.callback_query.edit_message_text(
        **pages.schedule(ctx, date=_date))

    # Save message to database
    data = {'date': _date.isoformat()}
    ctx.chat_data.save_message('schedule', msg, data)


@register_button('^open.select_group')
async def open_group_selection(ctx: ContextManager):
    """Open group selection menu"""

    msg = await ctx.update.callback_query.edit_message_text(
        **pages.structure_list(ctx))
    ctx.chat_data.save_message('structure_list', msg)


@register_button('^open.select_lang')
async def open_lang_selection(ctx: ContextManager):
    """Open language selection menu"""

    msg = await ctx.update.callback_query.edit_message_text(
        **pages.lang_selection(ctx))
    ctx.chat_data.save_message('lang_selection', msg)


@register_button('^open.settings')
async def open_settings(ctx: ContextManager):
    """Open settings menu"""

    msg = await ctx.update.callback_query.edit_message_text(
        **pages.settings(ctx))
    ctx.chat_data.save_message('settings', msg)


@register_button('^select.lang')
async def select_lang(ctx: ContextManager):
    """Select language"""

    lang_code = utils.parse_callback_query(ctx.update.callback_query.data)['args']['lang']

    if lang_code not in langs:
        lang_code = os.getenv('DEFAULT_LANG')

    # Open menu if user selected the same language
    if lang_code == ctx.chat_data.get('lang_code'):
        msg = await ctx.update.callback_query.edit_message_text(
            **pages.menu(ctx))
        ctx.chat_data.save_message('menu', msg)
        return

    # Update language and refresh page
    ctx.chat_data.set('lang_code', lang_code)
    msg = await ctx.update.callback_query.edit_message_text(
        **pages.lang_selection(ctx))
    ctx.chat_data.save_message('lang_selection', msg)


@register_button('^select.schedule.structure')
async def select_structure(ctx: ContextManager):
    """Select structure"""

    args = utils.parse_callback_query(ctx.update.callback_query.data)['args']

    structure_id = int(args['structureId'])

    # Send message
    msg = await ctx.update.callback_query.edit_message_text(
        **pages.faculty_list(ctx, structure_id))

    # Save message to database
    data = {'structureId': structure_id}
    ctx.chat_data.save_message('faculty_list', msg, data)


@register_button('^select.schedule.faculty')
async def select_faculty(ctx: ContextManager):
    """Select faculty"""

    args = utils.parse_callback_query(ctx.update.callback_query.data)['args']

    structure_id = int(args['structureId'])
    faculty_id = int(args['facultyId'])

    # Send message
    msg = await ctx.update.callback_query.edit_message_text(
        **pages.course_list(ctx, structure_id, faculty_id))

    # Save message to database
    data = {'structureId': structure_id, 'facultyId': faculty_id}
    ctx.chat_data.save_message('course_list', msg, data)


@register_button('^select.schedule.course')
async def select_course(ctx: ContextManager):
    """Select course"""

    args = utils.parse_callback_query(ctx.update.callback_query.data)['args']

    structure_id = int(args['structureId'])
    faculty_id = int(args['facultyId'])
    course = int(args['course'])

    # Send message
    msg = await ctx.update.callback_query.edit_message_text(
        **pages.group_list(ctx, structure_id, faculty_id, course))

    # Save message to database
    data = {'structureId': structure_id,
            'facultyId': faculty_id, 'course': course}
    ctx.chat_data.save_message('group_list', msg, data)


@register_button('^select.schedule.group')
async def select_group(ctx: ContextManager):
    """Select group"""

    args = utils.parse_callback_query(ctx.update.callback_query.data)['args']

    group_id = int(args['groupId'])
    ctx.chat_data.set('group_id', group_id)

    # Send message
    msg = await ctx.update.callback_query.edit_message_text(
        **pages.menu(ctx))

    # Save message to database
    ctx.chat_data.save_message('menu', msg)


@register_button('^set.cl_notif')
async def select_cl_notif_1m(ctx: ContextManager):
    """Enable/disable 1m notifications"""

    args = utils.parse_callback_query(ctx.update.callback_query.data)['args']

    time = args.get('time')
    state = args.get('state')
    if time not in ('1m', '15m'):
        time = '15m'
        state = '0'

    # Disable other notification time if needed
    # if state == '1':
    #     if time == '1m':
    #         ctx.chat_data.set('cl_notif_15m', False)
    #     else:
    #         ctx.chat_data.set('cl_notif_1m', False)

    # Set notification time
    ctx.chat_data.set(f'cl_notif_{time}', state == '1')

    # Show tooltip if needed
    if args.get('suggestion') is not None:
        # Get numberical remaining time
        remaining = re.sub(r'\D', '', time)

        await ctx.update.callback_query.answer(
            ctx.lang.get('alert.cl_notif_enabled_tooltip')
                .format(remaining=remaining), show_alert=True)

        await ctx.update.callback_query.delete_message()
        ctx.chat_data.remove_message(ctx.update.callback_query.message.message_id)
        return

    # Send message
    msg = await ctx.update.callback_query.edit_message_text(
        **pages.settings(ctx))
    ctx.chat_data.save_message('settings', msg)


@register_button('^open.students_list')
async def open_students_list(ctx: ContextManager):
    """Open students list"""

    msg = await ctx.update.callback_query.edit_message_text(
        **pages.students_list(ctx))
    ctx.chat_data.save_message('students_list', msg)
