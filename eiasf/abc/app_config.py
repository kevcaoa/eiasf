from abc import abstractmethod

import enum


class ServiceEnum(enum.Enum):
    pass


class ClusterEnum(enum.Enum):
    pass


class ServiceConfig:
    @abstractmethod
    def return_eias_service_dict(self) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def return_user_defined_dict(self) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def get_slack_channel_for_service(self, service: ServiceEnum) -> str:
        raise NotImplementedError()


class ClusterConfig:
    @abstractmethod
    def switch_cluster(self, cluster: ClusterEnum):
        raise NotImplementedError()
