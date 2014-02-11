#!/usr/bin/env python3

# Author: pluton <pluton.od (at) gmail.com>
# License: GPL v3

import os
import sys
import logging
import datetime

logger = None
episode_fname = ''


class WrongInvocationError(Exception):
    '''This error is thrown when the script is invoked not from gPodder.'''
    pass


def setupLogging():
    '''Set up the logging system.

    Use the global `logger` object to log events in the app.
    '''

    global logger
    logger = logging.getLogger(sys.argv[0])
    logger.setLevel(logging.DEBUG)

    # use file output
    LOG_FILENAME = os.path.join(os.path.dirname(sys.argv[0]), 'fixtags.log')
    filelog = logging.FileHandler(LOG_FILENAME, 'a')
    filelog.setLevel(logging.DEBUG)

    # use console
    conlog = logging.StreamHandler()
    conlog.setLevel(logging.DEBUG)

    # specify log formatting
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(lineno)s - %(levelname)s - %(message)s")
    conlog.setFormatter(formatter)
    filelog.setFormatter(formatter)

    logger.addHandler(conlog)
    logger.addHandler(filelog)

def setup():
    '''Initialize the app.'''
    setupLogging()

def main():
    # get episode info from the environment variables
    global episode_fname
    try:
        episode_title = os.environ['GPODDER_EPISODE_TITLE']
        episode_fname = os.environ['GPODDER_EPISODE_FILENAME']
        channel_title = os.environ['GPODDER_CHANNEL_TITLE']
        episode_pubdate = int(float(os.environ['GPODDER_EPISODE_PUBDATE']))
    except KeyError:
        print("""This script should be run by gPodder. Put its path and filename ({0}) as the argument to 'cmd_download_complete' option.
For more information, go to 'http://wiki.gpodder.org/wiki/User_Manual#Time_stretching_.28making_playback_slower_or_faster.29', the 'Using the post-download script hook' section.""".format(os.path.abspath(sys.argv[0])), file=sys.stderr)
        raise WrongInvocationError()
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

    elif channel_title == 'Институт разнородных вещиц':
        # read v1 tags and move them to v2, converting to utf-8 on the way
        tag = stagger.id3v1.Tag1.read(episode_fname, encoding='cp1251')
        tag2 = stagger.Tag24()
        tag2.title = episode_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.artist = tag.artist
        tag2.album = channel_title
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)

    elif channel_title == 'Зомбо-Ящик':
        # read v1 tags and move them to v2, converting to utf-8 on the way
        tag = stagger.id3v1.Tag1.read(episode_fname, encoding='cp1251')
        tag2 = stagger.Tag24()
        tag2.title = episode_title[27:]
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.artist = tag.artist
        tag2.album = channel_title
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)

    elif channel_title == 'Escape from Cubicle Nation Podcast':
        # set all v2 tags and remove v1
        tag2 = stagger.Tag24()
        tag2.title = episode_title
        tag2.artist = 'Pamela Slim'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)

    elif channel_title == 'Начинающий инвестор':
        # set all v2 tags and remove v1
        tag2 = stagger.Tag24()
        tag2.title = episode_title
        tag2.artist = 'Дмитрий Дмитриев'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)

    elif channel_title == 'EconTalk':
        # set all v2 tags
        tag2 = stagger.Tag24()
        tag2.title = episode_title
        tag2.artist = 'Russ Roberts'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write(episode_fname)

    elif channel_title == 'The Naked Scientists':
        # set all v2 tags
        tag2 = stagger.Tag24()
        tag2.title = episode_title[17:]
        tag2.artist = 'Chris Smith et al.'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write(episode_fname)

    elif channel_title == 'The Stack Exchange Podcast':
        # set all v2 tags
        tag2 = stagger.Tag24()
        tag2.title = episode_title
        tag2.artist = 'Jeff and Joel'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write(episode_fname)

    elif channel_title == 'Application Developer Days':
        # set all v2 tags
        tag2 = stagger.Tag24()
        import re
        parts = re.search(r'([^(]*) \((.*) на [^)]*\)', episode_title,
                flags=re.IGNORECASE)
        tag2.title = parts.group(1)
        tag2.artist = parts.group(2)
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write(episode_fname)

    elif channel_title == 'Wordmaster':
        # set all v2 tags
        tag2 = stagger.Tag24()
        tag2.title = episode_title[12:]
        tag2.artist = 'VOA'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write(episode_fname)

    elif channel_title == 'Fun English Lessons':
        # set all v2 tags
        tag2 = stagger.Tag24()
        tag2.title = episode_title
        tag2.artist = 'two Canadian brothers'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write(episode_fname)

    elif channel_title == 'Learn English Funcast':
        # set all v2 tags
        tag2 = stagger.Tag24()
        tag2.title = episode_title
        tag2.artist = 'Ron G'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write(episode_fname)

    elif channel_title == 'Все о США в подкастах':
        # set all v2 tags and remove v1
        tag2 = stagger.Tag24()
        tag2.title = episode_title
        tag2.artist = 'Тимур Тажетдинов'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)

    elif channel_title == 'Science Friday':
        # set all v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.artist = 'Ira Flatow'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)

    elif channel_title == 'Поверх барьеров - Американский час - Радио Свобода':
        # set all v2 tags and remove v1
        tag2 = stagger.Tag24()
        tag2.artist = 'Александр Генис'
        tag2.title = episode_title[37:]
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.composer = 'RFE/RL Russian Service'
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)

    elif channel_title == 'Америчка':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2.date = episode_year
        tag2.write()

    elif channel_title == 'Sick and Wrong':
        # fix some v2 tags
        try:
            tag2 = stagger.read_tag(episode_fname)
        except stagger.errors.NoTagError:
            tag2 = stagger.Tag24()
        tag2.artist = 'Dee Simon, Lance Wackerle'
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2.title = episode_title
        tag2.date = episode_year
        tag2.write(episode_fname)

    elif channel_title == 'Mysterious Universe':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.artist = 'Benjamin Grundy, Aaron Wright'
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'FLOSS Weekly':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Радио Бермудский Треугольник':
        # don't know what to do. it seems the podcast has changeable tags
        logger.warning('Please check the latest episode of {0}'.format(
            channel_title))
        #tag2 = stagger.read_tag(episode_fname)
        #tag2.title = tag2.album
        #tag2.album = channel_title
        #tag2.write()

    elif channel_title == 'This American Life':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.artist = 'Ira Glass'
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Evergreen':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2.comment = ''
        tag2.write()

    elif channel_title == 'The Linux Admin Show':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2.comment = ''
        tag2.write()

    elif channel_title == 'Freakonomics Radio':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.composer = tag2.artist
        tag2.artist = 'Steven D. Levitt, Stephen J. Dubner'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'Янки после пьянки':
        # fix some v2 tags and remove v1
        try:
            tag2 = stagger.read_tag(episode_fname)
        except stagger.errors.NoTagError:
            tag2 = stagger.Tag24()
        tag2.title = episode_title
        tag2.artist = 'Янки после пьянки'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)

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
        tag2.title = episode_title
        tag2.artist = 'Cristen and Caroline'
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'BrainStuff':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.artist = 'Marshall Brain'
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'Stuff To Blow Your Mind':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.artist = 'Robert and Julie'
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'Stuff You Should Know':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.artist = 'Josh Clark and Chuck Bryant'
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'Подкаст Кадры':
        # move v2.2 to v2.4 tags
        tag22 = stagger.read_tag(episode_fname)
        tag2 = stagger.Tag24()
        tag2.artist = tag22.artist
        tag2.album = channel_title
        tag2.title = tag22.title[14:]
        tag2.genre = 'Podcast'
        tag2.date = tag22.date
        tag2.write(episode_fname)

    elif channel_title == 'Machine of Death':
        # move v2.2 to v2.4 tags
        tag22 = stagger.read_tag(episode_fname)
        tag2 = stagger.Tag24()
        tag2.artist = tag22.artist
        tag2.album = channel_title
        tag2.title = tag22.title
        tag2.genre = 'Podcast'
        tag2.date = episode_year
        tag2.write(episode_fname)

    elif channel_title.startswith('English as a Second Language'):
        # move v2.2 to v2.4 tags
        tag22 = stagger.read_tag(episode_fname)
        tag2 = stagger.Tag24()
        tag2.artist = tag22.artist
        tag2.album = channel_title
        tag2.title = tag22.title
        tag2.genre = 'Podcast'
        tag2.date = episode_year
        tag2.comment = tag22.comment
        tag2.write(episode_fname)

    elif channel_title == 'www.BreakingNewsEnglish.com':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Wide Teams':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.album = channel_title
        tag2.write()

    elif channel_title == 'Radiolab':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'happy friday podcast from gAmUssA ;-)':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.album = channel_title
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
        # move v2.2 to v2.4 tags and remove v1
        tag22 = stagger.read_tag(episode_fname)
        tag2 = stagger.Tag24()
        tag2.artist = tag22.artist
        tag2.album = channel_title
        tag2.title = tag22.title[36:]
        tag2.genre = 'Podcast'
        tag2.date = episode_year
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)

    elif channel_title == 'Ask the Naked Scientists':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title[39:]
        tag2.artist = 'Chris Smith'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Listen to English':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'ЗаБугром Podcast':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.artist = 'Costya (aka sway)'
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2['COM'] = []
        tag2.write()

    elif channel_title == 'All In The Mind':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.album = channel_title
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
        tag2.title = episode_title
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2['COM'] = []
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'NPR: Intelligence Squared Podcast':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.album = 'Intelligence Squared'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'Подкаст из Силиконовой Долины':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.artist = 'Alex'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'Канадский Лось':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        title = episode_title[41:]
        if title == '':
            title = episode_title
        tag2.title = title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif ((channel_title == 'сегодня четверг - dugwin') or
            (channel_title == 'dugwin j. goines // podcast')):
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.artist = 'dugwin'
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'edUKation.com.ua':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title[22:]
        tag2.artist = 'Дмитрий Дмитриев'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'NPR: Planet Money':
        # fix some v2 tags and remove v1
        tag2 = stagger.Tag24()
        tag2.title = episode_title
        tag2.artist = 'Robert Smith'
        tag2.album = 'Planet Money'
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)

    elif channel_title == 'Разбор Полетов':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title[13:]
        tag2.date = episode_year
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)

    elif channel_title == 'The Adam Carolla Show':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write(episode_fname)

    elif channel_title == 'Chiptune - 8-bit game music podcast':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.artist = 'Дмитрий Зомбак'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        del tag2['COMM']
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'Software Engineering Radio':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Ирландское рагу by Emaster':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.artist = 'Emaster'
        tag2.album = channel_title
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
        tag2.album = channel_title
        tag2.write()

    elif channel_title == 'Common Sense with Dan Carlin':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.album = 'Common Sense'
        tag2.write()

    elif channel_title == 'EnglishLingQ':
        # fix some v2 tags
        try:
            tag2 = stagger.read_tag(episode_fname)
        except stagger.errors.NoTagError:
            tag2 = stagger.Tag24()
        import re
        parts = re.search(r'^\#(\d{1,3}) (?:[-–] )?([^-–]+) [-–] (.+)$',
                episode_title, flags=re.IGNORECASE)
        tag2.title = parts.group(3) if parts else episode_title
        tag2.artist = parts.group(2) if parts else 'Steve and Alex'
        #tag2.track = parts.group(1)
        tag2.genre = 'Podcast'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.write(episode_fname)

    elif channel_title == 'TuxRadar Linux Podcast':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Just Vocabulary':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.artist = 'Jan Folmer'
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2['COM'] = []
        tag2.write()

    elif channel_title == 'PODъезд. Записки со всего света':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.genre = 'Podcast'
        tag2.date = episode_year
        tag2.write()

    elif channel_title == 'Плёнки':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'A Way with Words':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'www.it4business.ru':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.artist = 'Слава Панкратов'
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2.date = episode_year
        tag2.write()

    elif channel_title == 'Fonarev':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'happypm':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title[:-15]
        tag2.artist = 'Слава Панкратов, Саша Орлов'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'No Agenda':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Неуёмная жажда жизни!':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'scene':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Казах в Канаде':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.album = channel_title
        tag2.title = episode_title
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'The English We Speak':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title[22:]
        tag2.write()

    elif channel_title == 'Nunavut':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title[20:]
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Sex Nerd Sandra':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.album = channel_title
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Dolce Welle - подкаст из Европы':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.artist = 'Alex'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Заметки о Qt':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'No BS IT':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.artist = 'Budam'
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'The Changelog':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.date = episode_year
        tag2.write()

    elif channel_title == 'Dr.Shadow из Британии':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.album = channel_title
        tag2.title = episode_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'The Haskell Cast':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'The raywenderlich.com Podcast':
        # fix some v2 tags
        tag2 = stagger.read_tag(episode_fname)
        tag2.genre = 'Podcast'
        tag2.write()

    elif channel_title == 'Healthcare IT Podcast':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'Подкаст 42':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.title = episode_title
        tag2.album = channel_title
        tag2.date = episode_year
        tag2.genre = 'Podcast'
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'The World in Words':
        # fix some v2 tags and remove v1
        tag2 = stagger.read_tag(episode_fname)
        tag2.album = channel_title
        stagger.id3v1.Tag1.delete(episode_fname)
        tag2.write()

    elif channel_title == 'Откровенно про IT-карьеризм':
        # remove v1
        stagger.id3v1.Tag1.delete(episode_fname)

    elif channel_title == 'Manager Tools':
        # remove picture element from v2.2 and fix date
        tag2 = stagger.read_tag(episode_fname)
        tag2.picture = []
        tag2.date = episode_year
        tag2.write()

    elif channel_title == 'Career Tools':
        # remove picture element from v2.2
        tag2 = stagger.read_tag(episode_fname)
        tag2.picture = []
        tag2.write()

    elif channel_title == 'UWP - Eженедельный подкаст от Umputun':
        # nothing to fix here
        pass

    elif channel_title == 'Talk About English (Learn English)':
        # nothing to fix here
        pass

    elif channel_title == 'Раша: Азбука Выживания':
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

    elif channel_title == 'The Skeptics Guide to the Universe':
        # nothing to fix here
        pass

    elif channel_title == 'this WEEK in TECH':
        # nothing to fix here
        pass

    elif channel_title == 'Radio Grinch':
        # nothing to fix here
        pass

    elif channel_title == 'Adam Curry\'s Daily Source Code':
        # nothing to fix here
        pass

    elif channel_title == 'Секспертиза':
        # nothing to fix here
        pass

    elif channel_title == 'Friends House':
        # nothing to fix here
        pass

    elif channel_title == 'Security Now!':
        # nothing to fix here
        pass

    elif channel_title == 'Software Indie':
        # nothing to fix here
        pass

    elif channel_title == 'Build Phase':
        # nothing to fix here
        pass

    elif channel_title == 'Functional Geekery':
        # nothing to fix here
        pass

    else:
        logger.info("No fixes for the episode. GPODDER_EPISODE_TITLE='{0}' "
            "GPODDER_EPISODE_FILENAME='{1}' GPODDER_CHANNEL_TITLE='{2}' "
            "GPODDER_EPISODE_PUBDATE='{3}'".format(episode_title,
                episode_fname, channel_title, episode_pubdate))

if __name__ == '__main__':
    try:
        setup()
        import stagger
        main()
    except ImportError:
        logger.critical("Couldn't import stagger! Please check.")
        sys.exit(3)
    except WrongInvocationError:
        # don't panic on this error
        pass
    except:
        # if happens something that we didn't foresee,
        # print traceback to the log
        import traceback
        logger.exception("An exception occurred with file '{}'".format(episode_fname))
        sys.exit(2)

