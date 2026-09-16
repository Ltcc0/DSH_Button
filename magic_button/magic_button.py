
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

import sys
import tty
import termios
import time
import math


class MagicButton(Node):

    def __init__(self):
        super().__init__('magic_button')

        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.linear_speed = 2.0
        self.angular_speed = 2.0

    def send_velocity(self, linear=0.0, angular=0.0):
        msg = Twist()

        msg.linear.x = linear
        msg.angular.z = angular

        self.publisher.publish(msg)

    def stop(self):
        self.send_velocity(0.0, 0.0)

    def move_for(self, linear=0.0, angular=0.0, duration=0.12):
        """
        Move for a short period.
        Holding W/A/S/D causes repeated movement.
        """

        end_time = time.monotonic() + duration

        while time.monotonic() < end_time:
            self.send_velocity(linear, angular)
            time.sleep(0.02)

        self.stop()

    def magic_360(self):
        """
        MAGIC BUTTON:
        Rotate the turtle approximately 360 degrees.
        """

        print("\r\nMAGIC BUTTON! Rotating 360 degrees...\r\n")

        angular_speed = 1.5          # radians / second
        angle = 2.0 * math.pi        # 360 degrees
        duration = angle / angular_speed

        start_time = time.monotonic()

        while time.monotonic() - start_time < duration:
            self.send_velocity(
                linear=0.0,
                angular=angular_speed
            )

            time.sleep(0.02)

        self.stop()

        print("360 rotation complete!\r\n")

    def keyboard_loop(self):

        old_settings = termios.tcgetattr(sys.stdin)

        print("")
        print("==============================")
        print("      MAGIC TURTLE CONTROL")
        print("==============================")
        print("")
        print("        W = Forward")
        print("        S = Backward")
        print("        A = Turn Left")
        print("        D = Turn Right")
        print("")
        print("        E = MAGIC 360")
        print("")
        print("        Q = Quit")
        print("")
        print("==============================")
        print("")

        try:
            tty.setraw(sys.stdin.fileno())

            while rclpy.ok():

                key = sys.stdin.read(1).lower()

                if key == 'w':
                    self.move_for(
                       linear=self.linear_speed
                    )

                elif key == 's':
                    self.move_for(
                        linear=-self.linear_speed
                    )

                elif key == 'a':
                    self.move_for(
                        angular=self.angular_speed
                    )

                elif key == 'd':
                    self.move_for(
                        angular=-self.angular_speed
                    )

                elif key == 'e':
                    self.magic_360()

                elif key == 'q' or key == '\x03':
                    break

        finally:
            self.stop()

            termios.tcsetattr(
                sys.stdin,
                termios.TCSADRAIN,
                old_settings
            )


def main(args=None):

    rclpy.init(args=args)

    node = MagicButton()

    try:
        node.keyboard_loop()

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
