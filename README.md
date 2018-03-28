# Boun Perception

In this package, we create a visual shortcut creating ros tf frames for each object with respect to world frame. It currently works in a manual way.

Two types of object shape is encoded:
* PolygonStamped
* PoseStamped

It works in following way. Through vrep, for some objects polygons, for some objects poses are published. Name given in vrep is also published. Then by listening to either "Shape_Polygon_List" or "Shape_Pose_List", objects topics are found. Then transformation frames are created and objects are stamped and then published.

I created a scene for testing. Imagine_Boun_Perception.ttt . ShapePublisher node in scene is publishing shape lists. For creating new shape, for pose, you can look at cup shape node in the scene and for creating polygon shape, you can look at HDD shape node.




 
