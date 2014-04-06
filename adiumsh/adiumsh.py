# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import
from bs4 import BeautifulSoup
import dateutil.parser
import glob
import os
import subprocess
import time
from watchdog.observers.kqueue import KqueueObserver as Observer
from watchdog.events import FileSystemEventHandler
from .utils import is_process_running
from .settings import PACKAGE_PATH, LOG_PATH
from .command import parse_args


EVENT_MESSAGE_RECEIVED = 'MESSAGE_RECEIVED'
EVENT_MESSAGE_SENT = 'MESSAGE_SENT'
EVENT_STATUS_AWAY = 'STATUS_AWAY'
EVENT_STATUS_ONLINE = 'STATUS_ONLINE'
EVENT_STATUS_OFFLINE = 'STATUS_OFFLINE'
EVENT_STATUS_CONNECTED = 'STATUS_CONNECTED'
EVENT_STATUS_DISCONNECTED = 'STATUS_DISCONNECTED'


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
        self._send(message, name)

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
        :param callback: a callback function to call upon receival (default
            to self.receive_callback)
        """

        if account is None and self.account is not None:
            account = self.account
        if service is None and self.service is not None:
            service = self.service
        if callback is None:
            callback = self.receive_callback
        sender = None
        if name is not None:
            sender = name
        elif alias is not None:
            sender = self.get_name(alias, account, service)
        self._receive(account, service, callback, sender)

    def _receive(self, account, service, callback, sender=None):
        event_handler = AdiumEventHandler(account, service, callback,
                                          EVENT_MESSAGE_RECEIVED,
                                          sender)

        start_watchdog(event_handler)

    def _send(self, message, name):
        self.call_script('send', [name, message])

    def receive_callback(self, event):
        """Default message receive callback"""
        data = event.data
        sender = event.sender 
        print(sender)
        print(data['text'])


class DoesNotExist(Exception):
    pass


class ExecutionError(Exception):
    pass


class AdiumEventHandler(FileSystemEventHandler):
    """Event handler based on Watchdog for logs"""
    patterns = {
        'status': ('connected', 'disconnected', 'away', 'online'),
        'message': ('sender'),
        'event': ('windowClosed'),
    }

    def __init__(self, account, service, callback,
                 event_type=None, sender=None):
        """
        :param account: account name of the current user
        :param service: service name of the account
        :param callback: a function to be called for event with `event_type`
            callback(event)
        :param event_type: a string representing an Adium event that callback
            will be called with; if None, all events will be used
        :param sender: the sender of the event; defaults to None, which is
            anyone
        """
        self.account = account
        self.service = service
        self.callback = callback
        self.event_type = event_type
        self.sender = sender
        self.adium_event = None
        self.src_path = os.path.join(LOG_PATH, service + '.' + account)
        super(AdiumEventHandler, self).__init__()

    def parse_event(self, event):
        """
        Parse the Watchdog event into Adium event and save to self.adium_event

        Return True if new event is emitted; False if no event
        """
        if event.is_directory:
            self.adium_event = None
            return False
        else:
            with open(event.src_path) as f:
                soup = BeautifulSoup(f.read())
                t = soup.find_all(['message', 'status', 'event'])[-1]
                event_time = dateutil.parser.parse(t.attrs['time'])
                sender = t.attrs['sender']
                if self.sender is not None:
                    if self.sender != sender:
                        self.adium_event = None
                        return False
                sender_alias = t.attrs['alias']
                data = {}
                if t.name == 'message':
                    data['text'] = t.text
                    if sender == self.account:
                        event_type = EVENT_MESSAGE_SENT
                        return self.emit_event(event_type, event_time, sender,
                                               sender_alias, data)
                    else:
                        event_type = EVENT_MESSAGE_RECEIVED
                        return self.emit_event(event_type, event_time, sender,
                                               sender_alias, data)
                elif t.name == 'status':
                    if t.attrs['type'] == 'away':
                        event_type = EVENT_STATUS_AWAY
                    elif t.attrs['type'] == 'online':
                        event_type = EVENT_STATUS_ONLINE
                    elif t.attrs['type'] == 'offline':
                        event_type = EVENT_STATUS_OFFLINE
                    elif t.attrs['type'] == 'connected':
                        event_type = EVENT_STATUS_CONNECTED
                    elif t.attrs['type'] == 'disconnected':
                        event_type = EVENT_STATUS_DISCONNECTED
                elif t.name == 'event':
                    # TODO: read more logs to understand event tags
                    pass
                return self.emit_event(event_type, event_time, sender,
                                       sender_alias)

    def emit_event(self, event_type, event_time,
                   sender, sender_alias, data=None):
        self.adium_event = AdiumEvent(
            event_type, event_time, sender, sender_alias, data)
        return True

    def on_modified(self, event):
        if self.parse_event(event):
            if self.event_type is not None:
                if self.adium_event.event_type == self.event_type:
                    self.callback(self.adium_event)
            else:
                self.callback(self.adium_event)


class AdiumEvent(object):
    def __init__(self, event_type, event_time, sender, sender_alias, data):
        self.event_type = event_type
        self.event_time = event_time
        self.sender = sender
        self.sender_alias = sender_alias
        self.data = data


def start_watchdog(event_handler):
    observer = Observer()
    observer.schedule(event_handler, event_handler.src_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    except Exception:
        raise
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
