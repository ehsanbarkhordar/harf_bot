import asyncio

from balebot.filters import DefaultFilter, TemplateResponseFilter, TextFilter
from balebot.handlers import MessageHandler, CommandHandler
from balebot.models.messages import TextMessage, TemplateMessageButton, TemplateMessage
from balebot.updater import Updater
from balebot.utils.logger import Logger

from constant.message import LogMessage, ReadyMessage, TMessage
from main_config import Config

updater = Updater(token=Config.bot_token, loop=asyncio.get_event_loop())
dispatcher = updater.dispatcher
my_logger = Logger.get_logger()


# =================================== Call Backs =======================================================
def success_send_message(response, user_data):
    kwargs = user_data['kwargs']
    update = kwargs["update"]
    user_peer = update.get_effective_user()
    my_logger.info(LogMessage.success_send_message, extra={"user_id": user_peer.peer_id, "tag": "info"})


def failure_send_message(response, user_data):
    kwargs = user_data['kwargs']
    bot = kwargs["bot"]
    message = kwargs["message"]
    update = kwargs["update"]
    try_times = int(kwargs["try_times"])
    if try_times < Config.max_total_send_failure:
        try_times += 1
        user_peer = update.get_effective_user()
        my_logger.error(LogMessage.fail_send_message, extra={"user_id": user_peer.peer_id, "tag": "error"})
        kwargs = {"message": message, "update": update, "bot": bot, "try_times": try_times}
        bot.respond(update=update, message=message, success_callback=success_send_message,
                    failure_callback=failure_send_message, kwargs=kwargs)
    else:
        my_logger.error(LogMessage.max_fail_retried, extra={"tag": "error"})


def success_send_message_and_start_again(response, user_data):
    kwargs = user_data['kwargs']
    update = kwargs["update"]
    bot = kwargs["bot"]
    user_peer = update.get_effective_user()
    my_logger.info(LogMessage.success_send_message, extra={"user_id": user_peer.peer_id, "tag": "info"})
    start_conversation(bot, update)


def is_admin(user_id):
    user_id = str(user_id)
    for admin_user_id in Config.admin_user_id_list:
        if user_id == admin_user_id:
            return True
    return False


# =================================== Start Conversation ===========================================
@dispatcher.message_handler(filters=[DefaultFilter()])
def start_conversation(bot, update):
    user_peer = update.get_effective_user()
    text_message = TextMessage(ReadyMessage.initiate)
    kwargs = {"message": text_message, "update": update, "bot": bot, "try_times": 1}
    bot.send_message(text_message, user_peer, success_callback=success_send_message,
                     failure_callback=success_send_message, kwargs=kwargs)
    dispatcher.register_conversation_next_step_handler(
        update, common_handlers + [
            MessageHandler(TemplateResponseFilter(keywords=TMessage.show_statements), request_permission)])


# =================================== help =======================================================
@dispatcher.message_handler(filters=[TemplateResponseFilter(keywords=[TMessage.help]), TextFilter(keywords="help")])
def help_me(bot, update):
    user_peer = update.get_effective_user()
    btn_list = [TemplateMessageButton(text=TMessage.back, value=TMessage.back, action=0)]
    general_message = TextMessage(ReadyMessage.help)
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    kwargs = {"message": template_message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(template_message, user_peer, success_callback=success_send_message,
                     failure_callback=failure_send_message, kwargs=kwargs)
    dispatcher.finish_conversation(update)


common_handlers = [
    CommandHandler(commands="/start", callback=start_conversation, include_template_response=True),
    CommandHandler(commands="/help", callback=help_me, include_template_response=True),
    MessageHandler(TemplateResponseFilter(keywords=[TMessage.help]), help_me)]

updater.run()
