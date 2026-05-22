import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    gazebo_ros_dir = get_package_share_directory('gazebo_ros')
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gazebo_ros_dir, 'launch', 'gazebo.launch.py'))
    )

    tb3_model = os.environ.get('TURTLEBOT3_MODEL', 'burger')
    
    # URDF is for RViz and TF distance math (The Visuals)
    urdf_path = os.path.join(
        get_package_share_directory('turtlebot3_description'),
        'urdf',
        f'turtlebot3_{tb3_model}.urdf'
    )
    
    # SDF is for Gazebo Physics (The Weight & Friction - FIXES THE SPINNING!)
    sdf_path = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'models',
        f'turtlebot3_{tb3_model}',
        'model.sdf'
    )

    def spawn_robot(name, x, y):
        state_publisher = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            namespace=name,
            parameters=[{'use_sim_time': True, 'frame_prefix': name + '/'}],
            arguments=[urdf_path]
        )
        spawner = Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-entity', name,
                '-file', sdf_path,  # Spawning with the tuned physics model
                '-x', str(x), '-y', str(y), '-z', '0.05',
                '-robot_namespace', name
            ]
        )
        return [state_publisher, spawner]

    master = spawn_robot('master_bot', 0.0, 0.0)
    f1 = spawn_robot('follower_1', -2.0, 2.0)
    f2 = spawn_robot('follower_2', -2.0, -2.0)

    ld = LaunchDescription()
    ld.add_action(gazebo_launch)
    for node in master + f1 + f2:
        ld.add_action(node)

    return ld