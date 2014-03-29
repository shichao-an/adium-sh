import os
import psutil
import configparser


def is_process_running(process_name):
    names = [proc.name() for proc in psutil.process_iter()]
    return process_name in names


def get_config(path, section):
    config = configparser.ConfigParser()
    if os.path.exists(path):
        config.read(path)
        if config.has_section(section):
            return dict(config.items(section))
