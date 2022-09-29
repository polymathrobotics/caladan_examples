# Copyright (c) 2022-present, Polymath Robotics, Inc.
# Example UI for using the Caladan API in Python to communicate with Fields2Cover to command tilling paths
# Designed as a simple teaching example, not feature complete or fully robust.

# Overall size of the map, south-west corner, then north-east corner
# south-west: 37.724243, -120.998530
# north-east: 37.725560, -120.997276

latlon_map = (
    (37.724243, -120.998530),
    (37.725560, -120.997276),
)

odom = dict()
stat = dict()

api_url = "https://beta-caladan.polymathrobotics.dev/api/"

# Enter your Polymath Robotics provided Bearer Token and Device Key here!
token = "Bearer Token"
key = "Device Key"