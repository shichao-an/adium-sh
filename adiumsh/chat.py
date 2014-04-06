# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import
import json
import requests
from .settings import SIMI_KEY


class BaseChat(object):
    def __init__(self, event):
        pass


class SimpleChat(object):
    """
    Simple Chat API
    """


class SimiChat(object):
    """
    SimiSimi API
    """
    trial_url = 'http://sandbox.api.simsimi.com/request.p'
    paid_url = 'http://api.simsimi.com/request.p'

    def __init__(self, text, callback, language='en', trial=False):
        self.text = text
        self.language = language
        self.trial = trial

    def request(self):
        if self.trial:
            url = self.trial_url
        else:
            url = self.paid_url
        params = {
            'key': SIMI_KEY,
            'lc': self.language,
            'text': self.text
        }
        r = requests.get(url, params=params)
        d = json.loads(r.text)

    def response(self):
        pass
