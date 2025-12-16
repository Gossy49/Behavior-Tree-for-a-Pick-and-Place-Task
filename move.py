import functools
import py_trees
import py_trees.display
import matplotlib.pyplot as plt
import world
from behaviors import MoveTo, Pickup, PlaceObject
from visualize import draw_scene


def post_tick_handler(snapshot_visitor, behaviour_tree):
    print(
        py_trees.display.unicode_tree(
            behaviour_tree.root,
            visited=snapshot_visitor.visited,
            previously_visited=snapshot_visitor.visited
        )
    )


def create_behavior_tree():
    root = py_trees.composites.Sequence("Root", memory=True)

   
    seq_obj1 = py_trees.composites.Sequence("SeqObj1", memory=True)
    seq_obj1.add_children([
        MoveTo("MoveToObj1", "obj1", "object"),
        Pickup("PickObj1", "obj1"),
        MoveTo("MoveToDrop1", "drop1", "drop"),
        PlaceObject("PlaceObj1", "drop1"),
    ])

   
    seq_obj2 = py_trees.composites.Sequence("SeqObj2", memory = True)
    seq_obj2.add_children ([
        MoveTo("MoveToObj2", "obj2", "object"),
        Pickup("PickObj2", "obj2"),
        MoveTo("MoveToDrop2", "drop2", "drop"),
        PlaceObject("PlaceObj2", "drop2"),
    ])
    return_home  = MoveTo("ReturnHome", "start", "drop")
    root.add_children([seq_obj1, seq_obj2, return_home])

    return root



if __name__ == "__main__":
    tree = create_behavior_tree()
    tree.setup(timeout=15)
    py_trees.display.render_dot_tree(tree, name="my_tree")

    snapshot_visitor = py_trees.visitors.SnapshotVisitor()
    behaviour_tree = py_trees.trees.BehaviourTree(tree)
    behaviour_tree.add_post_tick_handler(
            functools.partial(post_tick_handler,
                      snapshot_visitor))
    behaviour_tree.visitors.append(snapshot_visitor)

    plt.ion()
    plt.figure()

    for _ in range(50):
        tree.tick_once()
        world.robot_status()
        print("Tree status:", tree.status)
        draw_scene()

        if tree.status == py_trees.common.Status.SUCCESS:
            print("Complete")
            break

    plt.ioff()
    plt.show()
