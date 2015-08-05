# HBBatchster #
### _a Handbrake Batch GUI_ ###
is a very functional, easy to use wxPython-based application mainly designed for Windows using Handbrake Presets and a functional GUI to batch encode multiple files using the popular HandbrakeCLI command line tool of the Handbrake project (http://www.handbrake.fr) in a queue. It supports convenience functionality such as cleaning "garbage" in filenames, supporting pause/resume, drag&drop and much more.

This project was started in 2008 by me to circumvent the problem that the official GUI of Handbrake for Windows made/makes it really hard for the user to batch encode multiple video files. Currently HBBatchster is pretty final in its functionality so don't expect too frequent updates. The codebase by far isn't complete, well readable, documented, or anything, so don't complain. Too much try: except: in here aswell.


### Prerequisites ([Installer](http://code.google.com/p/hbbatchster/downloads/list?can=3&q=Type%3DInstaller+&colspec=Filename+Summary+Uploaded+ReleaseDate+Size+DownloadCount) assumed) ###
  * Windows OS (the app contains platform specific functions such as `_`winreg, it may be ported to UNIX-style platforms easily, if anyone wants to spend some time in it)
  * Handbrake ([preferred current Windows version](http://handbrake.fr/downloads.php))

### Using ###
  * [Python](http://www.python.org)
  * [HandbrakeCLI (Handbrake)](http://www.handbrake.fr)
  * [wxPython](http://www.wxpython.org/) ([wxWidgets](http://www.wxwidgets.org/))
  * [psutil](http://code.google.com/p/psutil/)
  * [PyInstaller](http://www.pyinstaller.org/) for packaging the Windows executable
  * [InnoSetup](http://www.jrsoftware.org/isinfo.php) for the installer

### What it does ###
  * automates your Handbrake encoding needs
  * (tries to) automatically find your Handbrake installation folder and its HandbrakeCLI.exe
  * automatically parses your existing Handbrake presets (%APPDATA%\Handbrake\presets.xml) and custom user presets (%APPDATA%\Handbrake\user\_presets.xml)
  * customize encoded file extension (initially the preset's chosen file extension is used)
  * optionally clear CRC tags in filenames (`File_[0AA0B0BA].avi -> File.mkv`)
  * optionally clear "garbage" in filenames (`[GarbageBlerg]File_[0AA0B0BA] .avi -> File.mkv`)
  * optionally replaces the original extension with the new one (`File.avi -> File.mkv instead of File.avi.mkv`)
  * ability to pause/resume encoding

### Howto ###
  * install [Handbrake](http://handbrake.fr/downloads.php)
  * [install HBBatchster](http://code.google.com/p/hbbatchster/downloads/list?can=3&q=Type%3DInstaller+&colspec=Filename+Summary+Uploaded+ReleaseDate+Size+DownloadCount) to any desired location or [unpack it](http://code.google.com/p/hbbatchster/downloads/list?can=3&q=Type%3DArchive+&colspec=Filename+Summary+Uploaded+ReleaseDate+Size+DownloadCount) and run HBBatchster.exe, or [unpack a source archive](http://code.google.com/p/hbbatchster/downloads/list?can=1&q=Type%3DSource&colspec=Filename+Summary+Uploaded+ReleaseDate+Size+DownloadCount) and run app.py
  * optional: create a custom profile using the Handbrake Windows GUI for your encoding needs
  * drag&drop multiple files into the main application window list
  * select the encoding profile you want to use for your file list
  * press Encode

### Help/Discussion ###
  * [Handbrake Forum thread](https://forum.handbrake.fr/viewtopic.php?f=6&t=8306&p=45819)
  * [Issues](http://code.google.com/p/hbbatchster/issues/list)