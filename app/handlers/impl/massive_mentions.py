from telegram import TelegramError

from app.handlers.context import Context
from app.handlers.inline_menu import InlineMenu
from app.models.all import Response, Request


def on_all_request(context: Context):
    users_list_str = ', '.join([user.login for user in context.group.users if user != context.sender])
    message = _('all_from_{user}').format(user=context.sender.name) + \
              '\n\n' + \
              users_list_str
    context.send_response_message(message)


_CALL_DECLINED = 0
_CALL_ACCEPTED = 1


def _message_for_call(context: Context, request: Request):
    joined = []
    declined = []
    for response in request.responses:
        if response.answer == _CALL_ACCEPTED:
            joined.append(response.user)
        elif response.answer == _CALL_DECLINED:
            declined.append(response.user)
    rest = [user for user in context.group.users if
            user != request.author and user not in joined and user not in declined]
    if not rest and not joined and not declined:
        return None
    message = request.title + '\n'
    if joined:
        message += '\n' + _('call_joined_{users}').format(users=', '.join([user.name for user in joined]))
    if declined:
        message += '\n' + _('call_declined_{users}').format(users=', '.join([user.name for user in declined]))
    if rest:
        message += '\n' + _('call_not_answered_{users}').format(users=', '.join([user.login for user in rest]))
    return message


def _markup_for_call(request: Request):
    return InlineMenu(
        [[(_('call_join'), ['call_join', request.id]), (_('call_decline'), ['call_decline', request.id])]])


def on_call_request(context: Context):
    user_message = context.update.message[context.update.message.find(' ') + 1:].strip()
    if user_message:
        title = user_message + '\n' + _('call_with_text_from_{user}').format(user=context.sender.name)
    else:
        title = _('call_from_{user}').format(context.sender.name)
    request = Request(message_id=context.update.effective_message.message_id,
                      chat_id=context.update.effective_chat.id,
                      author=context.sender,
                      title=title)
    context.session.add(request)
    context.send_response_message(_message_for_call(context, request), reply_markup=_markup_for_call(request))


def _on_call_response(context: Context, answer: int):
    request_id = int(InlineMenu.response_data(context.update)[0])
    request = context.session.query(Request).filter(Request.id == request_id).first()
    if not request:
        # TODO(Viers): Need some kind of CHECK here.
        return

    if context.sender == request.author:
        return

    response = context.session.query(Response).filter(Response.user == context.sender, Response.request == request)
    if response and response.answer == answer:
        return
    elif response:
        response.answer = answer
    else:
        response = Response(request=request, user=context.sender, answer=answer)
        context.session.add(response)

    try:
        context.update.callback_query.edit_message_text(text=_message_for_call(context, request))
    except TelegramError:
        context.send_response_message(_('too_old_request_{user}').format(user=context.sender.name))


def on_call_join(context: Context):
    _on_call_response(context, _CALL_ACCEPTED)


def on_call_decline(context: Context):
    _on_call_response(context, _CALL_DECLINED)
