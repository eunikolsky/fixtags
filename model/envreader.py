#!/usr/bin/env python3

import collections

EpisodeInfo = collections.namedtuple('EpisodeInfo', ['episode_title'])
'''A tuple containing episode information from gPodder.'''

def get_episode_info(environ):
    '''Reads episode information, supplied by gPodder via environment
    variables.

    Args:
        environ (Dict): The environment variables dictionary, compatible
            with `os.environ`.
    '''

    return EpisodeInfo(environ.get('GPODDER_EPISODE_TITLE'))
