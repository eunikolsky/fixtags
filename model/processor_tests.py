#!/usr/bin/env python3

from envvalidator import EpisodeInfo
from processor import EpisodeTags, post_process

import unittest

class TestPostProcessor(unittest.TestCase):
    def test_should_set_year_from_episode_info(self):
        anonymousYear = 2020
        info = EpisodeInfo('', '', '', anonymousYear)
        tags = EpisodeTags(year=None)
        ptags = post_process(info, tags)
        self.assertEqual(ptags.year, anonymousYear)

    def test_should_overwrite_year_from_episode_info(self):
        anonymousYear = 1980
        info = EpisodeInfo('', '', '', anonymousYear)
        tags = EpisodeTags(year=2008)
        ptags = post_process(info, tags)
        self.assertEqual(ptags.year, anonymousYear)

if __name__ == '__main__':
    unittest.main()
