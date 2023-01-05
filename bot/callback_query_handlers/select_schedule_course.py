import telebot.types
import logging
from ..settings import bot, chat_configs
from ..pages import select_group

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'select.schedule.course')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling callback query')
    structureId = int(call.args['structureId'])
    facultyId = int(call.args['facultyId'])
    course = int(call.args['course'])
    chat_configs.set_chat_config(call.message.chat.id, call.message.config)
    bot.edit_message_text(**select_group.create_message(call.message, structureId, facultyId, course), message_id=call.message.id)
