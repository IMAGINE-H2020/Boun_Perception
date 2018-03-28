#!/usr/bin/env python
import sys
import copy
import rospy
import tf
import rospkg
from visualization_msgs.msg import *
from geometry_msgs.msg import *
from std_msgs.msg import *

rospy.init_node("Boun_Perception")
shape_to_publisher_dict=dict()
frame_to_broadcaster_dict=dict()
def processShapePolygonList(data):
    shapeString = data.data
    ShapeList=shapeString.split(" ")
    for shape in ShapeList:
        if shape not in shape_to_publisher_dict.keys():
            br = tf.TransformBroadcaster()
            frame_to_broadcaster_dict[shape]=br
            pub = rospy.Publisher("/Shapes/"+shape, PolygonStamped,queue_size=1)
            shape_to_publisher_dict[shape]=pub
            rospy.Subscriber("/vrep_ros_interface/Shapes/"+shape, Polygon, broadcastShapePolygon,(shape))
def processShapePoseList(data):
    shapeString = data.data
    ShapeList=shapeString.split(" ")
    for shape in ShapeList:
        if shape not in shape_to_publisher_dict.keys():
            br = tf.TransformBroadcaster()
            frame_to_broadcaster_dict[shape]=br
            pub = rospy.Publisher("/Shapes/"+shape, PoseStamped,queue_size=1)
            shape_to_publisher_dict[shape]=pub
            rospy.Subscriber("/vrep_ros_interface/Shapes/"+shape, Pose, broadcastShapePose,(shape))
def broadcastShapePose(data,shape):
    # Create Header
    h = std_msgs.msg.Header()
    h.stamp = rospy.Time.now()
    h.frame_id=shape
    pose=Pose()
    br = frame_to_broadcaster_dict[shape]
    br.sendTransform((data.position.x, data.position.y, data.position.z),
        (data.orientation.x,data.orientation.y,data.orientation.z,data.orientation.w),
        rospy.Time.now(),
        shape,
        "world")
    quaternion = tf.transformations.quaternion_from_euler(0, 0, 0)
    pose.position=Point()
    pose.position.x=0
    pose.position.y=0
    pose.position.z=0
    pose.orientation=Quaternion()
    pose.orientation.x=0
    pose.orientation.y=0
    pose.orientation.z=0
    pose.orientation.w=1
    msg=PoseStamped()
    msg.header=h
    msg.pose=pose
    pub=shape_to_publisher_dict[shape]
    pub.publish(msg)

def broadcastShapePolygon(data,shape):
    # Create Header
    h = std_msgs.msg.Header()
    h.stamp = rospy.Time.now()
    h.frame_id=shape
    # Create New Polygon Object
    polygon=Polygon()
    points=list()
    # Calculating Middle Point and broadcasting shape polygon
    br = frame_to_broadcaster_dict[shape]
    sum_x=0
    sum_y=0
    sum_z=0
    for point in data.points:
        sum_x+=point.x
        sum_y+=point.y
        sum_z+=point.z
    aver_x=sum_x/len(data.points)
    aver_y=sum_y/len(data.points)
    aver_z=sum_z/len(data.points)
    br.sendTransform((aver_x, aver_y, aver_z),
        tf.transformations.quaternion_from_euler(0, 0, 0), # TODO: calculateAngleChange
        rospy.Time.now(),
        shape,
        "world")
    # Fixing shape polygon
    for point in data.points:
        newPoint=Point32()
        newPoint.x=point.x-aver_x
        newPoint.y=point.y-aver_y
        newPoint.z=point.z-aver_z
        points.append(newPoint)
    msg=PolygonStamped()
    msg.header=h
    polygon.points=points
    msg.polygon=polygon
    pub=shape_to_publisher_dict[shape]
    pub.publish(msg)

rospy.Subscriber("/Shape_Polygon_List", String, processShapePolygonList)
rospy.Subscriber("/Shape_Pose_List", String, processShapePoseList)

rospy.spin()
#rate = rospy.Rate(20)
#rate.sleep()
