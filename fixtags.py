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

    # do we have ID3 tags?
    has_v2 = has_v1 = True

    # try to read ID3v2 tags
    try:
        tag2 = stagger.read_tag(episode_fname)
    except stagger.errors.NoTagError as e:
        has_v2 = False

    # try to read ID3v1 tags (in cp1251)
    try:
        tag = stagger.id3v1.Tag1.read(episode_fname, encoding='cp1251')
    except stagger.errors.NoTagError as e:
        has_v1 = False

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

