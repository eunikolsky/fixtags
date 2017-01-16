#!/usr/bin/env python3

import collections

EpisodeTags = collections.namedtuple('EpisodeTags', [
    'genre'
    , 'year'
    ])
'''Represents a set of tags for a podcast episode.'''

def post_process(episode_info, episode_tags):
    '''Applies common fixes for all podcasts' tags.'''

    PODCAST_GENRE = 'Podcast'

    return episode_tags._replace(
            genre=PODCAST_GENRE,
            year=episode_info.episode_year)
