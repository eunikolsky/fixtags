#!/usr/bin/env python3

# integration tests for the stagger-based tag reader.
# these are not unit tests, because they have to talk with the filesystem

from processor import EpisodeTags
from tagreader import stagger_read_tags

import os.path
import unittest

class TestStaggerTagReader(unittest.TestCase):
    def test_should_return_EpisodeTags_from_file(self):
        tags = stagger_read_tags(self._testfilepath('all_tags.mp3'))
        expected = EpisodeTags(
                album='Album',
                artist='Artist',
                comment='Comment',
                composer='Composer',
                genre='Podcast',
                title='Title',
                track_number=642,
                year='2022'
                )
        self.assertEqual(tags, expected)

    def test_no_fields_should_return_EpisodeTags_with_None(self):
        tags = stagger_read_tags(self._testfilepath('no_fields.mp3'))
        expected = EpisodeTags(
                album=None,
                artist=None,
                comment=None,
                composer=None,
                genre=None,
                title=None,
                track_number=None,
                year=None
                )
        self.assertEqual(tags, expected)

    def _testfilepath(self, name):
        return os.path.join(os.path.dirname(__file__), 'test_files', name)

if __name__ == '__main__':
    unittest.main()
