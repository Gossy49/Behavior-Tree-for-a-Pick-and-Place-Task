import matplotlib.pyplot as plt
import world

def draw_scene():
    plt.clf()

    # robot
    plt.scatter(world.robot_x, world.robot_y, marker="o")
    plt.text(world.robot_x + 0.1, world.robot_y + 0.1, "robot")

    # objects
    for name, (x, y) in world.objects.items():
        plt.scatter(x, y, marker="s")
        plt.text(x + 0.1, y + 0.1, name)

    # drops
    for name, (x, y) in world.drops.items():
        plt.scatter(x, y, marker="x")
        plt.text(x + 0.1, y + 0.1, name)

    plt.xlim(-1, 7)
    plt.ylim(-1, 4)
    plt.grid(True)
    plt.pause(0.3)
