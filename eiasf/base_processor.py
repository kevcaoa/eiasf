from abc import abstractmethod
import enum
import logging
import os
import traceback
from datetime import datetime
from typing import NamedTuple, Union

from eiasf.eiasf_context import EiasContext
from eiasf import eiasf_slack

logger = logging.getLogger(f"wsaf.framework.{os.path.splitext(os.path.basename(__file__))[0]}")


class ProcessorExitCode(enum.Enum):
    EXIT_CODE_PROCESSOR_DOES_NOT_MATCH = enum.auto()
    EXIT_CODE_PROCESSOR_SUCCESS = enum.auto()
    EXIT_CODE_PROCESSOR_ERROR = enum.auto()
    EXIT_CODE_PROCESSOR_NONEXISTENT = enum.auto()


class ProcessorReturnValues(NamedTuple):
    first_error: datetime
    last_error: datetime
    processor_exit_code: ProcessorExitCode


class BaseProcessor:
    name: str

    def __init__(self, name):
        self.name = name

    @staticmethod
    def save_data(context: EiasContext, data: object, name: str) -> None:
        context.symptoms[name] = data

    @staticmethod
    def center_text(text) -> str:
        terminal_size = os.get_terminal_size()
        width = terminal_size.columns
        text_length = len(text)
        space = (width - text_length) // 2
        centered_text = ' ' * space + text
        return centered_text

    @staticmethod
    def open_slack_thread(context: EiasContext) -> str:
        if context.output == 'slack':
            message = (f"{context.cluster.name.upper()} `{context.function}` \n"
                       f"{context.service.name}"
                       )

            return eiasf_slack.post_message(channel=context.slack_channel, text=message, )

    @staticmethod
    def update_slack_thread(context: EiasContext) -> None:
        message = eiasf_slack.retrieve_message(
            channel=context.slack_channel, slack_message_ts=context.slack_message_ts
        )
        eiasf_slack.update_message(channel=context.slack_channel, text=message, thread_ts=context.slack_message_ts, )

    def run(self, context: EiasContext) -> ProcessorExitCode:
        try:
            if not self._is_processor_match(context):
                return ProcessorExitCode.EXIT_CODE_PROCESSOR_DOES_NOT_MATCH
            logger.info(f"\n\n"
                        f"{self.center_text('+-----------------------------------------------------+')}\n"
                        f"{self.center_text('|                                                     |')}\n"
                        f"{self.center_text('|          Everything Is A Service Framework          |')}\n"
                        f"{self.center_text('|       =======================================       |')}\n"
                        f"{self.center_text('|                                                     |')}\n"
                        f"{self.center_text('+-----------------------------------------------------+')}\n"
                        f"\n"
                        f"{self.center_text(f'<<<<<<<<<  Function: {context.function}  >>>>>>>>>')}\n"
                        f"\n\n")

            if context.output == 'slack':
                if os.environ.get('EIAS_SLACK_TOKEN') is None or os.environ.get('EIAS_SLACK_TOKEN') == '':
                    logger.error(f"Environment Variable EIAS_SLACK_TOKEN is not configured but you want slack output.")
                    return ProcessorExitCode.EXIT_CODE_PROCESSOR_ERROR
                context.slack_message_ts = self.open_slack_thread(context)

            return_values = self._run(context)

            if return_values is None:
                return ProcessorExitCode.EXIT_CODE_PROCESSOR_SUCCESS
            elif type(return_values) is ProcessorExitCode:
                return return_values
            elif type(return_values) is ProcessorReturnValues:
                return return_values.get("processor_exit_code", ProcessorExitCode.EXIT_CODE_PROCESSOR_SUCCESS)
        except Exception:
            logger.error(f"Processor exited with following exception: {traceback.format_exc()}")
            return ProcessorExitCode.EXIT_CODE_PROCESSOR_ERROR

    @abstractmethod
    def _get_help_text(self) -> str:
        return "No help text is provided for this function..."

    @abstractmethod
    def _is_processor_match(self, context: EiasContext) -> bool:
        raise NotImplementedError("_is_match() must be implemented in each subclass of BaseProcessor")

    @abstractmethod
    def _run(self, context: EiasContext) -> Union[ProcessorExitCode, ProcessorReturnValues]:
        raise NotImplementedError("_run() must be implemented in each subclass of BaseProcessor")
