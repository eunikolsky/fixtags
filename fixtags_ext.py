# -*- coding: utf-8 -*-

import gpodder

# Use a logger for debug output - this will be managed by gPodder
import logging
logger = logging.getLogger(__name__)

# Provide some metadata that will be displayed in the gPodder GUI
__title__ = 'fixtags Extension'
__description__ = 'Fixes mp3 tags in podcasts for Sandisk music players.'
__authors__ = 'Eugene Nikolsky <pluton.od@gmail.com>'
__category__ = 'post-download'

# Keys for the internal info dictionary.
class Key:
    FILENAME = 'filename'
    EPISODE_TITLE = 'episode_title'
    CHANNEL_TITLE = 'channel_title'
    EPISODE_PUBDATE = 'episode_pubdate'

class gPodderExtension:
    # The extension will be instantiated the first time it's used
    # You can do some sanity checks here and raise an Exception if
    # you want to prevent the extension from being loaded.
    def __init__(self, container):
        self.container = container

    # This function is called when an episode has been downloaded.
    # The episode param is a gpodder.model.PodcastEpisode instance.
    def on_episode_downloaded(self, episode):
        info = self.get_episode_info(episode)
        logger.info(u'on_episode_downloaded (filename="%s", '
                u'episode_title="%s", channel_title="%s", '
                u'episode_pubdate="%d")' %
                (info[Key.FILENAME],
                    info[Key.EPISODE_TITLE],
                    info[Key.CHANNEL_TITLE],
                    info[Key.EPISODE_PUBDATE]))

    # Gets necessary info from the episode object into a dictionary with
    # the keys specified earlier. The keys actually correspond to the values
    # gPodder 2 used when calling an external post-download script.
    def get_episode_info(self, episode):
        info = {
                Key.FILENAME: None,
                Key.EPISODE_TITLE: None,
                Key.CHANNEL_TITLE: None,
                Key.EPISODE_PUBDATE: None
        }

        info[Key.FILENAME] = episode.local_filename(create=False,
                check_only=True)
        info[Key.EPISODE_TITLE] = episode.trimmed_title
        info[Key.CHANNEL_TITLE] = episode.channel.title
        info[Key.EPISODE_PUBDATE] = episode.published

        return info

    # This function will be called when the extension is enabled or
    # loaded. This is when you want to create helper objects or hook
    # into various parts of gPodder.
    #def on_load(self):
        #logger.info('Extension is being loaded.')
        #print '='*40
        #print 'container:', self.container
        #print 'container.manager:', self.container.manager
        #print 'container.config:', self.container.config
        #print 'container.manager.core:', self.container.manager.core
        #print 'container.manager.core.db:', self.container.manager.core.db
        #print 'container.manager.core.config:', self.container.manager.core.config
        #print 'container.manager.core.model:', self.container.manager.core.model
        #print '='*40

    # This function will be called when the extension is disabled or
    # when gPodder shuts down. You can use this to destroy/delete any
    # objects that you created in on_load().
    #def on_unload(self):
        #logger.info('Extension is being unloaded.')

