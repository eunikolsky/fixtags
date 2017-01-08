#!/usr/bin/env python3

import envreader

import unittest

class TestEnvReader_EpisodeTitle(unittest.TestCase):
    def test_should_be_set_from_environ(self):
        anonymousTitle = 'anonymousTitle'
        fake_environ = self._get_fake_environ(anonymousTitle)

        info = envreader.get_episode_info(fake_environ)

        self.assertEqual(info.episode_title, anonymousTitle)

    def test_should_be_empty_when_empty(self):
        emptyTitle = ''
        fake_environ = self._get_fake_environ(emptyTitle)

        info = envreader.get_episode_info(fake_environ)

        self.assertEqual(info.episode_title, emptyTitle)

    def test_should_be_None_when_missing(self):
        fake_environ = {}

        info = envreader.get_episode_info(fake_environ)

        self.assertIsNone(info.episode_title)

    def _get_fake_environ(self, episode_title):
        return {'GPODDER_EPISODE_TITLE': episode_title}

if __name__ == '__main__':
    unittest.main()
