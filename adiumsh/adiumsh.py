# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import
import glob
import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .utils import is_process_running
from .settings import PACKAGE_PATH
from .command import parse_args

ADIUM_EVENT_MESSAGE_RECEIVED = 'MESSAGE_RECEIVED'
ADIUM_EVENT_MESSAGE_SENT = 'MESSAGE_SENT'
ADIUM_EVENT_STATUS_AWAY = 'STATUS_AWAY'
ADIUM_EVENT_STATUS_ONLINE = 'STATUS_ONLINE'
ADIUM_EVENT_STATUS_OFFLINE = 'STATUS_OFFLINE'


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
        name = self.get_name(alias, account, service)
        self.send(message, name)

    def send(self, message, name=None):
        """Send a message"""
        if name is None and self.buddy is not None:
            name = self.buddy
        self._send(message, name)

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
            raise ExecutionError('This alias does not exist in your account')

    def receive(self, alias=None, name=None, account=None, service=None,
                callback=None):
        """
        Receive a message
        :param callback: a callback function to call upon receival
        """
        pass
        # Call start_watchdog() with event_type and callback

    def _receive(self, account, service):
        pass

    def _send(self, message, name):
        self.call_script('send', [name, message])


class DoesNotExist(Exception):
    pass


class ExecutionError(Exception):
    pass


class AdiumEventHandler(FileSystemEventHandler):
    """Event handler based on Watchdog for logs"""
    def __init__(self, callback, event_type):
        """
        :param callback: a function to be called for event with `event_type`
            callback(event)
        :param event_type: a string representing an Adium event
        """
        self.callback = callback
        self.event_type = event_type
        super(AdiumEventHandler, self).__init__()

    def parse_event(self, event):
        """
        Parse the type and data of the FileSystemEvent event

        The type can be message (sent or received) and status

        Return a AdiumEvent event
        """
        pass

    def on_modified(self, event):
        pass
        # Call self.parse_event(event)
        # Generate AdiumEvent event
        # Call self.callback(event)


class AdiumEvent(object):
    def __init__(self, event_type, time, data):
        self.event_type = event_type
        self.time = time
        self.data = data


def start_watchdog(path, event_handler, event_type, callback):
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    args = parse_args()
    adium = Adium(buddy=args.buddy,
                  account=args.account,
                  service=args.service)
    if args.buddy:
        adium.send(args.message, args.buddy)
    else:
        adium.send_alias(args.message, args.alias)
