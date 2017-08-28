# LimeStyle
LimeStyle is a Sublime plugin that performs checkstyle according to CS1331's stylesheet.
The results of the checkstyle operation are displayed in Sublime's gutter.  
![Screen shot](https://github.com/kauboy26/LimeStyle/blob/master/screen_shot.png)

## Installation
LimeStyle will be installable via Package Control (once this plugin is approved).
Until then, this project (as a folder) can be downloaded and placed into "/sublime-text-3/Packages"

### Dependencies
JAVA must be accessible from the command line. To see if it is accessible,
run from command prompt or the terminal (on Linux and OSX):
```
java -version
```
If the version shows up, this plugin can be used.

## Usage
LimeStyle can be run either by navigating to "Tools > LimeStyle" in the menu bar.
OR  
Press "ctrl+shift+P" to open the command palette. Type in "Checkstyle 1331" or
"Javadoc 1331" and hit <Enter>.  
OR
View the .sublime-commands file and set up keybindings according to your preferences.
*IMPORTANT*: LimeStyle will be performed on all *open* .java files. These .java
files will also be *automatically saved*.

## License
This is available under the GNU Lesser Greater Public License (see LICENSE.txt).
The source code for the checkstyle jar used in this project can be found
[here](https://github.com/cs1331/checkstyle).