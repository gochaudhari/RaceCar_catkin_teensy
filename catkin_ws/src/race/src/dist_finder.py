#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import LaserScan
from race.msg import pid_input

desired_trajectory = 1
#vel = 30
vel = 8.0

pub = rospy.Publisher('error', pid_input, queue_size=10)
## Input: data: Lidar scan data
## theta: The angle at which the distance is requried
## OUTPUT: distance of scan at angle theta

def getRange(data,theta):
# Find the index of the arary that corresponds to angle theta.
# Return the lidar scan value at that index
# Do some error checking for NaN and ubsurd values
## Your code goes here
#    print theta
#    print data.ranges[theta]
    index = theta + 45
    #print index
    #print data.ranges[index]
    return data.ranges[index]

def callback(data):
	theta = 50
	a = getRange(data,theta)
	b = getRange(data,0)
	swing = math.radians(theta)
	## Your code goes here

	## Calculating orientation (alpha) of the car with respect to the wall
	nr = (a * (math.cos(swing)) - b)
	dr = a * math.sin(swing)
	x = nr / dr
	alpha = math.atan(x)

	## Calculating distance AB of the car from the wall
	AB = b * math.cos(alpha)
	
	## Due to high speed, we need to compensate for error
	AC = 0.5 # Distance of the car travelled from its current position
	CD = AB + AC * math.sin(alpha) # New distance of the car from the wall
	print CD
	print desired_trajectory
	error = CD -  desired_trajectory
	 
	## END
	msg = pid_input()
	msg.pid_error = error
	msg.pid_vel = vel
	pub.publish(msg)
if __name__ == '__main__':
	print("Laser node started")
	rospy.init_node('dist_finder',anonymous = True)
	rospy.Subscriber("scan",LaserScan,callback)
	rospy.spin()
