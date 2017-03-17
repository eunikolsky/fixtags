#!/usr/bin/env python3

from processor import EpisodeTags

import stagger

def stagger_read_tags(filepath):
    """Reads podcast's tags from the file at `filepath` into `EpisodeTags`.

    NB: stagger returns an empty string if the tag is missing when asked by
    "friendly name". so empty strings are mapped into `None`.

    `stagger_read_tags :: FilePath -> EpisodeTags`
    """

    try:
        tag = stagger.read_tag(filepath)

        tag_or_none = lambda x: x if (x != '') and (x != 0) else None
        fields = [tag.album, tag.artist, tag.comment, tag.composer, tag.genre,
                tag.title, tag.track, tag.date]

        return EpisodeTags(*(tag_or_none(f) for f in fields))
    except stagger.errors.NoTagError:
        return EpisodeTags(*([None] * len(EpisodeTags._fields)))
