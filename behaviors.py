# behaviors.py
import py_trees
import math
import world  

class MoveTo(py_trees.behaviour.Behaviour):
    def __init__(self, name, target_name, target_type):
        super().__init__(name)
        self.target_name = target_name
        self.target_type = target_type

    def update(self):
        if self.target_type == "object":
            target_x, target_y = world.objects[self.target_name]
        else:
            target_x, target_y = world.drops[self.target_name]

        dx = target_x - world.robot_x
        dy = target_y - world.robot_y
        distance = math.sqrt(dx*dx + dy*dy)

        if distance < 0.1:
            print(f"MoveTo: Arrived at {self.target_name}")
            return py_trees.common.Status.SUCCESS

        step = 1.0
        if abs(dx) > 0.0:
            if dx > 0:
                world.robot_x = min(world.robot_x + step, target_x)
            else:
                world.robot_x = max(world.robot_x - step, target_x)
        else:
            if dy > 0:
                world.robot_y = min(world.robot_y + step, target_y)
            else:
                world.robot_y = max(world.robot_y - step, target_y)

        print(f"MoveTo: Moving to {self.target_name}")
        return py_trees.common.Status.RUNNING


class Pickup(py_trees.behaviour.Behaviour):
    def __init__(self, name, obj_name):
        super().__init__(name)
        self.obj_name = obj_name

    def update(self):
        if world.carrying is not None:
            print("Pickup: Already carrying something")
            return py_trees.common.Status.FAILURE

        obj_x, obj_y = world.objects[self.obj_name]
        if abs(world.robot_x - obj_x) < 0.1 and abs(world.robot_y - obj_y) < 0.1:
            world.carrying = self.obj_name
            print(f"Pickup: Picked up {self.obj_name}")
            return py_trees.common.Status.SUCCESS

        print("Pickup: Not at object yet")
        return py_trees.common.Status.RUNNING


class PlaceObject(py_trees.behaviour.Behaviour):
    def __init__(self, name, drop_name):
        super().__init__(name)
        self.drop_name = drop_name

    def update(self):
        if world.carrying is None:
            print("PlaceObject: Nothing to place")
            return py_trees.common.Status.FAILURE

        drop_x, drop_y = world.drops[self.drop_name]
        if abs(world.robot_x - drop_x) < 0.1 and abs(world.robot_y - drop_y) < 0.1:
            world.objects[world.carrying] = (drop_x, drop_y)
            print(f"PlaceObject: Placed {world.carrying} at {self.drop_name}")
            world.carrying = None
            return py_trees.common.Status.SUCCESS

        print("PlaceObject: Not at drop yet")
        return py_trees.common.Status.RUNNING
