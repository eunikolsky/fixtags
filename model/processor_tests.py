#!/usr/bin/env python3

from envvalidator import EpisodeInfo
from processor import EpisodeTags, post_process

import unittest

class TestPostProcessor(unittest.TestCase):
    def test_should_set_year_from_episode_info(self):
        anonymousYear = 2020
        info = EpisodeInfo('', '', '', anonymousYear)
        tags = self._episode_tags(year=None)
        ptags = post_process(info, tags)
        self.assertEqual(ptags.year, anonymousYear)

    def test_should_overwrite_year_from_episode_info(self):
        anonymousYear = 1980
        info = EpisodeInfo('', '', '', anonymousYear)
        tags = self._episode_tags(year=2008)
        ptags = post_process(info, tags)
        self.assertEqual(ptags.year, anonymousYear)

    def test_should_set_genre_to_Podcast(self):
        info = EpisodeInfo('', '', '', 0)
        tags = self._episode_tags(genre=None)
        ptags = post_process(info, tags)
        self.assertEqual(ptags.genre, 'Podcast')

    def _episode_tags(self, genre=None, year=None):
        return EpisodeTags(genre=genre, year=year)

if __name__ == '__main__':
    unittest.main()
