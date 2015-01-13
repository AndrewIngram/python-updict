#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_updict
----------------------------------

Tests for `updict` module.
"""

import unittest

from updict import updict, UpdictException


class TestUpdict(unittest.TestCase):

    def setUp(self):
        pass

    def test_push(self):
        self.assertEquals(
            updict([1], {'$push': [7]}),
            [1, 7]
        )

        with self.assertRaises(UpdictException):
            updict([], {'$push': 7})

        with self.assertRaises(UpdictException):
            updict(1, {'$push': [7]})

    def test_unshift(self):
        self.assertEquals(
            updict([1], {'$unshift': [7]}),
            [7, 1]
        )

        with self.assertRaises(UpdictException):
            updict([], {'$unshift': 7})

        with self.assertRaises(UpdictException):
            updict(1, {'$unshift': [7]})

    def test_merge(self):
        self.assertEquals(
            updict({'a': 'b'}, {'$merge': {'c': 'd'}}),
            {'a': 'b', 'c': 'd'}
        )

        with self.assertRaises(UpdictException):
            updict({}, {'$merge': 7})

        with self.assertRaises(UpdictException):
            updict(7, {'$merge': {'a': 'b'}})

    def test_set(self):
        self.assertEquals(
            updict({'a': 'b'}, {'$set': {'c': 'd'}}),
            {'c': 'd'}
        )

    def test_deep_updates(self):
        self.assertEquals(
            updict({'a': 'b', 'c': {'d': 'e'}}, {'c': {'d': {'$set': 'f'}}}),
            {'a': 'b', 'c': {'d': 'f'}}
        )

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
