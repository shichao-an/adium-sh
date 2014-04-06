# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import
from fnmatch import fnmatch
import json
try:
    import langid
except:
    pass
import requests
import sys
import warnings
from .settings import (EVENT_MESSAGE_RECEIVED, EVENT_MESSAGE_SENT,
                       EVENT_STATUS_AWAY, EVENT_STATUS_ONLINE,
                       EVENT_STATUS_OFFLINE, EVENT_STATUS_CONNECTED,
                       EVENT_STATUS_DISCONNECTED)


class BaseChat(object):
    def __init__(self, adium, event_types=[EVENT_MESSAGE_RECEIVED]):
        """
        A Chat instance represents a single chat, consists of a `reply` method
        :param adium: an Adium instance
        :param event: an AdiumEvent object that invokes this chat
        :param event_types: a list of event types for this chat to catch and
            reply
        """
        self.adium = adium
        self.event_types = event_types

    def reply(self):
        text = self.response()
        if text:
            self.adium.send(text, self.event.sender)
        if hasattr(self, 'active_chat'):
            self.chat()

    def response(self):
        """
        This method is to be implemented

        Return text to be replied
        """
        raise NotImplementedError


class SimpleChat(BaseChat):
    """
    Simple Chat API
    """
    def __init__(self, adium, patterns, pattern_type,
                 event_types=[EVENT_MESSAGE_RECEIVED]):
        self.patterns = patterns
        self.pattern_type = pattern_type
        super(SimpleChat, self).__init__(adium, event_types)

    def response(self):
        if (self.event.event_type == EVENT_MESSAGE_RECEIVED
                and EVENT_MESSAGE_RECEIVED in self.event_types):
            text = self.event.data['text']
            parser = PatternParser(text, self.patterns, self.pattern_type)
            return parser.parse()


class ActiveChatMixin(object):
    """
    Mixin for BaseChat classes to enable active chat
    """
    active_chat = True

    def chat(self):
        pass


class SimiChat(BaseChat):
    """
    SimiSimi API
    """
    trial_url = 'http://sandbox.api.simsimi.com/request.p'
    paid_url = 'http://api.simsimi.com/request.p'

    def __init__(self, adium, key, event_types=[EVENT_MESSAGE_RECEIVED],
                 language=None, key_type='trial'):
        self.key = key
        self.language = language
        self.trial = True if key_type == 'trial' else False
        super(SimiChat, self).__init__(adium, event_types)

    def response(self):
        if self.trial:
            url = self.trial_url
        else:
            url = self.paid_url
        text = self.event.data['text']
        if 'langid' not in sys.modules:
            warnings.warn('langid is unavailable', UserWarning)
            if self.language is None:
                warnings.warn('Language auto detection is not in effect',
                              UserWarning)
            lc = 'en' if self.language is None else self.language
        else:
            lc = langid.classify(text)[0] if self.language is None\
                else self.language
        params = {
            'key': self.key,
            'lc': lc,
            'text': text,
        }
        r = requests.get(url, params=params)
        d = json.loads(r.text)
        print(d)
        return d['response']


class PatternParser(object):
    """
    PatternParser: parse user-defined patterns for Chat instances
    """
    def __init__(self, text, patterns, pattern_type='wildcard'):
        """
        :param text: a string of text to parse
        :param patterns: a raw pattern string from the config file
        :param pattern_type: 'wildcard' or 'regex'
        """
        self.text = text
        r = patterns.strip('\n').split('\n')
        self.patterns = \
            map(lambda x: tuple(map(lambda y: y.strip(), x.split(':'))), r)
        self.pattern_type = pattern_type

    def parse(self):
        if self.pattern_type == 'wildcard':
            return self.parse_wildcard()
        elif self.pattern_type == 'regex':
            return self.parse_regex()

    def parse_wildcard(self):
        for pattern in self.patterns:
            if fnmatch(self.text, pattern[0]):
                return pattern[1]
        return None

    def parse_regex(self):
        # TODO
        pass
