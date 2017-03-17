#!/usr/bin/env python3

# integration tests for the stagger-based tag reader.
# these are not unit tests, because they have to talk with the filesystem

from processor import EpisodeTags
from tagreader import stagger_read_tags, stagger_write_tags

import stagger

import os
import os.path
import shutil
import unittest

class Const:
    CWD = os.path.dirname(__file__)
    SRC_DIRNAME = 'test_files'
    DST_DIRNAME = 'test_dst_files'

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
        return os.path.join(Const.CWD, Const.SRC_DIRNAME, name)


class TestStaggerTagWriter(unittest.TestCase):
    DST_DIR = os.path.join(Const.CWD, Const.DST_DIRNAME)

    @classmethod
    def setUpClass(cls):
        if os.path.exists(cls.DST_DIR):
            shutil.rmtree(cls.DST_DIR)
        os.mkdir(cls.DST_DIR)

    def test_should_write_EpisodeTags_to_file_without_tags(self):
        tags = EpisodeTags(
                album='Album',
                artist='Artist',
                comment='Comment',
                composer='Composer',
                genre='Podcast',
                title='Title',
                track_number=642,
                year='2022'
                )
        filepath = self._prepared_testfilepath('no_fields.mp3')
        stagger_write_tags(filepath, tags)

        actual = stagger.read_tag(filepath)
        self.assertEqual(actual.album, tags.album)
        self.assertEqual(actual.artist, tags.artist)
        self.assertEqual(actual.comment, tags.comment)
        self.assertEqual(actual.composer, tags.composer)
        self.assertEqual(actual.genre, tags.genre)
        self.assertEqual(actual.title, tags.title)
        self.assertEqual(actual.track, tags.track_number)
        self.assertEqual(actual.date, tags.year)


    def test_should_update_set_EpisodeTags_in_file_with_tags(self):
        tags = EpisodeTags(
                album='### foo',
                artist='### megaBAR',
                comment=None,
                composer=None,
                genre=None,
                title='### BAZ',
                track_number=1,
                year=None
                )
        filepath = self._prepared_testfilepath('all_tags.mp3')
        original = stagger.read_tag(filepath)
        stagger_write_tags(filepath, tags)

        actual = stagger.read_tag(filepath)
        self.assertEqual(actual.album, tags.album)
        self.assertEqual(actual.artist, tags.artist)
        self.assertEqual(actual.title, tags.title)
        self.assertEqual(actual.track, tags.track_number)
        self.assertEqual(actual.comment, original.comment)
        self.assertEqual(actual.composer, original.composer)
        self.assertEqual(actual.genre, original.genre)
        self.assertEqual(actual.date, original.date)

    def _prepared_testfilepath(self, name):
        dst_file = os.path.join(self.DST_DIR, name)
        src_file = os.path.join(Const.CWD, Const.SRC_DIRNAME, name)
        shutil.copyfile(src_file, dst_file)
        return dst_file

if __name__ == '__main__':
    unittest.main()
