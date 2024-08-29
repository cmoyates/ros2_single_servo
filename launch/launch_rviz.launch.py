import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():

    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    package_name = "single_servo"

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory(package_name), "launch", "rsp.launch.py"
                )
            ]
        ),
        launch_arguments={"use_sim_time": "true"}.items(),
    )

    # Specify the relative path to the RViz configuration file
    rviz_config_file = os.path.join(
        os.getcwd(), "src", "ros2_single_servo", "config", "view_bot.rviz"
    )
    print(rviz_config_file)

    # Add RViz2 node to launch with the specific RViz configuration file
    rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config_file],
        output="screen",
    )

    # Add joint_state_publisher_gui node to launch the GUI for joint state control
    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        output="screen",
    )

    # Launch them all!
    return LaunchDescription(
        [
            rsp,
            rviz2,
            joint_state_publisher_gui,
        ]
    )
