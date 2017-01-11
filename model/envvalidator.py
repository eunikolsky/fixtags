#!/usr/bin/env python3

import collections

EpisodeInfo = collections.namedtuple('EpisodeInfo',
        ['episode_title'])
'''A tuple containing validated episode information from gPodder.'''

def validate_episode_info(raw):
    '''Validates the `RawEpisodeInfo` object and returns a valid
    `EpisodeInfo` object or `None`.

    To be valid, the raw episode info must meet ALL of the criteria:
    * `episode_title` is not `None`.

    `validate_episode_info :: RawEpisodeInfo -> Maybe EpisodeInfo`
    '''

    return (EpisodeInfo(raw.episode_title)
            if raw.episode_title
            else None)
