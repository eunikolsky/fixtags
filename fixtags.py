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

    # the main set of checks
    if channel_title == 'psychologist':
        # read v1 tags and move them to v2, converting to utf-8 on the way
        tag = stagger.id3v1.Tag1.read(episode_fname, encoding='cp1251')
        tag2 = stagger.Tag24()
        tag2.title = episode_title
        tag2.artist = tag.artist
        tag2.album = tag.album      # 'The PsychoPodcast'
        tag2.date = tag.year
        tag2.comment = tag.comment
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)

    elif channel_title == 'Escape from Cubicle Nation Podcast':
        # set all v2 tags and remove v1
        tag = stagger.id3v1.Tag1.read(episode_fname)
        tag2 = stagger.Tag24()
        tag2.title = episode_title
        tag2.artist = 'Pamela Slim'
        tag2.album = 'Escape from Cubicle Nation Podcast'
        tag2.date = tag.year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)

    elif channel_title == 'EconTalk':
        # set all v2 tags
        tag2 = stagger.Tag24()
        tag2.title = episode_title
        tag2.artist = 'Russ Roberts'
        tag2.album = 'EconTalk'
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write(episode_fname)

    elif channel_title == 'NPR: Science Friday Podcast':
        # set all v2 tags and remove v1
        tag2 = stagger.Tag24()
        tag2.title = episode_title
        tag2.artist = 'Ira Flatow'
        tag2.album = 'Science Friday'
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.track = int(os.path.basename(episode_fname)[-6:-4])
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)

    elif channel_title == 'Америчка':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = tag2.album
        tag2.album = 'Америчка'
        tag2.write()

    elif channel_title == 'Sick and Wrong':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.artist = 'Dee Simon, Lance Wackerle'
        tag2.album = 'Sick and Wrong'
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Mysterious Universe':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.artist = 'Benjamin Grundy, Aaron Wright'
        tag2.album = 'Mysterious Universe'
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Радио Бермудский Треугольник':
        # don't know what to do. it seems the podcast has changeable tags
        logging.warning('Please check the latest episode of {0}'.format(
            channel_title))
        #tag2 = stagger.read_tag(episode_fname)
        #tag2.title = tag2.album
        #tag2.album = 'Радио Бермудский Треугольник'
        #tag2.write()

    elif channel_title == 'This American Life':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.artist = 'Ira Glass'
        tag2.album = 'This American Life'
        tag2.write()

    elif channel_title == 'No Agenda':
        # nothing to fix here. In the Morning!
        pass

    elif channel_title == 'Еженедельный подкаст от Umputun':
        # nothing to fix here
        pass

    elif channel_title == 'All in the Mind':
        # nothing to fix here
        pass

    elif channel_title == 'Talk About English (Learn English)':
        # nothing to fix here
        pass

    elif channel_title == 'Раша: Азбука Выживания':
        # nothing to fix here
        pass

    elif channel_title == 'English as a Second Language Podcast':
        # nothing to fix here
        pass

    else:
        logging.info("No fixes for the episode. GPODDER_EPISODE_TITLE='{0}' "
            "GPODDER_EPISODE_FILENAME='{1}' GPODDER_CHANNEL_TITLE='{2}' "
            "GPODDER_EPISODE_PUBDATE='{3}'".format(episode_title,
                episode_fname, channel_title, episode_pubdate))

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

