## fixtags.py

It's a python script that fixes podcasts' MP3 tags after downloading the podcasts with [gPodder](http://gpodder.org/). The fixes are required for Sansa Sandisk Clip+ players to display the podcasts properly.

Requirements to run:

* [gPodder 2.\*](http://gpodder.org/) -- (for gPodder 3.\* see the extension below)

* [python 3](http://python.org/download/releases/)

* [stagger library](http://code.google.com/p/stagger/)

**NB:** Due to the vast difference in filling in of podcasts' tags, the script processes only the podcasts it knows about and has fixes for.

More detailed info on how to use the script is here: [http://www.egeek.me/2011/05/30/sandisk-sansa-clip-podcasts-gpodder/](http://www.egeek.me/2011/05/30/sandisk-sansa-clip-podcasts-gpodder/).

You are welcome to send pull requests.


## fixtags_ext.py

This is the fixtags extension for gPodder 3, whereas the `fixtags.py` is for gPodder 2. Note, however, that you will need both these files to work with gPodder 3, as the extension internally calls the old script. The extension has been tested with gPodder.app bundle 3.5.0 on OS X 10.8.3, and it should also work on Linux.

Requirements to run:

* [gPodder 3.\*](http://gpodder.org/)

* fixtags.py script, with python 3 and stagger library (above)

The setup is a bit longer this time:

1. Copy/softlink the `fixtags_ext.py` to the gPodder's extensions directory, usually `~/gPodder/Extensions/`.

2. Launch gPodder, go to Preferences, Extensions tab. In the 'Post download' section, enable the 'fixtags Extension'.

3. Still in Preferences, click the 'Edit config' button. Find the `extensions.fixtags_ext.fixtags_cmd` setting, and set it to the path and filename of the `fixtags.py` script (e.g., `~/bin/fixtags/fixtags.py`). If you can't find the setting, check that the extension is checked, and maybe restart gPodder.

Done, it should work now. You may enable verbose mode in gPodder (running it with the `-v` flag) and check the logs for errors.

