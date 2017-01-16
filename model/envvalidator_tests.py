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

    def test_should_copy_episode_filename(self):
        anonymousFilename = 'anonymousFilename'
        info = RawEpisodeInfo('', anonymousFilename, '', 0)
        validated = envvalidator.validate_episode_info(info)
        self.assertEqual(validated.episode_filename, anonymousFilename)

    def test_no_episode_filename_should_return_None(self):
        info = RawEpisodeInfo('', None, '', 0)
        validated = envvalidator.validate_episode_info(info)
        self.assertIsNone(validated)

    def test_should_copy_podcast_title(self):
        anonymousTitle = 'anonymousTitle'
        info = RawEpisodeInfo('', '', anonymousTitle, 0)
        validated = envvalidator.validate_episode_info(info)
        self.assertEqual(validated.podcast_title, anonymousTitle)

    def test_no_podcast_title_should_return_None(self):
        info = RawEpisodeInfo('', '', None, 0)
        validated = envvalidator.validate_episode_info(info)
        self.assertIsNone(validated)

    def test_should_convert_timestamp_to_year(self):
        info = RawEpisodeInfo('', '', '', 1583025003)
        validated = envvalidator.validate_episode_info(info)
        self.assertEqual(validated.episode_year, 2020)

    def test_no_timestamp_should_return_None(self):
        info = RawEpisodeInfo('', '', '', None)
        validated = envvalidator.validate_episode_info(info)
        self.assertIsNone(validated)

if __name__ == '__main__':
    unittest.main()
