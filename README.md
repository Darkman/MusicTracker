Foobar Music Tracker

Get this foobar component to be able to output the currently playing song information to a file.

http://skipyrich.com/wiki/Foobar2000:Now_Playing_Simple

Install component

In Foobar settings -> Tools -> Now Playing Simple. Set the following options.

Encoding: UTF-8 with header

Formatting string:
%artist%
$crlf()
%album%
$crlf()
%title%
$crlf()
%path%

On Exit:
not running

Use the AutoHotkey program to setup keyboard shortcuts to run the python script with the wanted parameters.
Example AutoHotkey config:
SetWorkingDir, E:\Users\Test\Projects\MusicTracker\
^!f:: Run E:\Users\Test\Virtualenvs\MusicTracker\Scripts\pythonw.exe E:\Users\Test\Projects\MusicTracker\music_tracking.py -f

Tip: run pythonw.exe with AutoHotkey to not show a prompt on run

