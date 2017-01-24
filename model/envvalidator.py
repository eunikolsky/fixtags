#!/usr/bin/env python3

import collections
import datetime

EpisodeInfo = collections.namedtuple('EpisodeInfo',
        ['episode_title', 'episode_filename', 'podcast_title', 'episode_year'])
'''A tuple containing validated episode information from gPodder.'''

def validate_episode_info(raw):
    '''Validates the `RawEpisodeInfo` object and returns a valid
    `EpisodeInfo` object or `None`.

    TODO return a list of errors if failed

    To be valid, the raw episode info must meet ALL of the criteria:
    * `episode_title` is not `None`
    * `episode_filename` is not `None`
    * `podcast_title` is not `None`
    * `episode_timestamp` is not `None`
    * TODO check input types

    `validate_episode_info :: RawEpisodeInfo -> Maybe EpisodeInfo`
    '''

    valid = (
            (raw.episode_title is not None)
            and (raw.episode_filename is not None)
            and (raw.podcast_title is not None)
            and (raw.episode_timestamp is not None)
            )
    year = lambda ts: datetime.date.fromtimestamp(ts).year

    return (EpisodeInfo(
        raw.episode_title
        , raw.episode_filename
        , raw.podcast_title
        , year(raw.episode_timestamp)
        ) if valid else None)
