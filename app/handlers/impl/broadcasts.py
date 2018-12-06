from telegram import TelegramError

from app.handlers import actions
from app.handlers.context import Context
from app.handlers.inline_menu import InlineMenu
from app.models.all import Request, Response


def on_all_request(context: Context):
    users_list = [user for user in context.group.users if user != context.sender]
    if not users_list:
        context.send_response_message(_('no_users_for_broadcast_message'))
        return
    user_message = context.command_arguments()
    if user_message:
        message = user_message + '\n' + _('all_with_text_from_{user}').format(user=context.sender.name)
    else:
        message = _('all_from_{user}').format(user=context.sender.name)
    message += '\n\n' + \
               ', '.join([user.login_if_exists() for user in users_list])
    context.send_response_message(message)


_RECALL_DECLINED = 0
_RECALL_ACCEPTED = 1
_MESSAGE_UNDEFINED = -777


def _markup_for_call():
    return InlineMenu([[(_('recall_join'), [actions.Callback.RECALL_JOIN]),
                        (_('recall_decline'), [actions.Callback.RECALL_DECLINE])]])


def _get_users_for_recall(context: Context, request: Request) -> ([], [], []):
    joined = []
    declined = []
    for response in request.responses:
        if response.answer == _RECALL_ACCEPTED:
            joined.append(response.user)
        elif response.answer == _RECALL_DECLINED:
            declined.append(response.user)
    rest = [user for user in context.group.users if
            user != request.author and user not in joined and user not in declined]
    return joined, declined, rest


def _message_for_recall(context: Context, request: Request):
    joined, declined, rest = _get_users_for_recall(context, request)
    message = request.title + '\n'
    if joined:
        message += '\n' + _('recall_joined_{users}').format(users=', '.join([user.login_if_exists() for user in joined]))
    if declined:
        message += '\n' + _('recall_declined_{users}').format(
            users=', '.join([user.login_if_exists() for user in declined]))
    if rest:
        message += '\n' + _('recall_not_answered_{users}').format(
            users=', '.join([user.login_if_exists() for user in rest]))
    return message


def on_recall_request(context: Context):
    available_users = [user for user in context.group.users if user != context.sender]
    if not available_users:
        context.send_response_message(_('no_users_for_broadcast_message'))
        return
    user_message = context.command_arguments()
    if user_message:
        title = user_message + '\n' + _('recall_with_text_from_{user}').format(user=context.sender.name)
    else:
        title = _('recall_from_{user}').format(user=context.sender.name)
    request = Request(message_id=_MESSAGE_UNDEFINED,
                      chat_id=context.update.effective_chat.id,
                      author=context.sender,
                      title=title)
    context.session.add(request)
    request_message = context.send_response_message(_message_for_recall(context, request),
                                                    reply_markup=_markup_for_call())
    request.message_id = request_message.message_id


def _try_update_message(context: Context, request: Request):
    try:
        context.update.callback_query.edit_message_text(text=_message_for_recall(context, request),
                                                        reply_markup=_markup_for_call())
    except TelegramError:
        context.send_response_message(_('invalid_request_{user}').format(user=context.sender.name))


def _on_recall_response(context: Context, answer: int):
    request = context.session.query(Request).filter(
        Request.message_id == context.update.callback_query.message.message_id).first()
    if request and context.sender != request.author:
        response = context.session.query(Response).filter(Response.user == context.sender,
                                                          Response.request == request).first()
        if response:
            response.answer = answer
        else:
            response = Response(request=request, user=context.sender, answer=answer)
            context.session.add(response)
    _try_update_message(context, request)


def on_recall_join(context: Context):
    _on_recall_response(context, _RECALL_ACCEPTED)


def on_recall_decline(context: Context):
    _on_recall_response(context, _RECALL_DECLINED)
