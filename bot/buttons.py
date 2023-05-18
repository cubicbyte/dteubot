import os
from datetime import date, timedelta
from telegram.ext import CallbackQueryHandler
from telegram import Update
from telegram.ext import CallbackContext
from bot import pages, utils
from settings import api, langs, API_TYPE, API_TYPE_DEFAULT

handlers = list[CallbackQueryHandler]()


def register_button_handler(pattern=None, block=None):
    def decorator(func):
        handlers.append(CallbackQueryHandler(callback=func, pattern=pattern, block=block))
        return func

    return decorator


def validate_admin(func):
    async def wrapper(update, context):
        if not context._user_data.get('admin'):
            if not update.callback_query:
                return
            await update.callback_query.answer(
                text=context._chat_data.get_lang()['alert.no_permissions'],
                show_alert=True)
            return
        return await func(update, context)

    return wrapper



@register_button_handler('^admin.clear_all_cache$')
@validate_admin
async def clear_all_cache(upd: Update, ctx: CallbackContext):
    if API_TYPE == API_TYPE_DEFAULT:
        api._session.remove_expired_responses(expire_after=1)
    await upd.callback_query.answer(
        text=ctx._chat_data.get_lang()['alert.done'],
        show_alert=True
    )


@register_button_handler('^admin.clear_expired_cache$')
@validate_admin
async def clear_expired_cache(upd: Update, ctx: CallbackContext):
    if API_TYPE == API_TYPE_DEFAULT:
        api._session.remove_expired_responses()
    await upd.callback_query.answer(
        text=ctx._chat_data.get_lang()['alert.done'],
        show_alert=True
    )


@register_button_handler('^admin.clear_logs$')
@validate_admin
async def clear_logs(upd: Update, ctx: CallbackContext):
    # Clear logs file
    open(os.path.join(os.getenv('LOGS_PATH'), 'debug.log'), 'w').close()

    await upd.callback_query.answer(
        text=ctx._chat_data.get_lang()['alert.done'],
        show_alert=True
    )


@register_button_handler('^admin.get_logs$')
@validate_admin
async def get_logs(upd: Update, ctx: CallbackContext):
    # Show user that bot is sending file
    await ctx.bot.send_chat_action(upd.callback_query.message.chat.id, 'upload_document')

    # Read and send logs file
    filepath = os.path.join(os.getenv('LOGS_PATH'), 'debug.log')
    with open(filepath, 'rb') as file:
        await ctx.bot.send_document(upd.callback_query.message.chat.id, file)


@register_button_handler('^admin.open_panel$')
@validate_admin
async def open_admin_panel(upd: Update, ctx: CallbackContext):
    msg = await upd.callback_query.edit_message_text(**pages.admin_panel(ctx))
    ctx._chat_data.save_message('admin_panel', msg)


@register_button_handler('^close_page$')
async def close_page(upd: Update, ctx: CallbackContext):
    await upd.callback_query.delete_message()
    ctx._chat_data.remove_message(upd.callback_query.message.message_id)


@register_button_handler('^open.calls$')
async def open_calls(upd: Update, ctx: CallbackContext):
    msg = await upd.callback_query.edit_message_text(**pages.calls(ctx))
    ctx._chat_data.save_message('calls', msg)


@register_button_handler('^open.info$')
async def open_info(upd: Update, ctx: CallbackContext):
    msg = await upd.callback_query.edit_message_text(**pages.info(ctx))
    ctx._chat_data.save_message('info', msg)


@register_button_handler('^open.left$')
async def open_left(upd: Update, ctx: CallbackContext):
    msg = await upd.callback_query.edit_message_text(**pages.left(ctx))
    ctx._chat_data.save_message('left', msg)


@register_button_handler('^open.menu$')
async def open_menu(upd: Update, ctx: CallbackContext):
    msg = await upd.callback_query.edit_message_text(**pages.menu(ctx))
    ctx._chat_data.save_message('menu', msg)


@register_button_handler('^open.more$')
async def open_more(upd: Update, ctx: CallbackContext):
    msg = await upd.callback_query.edit_message_text(**pages.more(ctx))
    ctx._chat_data.save_message('more', msg)


@register_button_handler('^open.schedule.day')
async def open_schedule(upd: Update, ctx: CallbackContext):
    date = utils.parse_callback_query(upd.callback_query.data)['args']['date']
    msg = await upd.callback_query.edit_message_text(
        **pages.schedule(ctx, date=date))
    ctx._chat_data.save_message('schedule', msg)


@register_button_handler('^open.schedule.today$')
async def open_today(upd: Update, ctx: CallbackContext):
    # Send message
    _date = date.today()
    msg = await upd.callback_query.edit_message_text(
        **pages.schedule(ctx, date=_date))

    # Save message to database
    data = {'date': _date.strftime('%Y-%m-%d')}
    ctx._chat_data.save_message('schedule', msg, data)


@register_button_handler('^open.schedule.tomorrow$')
async def open_tomorrow(upd: Update, ctx: CallbackContext):
    # Send message
    _date = date.today() + timedelta(days=1)
    msg = await upd.callback_query.edit_message_text(
        **pages.schedule(ctx, date=_date))

    # Save message to database
    data = {'date': _date.strftime('%Y-%m-%d')}
    ctx._chat_data.save_message('schedule', msg, data)


