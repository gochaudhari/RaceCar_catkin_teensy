#!/usr/bin/env python

import rospy
from race.msg import drive_param
from race.msg import pid_input

kp = 14.0
kd = 0.09
#servo_offset = 18.5
servo_offset = 19
prev_error = 0.0 
#vel_input = 7.8

pub = rospy.Publisher('drive_parameters', drive_param, queue_size=10)

def control(data):
	global prev_error
	global vel_input
	global kp
	global kd

	## Your code goes here
	# 1. Scale the error
	# 2. Apply the PID equation on error
	# 3. Make sure the error is within bounds
 	error = data.pid_error * 2 # Error scale
	pid_eq = kp * error + kd * (prev_error - error) # PID
	angle = pid_eq - servo_offset # steering angle
	prev_error = error
	## END

	msg = drive_param();
	msg.velocity = data.pid_vel
	msg.angle = angle
	rospy.sleep(0.1) ## <<<<<<<< optimization needed to solve SYNC LOST problem with Teensy
	pub.publish(msg)

if __name__ == '__main__':
	global kp
	global kd
	global vel_input
	print("Listening to error for PID")
	kp = 14
	kd = 0.09
	rospy.init_node('pid_controller', anonymous=True)
	rospy.Subscriber("error", pid_input, control)
	rospy.spin()

	
