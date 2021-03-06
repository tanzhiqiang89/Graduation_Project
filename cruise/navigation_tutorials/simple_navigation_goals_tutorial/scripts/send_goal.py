#!/usr/bin/env python
# -*- coding: utf-8 -*-


import roslib
roslib.load_manifest('simple_navigation_goals_tutorial')
import rospy
import actionlib

from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


class MoveBaseDoor():
	def __init__(self):
		rospy.init_node('send_goals_node', anonymous=False)
        
		#rospy.on_shutdown(self.shutdown)

		MoveBaseClient = actionlib.SimpleActionClient('send_goals_node', MoveBaseAction)

        # 订阅move_base服务器的消息
		self.ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)

		rospy.loginfo("Waiting for move_base action server...")

		self.ac.wait_for_server(rospy.Duration(60))

		rospy.loginfo("Connected to move base server");

		# 初始化goal为MoveBaseGoal类型

		goal = MoveBaseGoal()

		# 使用map的frame定义goal的frame id
		goal.target_pose.header.frame_id = 'map'

		# 设置时间戳
		goal.target_pose.header.stamp = rospy.Time.now()

		# 设置目标位置
		goal.target_pose.pose.position.x = 54.7
		goal.target_pose.pose.position.y = 20.7
		goal.target_pose.pose.orientation.w = 0.00581
		rospy.loginfo("Sending goal")
		# 机器人移动
		self.move(goal)



	def move(self, goal):
		self.ac.send_goal(goal)

		# 设定5分钟的时间限制
		finished_within_time = self.ac.wait_for_result(rospy.Duration(300))

		# 如果5分钟之内没有到达，放弃目标
		if not finished_within_time:
			self.ac.cancel_goal()
			rospy.loginfo("Timed out achieving goal")
		else:
			state = self.ac.get_state()
			if state == GoalStatus.SUCCEEDED:
				rospy.loginfo("Goal succeeded!")


'''
	def shutdown(self):
		rospy.loginfo("Stopping the robot...")

		# Cancel any active goals
		self.ac.cancel_goal()
		rospy.sleep(2)

		# Stop the robot
		#self.cmd_vel_pub.publish(Twist())
		#rospy.sleep(1)
'''


if __name__ == '__main__':
	try:
		MoveBaseDoor()
	except rospy.ROSInterruptException:
		rospy.loginfo("Navigation finished.")
