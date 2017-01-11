#!/usr/bin/env python3

import collections

RawEpisodeInfo = collections.namedtuple('RawEpisodeInfo',
        ['episode_title', 'episode_filename', 'podcast_title', 'episode_timestamp'])
'''A tuple containing raw, parse episode information from gPodder.'''

def get_episode_info(environ):
    '''Reads episode information, supplied by gPodder via environment
    variables.

    `get_episode_info :: Dict -> RawEpisodeInfo`

    Args:
        environ (Dict): The environment variables dictionary, compatible
            with `os.environ`.
    '''

    def parse_timestamp(key):
        try:
            return int(environ[key])
        except (ValueError, KeyError):
            return None

    KEYS = ['GPODDER_EPISODE_TITLE',
            'GPODDER_EPISODE_FILENAME',
            'GPODDER_CHANNEL_TITLE']
    pubdate = parse_timestamp('GPODDER_EPISODE_PUBDATE')
    return RawEpisodeInfo(*map(environ.get, KEYS), pubdate)

# Getter functions
episode_title = lambda x: x.episode_title
episode_filename = lambda x: x.episode_filename
podcast_title = lambda x: x.podcast_title
episode_timestamp = lambda x: x.episode_timestamp
