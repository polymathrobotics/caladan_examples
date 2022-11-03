# Copyright (c) 2022-present, Polymath Robotics, Inc.
# Example farmworld UI for using the Caladan API in Python
# Designed as a simple teaching example, not feature complete or fully robust.

# Example set of goals for vehicle to follow
tilling_goals = [
    (37.724908, -120.998889, 1.57),  # start of row 1
    (37.725445, -120.998889, 1.57),  # end of row 1
    (37.725495, -120.998857, 0),  # turn around midpoint
    (37.725445, -120.998811, -1.57),  # start of row 2
    (37.724908, -120.998811, -1.57),  # end of row 2
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
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InIwdDRQVnowQklGVjhOSFVhbU5ISyJ9.eyJpc3MiOiJodHRwczovL3BvbHltYXRocm9ib3RpY3MudXMuYXV0aDAuY29tLyIsInN1YiI6ImdCMjhGYUFHMjRnZXdmeGlGZE9zN3REUDFTTEJROExFQGNsaWVudHMiLCJhdWQiOiJodHRwOi8vb3BlbnNpbS1jdXN0b21lci1hcGkuY29tIiwiaWF0IjoxNjYzMzUyOTAzLCJleHAiOjE2NjU5NDQ5MDMsImF6cCI6ImdCMjhGYUFHMjRnZXdmeGlGZE9zN3REUDFTTEJROExFIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOltdfQ.Ne_5v5whfH67nO-UFQg7qQMlMbFx5MHqdJEL1smjRPJ1VehFKuceq0XpW4X3v0yNgoKjzzeK1R3JQgl2pA5GoLqAbfb_holPa2UHUU8c9se5ae_300YHIENcfLpuoVob0YYGErrbzNDOzrf4w_gqf58pApQC6MoGk-ZYFIlvc60SGilhYeYfm_670hd3OAXEBsd808xngZ3P0QtEdxP66TZlXOSpaTx9ua6lcdKnwlYIAL8xUu2yECuLto7kSAQ88Ru5m8WNz4JSuxrn_YmW9WbgvCpX6D89iu3_jj119Y0W1MATdBIeVGmljIMkTXzOmlGoznkok3xn8RR2_nuSnw"
key = "ps2g9vajn"
