# TurtleBot3 Multi-Robot Swarm Simulation

This project demonstrates a multi-robot swarm behavior using **ROS 2 Humble** and **Gazebo**. One "Master" robot is controlled via keyboard, while two "Follower" robots autonomously maintain a tethered distance from the master using odometry-based proportional control.

## 🚀 Concept: How the Swarm Works
The swarm utilizes a **Proportional Tether Algorithm**. Instead of relying on complex, unreliable coordinate transforms, each follower subscribes to the Master's `/odom` topic. 
* **Odometry Tracking**: Followers read the Master's raw position in the simulation grid.
* **Proportional Control**: Followers calculate a "distance error" (current distance vs. desired 1.0m radius). 
* **Smooth Motion**: They apply a proportional velocity to close the gap or back away, creating a smooth, spring-like "tether" effect.



## 🛠️ Prerequisites
- Ubuntu 22.04 or later (or Windows with WSL2)
- Docker Desktop or Docker Engine installed
- NVIDIA/Intel GPU drivers installed on the host

## 📦 Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/codeIshan/turtlebot_swarm_demo.git](https://github.com/codeIshan/turtlebot_swarm_demo.git)
   cd turtlebot_swarm_demo
   ```

2. **Download Gazebo Models:**
  *The simulation needs local floor and environment assets to avoid online database timeouts.*
  ```bash
  git clone [https://github.com/osrf/gazebo_models.git](https://github.com/osrf/gazebo_models.git) gazebo_models
  touch gazebo_models/COLCON_IGNORE
  ```


3. **Build the Docker Container:**
  ```bash
  docker compose build
  ```



## 🎮 Running the Demo

### Step 1: Initialize the Environment
  
  Run the container in the background and grant display permissions:
  
  ```bash
  docker compose up -d
  xhost +
  ```

### Step 2: Launch the Simulation

Enter the container and launch the Gazebo world:

  ```bash
  docker exec -it turtlebot_swarm bash
  source install/setup.bash
  ros2 launch swarm_control swarm.launch.py
  ```

### Step 3: Drive the Master Robot

  In a **new terminal**, connect to the container and start the keyboard controller:
  
  ```bash
  docker exec -it turtlebot_swarm bash
  ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=/master_bot/cmd_vel 
  ```

*Use `i`, `j`, `k`, `l` to drive. Use `i` for forward.*

### Step 4: Activate the Swarm

  In another **new terminal**, connect to the container and start the follower "brains":
  
  ```bash
  docker exec -it turtlebot_swarm bash
  source install/setup.bash
  ros2 run swarm_control swarm_follower --ros-args -r __ns:=/follower_1 -p use_sim_time:=true &
  ros2 run swarm_control swarm_follower --ros-args -r __ns:=/follower_2 -p use_sim_time:=true &
  ```

*Created by [codeIshan]. Happy Hacking!*
