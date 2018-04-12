#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import roslib
import os.path
import vrep_common.srv
import rospy
import time

MAX_SCENE = 8
simRosSetStringSignal = rospy.ServiceProxy('/vrep/simRosSetStringSignal', vrep_common.srv.simRosSetStringSignal)
simRosGetStringSignal = rospy.ServiceProxy('/vrep/simRosGetStringSignal', vrep_common.srv.simRosGetStringSignal)
simRosGetIntegerSignal = rospy.ServiceProxy('/vrep/simRosGetIntegerSignal', vrep_common.srv.simRosGetIntegerSignal)
simRosSetIntegerSignal = rospy.ServiceProxy('/vrep/simRosSetIntegerSignal', vrep_common.srv.simRosSetIntegerSignal)


def load_scene(load_scene=2):
    boun_path = os.path.join(roslib.packages.get_pkg_dir("boun_perception"))
    fullpath = os.path.join(boun_path, "HDD_models").rstrip("/")+"/"
    print("Trying to load boun models from: %s" % (fullpath,))
    assert os.path.exists(os.path.join(fullpath, "HddModel1.ttm")), "could not find HddModel1.ttm at %s" % (fullpath,)
    assert simRosSetStringSignal("PathToModels", fullpath).result == 1
    status = [simRosGetIntegerSignal("LoadScene%d" % (i,)).signalValue for i in range(1, MAX_SCENE + 1)]
    if any(status):
        assert simRosSetIntegerSignal("RemoveHdd", 1).result == 1
        for i in range(20):
            if simRosGetIntegerSignal("RemoveHdd").signalValue == 0:
                break
            time.sleep(0.01)
    simRosSetIntegerSignal("LoadScene%d" % (load_scene,), 1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("run this script with an integer cmdline parameter between 1 and %d to select the scene!" % (MAX_SCENE,))
        print("usage: %s SCENE_NUMBER" % (sys.argv[0],))
        sys.exit(1)
    scene_number = int(sys.argv[-1])
    assert scene_number >= 1
    assert scene_number <= MAX_SCENE
    print("Trying to load scene #%d" % (scene_number,))
    load_scene(scene_number)
