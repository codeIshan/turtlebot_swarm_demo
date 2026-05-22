import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.qos import qos_profile_sensor_data
import math

class SwarmFollower(Node):
    def __init__(self):
        super().__init__('swarm_follower')
        
        self.desired_distance = 1.0   
        self.namespace = self.get_namespace().strip('/')
        self.spawn_x = 0.0
        self.spawn_y = 0.0
        
        if self.namespace == 'follower_1':
            self.spawn_x = -2.0
            self.spawn_y = 2.0
        elif self.namespace == 'follower_2':
            self.spawn_x = -2.0
            self.spawn_y = -2.0

        self.master_x = 0.0
        self.master_y = 0.0
        self.self_x = 0.0
        self.self_y = 0.0
        self.self_yaw = 0.0

        self.master_sub = self.create_subscription(
            Odometry, '/master_bot/odom', self.master_odom_cb, qos_profile_sensor_data)
        self.self_sub = self.create_subscription(
            Odometry, 'odom', self.self_odom_cb, qos_profile_sensor_data)

        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.control_loop) 
        self.get_logger().info(f"Swarm Follower [{self.namespace}] Online!")

    # --- THESE METHODS MUST BE INDENTED UNDER THE CLASS ---
    def euler_from_quaternion(self, x, y, z, w):
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        return math.atan2(t3, t4)

    def master_odom_cb(self, msg):
        self.master_x = msg.pose.pose.position.x
        self.master_y = msg.pose.pose.position.y

    def self_odom_cb(self, msg):
        self.self_x = msg.pose.pose.position.x
        self.self_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        self.self_yaw = self.euler_from_quaternion(q.x, q.y, q.z, q.w)

    def control_loop(self):
        msg = Twist()
        global_self_x = self.self_x + self.spawn_x
        global_self_y = self.self_y + self.spawn_y
        dx = self.master_x - global_self_x
        dy = self.master_y - global_self_y
        distance = math.sqrt(dx**2 + dy**2)
        
        target_angle = math.atan2(dy, dx)
        angle_diff = target_angle - self.self_yaw
        
        while angle_diff > math.pi: angle_diff -= 2 * math.pi
        while angle_diff < -math.pi: angle_diff += 2 * math.pi

        distance_error = distance - self.desired_distance
        msg.linear.x = max(-0.20, min(0.20, 0.6 * distance_error))
        msg.angular.z = max(-2.0, min(2.0, 1.5 * angle_diff))
        self.cmd_vel_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = SwarmFollower()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()