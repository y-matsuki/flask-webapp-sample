# -*- coding: utf-8 -*-
import os
import sample
import unittest
import tempfile

class SampleTestCase(unittest.TestCase):

    def setUp(self):
        self.app = sample.app.test_client()

    def tearDown(self):
        pass

    def test_show_login(self):
        rv = self.app.get('/')
        assert '＊ Reco-study ＊' in rv.data

    def test_login_logout(self):
        rv = self.app.post('/login', data=dict(
            username='admin',
            password='password'), follow_redirects=True)
        assert '次回の勉強会' in rv.data
        assert '過去の勉強会' in rv.data
        rv = self.app.get('/logout', follow_redirects=True)
        assert '＊ Reco-study ＊' in rv.data
        rv = self.app.post('/login', data=dict(
            username='adminx',
            password='password'), follow_redirects=True)
        assert 'Invalid username/password' in rv.data

if __name__ == '__main__':
    unittest.main()
