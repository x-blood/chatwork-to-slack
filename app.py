import json
import os
import base64
import hashlib
import hmac
from chalice import Chalice, Response
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Chalice(app_name='chatwork-to-slack')


@app.route('/chatwork', methods=['POST'] )
def chatwork():
    request = app.current_request

    if 'X-ChatWorkWebhookSignature' not in request.headers:
        return Response(body='Bad Request',
                        status_code=400,
                        headers={'Content-Type': 'text/plain'})

    request_body = request.raw_body.decode('utf-8')

    if token_check(request.headers['X-ChatWorkWebhookSignature'], request_body):
        send_to_slack(request.json_body)

        return Response(body='OK',
                        status_code=200,
                        headers={'Content-Type': 'text/plain'})

    return Response(body='Bad Request',
                    status_code=400,
                    headers={'Content-Type': 'text/plain'})


def token_check(request_signature, request_body):
    allowed_tokens = os.environ['ALLOWED_TOKENS'].split(',')

    for token in allowed_tokens:
        logger.info(token)
        digest = hmac.new(base64.b64decode(token), request_body.encode('utf-8'), hashlib.sha256).hexdigest()
        expected_signature = base64.b64encode(bytes.fromhex(digest)).decode('utf-8')
        if request_signature == expected_signature:
            return True
    return False


def send_to_slack(request_json_body):

    slack_message = {
        'username': 'Chatwork Notification',
        'channel': os.environ['SLACK_CHANNEL_ID'],
        'icon_emoji': 'chatwork',
        'attachments': [
            {
                'color': 'good',
                'pretext': 'Chatworkに新規メッセージがあります',
                'fields': [
                    {
                        'title': 'room_id',
                        'value': request_json_body['webhook_event']['room_id'],
                        'short': True
                    },
                    {
                        'title': 'message_url',
                        'value': "https://www.chatwork.com/#!rid" + str(request_json_body['webhook_event']['room_id']) + "-" + str(request_json_body['webhook_event']['message_id']),
                        'short': False
                    }
                 ]
            }
        ]
    }
    send(slack_message)


def send(slack_message):
    req = Request(
        os.environ['SLACK_WEBHOOK_URL'],
        json.dumps(slack_message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)

