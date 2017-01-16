#!/usr/bin/env python3

import collections

EpisodeTags = collections.namedtuple('EpisodeTags', [
    'year'
    ])
'''Represents a set of tags for a podcast episode.'''

def post_process(episode_info, episode_tags):
    '''Applies common fixes for all podcasts' tags.'''

    return episode_tags._replace(year=episode_info.episode_year)
