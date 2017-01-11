#!/usr/bin/env python3

import envreader

import unittest

class _TestEnvReader_Base(unittest.TestCase):
    '''Base class providing helpers to verify RawEpisodeInfo.'''

    def verify_with_env(self, assertion, field, environ):
        assertion(field(envreader.get_episode_info(environ)))

    def assertEqualC(self, x):
        '''Curried version of `assertEqual`.'''
        def _assertEqualC(y):
            self.assertEqual(x, y)
        return _assertEqualC

class TestEnvReader_EpisodeTitle(_TestEnvReader_Base):
    def test_should_be_set_from_environ(self):
        self._verify_equal_title('anonymousTitle')

    def test_should_be_empty_when_empty(self):
        self._verify_equal_title('')

    def test_should_be_None_when_missing(self):
        self._verify_title_env(self.assertIsNone, {})

    def _verify_equal_title(self, title):
        self._verify_title(self.assertEqualC(title), title)

    def _verify_title(self, assertion, title):
        fake_environ = self._get_fake_environ(title)
        self._verify_title_env(assertion, fake_environ)

    def _verify_title_env(self, assertion, fake_environ):
        self.verify_with_env(assertion, envreader.episode_title, fake_environ)

    def _get_fake_environ(self, episode_title):
        return {'GPODDER_EPISODE_TITLE': episode_title}

class TestEnvReader_EpisodeFilename(_TestEnvReader_Base):
    def test_should_be_set_from_environ(self):
        self._verify_equal_filename('anonymousFilename')

    def test_should_be_empty_when_empty(self):
        self._verify_equal_filename('')

    def test_should_be_None_when_missing(self):
        self._verify_filename_env(self.assertIsNone, {})

    def _verify_equal_filename(self, filename):
        self._verify_filename(self.assertEqualC(filename), filename)

    def _verify_filename(self, assertion, filename):
        fake_environ = self._get_fake_environ(filename)
        self._verify_filename_env(assertion, fake_environ)

    def _verify_filename_env(self, assertion, fake_environ):
        self.verify_with_env(assertion, envreader.episode_filename, fake_environ)

    def _get_fake_environ(self, episode_title):
        return {'GPODDER_EPISODE_FILENAME': episode_title}

class TestEnvReader_PodcastTitle(_TestEnvReader_Base):
    def test_should_be_set_from_environ(self):
        self._verify_equal_title('anonymousTitle')

    def test_should_be_empty_when_empty(self):
        self._verify_equal_title('')

    def test_should_be_None_when_missing(self):
        self._verify_title_env(self.assertIsNone, {})

    def _verify_equal_title(self, title):
        self._verify_title(self.assertEqualC(title), title)

    def _verify_title(self, assertion, title):
        fake_environ = self._get_fake_environ(title)
        self._verify_title_env(assertion, fake_environ)

    def _verify_title_env(self, assertion, fake_environ):
        self.verify_with_env(assertion, envreader.podcast_title, fake_environ)

    def _get_fake_environ(self, episode_title):
        return {'GPODDER_CHANNEL_TITLE': episode_title}

class TestEnvReader_PublicationTimestamp(_TestEnvReader_Base):
    def test_should_be_set_as_int_from_environ(self):
        anonymousTimestamp = 1234567890
        self._verify_equal_timestamp(anonymousTimestamp, str(anonymousTimestamp))

    def test_should_be_None_when_empty(self):
        self._verify_timestamp(self.assertIsNone, '')

    def test_should_be_None_when_not_a_number(self):
        self._verify_timestamp(self.assertIsNone, '123x')

    def test_should_be_None_when_missing(self):
        self._verify_timestamp_env(self.assertIsNone, {})

    def _verify_equal_timestamp(self, expected, timestamp):
        self._verify_timestamp(self.assertEqualC(expected), timestamp)

    def _verify_timestamp(self, assertion, timestamp):
        fake_environ = self._get_fake_environ(timestamp)
        self._verify_timestamp_env(assertion, fake_environ)

    def _verify_timestamp_env(self, assertion, fake_environ):
        self.verify_with_env(assertion, envreader.episode_timestamp, fake_environ)

    def _get_fake_environ(self, episode_timestamp):
        return {'GPODDER_EPISODE_PUBDATE': episode_timestamp}

if __name__ == '__main__':
    unittest.main()
