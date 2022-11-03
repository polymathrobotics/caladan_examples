# Copyright (c) 2022-present, Polymath Robotics, Inc.
# Example farmworld UI for using the Caladan API in Python
# Designed as a simple teaching example, not feature complete or fully robust.



# Example single goal to return to the shed
shed_goal = (37.724570, -120.998354, 0)

# Example Buttons, experiment by changing the name and location/orientations sent
button_a = ("Mine Site A", 37.725380, -120.998295, -3.14)
button_b = ("Mine Site B", 37.725189, -120.998295, -3.14)
button_c = ("Processing Plant", 37.724960, -120.998295, -3.14)
button_d = ("Bulldozer Mode", 37.72466, -120.99931, -3.14)
button_e = ("Dump Truck Mode", 37.72466, -120.99944, 0)

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
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InIwdDRQVnowQklGVjhOSFVhbU5ISyJ9.eyJpc3MiOiJodHRwczovL3BvbHltYXRocm9ib3RpY3MudXMuYXV0aDAuY29tLyIsInN1YiI6ImdCMjhGYUFHMjRnZXdmeGlGZE9zN3REUDFTTEJROExFQGNsaWVudHMiLCJhdWQiOiJodHRwOi8vb3BlbnNpbS1jdXN0b21lci1hcGkuY29tIiwiaWF0IjoxNjY2MTMwMzQyLCJleHAiOjE2Njg3MjIzNDIsImF6cCI6ImdCMjhGYUFHMjRnZXdmeGlGZE9zN3REUDFTTEJROExFIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOltdfQ.CeCFTqqpuIoX7y6g2nDW91sznE6oejA7ohj3cDZ7IL5c9VpvW9tHgz_BynfuznPCWfg2N4BAe--AKu7ikNUfQMQJTscCMo6ZgM14z09K4jCyVDy6yxpUtXDeIq_3VXX5YiWmP3RS_1yzqeyy4IF-02GvsUX9vO8oowmNYI_dxhP5eKzLhWgerNGNlhpWwDRM6O13yrWuFzTIlijw0MxGIh50yb7CB3EfVCoCLalgLHPy_VWJL8Er4_JZMoNTE5MJKlTtCLn41Olq2PYov8TxIo0ALSjXll7Q0Z1wfBt_tl2vId9qtmXPIRPX6R7qgblfXmQ7iJMiRDQ0SquldFpHQA"
key = "ps76qow4c"
