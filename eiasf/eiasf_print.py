from contextlib import contextmanager
from logging import Logger
import typing

from eiasf.eiasf_context import EiasContext
from eiasf import eiasf_slack


class EiasPrintBuffer:
    header: str
    messages: typing.Sequence[str]

    def __init__(self, header: str):
        self.header = header
        self.messages = []

    def print(self, message: str):
        self.messages.append(message)

    def flush(self, context: EiasContext, logger: Logger):
        if context.output == 'local' or context.output is None:
            logger.info(f"======== {self.header} ========")
            for message in self.messages:
                logger.info(message)
        if context.output == 'slack':
            logger.info(f'{{"header": "{self.header}", "messages": {self.messages}}}')
            expanded_message = "\n".join(self.messages)
            eiasf_slack.post_message_thread(channel=context.slack_channel, text=f"{self.header}\n```\n{expanded_message}\n```", thread_ts=context.slack_message_ts, )


@contextmanager
def eias_print_buf(header: str, context: EiasContext, logger: Logger) -> EiasPrintBuffer:
    buffer = EiasPrintBuffer(header)
    yield buffer
    buffer.flush(context, logger)
