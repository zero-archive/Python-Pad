#!/usr/bin/env python
# -*- coding: utf-8 -*-

import app as a
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
        a.app.config.update(dict(
            TESTING=True,
            REDIS_PROVIDER=MockRedisWrapper,
        ))

        self.app = a.app.test_client()

    def test_pad_key(self):
        self.assertEqual(a.pad_key('bar'), 'pad:bar')
        self.assertEqual(a.pad_key('bar', 'foo'), 'foo:bar')

    def test_pad_get(self):
        with a.app.app_context():
            rs = a.get_redis()
            rs.set('pad:foo', 'bar')
            self.assertEqual(a.pad_get('foo'), 'bar')

    def test_pad_set(self):
        with a.app.app_context():
            rs = a.get_redis()
            a.pad_set('foo', 'bar')
            a.pad_set('foobar', 'foobar')
            self.assertEqual(rs.get('pad:foo'), 'bar')
            self.assertEqual(rs.get('pad:foobar'), 'foobar')

    def test_main(self):
        rv = self.app.get('/')
        self.assertTrue(
            str(rv.headers['Location']).startswith('http://localhost/')
        )

    def test_get(self):
        rv = self.app.get('/foo')
        self.assertGreater(len(rv.data), 0)

    def test_post(self):
        rv = self.app.post('/foo', data=dict(
            t='foobar'
        ))
        data = self.load_json(rv.data)
        self.assertEqual(data['message'], 'ok')
        self.assertEqual(data['padname'], 'foo')

    @staticmethod
    def load_json(string):
        try:
            data = json.loads(string)
        except ValueError:
            return False

        return data


if __name__ == '__main__':
    unittest.main()
