FROM osrf/ros:humble-desktop
    # Install Gazebo, TurtleBot3, and transform tools
    RUN apt-get update && apt-get install -y \
        ros-humble-gazebo-ros-pkgs \
        ros-humble-turtlebot3 \
        ros-humble-turtlebot3-msgs \
        ros-humble-turtlebot3-simulations \
        ros-humble-tf2-ros \
        && rm -rf /var/lib/apt/lists/*


    # Set default robot model and source ROS 2 automatically
    ENV TURTLEBOT3_MODEL=burger
    RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
    WORKDIR /root/swarm_ws