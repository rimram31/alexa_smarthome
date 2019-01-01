#!/usr/bin/env python3.6
# coding: utf-8

import os
import json
import logging
import requests

logger = logging.getLogger()

class SmartHomeServer(object):
    def __init__(self, config):
        self.config = config
        self.url = config.url.rstrip('/')
        agent_str = 'Alexa Smart Home Skill - %s - %s'
        agent_fmt = agent_str % (os.environ['AWS_DEFAULT_REGION'],
                                 requests.utils.default_user_agent())
        self.session = requests.Session()
        self.session.headers = {'content-type': 'application/json',
                                'X-HA-Access': config.password,
                                'User-Agent': agent_fmt}
        self.session.verify = config.ssl_verify
        self.session.cert = config.ssl_client

    def build_url(self, relurl):
        return '%s/%s' % (self.config.url, relurl)

    def get(self, relurl):
        r = self.session.get(self.build_url(relurl))
        r.raise_for_status()
        return r.json()

    def post(self, relurl, d, wait=False):
        read_timeout = None if wait else 0.01
        r = None
        try:
            logger.debug('calling %s with %s', relurl, str(d))
            r = self.session.post(self.build_url(relurl),
                                  data=json.dumps(d),
                                  timeout=(None, read_timeout))
            r.raise_for_status()
        except requests.exceptions.ReadTimeout:
            # Allow response timeouts after request was sent
            logger.debug('request for %s sent without waiting for response',
                         relurl)
        return r


class Configuration(object):
    def __init__(self, filename=None, optsDict=None):
        self._json = {}
        if filename is not None:
            with open(filename) as f:
                self._json = json.load(f)

        if optsDict is not None:
            self._json = optsDict

        opts = {}
        opts['url'] = self.get(['url', 'ha_url'],
                               default='http://localhost:8123/api')
        opts['ssl_verify'] = self.get(['ssl_verify', 'ha_cert'], default=True)
        opts['ssl_client'] = self.get(['ssl_client'], default='')
        opts['debug'] = self.get(['debug'], default=False)
        opts['password'] = self.get(['password'], default='')
        self.opts = opts

    def __getattr__(self, name):
        return self.opts[name]

    def get(self, keys, default):
        for key in keys:
            if key in self._json:
                return self._json[key]
        return default

    def dump(self):
        return json.dumps(self.opts, indent=2, separators=(',', ': '))


def event_handler(event, context):
    config = Configuration('config.json')
    if config.debug:
        logger.setLevel(logging.DEBUG)

    server = SmartHomeServer(config)

    #return server.post('smarthome', event, wait=True).json()    
    return server.post('alexa/smart_home', event, wait=True).json()