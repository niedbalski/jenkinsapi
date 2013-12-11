#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  This module is used for authenticate users against the acegi security
  framework ( used by jenkins LDAP support )
"""
__author__ = 'Jorge Niedbalski R. <jnr@pyrosome.org>'

import urllib
import urllib2

from urlparse import urlparse

from jenkinsapi.utils.requester import Requester
from jenkinsapi.custom_exceptions import JenkinsAPIException


class LDAPRequester(Requester):

    def __init__(self, **kwargs):
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)
        urllib2.install_opener(self.opener)

        Requester.__init__(self, **kwargs)

    def login(self, url):
        parsed = urlparse(url)
        return urllib2.urlopen('%s://%s/login' % (parsed.scheme, parsed.netloc),
                        data=urllib.urlencode({'j_username': self.username,
                                               'j_password': self.password}))

    def get_url(self, url, params=None, headers=None):
        params = self.get_request_dict(params=params, headers=headers)
        updated_url = self._update_url_scheme(url)
        self.login(updated_url)
        return urllib2.urlopen(updated_url, **params)

    def post_url(self, url, params=None, data=None, files=None, headers=None):
        # params = self.get_request_dict(
        #     params=params,
        #     data=data,
        #     files=files,
        #     headers=headers)
        updated_url = self._update_url_scheme(url)
        self.login(updated_url)
        return urllib2.urlopen(updated_url)

    def get_and_confirm_status(self, url, params=None, headers=None, valid=None):
        valid = valid or self.VALID_STATUS_CODES
        response = self.get_url(url, params, headers)
        if not response.status_code in valid:
            raise JenkinsAPIException('Operation failed. url={0}, headers={1}, status={2}, text={3}'.format(
                response.url, headers, response.status_code, response.text.encode('UTF-8')))
        return response
