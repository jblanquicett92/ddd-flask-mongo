from __future__ import annotations

from abc import ABC


class SlackMessage(ABC):
    level: str
    title: str
    body: dict

    def __init__(self, body: dict):
        self.body = body

    def format_message(self) -> dict:
        message = {
            'attachments': [
                {
                    'title': f'{self.level} {self.title}',
                    'fields': [
                        {'title': key, 'value': value, 'short': True}
                        for key, value in self.body.items()
                    ],
                    'footer': 'Tower Digitalization Bot',
                },
            ],
        }

        return message


class DigitalizationOKSlackMessage(SlackMessage):
    level = ':white_check_mark:'
    title = 'QRCodes PDF File Created correctly'
