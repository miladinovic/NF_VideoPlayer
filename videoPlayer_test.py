import subprocess
from tkinter import filedialog
"""
filedialog.askdirectory(initialdir="/tmp/test")


filepath2="C:/Program Files/openvibe-2.0.1/openvibe-designer.cmd --play Y:\Downloads\OpenVibeConfigurationTest\motor-imagery\motor-imagery-bci-1-acquisition.xml --no-gui"
filepath1="C:/Program Files/openvibe-2.0.1/openvibe-acquisition-server.cmd"
p = subprocess.Popen(filepath1, shell=False, stdout = subprocess.PIPE)
p2 = subprocess.Popen(filepath2, shell=False)

p2.communicate()"""

import videoPlayer



videoPlayer.runVideoPlayer()


print "Test"
#stdout, stderr = p.communicate()
#print p.returncode # is 0 if success


"""Possible switches :
  --help                  : displays this help message and exits
  --config filename       : path to config file
  --define token value    : specify configuration token with a given value
  --open filename         : opens a scenario (see also --no-session-management)
  --play filename         : plays the opened scenario (see also --no-session-management)
  --play-fast filename    : plays fast forward the opened scenario (see also --no-session-management)
  --no-gui                : hides the Designer graphical user interface (assumes --no-color-depth-test)
  --no-visualization      : hides the visualisation widgets
  --invisible             : hides the designer and the visualisation widgets (assumes --no-check-color-depth and --no-session-management)
  --no-check-color-depth  : does not check 24/32 bits color depth
  --no-session-management : neither restore last used scenarios nor saves them at exit
  --random-seed uint      : initialize random number generator with value, default=time(NULL)
  --no-pause
  --run-bg
  """

"""
 --config filename       : path to config file
  --define token value    : specify configuration token with a given value
  --help                  : displays this help message and exits
  --kernel filename       : path to openvibe kernel library"""
