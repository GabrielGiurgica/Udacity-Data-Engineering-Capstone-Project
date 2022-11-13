"""Provide functions to parse the config file."""

from configparser import ConfigParser


def get_config(config_file: str) -> ConfigParser:
    """Get the config parser."""
    config = ConfigParser()
    config.read(config_file)
    return config
