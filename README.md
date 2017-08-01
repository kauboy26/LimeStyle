# LimeStyle
LimeStyle is a Sublime plugin that performs GT's checkstyle operation.
The results of the checkstyle operation are displayed in Sublime's gutter.  
![Screen shot](https://github.com/kauboy26/LimeStyle/blob/master/screen_shot.png)

## Installation
LimeStyle will be installable via Package Control (once this plugin is approved).
Until then, this project (as a folder) can be downloaded and placed into "/sublime-text-3/Packages"

### Dependencies
JAVA must be accessible from the command line. To see if it is accessible,
run from command prompt or the terminal (on Linux and OSX):
'''
java -version
'''
If the version shows up, this plugin can be used.

## Usage
LimeStyle can be run either by navigating to "Tools > LimeStyle" in the menu bar.
Alternatively, the keyboard shortcuts listed below can be used.  
*IMPORTANT*: LimeStyle will be performed on all *open* .java files. These .java
files will also be *automatically saved*.

### Linux
Standard Checkstyle: Press "ctrl+L", release "L", and then press "S".  
JavaDoc: Press "ctrl+L", release "L", and then press "J".

### Windows
Standard Checkstyle: Press "ctrl+L", release "L", and then press "S".  
JavaDoc: Press "ctrl+L", release "L", and then press "J".

### OSX
Standard Checkstyle: Press "command+L", release "L", and then press "S".  
JavaDoc: Press "command+L", release "L", and then press "J".  
NOTE: The OSX keys need to be tested. The key-bindings file specifies "super" in
the place of "command". Not sure if these are equivalent