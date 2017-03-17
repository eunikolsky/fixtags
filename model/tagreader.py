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

def stagger_write_tags(filepath, tags):
    """Write the `EpisodeTags` into the file at `filepath`.

    Existing tags, if any, are left as is unless overwritten from `tags`.

    `stagger_write_tags :: FilePath -> EpisodeTags -> ()`
    """

    def tag_key(episode_tags_key):
        tags_map = {
                'track_number': 'track',
                'year': 'date',
                }

        return tags_map.get(episode_tags_key, episode_tags_key)

    try:
        tag2 = stagger.read_tag(filepath)
    except stagger.errors.NoTagError:
        tag2 = stagger.Tag24()

    for (key, value) in tags._asdict().items():
        if value is not None:
            setattr(tag2, tag_key(key), value)

    tag2.write(filepath)
