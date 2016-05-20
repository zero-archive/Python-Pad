#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import app
import json
import unittest
from mockredis import MockRedis


class MockRedisWrapper(MockRedis):
    '''A wrapper to add the `from_url` classmethod'''
    @classmethod
    def from_url(cls, *args, **kwargs):
        return cls()


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.config.update(dict(
            TESTING = True,
            REDIS_PROVIDER = MockRedisWrapper,
        ))

        self.app = app.app.test_client()

    @staticmethod
    def load_json(string):
        try:
            data = json.loads(string)
        except ValueError:
            return False

        return data

    def test_main(self):
        rv = self.app.get('/')
        self.assertTrue(str(rv.headers['Location']).startswith('http://localhost/'))

        # rv = self.app.get('/', follow_redirects=True)
        # self.assertTrue(str(rv.headers['Location']).startswith('http://localhost/'))

    def test_get(self):
        rv = self.app.get('/foo')
        # print .message
        # print self.load_json()


    def test_post(self):
        rv = self.app.post('/foo', data=dict(
            t = 'foobar'
        ))
        data = self.load_json(rv.data)
        self.assertEqual(data['message'], 'ok')
        self.assertEqual(data['padname'], 'foo')

if __name__ == '__main__':
    unittest.main()
