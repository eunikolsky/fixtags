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
        has_v1 = True
        try:
            tag = stagger.id3v1.Tag1.read(episode_fname, encoding='cp1251')
        except stagger.errors.NoTagError:
            # if there's no v1 tag, fill v2 from gPodder
            has_v1 = False
        tag2 = stagger.Tag24()
        tag2.title = episode_title[18:]
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        if has_v1:
            tag2.artist = tag.artist
            tag2.album = tag.album      # 'The PsychoPodcast'
            tag2.comment = tag.comment
            stagger.id3v1.Tag1.delete(episode_fname)
        else:
            tag2.artist = 'Mulder & Co'
            tag2.album = 'The PsychoPodcast'
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

    elif channel_title == 'The Naked Scientists - Stripping Down Science':
        # set all v2 tags
        tag2 = stagger.Tag24()
        tag2.title = episode_title[17:]
        tag2.artist = 'Chris Smith et al.'
        tag2.album = 'The Naked Scientists'
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

    elif channel_title == 'FLOSS Weekly':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
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
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Freakonomics Radio':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.composer = tag2.artist
        tag2.artist = 'Steven D. Levitt, Stephen J. Dubner'
        tag2.album = 'Freakonomics Radio'
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'Янки после пьянки':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.artist = 'Янки после пьянки'
        tag2.album = 'Янки после пьянки'
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'Радио "Свободная Деревня"':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'Stuff Mom Never Told You':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.artist = 'Cristen and Molly'
        tag2.album = 'Stuff Mom Never Told You'
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'BrainStuff':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.artist = 'Marshall Brain'
        tag2.album = 'BrainStuff'
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'Stuff To Blow Your Mind':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.artist = 'Robert and Julie'
        tag2.album = 'Stuff To Blow Your Mind'
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'Stuff You Should Know':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.artist = 'Josh Clark and Chuck Bryant'
        tag2.album = 'Stuff You Should Know'
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'Подкаст Кадры':
        # move v2.2 to v2.4 tags
        tag22 = stagger.read_tag(episode_fname)
        tag2 = stagger.Tag24()
        tag2.artist = tag22.artist
        tag2.album = tag22.album
        tag2.title = tag22.title[14:]
        tag2.genre = 'Podcast'
        tag2.date = tag22.date
        tag2.write(episode_fname)

    elif channel_title == 'Machine of Death':
        # move v2.2 to v2.4 tags
        tag22 = stagger.read_tag(episode_fname)
        tag2 = stagger.Tag24()
        tag2.artist = tag22.artist
        tag2.album = tag22.album
        tag2.title = tag22.title
        tag2.genre = 'Podcast'
        tag2.date = tag22.date
        tag2.write(episode_fname)

    elif channel_title == 'www.BreakingNewsEnglish.com':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Material World':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title.find('Quick and Dirty Tips') > 0:
        # move v2.2 to v2.4 tags
        tag22 = stagger.read_tag(episode_fname)
        tag2 = stagger.Tag24()
        tag2.artist = tag22.artist
        tag2.album = tag22.album
        tag2.title = tag22.title
        tag2.genre = 'Podcast'
        tag2.date = tag22.date
        tag2.track = tag22.track
        tag2.write(episode_fname)

    elif channel_title == 'The Art Of Programming':
        # move v2.2 to v2.4 tags
        tag22 = stagger.read_tag(episode_fname)
        tag2 = stagger.Tag24()
        tag2.artist = tag22.artist
        tag2.album = tag22.album
        tag2.title = tag22.title[32:]
        tag2.genre = 'Podcast'
        tag2.date = episode_year
        tag2.write(episode_fname)

    elif channel_title == 'Ask the Naked Scientists PODCAST':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title[39:]
        tag2.artist = 'Chris Smith'
        tag2.album = 'Ask the Naked Scientists'
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Listen to English':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.album = 'Listen to English'
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'NPR: Car Talk Podcast':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title[9:]
        tag2.artist = 'Click and Clack, the Tappet Brothers'
        tag2.album = 'Car Talk'
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title.startswith('60-Second '):
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.album = tag2.album[20:]
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'NPR: Intelligence Squared Podcast':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.album = 'Intelligence Squared'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'Software Engineering Radio':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.album = 'Software Engineering Radio'
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Chiptune - 8-bit game music podcast':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title[46:54] + episode_title[55:]
        tag2.artist = 'Дмитрий Зомбак'
        tag2.album = 'Chiptune - 8-bit game music podcast'
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Ирландское рагу by Emaster':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.artist = 'Emaster'
        tag2.album = 'Ирландское рагу by Emaster'
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Эхо Москвы. Точка':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.artist = 'Александр Плющев'
        tag2.composer = 'Эхо Москвы'
        tag2.album = 'Точка'
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Радио-Т' or channel_title == 'Пираты-РТ':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.date = episode_year
        tag2.write()

    elif channel_title == 'The Dave Ramsey Show':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.album = 'The Dave Ramsey Show'
        tag2.write()

    elif channel_title == 'Common Sense with Dan Carlin':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.album = 'Common Sense'
        tag2.write()

    elif channel_title == 'Manager Tools':
        # remove picture element from v2.2 and fix date
        tag2 = stagger.read_tag(episode_fname)
        tag2.picture = []
        tag2.date = episode_year
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

    elif channel_title == 'A Way with Words':
        # nothing to fix here
        pass

    elif channel_title == 'Discovery':
        # nothing to fix here
        pass

    elif channel_title == 'Охотник За Головами - Денис aka Radio Grinch':
        # nothing to fix here
        pass

    elif channel_title == '6 Minute English':
        # nothing to fix here
        pass

    elif channel_title == 'Learn English with BBCRussian':
        # nothing to fix here
        pass

    elif channel_title == 'The Java Posse':
        # nothing to fix here
        pass

    elif channel_title == 'Эксперт-шоу Рунетология':
        # nothing to fix here
        pass

    elif channel_title == 'Friday Night Comedy from BBC Radio 4':
        # nothing to fix here
        pass

    elif channel_title == 'The Skeptics\' Guide to the Universe':
        # nothing to fix here
        pass

    elif channel_title == 'this WEEK in TECH':
        # nothing to fix here
        pass

    elif channel_title == 'Radio Grinch':
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

