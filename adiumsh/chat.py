# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import
import json
try:
    import langid
except:
    pass
import requests
import sys
import warnings
from .settings import SIMI_KEY
from .settings import (EVENT_MESSAGE_RECEIVED, EVENT_MESSAGE_SENT,
                       EVENT_STATUS_AWAY, EVENT_STATUS_ONLINE,
                       EVENT_STATUS_OFFLINE, EVENT_STATUS_CONNECTED,
                       EVENT_STATUS_DISCONNECTED)


class BaseChat(object):
    def __init__(self, adium, event, event_types=[EVENT_MESSAGE_RECEIVED]):
        """
        A Chat instance represents a single chat, consists of a `reply` method
        :param adium: an Adium instance
        :param event: an AdiumEvent object that invokes this chat
        :param event_types: a list of event types for this chat to catch and
            reply
        """
        self.adium = adium
        self.event = event
        self.event_types = event_types

    def reply(self):
        text = self.response()
        self.adium.send(text, self.event.sender)
        if hasattr(self, 'active_chat'):
            self.chat()

    def response(self):
        """
        This method is to be implemented

        Return text to be replied
        """
        raise NotImplementedError


class SimpleChat(object):
    """
    Simple Chat API
    """
    def __init__(self):
        super(SimiChat, self).__init__()

    def response(self):
        pass


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

    def __init__(self, adium, event, event_types=[EVENT_MESSAGE_RECEIVED],
                 language=None, trial=True):
        self.language = language
        self.trial = trial
        super(SimiChat, self).__init__(adium, event, event_types)

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
            'key': SIMI_KEY,
            'lc': lc,
            'text': text,
        }
        r = requests.get(url, params=params)
        d = json.loads(r.text)
        print(d)
        return d['response']
