import os
import psutil
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
from xml.sax import saxutils


def is_process_running(process_name):
    names = [proc.name() for proc in psutil.process_iter()]
    return process_name in names


def get_process(process_name):
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            return proc
    else:
        return None


def get_config(path, section):
    config = configparser.ConfigParser()
    if os.path.exists(path):
        config.read(path)
        if config.has_section(section):
            return dict(config.items(section))


def get_config_value(path, section, name):
    config = get_config(path, section)
    return config.get(name, None)


def unescape(text):
    entities = {"&apos;": "'", "&quot;": '"'}
    return saxutils.unescape(text, entities)


def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def get_old_entries(dirpath, at_least=5):
    """
    Get a list of n least recently modified entries of dirpath except the most
    recently modified entry if any
    :param at_least: `dirpath` must contain at least `at_least` entries,
        or return empty list
    """
    entries = listdir_fullpath(dirpath)
    if len(entries) < at_least:
        return []
    entries.sort(key=os.path.getmtime)
    return entries[1:]
