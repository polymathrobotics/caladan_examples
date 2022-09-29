#! /usr/bin/env python3

# Copyright (c) 2022-present, Polymath Robotics, Inc.
# Example UI for using the Caladan API in Python to communicate with Fields2Cover to command tilling paths
# Designed as a simple teaching example, not feature complete or fully robust.

import rospy
import time  # used for sleep
import math  # used for some basic trigonometry
import PySimpleGUI as sg  # used for the Gui
import caladan_api  # example API library
import config.realworld_config as realworld_config  # simple convenience, used to store config values
import tf2_ros
from std_msgs.msg import Bool
from geographic_msgs.msg import GeoPose

url = realworld_config.api_url
token = realworld_config.token
key = realworld_config.key

font = ("Courier New", 7)

rospy.init_node('caladan_example')
tfBuffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tfBuffer)
rate_hz = rospy.get_param('~rate', 120)
rate = rospy.Rate(rate_hz)
rospy.loginfo(f"Starting nav gui at {rate_hz} Hz.")

rospy.loginfo(f" realworld_config.latlon_map[0][0] {realworld_config.latlon_map[0][0]}")
rospy.loginfo(f" realworld_config.latlon_map[1][0] {realworld_config.latlon_map[1][0]}")
rospy.loginfo(f" realworld_config.latlon_map[0][1] {realworld_config.latlon_map[0][1]}")
rospy.loginfo(f" realworld_config.latlon_map[1][1] {realworld_config.latlon_map[1][1]}")

y_gps = abs(realworld_config.latlon_map[0][0] - realworld_config.latlon_map[1][0])
x_gps = abs(realworld_config.latlon_map[0][1] - realworld_config.latlon_map[1][1])
y_scale = 878/y_gps
x_scale = 935/x_gps

rospy.loginfo(f"y gps {y_gps}")
rospy.loginfo(f"x gps {x_gps}")

api = caladan_api.SimpleAPI("", "", "")  # Init to avoid flake8 issues

sg.theme("DarkGrey10")
layout = [
    [sg.Text("Please provide Token and Key below", key="-PROMPT-")],
    [sg.Input(token)],
    [sg.Input(key)],
    [sg.Button("Connect"), sg.Text("", key="-VEL-"), sg.Text("", key="-POSE-")],
    [
        sg.Graph(
            canvas_size=(x_gps * x_scale, y_gps * y_scale),
            graph_bottom_left=(0, 0),
            graph_top_right=(x_gps * x_scale, y_gps * y_scale),
            background_color="#1C1E23",
            enable_events=True,
            key="graph",
        )
    ],
    [
        sg.Button("Start Tilling"),
        sg.Button("STOP", button_color=("white", "red")),
        sg.Text("", key="-STATUS-", size=(45, None)),
    ],
]


window = sg.Window(
    "Polymath Robotics real World Example",
    layout,
    icon="./images/icon.png",
    finalize=True,
)
graph = window["graph"]

def latlon_to_pixelXY(lat, lon):
    return (
        -x_scale * (realworld_config.latlon_map[0][1] - lon),
        -y_scale * (realworld_config.latlon_map[0][0] - lat),
    )

def pixelXY_to_latlon(x, y):
    return (
        realworld_config.latlon_map[0][0] + y / y_scale,
        realworld_config.latlon_map[0][1] + x / x_scale,
    )

def send_laton_goal(lat, lon, yaw):
    x, y = latlon_to_pixelXY(lat, lon)
    graph.draw_circle((x, y), 3, fill_color="#1C1E23", line_color="red")
    graph.DrawText(
        text=(round(lat, 12), round(lon, 12)),
        location=(x - 50, y),
        font=font,
        color="white",
    )
    goalPose = GeoPose()
    goalPose.position.latitude = lat
    goalPose.position.longitude = lon
    field_vertices_pub.publish(goalPose)

def update_loop():
    while True:
        """
        farmworld_config.stat = api.goal_status()
        farmworld_config.odom = api.pose_with_odometry()
        if "orientation" in farmworld_config.odom:
            quat = farmworld_config.odom["orientation"]
            farmworld_config.odom["orientation"] = math.atan2(
                2.0 * (quat["w"] * quat["z"]), 1.0 - 2.0 * (quat["z"] * quat["z"])
            )
            window.write_event_value("-UPDATE-", "updated")
        else:
            print(farmworld_config.odom)
        """

        time.sleep(1.2)

def tilling():
    print("begin tilling")
    begin_tilling_bool = Bool()
    begin_tilling_bool.data = 1
    begin_tilling_pub.publish(begin_tilling_bool)

def graph_clean():
    graph.Erase()
    graph.DrawImage(filename="./images/realwithgeofence.png", location=(0, y_gps * y_scale))

field_vertices_pub = rospy.Publisher("/fields_vertices_sub", GeoPose, queue_size = 1000)
begin_tilling_pub = rospy.Publisher("/begin_tilling_sub", Bool, queue_size = 1000)

graph_clean()

rate.sleep()

while True:  # Main UI Loop
    event, values = window.read()

    if event == sg.WIN_CLOSED:  # Handle closing window
        break

    if window["Connect"].get_text() == "Connected":
            if event == "Start Tilling":
                window.perform_long_operation(tilling, "-tilling DONE-")

            if event == "STOP":
                graph_clean()
                api.cancel_prev_goal()

            if event == "graph":
                x, y = values["graph"]
                lat, lon = pixelXY_to_latlon(x, y)
                send_laton_goal(lat, lon, yaw = 0)

    if event == "Connect":  # First time clicking the connect button, check we get UUID

        window["Connect"].update(button_color=("black", "green"))
        window.perform_long_operation(update_loop, "-OPERATION DONE-")
        window["Connect"].update("Connected")
        graph_clean()

        api = caladan_api.SimpleAPI(url, values[1], values[0])
        uuid_response = api.get_uuid()
        if "uuid" in uuid_response:
            window["-PROMPT-"].update(
                "Successfully connected to vehicle " + uuid_response["uuid"]
            )
            window["Connect"].update(button_color=("black", "green"))
            window.perform_long_operation(update_loop, "-OPERATION DONE-")
            window["Connect"].update("Connected")
            graph_clean()
        else:
            window["-PROMPT-"].update(
                uuid_response
            )  # otherwise, print returned error message


window.close()
