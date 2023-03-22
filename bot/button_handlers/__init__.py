from telegram.ext import CallbackQueryHandler
from ..pages import menu

handlers = list[CallbackQueryHandler]()
def register_button_handler(pattern = None, block = None):
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

# https://stackoverflow.com/questions/1057431/how-to-load-all-modules-in-a-folder
# Necessary to initialize the handlers
from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
