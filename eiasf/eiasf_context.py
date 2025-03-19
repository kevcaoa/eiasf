import enum
import logging
import os

from eiasf.abc.app_config import ServiceConfig, ServiceEnum, ClusterEnum

from eiasf.eiasf_symptoms import Symptoms


class EiasBusEnum(enum.Enum):
    EIAS_BUS = enum.auto()


logger = logging.getLogger(f"wsaf.framework.{os.path.splitext(os.path.basename(__file__))[0]}")


class EiasContext:
    eias_bus: EiasBusEnum
    bus: str
    symptoms: Symptoms
    eias_service_dict: dict
    user_defined_dict: dict
    function: str
    logging_level: str
    output: str
    slack_channel: str
    slack_message_ts: str
    cluster: ClusterEnum
    service: ServiceEnum
    parameters: str

    def __new__(
        cls,
        *,
        eias_bus: EiasBusEnum,
        bus: str = "",
        symptoms: Symptoms = {},
        eias_service_dict: dict = {},
        user_defined_dict: dict = {},
        function: str = None,
        logging_level: str = None,
        output: str = None,
        slack_channel: str = None,
        slack_message_ts: str = None,
        cluster: ClusterEnum = None,
        service: ServiceEnum = None,
        parameters: str = None,
    ):
        self = object.__new__(cls)
        self.eias_bus = eias_bus
        self.bus = bus
        self.symptoms = symptoms
        self.eias_service_dict = eias_service_dict
        self.user_defined_dict = user_defined_dict
        self.function = function
        self.logging_level = logging_level
        self.output = output
        self.slack_channel = slack_channel
        self.slack_message_ts = slack_message_ts
        self.cluster = cluster
        self.service = service
        self.parameters = parameters
        logger.debug(f'Context created: {", ".join([f"{k}={v}" for k, v in self.__dict__.items()])}')
        return self

    def __getnewargs_ex__(self):
        return (), self.__dict__

    @classmethod
    def init_for_eias_bus(
        cls,
        bus: str,
        service_config: ServiceConfig,
        function: str,
        logging_level: str,
        output: str,
        service: ServiceEnum,
        cluster: ClusterEnum,
        parameters: str,
    ) -> "EiasContext":

        service = service
        cluster = cluster

        return cls(
            eias_bus=EiasBusEnum.EIAS_BUS,
            bus=bus,
            eias_service_dict=service_config.return_eias_service_dict(),
            user_defined_dict=service_config.return_user_defined_dict(),
            function=function,
            logging_level=logging_level,
            output=output,
            slack_channel=service_config.get_slack_channel_for_service(service),
            service=service,
            cluster=cluster,
            parameters=parameters,
        )
