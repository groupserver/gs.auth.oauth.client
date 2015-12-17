# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2011, 2012, 2013, 2014, 2015 E-Democracy.org and
# Contributors.
#
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
# Partially borrowed from django_social_auth
from __future__ import absolute_import, unicode_literals, print_function, division
import base64
import cgi
from logging import getLogger
log = getLogger("gs.auth.oauth.client")
import sys
if sys.version_info >= (3, ):
    from urllib.parse import urlencode
    from urllib.request import urlopen
else:  # Python 2
    from urllib import urlencode, urlopen
import simplejson

FACEBOOK_SERVER = "graph.facebook.com"
FACEBOOK_AUTHORIZATION_URI = "https://%s/oauth/authorize" % FACEBOOK_SERVER
FACEBOOK_ACCESS_TOKEN_URI = "https://%s/oauth/access_token" % FACEBOOK_SERVER
FACEBOOK_CHECK_AUTH = "https://%s/me" % FACEBOOK_SERVER


def auth_url(redirect_uri, client_id, scope=('email',)):
    """ Return URL which will initiate oauth authentication.

    """
    params = {'redirect_uri': redirect_uri,
              'client_id': client_id,
              'scope': ','.join(scope)}
    retval = '{uri}?{params}'.format(uri=FACEBOOK_AUTHORIZATION_URI, params=urlencode(params))
    return retval


def encode_parameters(params):
    return base64.urlsafe_b64encode(urlencode(params))


def decode_parameters(s):
    return base64.urlsafe_b64decode(s)


class FacebookAuth:
    def __init__(self, redirect_uri, client_id, client_secret, scope=('email',)):
        self.redirect_uri = redirect_uri
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope

    def complete_auth(self, request):
        """ Finish second stage of oauth2 dance.

        """
        self.access_token = None
        if 'code' in request:
            params = {'redirect_uri': self.redirect_uri,
                      'client_id': self.client_id,
                      'client_secret': self.client_secret,
                      'code': request['code']}

            url = FACEBOOK_ACCESS_TOKEN_URI+'?'+urlencode(params)
            response = cgi.parse_qs(urlopen(url).read())
            try:
                self.access_token = response['access_token'][0]
                log.info('Received access token from facebook')
            except KeyError:
                log.error('Did not receive access token from facebook, instead: %s' % response)

    def data(self):
        """ Retrieve user data from service."""
        params = {'access_token': self.access_token}
        url = FACEBOOK_CHECK_AUTH+'?'+urlencode(params)
        userdata = simplejson.load(urlopen(url))
        log.info('Received user data from facebook: %s' % userdata)
        return userdata
