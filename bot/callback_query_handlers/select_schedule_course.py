import telebot.types
import logging
from ..settings import bot, chat_configs
from ..messages import create_select_group_message

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'select.schedule.course')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling callback query')
    structureId = int(call.args['structureId'])
    facultyId = int(call.args['facultyId'])
    course = int(call.args['course']) + 9
    chat_configs.set_chat_config(call.message.chat.id, call.message.config)
    bot.edit_message_text(**create_select_group_message(call.message, structureId, facultyId, course), message_id=call.message.id)
