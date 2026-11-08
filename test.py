from codrone_edu.drone import *
drone = Drone()
drone.pair()

drone.takeoff()
drone.move_distance(0, 0.5, 0, 1)
drone.hover(1)
drone.move_distance(0, -0.5, 0, 1)
drone.hover(1)
drone.land()

drone.close()