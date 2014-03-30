# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import
import glob
import os
import subprocess
import time
from .utils import is_process_running
from .settings import PACKAGE_PATH
from .command import parse_args


class Adium(object):
    script_prefix = r'adium-'
    script_ext = r'.scpt'
    open_cmd = ['open', '-a', 'Adium']

    def __init__(self, buddy=None, account=None, service=None):
        """
        :param buddy: account name of the target user to chat with
        :param account: default account to use
        :param service: default service of the account
        """
        if not self.is_running:
            self.start()
            while not self.is_running:
                time.sleep(1)
            # Wait for Adium to load accounts
            time.sleep(1)
        self.buddy = buddy
        self.account = account
        self.service = service

    @property
    def is_running(self):
        """Whether the application is running"""
        return is_process_running('Adium')

    def start(self):
        """Start the application"""
        subprocess.Popen(self.open_cmd)

    def send_alias(self, message, alias, account=None, service=None):
        """Send a message to an alias"""
        if account is None and self.account is not None:
            account = self.account
        if service is None and self.service is not None:
            service = self.service
        name = self.get_name(alias, account, service)
        self.send(message, name)

    def send(self, message, name=None):
        """Send a message"""
        if name is None and self.buddy is not None:
            name = self.buddy
        self.call_script('send', [name, message])

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
            except OSError as e:
                raise e
        else:
            raise DoesNotExist(script + ' does not exist')

    def get_name(self, alias, account=None, service=None):
        """Get account name by alias"""
        if account is None and self.account is not None:
            account = self.account
        if service is None and self.service is not None:
            service = self.service
        name = self.call_script('name', [service, account, alias])
        if name:
            return name.rstrip(b'\n')
        else:
            raise DoesNotExist('This alias does not exist in your account')


class DoesNotExist(Exception):
    pass


class ExecutionError(Exception):
    pass


def main():
    args = parse_args()
    adium = Adium(buddy=args.buddy,
                  account=args.account,
                  service=args.service)
    if args.buddy:
        adium.send(args.message, args.buddy)
    else:
        adium.send_alias(args.message, args.alias)
