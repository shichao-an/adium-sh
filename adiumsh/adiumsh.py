# -*- coding: utf-8 -*-
import glob
import os
import shlex
import subprocess
from .utils import is_process_running
from .settings import PACKAGE_PATH


class Adium(object):
    script_prefix = 'adium-'
    script_ext = '.scpt'
    open_cmd = 'open -a Adium'

    def __init__(self):
        if not self.is_running:
            self.start()

    @property
    def is_running(self):
        """Whether the application is running"""
        return is_process_running('Adium')

    def start(self):
        """Start the application"""
        subprocess.Popen(shlex.split(self.open_cmd))

    def send_alias(self, alias, message, account, service):
        """Send a message to an alias"""
        pass

    def send(self, name, message):
        """Send a message"""
        self.call_script('send', [message])

    def call_script(self, suffix, args):
        """
        Call AppleScript adium-suffix.scpt
        :param suffix: a string as the suffix of adium AppleScript
        :param args: a list of strings as arguments pass to the script
        """
        script = self.script_prefix + suffix + self.script_ext
        script_path = os.path.join(PACKAGE_PATH, script)
        path = os.path.join(PACKAGE_PATH, '*' + self.script_ext)
        if script_path in glob.glob(path):
            try:
                p = subprocess.Popen([script_path] + args,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
                stdout, stderr = p.communicate()
                if p.returncode != 0:
                    raise ExecutionError(stderr)
                return stdout
            except OSError, e:
                raise e
        else:
            raise DoesNotExist(script + 'does not exist')

    def get_name(self, alias, account, service):
        name = self.call_script('name', [service, account, alias])
        if name:
            return name.rstrip('\n')
        else:
            return None


class DoesNotExist(Exception):
    pass


class ExecutionError(Exception):
    pass


def main():
    pass
