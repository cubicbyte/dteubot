from telegram.ext import CommandHandler

handlers = list[CommandHandler]()


def register_command_handler(command, filters=None, block=None):
    def decorator(func):
        handlers.append(CommandHandler(command=command, callback=func, filters=filters, block=block))
        return func

    return decorator


# https://stackoverflow.com/questions/1057431/how-to-load-all-modules-in-a-folder
# Necessary to initialize the handlers
from os.path import dirname, basename, isfile, join
import glob

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
