# Boun Perception

In this package, we create a visual shortcut creating ros tf frames for each object with respect to world frame. It currently works in a manual way.

Two types of object shape is encoded:
* PolygonStamped
* PoseStamped

It works in following way. Through vrep, for some objects polygons, for some objects poses are published. Name given in vrep is also published. Then by listening to either "Shape_Polygon_List" or "Shape_Pose_List", objects topics are found. Then transformation frames are created and objects are stamped and then published.

I created a scene for testing. Imagine_Boun_Perception.ttt . ShapePublisher node in scene is publishing shape lists. For creating new shape, for pose, you can look at cup shape node in the scene and for creating polygon shape, you can look at HDD shape node.

## How To Add Boun Perception To Your Seen

### Prerequisites:

* V-Rep version compatible with ros interface.
* Ros interface.

### How to use

With boun perception, 4 V-rep models are provided.

* HDDModel1.ttm
* HDDModel2.ttm
* shapePublisher.ttm : This publishes some messages necessary for boun perception.
* screwRemover.ttm : Contains shortcut function which removes all screws in the scene.
* sceneLoader.ttm : Loads 8 different scenes using signals.

### Steps
1. Load shapePublisher,screwRemover,sceneLoader in your scene.
2. Run boun perception preparePolygons.
3. You can load different scenes using sceneLoader script. You need to update path to Hdd models in the given variable.

This will provide you positions of HDD parts. Currently, functionality of screws are designed around UIBK's workspace.
