# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals, print_function, division
# from mock import patch
from unittest import TestCase
from gs.auth.oauth.client.facebook import (auth_url, encode_parameters, decode_parameters)


class AuthUrlTest(TestCase):

    def test_defaults(self):
        'Test the default params'
        url = 'https://groups.example.com/'
        clientId = 'ThisIsNotAnID'
        r = auth_url(url, clientId)

        self.assertIn('groups.example.com', r)
        self.assertIn(clientId, r)
        self.assertIn('scope', r)
        self.assertIn('email', r)

    def test_scope(self):
        'Test setting the scope'
        url = 'https://groups.example.com/'
        clientId = 'ThisIsNotAnID'
        r = auth_url(url, clientId, ('wibble', ))

        self.assertIn('groups.example.com', r)
        self.assertIn(clientId, r)
        self.assertIn('scope', r)
        self.assertIn('wibble', r)
        self.assertNotIn('email', r)


class EncodeParametersTest(TestCase):
    def test_empty(self):
        'Test encoding an empty string'
        r = encode_parameters({})
        self.assertEqual('', r)

    def test_encode(self):
        'Test encoding a dict'
        r = encode_parameters({'tonight': 'we look at violence'})
        expected = 'dG9uaWdodD13ZStsb29rK2F0K3Zpb2xlbmNl'
        self.assertEqual(expected, r)


class DecodeParametersTest(TestCase):

    def test_empty(self):
        r = decode_parameters('')
        self.assertEqual('', r)

    def test_decode(self):
        'Test decoding'
        r = decode_parameters(b'dG9uaWdodD13ZStsb29rK2F0K3Zpb2xlbmNl')
        expected = 'tonight=we+look+at+violence'
        self.assertEqual(expected, r)
