from __future__ import annotations

import io
import json

from integrators.slack.client import SlackClient
from integrators.slack.message import DigitalizationOKSlackMessage
from integrators.slack.message import SlackMessage


def post_message(message: SlackMessage) -> dict:
    """
    :param message:
    :return:
    """
    slack_client = SlackClient()

    body = message.format_message()

    body.update({'channel': slack_client.channel_id})
    # body.update({'channel': slack_client.channel})
    body.update({'username': slack_client.username})

    payload = json.dumps(body)

    result = slack_client.send_request(payload, 'POST')

    return result


def post_file_attached(file_path, text_msg):
    slack_client = SlackClient()

    with open(file_path, 'rb') as file:
        file_read = io.BytesIO(file.read())

        file_name = file.name

        print(f'filename: {file_name}')

        result = slack_client.post_file_message(file_read, file_name, text_msg)

        file.flush()

    return result


if __name__ == '__main__':
    message_text = DigitalizationOKSlackMessage({
        'msg': 'Este es un mensaje para API Slack desde Python',
    })

    # response = post_message(message_text)

    # print(f'response_on_main: {response}')

    # Attach
    file_path_to_attach = '../integrators/prueba.pdf'

    response_attached = post_file_attached(file_path_to_attach, message_text)

    # print(f'response_attached_on_main: {response_attached}')