@register_button_handler('^open.select_group$')
async def open_group_selection(upd: Update, ctx: CallbackContext):
    msg = await upd.callback_query.edit_message_text(
        **pages.structure_list(ctx))
    ctx._chat_data.save_message('structure_list', msg)


@register_button_handler('^open.select_lang$')
async def open_lang_selection(upd: Update, ctx: CallbackContext):
    msg = await upd.callback_query.edit_message_text(
        **pages.lang_selection(ctx))
    ctx._chat_data.save_message('lang_selection', msg)


@register_button_handler('^open.settings$')
async def open_settings(upd: Update, ctx: CallbackContext):
    msg = await upd.callback_query.edit_message_text(
        **pages.settings(ctx))
    ctx._chat_data.save_message('settings', msg)


@register_button_handler('^select.lang')
async def select_lang(upd: Update, ctx: CallbackContext):
    lang_code = utils.parse_callback_query(upd.callback_query.data)['args']['lang']

    if not lang_code in langs:
        lang_code = os.getenv('DEFAULT_LANG')

    # Open menu if user selected the same language
    if lang_code == ctx._chat_data.get('lang_code'):
        msg = await upd.callback_query.edit_message_text(
            **pages.menu(ctx))
        ctx._chat_data.save_message('menu', msg)
        return

    # Update language and refresh page
    ctx._chat_data.set('lang_code', lang_code)
    msg = await upd.callback_query.edit_message_text(
        **pages.lang_selection(ctx))
    ctx._chat_data.save_message('lang_selection', msg)


@register_button_handler('^select.schedule.structure')
async def select_structure(upd: Update, ctx: CallbackContext):
    args = utils.parse_callback_query(upd.callback_query.data)['args']

    structure_id = int(args['structureId'])

    # Send message
    msg = await upd.callback_query.edit_message_text(
        **pages.faculty_list(ctx, structure_id))

    # Save message to database
    data = {'structureId': structure_id}
    ctx._chat_data.save_message('faculty_list', msg, data)


@register_button_handler('^select.schedule.faculty')
async def select_faculty(upd: Update, ctx: CallbackContext):
    args = utils.parse_callback_query(upd.callback_query.data)['args']

    structure_id = int(args['structureId'])
    faculty_id = int(args['facultyId'])

    # Send message
    msg = await upd.callback_query.edit_message_text(
        **pages.course_list(ctx, structure_id, faculty_id))

    # Save message to database
    data = {'structureId': structure_id, 'facultyId': faculty_id}
    ctx._chat_data.save_message('course_list', msg, data)


@register_button_handler('^select.schedule.course')
async def select_course(upd: Update, ctx: CallbackContext):
    args = utils.parse_callback_query(upd.callback_query.data)['args']

    structure_id = int(args['structureId'])
    faculty_id = int(args['facultyId'])
    course = int(args['course'])

    # Send message
    msg = await upd.callback_query.edit_message_text(
        **pages.group_list(ctx, structure_id, faculty_id, course))

    # Save message to database
    data = {'structureId': structure_id,
            'facultyId': faculty_id, 'course': course}
    ctx._chat_data.save_message('group_list', msg, data)


@register_button_handler('^select.schedule.group')
async def select_group(upd: Update, ctx: CallbackContext):
    args = utils.parse_callback_query(upd.callback_query.data)['args']

    group_id = int(args['groupId'])
    ctx._chat_data.set('group_id', group_id)

    # Send message
    msg = await upd.callback_query.edit_message_text(
        **pages.menu(ctx))

    # Save message to database
    ctx._chat_data.save_message('menu', msg)


@register_button_handler('^set.cl_notif_1m')
async def select_cl_notif_1m(upd: Update, ctx: CallbackContext):
    args = utils.parse_callback_query(upd.callback_query.data)['args']

    state = args.get('state') == '1'
    suggestion = args.get('suggestion') == '1'
    ctx._chat_data.set('cl_notif_1m', state)

    # Disable 15m notifications if needed
    if state:
        ctx._chat_data.set('cl_notif_15m', False)

    # Show tooltip if needed
    if suggestion:
        await upd.callback_query.answer(
            ctx._chat_data.get_lang()['alert.cl_notif_enabled_tooltip']
                .format(remaining='1'), show_alert=True)
        await upd.callback_query.delete_message()
        ctx._chat_data.remove_message(upd.callback_query.message.message_id)
        return

    # Send message
    msg = await upd.callback_query.edit_message_text(
        **pages.settings(ctx))
    ctx._chat_data.save_message('settings', msg)


@register_button_handler('^set.cl_notif_15m')
async def select_cl_notif_15m(upd: Update, ctx: CallbackContext):
    args = utils.parse_callback_query(upd.callback_query.data)['args']

    state = args.get('state') == '1'
    suggestion = args.get('suggestion') == '1'
    ctx._chat_data.set('cl_notif_15m', state)

    # Disable 1m notifications if needed
    if state:
        ctx._chat_data.set('cl_notif_1m', False)

    # Show tooltip if needed
    if suggestion:
        await upd.callback_query.answer(
            ctx._chat_data.get_lang()['alert.cl_notif_enabled_tooltip']
                .format(remaining='15'), show_alert=True)
        await upd.callback_query.delete_message()
        ctx._chat_data.remove_message(upd.callback_query.message.message_id)
        return

    # Send message
    msg = await upd.callback_query.edit_message_text(
        **pages.settings(ctx))
    ctx._chat_data.save_message('settings', msg)
