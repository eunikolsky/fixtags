#!/usr/bin/env python3

from envvalidator import EpisodeInfo
from processor import EpisodeFix, EpisodeTags, process, post_process

import unittest

def _episode_tags(genre=None, year=None):
    return EpisodeTags(genre=genre, year=year)

class TestProcessor(unittest.TestCase):
    def test_should_return_None_when_no_fixes(self):
        info = EpisodeInfo('', '', '', 0)
        no_fixes = []
        tags = _episode_tags()

        ptags = process(no_fixes, info, tags)

        self.assertIsNone(ptags)

    def test_should_return_None_when_no_matching_fixes(self):
        class FalseFix(EpisodeFix):
            def canFix(self, _): return False
            def fix(self, _, __): return _episode_tags()

        info = EpisodeInfo('', '', '', 0)
        fixes = [FalseFix(), FalseFix()]
        tags = _episode_tags()

        ptags = process(fixes, info, tags)

        self.assertIsNone(ptags)

    def test_should_return_None_when_more_than_one_matching_fixes(self):
        class FakeFix(EpisodeFix):
            def canFix(self, _): return True
            def fix(self, _, __): return _episode_tags()

        info = EpisodeInfo('', '', '', 0)
        fixes = [FakeFix(), FakeFix()]
        tags = _episode_tags()

        ptags = process(fixes, info, tags)

        self.assertIsNone(ptags)

    def test_should_return_fixed_tags_when_exactly_one_matching_fix(self):
        class FakeFix(EpisodeFix):
            def __init__(self, expected_title, fixed_tags):
                self.expected_title = expected_title
                self.fixed_tags = fixed_tags

            def canFix(self, episode_title): return episode_title == self.expected_title
            def fix(self, _, __): return self.fixed_tags

        title = 'FooBar'
        info = EpisodeInfo(title, '', '', 0)
        expected_tags = _episode_tags(genre='Z', year=1999)
        fixes = [
                FakeFix('not FooBar', _episode_tags()),
                FakeFix(title, expected_tags),
                FakeFix('AbCxYz', _episode_tags())
                ]
        tags = _episode_tags()

        ptags = process(fixes, info, tags)

        self.assertEqual(ptags, expected_tags)

class TestPostProcessor(unittest.TestCase):
    def test_should_set_year_from_episode_info(self):
        anonymousYear = 2020
        info = EpisodeInfo('', '', '', anonymousYear)
        tags = _episode_tags(year=None)
        ptags = post_process(info, tags)
        self.assertEqual(ptags.year, anonymousYear)

    def test_should_overwrite_year_from_episode_info(self):
        anonymousYear = 1980
        info = EpisodeInfo('', '', '', anonymousYear)
        tags = _episode_tags(year=2008)
        ptags = post_process(info, tags)
        self.assertEqual(ptags.year, anonymousYear)

    def test_should_set_genre_to_Podcast(self):
        info = EpisodeInfo('', '', '', 0)
        tags = _episode_tags(genre=None)
        ptags = post_process(info, tags)
        self.assertEqual(ptags.genre, 'Podcast')

if __name__ == '__main__':
    unittest.main()
