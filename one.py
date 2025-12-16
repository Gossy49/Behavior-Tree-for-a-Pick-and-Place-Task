import py_trees
import math 
import matplotlib.pyplot as plt
import py_trees.display


robot_x = 0.0
robot_y = 0.0
carrying = None

objects = {
    "obj1" :(3.0, 0.0),
    "obj2": (3.0, 2.0),
    }
drops = {
    "drop1": (0.0,0.0),
    "drop2": (0.0, 2.0),
    "start": (0.0, 0.0),
         }

def robot_status():
    print(f"ROBOT Position ({robot_x:.1f}, {robot_y:.1f}), carrying = {carrying}")

class MoveTo(py_trees.behaviour.Behaviour):
    def __init__(self, name, target_name, target_type):
        super(MoveTo, self).__init__(name)
        self.target_name = target_name
        self.target_type= target_type

    def update(self):
        global robot_x, robot_y

        if self.target_type == "object":
            target_x, target_y = objects[self.target_name]
        else:
            target_x,target_y = drops[self.target_name]

        dx = target_x - robot_x
        dy = target_y - robot_y
        distance = math.sqrt (dx * dx + dy * dy)

        if distance < 0.1:
            print(f"MoveTO: Arrived at {self.target_name}")
            return py_trees.common.Status.SUCCESS
        
        step = 1.0

        if abs (dx) > 0.0:
            if dx > 0:
                robot_x = min (robot_x + step, target_x)
            else:
                robot_x = max(robot_x -step, target_x)

        else:
            if dy > 0:
                robot_y = min (robot_y + step, target_y)
            else:
                robot_y = max (robot_y - step, target_y)
            
        print(f"MoveTo: Moving to {self.target_name}")
        return py_trees.common.Status.RUNNING
    


class Pickup(py_trees.behaviour.Behaviour):
    def __init__(self, name, obj_name):
        super().__init__(name)
        self.obj_name = obj_name


    def update(self):
        global carrying, robot_x, robot_y, objects

        if carrying is not None:
            print("PickObject: Already carrying something  cannot pick")
            return py_trees.common.Status.FAILURE
        
        obj_x, obj_y = objects[self.obj_name]
        if abs(robot_x -obj_x) < 0.1 and abs (robot_y - obj_y) < 0.1:
            carrying = self.obj_name
            print(f"PickObject:Picke Up {self.obj_name}")
            return py_trees.common.Status.SUCCESS
        
        print (f"PickObject: Not at object location yet")
        return py_trees.common.Status.RUNNING
    
class PlaceObject (py_trees.behaviour.Behaviour):
    def __init__(self, name, drop_name):
        super().__init__(name)
        self.drop_name = drop_name

    def update(self):
        global carrying, robot_x, robot_y, objects, drops

        if carrying is None:
            print("Place object: Nothing to place")
            return py_trees.common.Status.FAILURE
        
        drop_x, drop_y = drops[self.drop_name]

        if abs (robot_x - robot_x) < 0.1 and abs (robot_y - drop_y) < 0.1:
            objects [carrying] = (drop_x, drop_y)
            print (f"PlaceObject: PLaced {carrying} at {self.drop_name}")
            carrying = None
            return py_trees.common.Status.SUCCESS
        
        print("Place Object: Not at drop location yet")
        return py_trees.common.Status.RUNNING
    

def create_behavior_tree():
    root = py_trees.composites.Sequence("Root", memory=True)
    move_to_pick = MoveTo(name="MoveToPick", target_name="obj1", target_type="object")
    pick_up = Pickup("Pickupobject", "obj1")
    move_to_drop = MoveTo( name = "MoveToDrop", target_name= "drop1", target_type= "drop")
    place_object = PlaceObject ("placeobj1", "drop1") 

    move_to_obj2 = MoveTo(name="MoveToObj2", target_name="obj2", target_type="object")
    pick_obj2 = Pickup("PickObj2", "obj2")
    move_to_drop2 = MoveTo("MoveToDrop2", target_name="drop2", target_type="drop")
    place_obj2 = PlaceObject("PlaceObj2", "drop2")
    
    return_home =MoveTo("ReturnHome",target_name = "start", target_type ="drop")

    root.add_children([
        move_to_pick, pick_up, move_to_drop, place_object,
        move_to_obj2, pick_obj2, move_to_drop2, place_obj2,
        return_home
    ])
    return root


def draw_scene ():
    plt.clf

    plt.scatter(robot_x, robot_y, marker="o")
    plt.text(robot_x + 0.1,robot_y + 0.1, "robot")

    for name, (x, y) in objects.items():
        plt.scatter(x, y, marker="s")
        plt.text(x + 0.1, y + 0.1, name)

    # draw drop zones
    for name, (x, y) in drops.items():
        plt.scatter(x, y, marker="x")
        plt.text(x + 0.1, y + 0.1, name)


        plt.xlim(-1, 7)
        plt.ylim(-1, 4)
        plt.grid(True)
        plt.pause(0.3)








if __name__ == "__main__":
    tree = create_behavior_tree()
    py_trees.display.render_dot_tree(tree, name="my_tree")
    print("Starting behavior tree execution:")
    tree.setup(timeout=15)

    for _ in range(50):
        tree.tick_once()
        robot_status()
        print(f"Tree status: {tree.status}")
        draw_scene()

        if tree.status == py_trees.common.Status.SUCCESS:
            print("Complete")
            print("=" * 40)

            break

plt.ioff()
plt.show()

