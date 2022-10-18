# Copyright (c) 2022-present, Polymath Robotics, Inc.
# Example farmworld UI for using the Caladan API in Python
# Designed as a simple teaching example, not feature complete or fully robust.

# Example set of goals for vehicle to follow
tilling_goals = [
    (37.724908, -120.998889, 0),  # start of row 1
    (37.725445, -120.998889, 0),  # end of row 1
    (37.725495, -120.998857, -1.57),  # turn around midpoint
    (37.725445, -120.998811, -3.14),  # start of row 2
    (37.724908, -120.998811, -3.14),  # end of row 2
]

# Example single goal to return to the shed
shed_goal = (37.72448, -120.998921, 0)

# Overall size of the map, south-west corner, then north-east corner
# south-west: 37.724367, -120.999586
# north-east: 37.725545, -120.998047
# Hence, window will be 0.001178 by 0.001539 in lat/lon coordinates
# Latitude is North to South (equator 0), Longitude is West to East (Greenwich 0)
# Graphing is +x to the right, +y upwards
# Multiplying by 400000 to get pixel space (so ~ 616 by 471 )
# In a real application, please convert correctly, this only works well for small toy examples
latlon_map = (
    (37.724367, -120.999586),
    (37.725545, -120.998047),
)

odom = dict()
stat = dict()

api_url = "https://beta-caladan.polymathrobotics.dev/api/"

# Enter your Polymath Robotics provided Bearer Token and Device Key here!
token = "Bearer Token"
key = "Device Key"
