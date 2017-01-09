#!/usr/bin/env python3

import collections

EpisodeInfo = collections.namedtuple('EpisodeInfo',
        ['episode_title', 'episode_filename', 'podcast_title'])
'''A tuple containing episode information from gPodder.'''

def get_episode_info(environ):
    '''Reads episode information, supplied by gPodder via environment
    variables.

    Args:
        environ (Dict): The environment variables dictionary, compatible
            with `os.environ`.
    '''

    KEYS = ['GPODDER_EPISODE_TITLE',
            'GPODDER_EPISODE_FILENAME',
            'GPODDER_CHANNEL_TITLE']
    return EpisodeInfo(*map(environ.get, KEYS))

# Getter functions
episode_title = lambda x: x.episode_title
episode_filename = lambda x: x.episode_filename
podcast_title = lambda x: x.podcast_title
