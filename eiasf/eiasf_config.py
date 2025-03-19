import os


class EiasConfig:
    processors_package: str

    def __init__(self):
        processors_package = os.environ.get('PROCESSORS_PACKAGE')
        if processors_package is not None and processors_package != '':
            self.processors_package = processors_package
        else:
            self.processors_package = 'eias_cli'
