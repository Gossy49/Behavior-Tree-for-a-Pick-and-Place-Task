# Behavior Tree for a Pick and Place Task

This project implements a simple behavior tree to simulate a robot performing a pick-and-place task using the `py_trees` library.

The robot operates in a 2D world and must pick up two different objects from their locations and place them at predefined drop locations. After completing both pick-and-place actions, the robot returns to its starting position. When all tasks are completed successfully, the behavior tree finishes with a SUCCESS status.

## Task Description

The task follows this sequence:

1. The robot moves to the location of Object 1.
2. The robot picks up Object 1.
3. The robot moves to Drop Location 1.
4. The robot places Object 1.
5. The robot moves to the location of Object 2.
6. The robot picks up Object 2.
7. The robot moves to Drop Location 2.
8. The robot places Object 2.
9. The robot returns to its initial position (0, 0).

This sequence is modeled using a behavior tree composed of sequences and action nodes.

## Project Structure

The project is implemented using the following Python files:

- `world.py`  
  Defines the robot state, object positions, drop locations, and the shared world data used by all behaviors.

- `behaviors.py`  
  Contains custom behavior tree nodes such as:
  - MoveTo: moves the robot toward an object or drop location
  - Pickup: picks up an object if the robot is at the correct location
  - PlaceObject: places the carried object at a drop location

- `visualize.py`  
  Handles visualization of the robot, objects, and drop zones using matplotlib.

- `move.py`  
  This is the main file that builds and runs the full behavior tree.  
  It connects the world, behaviors, and visualization, and also generates SVG and PNG images of the behavior tree structure.

- `one.py`  
  An earlier trial version of the task.  
  In this version, the robot picks up Object 1, drops it at the initial position, then repeats the process for Object 2 before returning home.  
  This file was used for testing and was later improved in `move.py`.

## Implementation Details

- The robot moves in discrete steps based on world coordinates.
- Movement is constrained so the robot stays within the map.
- Each pick-and-place task is implemented as a Sequence node in the behavior tree.
- The full task consists of two sequential object-handling sequences followed by a return-to-home action.
- The behavior tree structure is exported as both SVG and PNG files for visualization.

## How to Run

Make sure Python 3 is installed and that the `py_trees` and `matplotlib` libraries are available.

Run the main implementation:

```bash
python3 move.py 
 or 
python3 one.py (to run trial script)

