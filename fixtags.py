#!/usr/bin/env python

# Author: pluton <pluton.od (at) gmail.com>
# License: GPL v3

import os
import sys
import logging
import datetime

import stagger

def setup():
    '''Set up the logging system.'''

    LOG_FILENAME = os.path.join(os.path.dirname(sys.argv[0]), 'fixtags.log')
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

def main():
    # get episode info from the environment variables
    try:
        episode_title = os.environ['GPODDER_EPISODE_TITLE']
        episode_fname = os.environ['GPODDER_EPISODE_FILENAME']
        channel_title = os.environ['GPODDER_CHANNEL_TITLE']
        episode_pubdate = int(os.environ['GPODDER_EPISODE_PUBDATE'])
    except KeyError:
        print("""This script should be run by gPodder. Put its path and filename ({0}) as the argument to 'cmd_download_complete' option.
For more information, go to 'http://wiki.gpodder.org/wiki/User_Manual#Time_stretching_.28making_playback_slower_or_faster.29', the 'Using the post-download script hook' section.""".format(os.path.abspath(sys.argv[0])), file=sys.stderr)
        sys.exit(1)
    #print('Processing {0}'.format(episode_fname))

    # calculate the publication year
    episode_year = str(datetime.date.fromtimestamp(episode_pubdate).year)

    # test for podcasts that don't have ID3v2 tags
    # such as psychologist
    if channel_title == 'psychologist':
        # read ID3v1 tags and move them to ID3v2, converting to utf-8 on the way
        tag = stagger.id3v1.Tag1.read(episode_fname, encoding='cp1251')
        tag2 = stagger.Tag24()
        tag2.title = tag.title
        tag2.artist = tag.artist
        tag2.album = tag.album
        tag2.date = tag.year
        tag2.comment = tag.comment
        tag2.genre = 'Podcast'
        #tag2.genre = stagger.id3.genres[tag._genre]
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)
        return

    elif channel_title == 'Escape from Cubicle Nation Podcast':
        tag = stagger.id3v1.Tag1.read(episode_fname)
        tag2 = stagger.Tag24()
        tag2.title = episode_title
        tag2.artist = 'Escape from Cubicle Nation Podcast'
        tag2.date = tag.year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)
        return

    elif channel_title == 'EconTalk':
        tag2 = stagger.Tag24()
        tag2.title = episode_title
        tag2.artist = 'EconTalk'
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write(episode_fname)
        return

    elif channel_title == 'NPR: Science Friday Podcast':
        tag2 = stagger.Tag24()
        tag2.title = episode_title
        tag2.artist = 'Science Friday'
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.track = int(os.path.basename(episode_fname)[-6:-4])
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)
        return

    # open the file to change mp3 tags
    try:
        tag = stagger.read_tag(episode_fname)
    except stagger.errors.NoTagError as e:
        logging.error("{0} GPODDER_EPISODE_TITLE='{1}' "
            "GPODDER_EPISODE_FILENAME='{2}' GPODDER_CHANNEL_TITLE='{3}' "
            "GPODDER_EPISODE_PUBDATE='{4}'".format(e, episode_title,
                episode_fname, channel_title, episode_pubdate))
        return

    # do we need to update tags?
    update_flag = True

    # fix tags depending on the podcast
    if channel_title == 'Америчка':
        tag.title = tag.album
        tag.album = 'Америчка'

    elif channel_title == 'Sick and Wrong':
        tag.artist = 'Sick and Wrong'
        tag.genre = 'Podcast'

    elif channel_title == 'Mysterious Universe':
        tag.artist = 'Mysterious Universe'
        tag.genre = 'Podcast'

    elif channel_title == 'Радио Бермудский Треугольник':
        tag.title = tag.album
        tag.album = 'Радио Бермудский Треугольник'

    else:
        # if we don't know the podcast, don't change tags
        update_flag = False

    if update_flag:
        tag.write()

if __name__ == '__main__':
    try:
        setup()
        main()
    except:
        # if happens something that we didn't foresee,
        # print traceback to the log
        import traceback
        logging.exception("An exception occured")
        sys.exit(2)

