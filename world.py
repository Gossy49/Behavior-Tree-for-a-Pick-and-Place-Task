
robot_x = 0.0
robot_y = 0.0
carrying = None

objects = {
    "obj1": (3.0, 0.0),
    "obj2": (3.0, 2.0),
}

drops = {
    "drop1": (2.0, 1.0),
    "drop2": (4.0, 2.0),
    "start": (0.0, 0.0),
}

def robot_status():
    print(f"ROBOT Position ({robot_x:.1f}, {robot_y:.1f}), carrying = {carrying}")
