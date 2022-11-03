# Copyright (c) 2022-present, Polymath Robotics, Inc.
# Example farmworld UI for using the Caladan API in Python
# Designed as a simple teaching example, not feature complete or fully robust.

# Example single goal to return to the shed
shed_goal = (37.724570, -120.998354, 0)

# Example Buttons, experiment by changing the name and location/orientations sent
button_a = ("Crane A", 37.725380, -120.998295, -3.14)
button_b = ("Crane B", 37.725189, -120.998295, -3.14)
button_c = ("Crane C", 37.724960, -120.998295, -3.14)
button_d = ("Train Load", 37.72465, -120.99914, 0)
button_e = ("Train Unload", 37.72481, -120.99947, -1.57)

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
token = "bearer_token"
key = "device_key"
