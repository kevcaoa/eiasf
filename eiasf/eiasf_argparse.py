import argparse


def add_arguments_env(parser):
    parser.add_argument(
        "-e",
        "--environment",
        help="Environment",
        required=False,
    )


def add_arguments_function(parser):
    parser.add_argument(
        "-f",
        "--function",
        help="Function",
        required=True,
    )


def add_arguments_output(parser, output_list):
    parser.add_argument(
        "-o",
        "--output",
        help="output",
        choices=output_list,
        required=False,
    )


def add_arguments_parameters(parser):
    parser.add_argument(
        "-p",
        "--parameters",
        help="Parameters",
        required=False,
    )


def add_arguments_service(parser):
    parser.add_argument(
        "-s",
        "--service",
        help="Service",
        required=False,
    )


def add_arguments_logging_level(parser, logging_level_list):
    parser.add_argument(
        "-L",
        "--logging_level",
        help="Logging level",
        choices=logging_level_list,
        required=False,
    )


def parse(sys_args: list) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    sp = parser.add_subparsers(required=True, dest="eias_bus")

    eias_bus_parser = sp.add_parser("eias_bus")

    logging_level_choices = [
        "FATAL",
        "CRITICAL",
        "ERROR",
        "WARNING",
        "INFO",
        "DEBUG",
    ]

    output_choices = ["local", "slack", ]

    add_arguments_env(eias_bus_parser)
    add_arguments_service(eias_bus_parser)
    add_arguments_function(eias_bus_parser)
    add_arguments_parameters(eias_bus_parser)
    add_arguments_logging_level(eias_bus_parser, logging_level_list=logging_level_choices)
    add_arguments_output(eias_bus_parser, output_list=output_choices)

    return parser.parse_args(sys_args[1:])
