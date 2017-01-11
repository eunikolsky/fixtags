#!/usr/bin/env python3

from envreader import RawEpisodeInfo
import envvalidator

import unittest

class TestEnvValidator(unittest.TestCase):
    def test_should_copy_episode_title(self):
        anonymousTitle = 'anonymousTitle'
        info = RawEpisodeInfo(anonymousTitle, '', '', 0)
        validated = envvalidator.validate_episode_info(info)
        self.assertEqual(validated.episode_title, anonymousTitle)

    def test_no_episode_title_should_return_None(self):
        info = RawEpisodeInfo(None, '', '', 0)
        validated = envvalidator.validate_episode_info(info)
        self.assertIsNone(validated)

if __name__ == '__main__':
    unittest.main()
