from telegram import TelegramError

from app.handlers.callback_utils import AttachedMenu, decode
from app.handlers.context import Context
from app.models.all import Response, Request


def _all_logins_except_sender(context: Context) -> str:
    return ' '.join([user.login for user in context.group.users if user != context.sender])


def on_all_request(context: Context):
    if not context.group:
        return
    message = _('all_from_{user}').format(context.sender.name)
    context.send_response_message(message + '\n\n' + _all_logins_except_sender(context))


def on_call_request(context: Context):
    if not context.group:
        return
    user_message = context.update.message[context.update.message.find(' ') + 1:].strip()
    if user_message:
        message = user_message + '\n' + _('call_with_text_from_{user}').format(context.sender.name)
    else:
        message = _('call_from_{user}').format(context.sender.name)
    message = message + '\n\n' + _all_logins_except_sender(context)
    request = Request(message_id=context.update.effective_message.message_id,
                      chat_id=context.update.effective_chat.id,
                      author=context.sender,
                      title=message)
    context.session.add(request)
    reply_markup = AttachedMenu(
        [[(_('call_join'), ['call_join', request.id]), (_('call_decline'), ['call_decline', request.id])]])
    context.send_response_message(message, reply_markup=reply_markup)


def _on_call_response(context: Context, answer: int):
    request_id = decode(context.update)[0]
    request = context.session.query(Request).filter(Request.id == request_id).first()
    if not request:
        # TODO(Viers): Need some kind of CHECK here.
        return

    if context.sender != request.author:
        response = context.session.query(Response).filter(Response.user_id == context.sender.id,
                                                          Response.request_id == request_id)
        if not response:
            response = Response(request_id=request_id, user_id=context.sender.id, answer=1)
            context.session.add(response)
        else:
            response.answer = answer

    all_responses = context.session.query(Response).filter(Response.request_id == request_id)
    new_message_text = request.title
    joined = [response.user.name for response in all_responses if response.answer == 1]
    if joined:
        new_message_text += '\n' + _('call_joined_{users}').format(users=', '.join(joined))
    declined = [response.user.name for response in all_responses if response.answer == 0]
    if declined:
        new_message_text += '\n' + _('call_declined_{users}').format(users=', '.join(declined))
    try:
        context.update.callback_query.edit_message_text(text=new_message_text)
    except TelegramError:
        context.send_response_message(_('too_old_request_{user}').format(context.sender.name))


def on_call_join(context: Context):
    _on_call_response(context, 1)


def on_call_decline(context: Context):
    _on_call_response(context, 0)
