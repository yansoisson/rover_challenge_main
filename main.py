import rospy
from geometry_msgs.msg import Twist
from ar_track_alvar_msgs.msg import AlvarMarkers

# Initialize ROS node
rospy.init_node('turtlebot3_robot', anonymous=True)

# Create publisher topic
velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
vel_msg = Twist()

# Receiveing the user's input
print("Let's move your robot")
speed = 0.5 # input("Input your speed (e.g. 2, 3):")
distance = 50 # input("Type your distance (e.g. 10, 15):")

x = None
y = None

def callback_marker(msg):
    print('Looking for a marker')
    global x
    global y
    if(len(msg.markers) == 0):
        print('Too far from the marker!')
    else:
        x = msg.markers[0].pose.pose.position.x
        y = msg.markers[0].pose.pose.position.y
            

def forward():
    # Go forward for a certain distance
    print('Going forward...')
    vel_msg.linear.x = abs(speed)
    velocity_publisher.publish(vel_msg)

def backward():
    # Go backward for a certain distance
    print('Going backward...')
    vel_msg.linear.x = -abs(speed)
    velocity_publisher.publish(vel_msg)

def turn_left():
    # Turn left with a certain degree
    print('Turning left...')
    vel_msg.angular.z = 0.2
    velocity_publisher.publish(vel_msg)

def turn_right():
    print('Turning right...')
    vel_msg.angular.z = -0.2
    velocity_publisher.publish(vel_msg)

def stop():
    print('Stopping...')
    vel_msg.linear.x = 0.0
    vel_msg.angular.z = 0.0
    velocity_publisher.publish(vel_msg)
    

def move(speed):
    # Setting the current time for distance calculus
    rospy.Subscriber("/ar_pose_marker", AlvarMarkers, callback_marker)     
    rate = rospy.Rate(10)

   
    while not rospy.is_shutdown():
        print("Marker's x position: {}".format(x))
        print("Marker's y position: {}".format(y))
        print(' ')
        forward()
        rate.sleep()
        print('Going forward... Looking for Marker!')
        if (x is None or y is None):
            forward()
            rate.sleep()
            print('Going forward... Looking for Marker!')
        elif(x < 0.5 or y < 0.004):
            print("Stopping! Too close to the marker.")
            print("Marker's x position: {}".format(x))
            print("Marker's y position: {}".format(y))
            stop()
            rate.sleep()
            break
        
       

if __name__ == '__main__':
    try:
        move(speed)
    except rospy.ROSInterruptException: pass