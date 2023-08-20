from __future__ import annotations

from http import HTTPStatus

import requests
import structlog
from decouple import config as environment


class SlackApiProxy:
    app_code = (
        'SLackAPI',
        HTTPStatus.BAD_GATEWAY,
        'There was an error in slack api micro-service',
    )


class SlackClient:
    """
    Requests Slack API and send messages to a slack channel
    """

    url: str
    channel_id: str
    channel: str
    username: str

    def __init__(self):
        self.url = environment('SLACK_URL_POST_MESSAGE')

        self.channel_id = environment('SLACK_CHANNEL_ID')

        self.channel = environment('SLACK_CHANNEL')

        self.username = environment('SLACK_USERNAME')

        self.headers = {
            'Authorization': f"Bearer {environment('SLACK_TOKEN_BOT')}",
            'Content-Type': 'application/json; charset=utf-8;',
        }

        self.params = {'channel': self.channel_id}

        self.logger = structlog.getLogger(__name__)

    def send_request(self, payload, method):

        response = requests.request(
            method=method,
            url=self.url,
            headers=self.headers,
            data=payload,
        )

        return response

    def send_post_request(self, payload):
        try:
            request_response = requests.post(
                self.url, {
                    'token': environment('SLACK_TOKEN_BOT'),
                    'channel': self.channel,
                    'text': payload,
                    'username': self.username,
                },
            ).json()

            http_response = (request_response, 200)
        except requests.ConnectionError as ex:
            response = f'Request to channel: {self.channel} with text: {payload} ' \
                       f'failed with response connection error: {ex}'
            self.logger.error(response)
            http_response = ({'slack_response': response}, 400)
        except requests.HTTPError as ex:
            response = f'Request to channel: {self.channel} with text: {payload} ' \
                       f'failed with HttpError: {ex}'
            self.logger.error(response)
            http_response = ({'slack_response': response}, 400)
        except requests.Timeout as ex:
            response = f'Request to channel: {self.channel} with text: {payload} ' \
                       f'failed with request time out: {ex}'
            self.logger.error(response)
            http_response = ({'slack_response': response}, 400)

        return http_response

    def post_file_message(self, file_attached, file_name, text_msg):

        try:
            headers = {
                'Authorization': f"Bearer {environment('SLACK_TOKEN_BOT')}",
                'Content-Type': 'multipart/form-data; charset=utf-8;',
                'channel': self.channel_id,
            }

            request_response = requests.request(
                method='POST',
                url=self.url,
                headers=headers,
                data={
                    'token': environment('SLACK_TOKEN_BOT'),
                    'channels': [self.channel],
                    'filename': file_name,
                    'initial_comment': text_msg,
                    'title': 'B2B Digitalizacion PDF Users QR Codes',
                    'file': file_attached,
                    'username': self.username,
                },
            )

            http_response = request_response
        except requests.ConnectionError as ex:
            response = f'Request to channel: {self.channel} with text: {text_msg} ' \
                       f'failed with response connection error: {ex}'
            self.logger.error(response)
            http_response = ({'slack_response': response}, 400)
        except requests.HTTPError as ex:
            response = f'Request to channel: {self.channel} with text: {text_msg} ' \
                       f'failed with HttpError: {ex}'
            self.logger.error(response)
            http_response = ({'slack_response': response}, 400)
        except requests.Timeout as ex:
            response = f'Request to channel: {self.channel} with text: {text_msg} ' \
                       f'failed with request time out: {ex}'
            self.logger.error(response)
            http_response = ({'slack_response': response}, 400)

        return http_response

    # def send_request(self, request_function, method, **kwargs):
    #
    #     if has_request_context():
    #         headers = kwargs.get("headers", {})
    #         headers.update({"x-request-id": request.environ.get("request_id")})
    #         kwargs.update({"headers": headers})
    #
    #     try:
    #         response = request_function(timeout=15, **kwargs)
    #         try:
    #             result = response.json()
    #         except json.decoder.JSONDecodeError:
    #             result = response.content
    #             if not result:
    #                 result = {}
    #         self.logger.debug(
    #             self.api_name, method=method, **kwargs, response=result
    #         )
    #     except (Exception, SystemExit) as e:
    #         result = e
    #         response = None
    #
    #     if not response or not isinstance(result, dict):
    #         kwargs.update({"method": method})
    #         self.manage_errors(result, **kwargs)
    #     return result
    #
    # def send_post_request(self, **kwargs):
    #     return self.send_request(requests.post, "POST", **kwargs)
