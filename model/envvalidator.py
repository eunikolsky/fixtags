#!/usr/bin/env python3

import collections

EpisodeInfo = collections.namedtuple('EpisodeInfo',
        ['episode_title', 'episode_filename'])
'''A tuple containing validated episode information from gPodder.'''

def validate_episode_info(raw):
    '''Validates the `RawEpisodeInfo` object and returns a valid
    `EpisodeInfo` object or `None`.

    To be valid, the raw episode info must meet ALL of the criteria:
    * `episode_title` is not `None`
    * `episode_filename` is not `None`

    `validate_episode_info :: RawEpisodeInfo -> Maybe EpisodeInfo`
    '''

    valid = (
            (raw.episode_title is not None)
            and (raw.episode_filename is not None)
            )
    return (EpisodeInfo(raw.episode_title, raw.episode_filename) if valid else None)
