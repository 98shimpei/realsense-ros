#!/usr/bin/env python

import rospy
from sensor_msgs.msg import PointCloud2 as msg_PointCloud2
from laser_assembler.srv import AssembleScans2 as srv_AssembleScans2

def assembled_pointcloud2_publisher():

    pub = rospy.Publisher("/assembled_pointcloud2", msg_PointCloud2, queue_size=1)
    rospy.init_node("assembled_pointcloud2_publisher", anonymous=True)
    rospy.wait_for_service("assemble_scans2")
    r = rospy.Rate(1) # 1hz

    while not rospy.is_shutdown():
        end = rospy.Time.now()
        begin = rospy.Time(end.secs-10, end.nsecs)
        srv = rospy.ServiceProxy("/assemble_scans2", srv_AssembleScans2)
        try:
            res = srv(begin, end)
            pub.publish(res.cloud)
            print("Publish assembled pointcloud")
        except:
            rospy.logerr("Failed to get assembled pointcloud")
        r.sleep()

if __name__ == '__main__':
    try:
        assembled_pointcloud2_publisher()
    except rospy.ROSInterruptException: pass
