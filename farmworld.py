#! /usr/bin/env python3

# Copyright (c) 2022-present, Polymath Robotics, Inc.
# Example farmworld UI for using the Caladan API in Python
# Designed as a simple teaching example, not feature complete or fully robust.

import time  # used for sleep
import math  # used for some basic trigonometry
import PySimpleGUI as sg  # used for the Gui
import CaladanAPI  # example API library included with this example
import farmworld_config  # simple convinience, used to store

url = "https://beta-caladan.polymathrobotics.dev/api/"
api = CaladanAPI.simple_api("", "", "")
scale = 400000.0  # Used to change scale of drawing scene
font = ("Courier New", 7)

sg.theme("DarkGrey10")
layout = [
    [sg.Text("Please provide Token and Key below", key="-PROMPT-")],
    [sg.Input("Bearer Token")],
    [sg.Input("Unique Key")],
    [sg.Button("Connect"), sg.Text("", key="-VEL-"), sg.Text("", key="-POSE-")],
    [
        sg.Graph(
            canvas_size=(0.001248654 * scale, 0.001578659 * scale),
            graph_bottom_left=(0, 0),
            graph_top_right=(0.001248654 * scale, 0.001578659 * scale),
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
    [sg.Button("Return to Equipment Shed")],
]


window = sg.Window(
    "Polymath Robotics Caladan Farmworld Example",
    layout,
    icon="icon.png",
    finalize=True,
)
graph = window["graph"]

# GPS Coordinates hardcoded for example simplicity
# bottom left: 37.72475936903438, -120.99873450248205
# top right: 37.72600802278773, -121.00031316114797
# top left: 37.72475936903438, -121.00031316114797
# bottom right: 37.72600802278773, -120.99873450248205
# Hence, window will be 0.001248654 by 0.001578659 in lat/lon coordinates
# Multiplying by 400000 to get pixel space (so ~ 500 x 632)
# In a real application, please convert correctly, this only works well for small toy examples


def latlon_to_pixelXY(lat, lon):
    return (scale * (37.72600802278773 - lat), -scale * (-121.00031316114797 - lon))


def pixelXY_to_latlon(x, y):
    return (37.72600802278773 - x / scale, -121.00031316114797 - y / -scale)


def send_goal(lat, lon, yaw):
    x, y = latlon_to_pixelXY(lat, lon)
    target = graph.draw_circle((x, y), 3, fill_color="#1C1E23", line_color="red")
    target_text = graph.DrawText(
        text=(round(lat, 5), round(lon, 5)),
        location=(x, y - 7),
        font=font,
        color="white",
    )
    api.send_gps_goal(lat, lon, yaw)


def update_loop():
    while True:
        farmworld_config.stat = api.goal_status()
        farmworld_config.odom = api.pose_with_odometry()
        quat = farmworld_config.odom["orientation"]
        farmworld_config.odom["orientation"] = math.atan2(
            2.0 * (quat["w"] * quat["z"]), 1.0 - 2.0 * (quat["z"] * quat["z"])
        )
        window.write_event_value("-UPDATE-", "updated")
        time.sleep(1.2)


def tolerance_check(goal, tol):
    if (
        abs(farmworld_config.odom["position"]["latitude"] - goal[0]) < tol
        and abs(farmworld_config.odom["position"]["longitude"] - goal[1]) < tol
    ):
        return False
    else:
        return True


def tilling():
    for goal in farmworld_config.tilling_goals:
        send_goal(*goal)
        while tolerance_check(goal, 0.00003):
            time.sleep(0.5)


def graph_clean():
    graph.Erase()
    image = graph.DrawImage(
        filename="farm_world.png", location=(0, 0.001578659 * scale - 1)
    )


while True:  # Main UI Loop
    event, values = window.read()

    if event == sg.WIN_CLOSED:  # Handle closing window
        break

    if (
        window["Connect"].get_text() == "Connected"
    ):  # Only update and accept other commands if already connected
        window["-VEL-"].update(
            str(round(farmworld_config.odom["odometry"]["linear.x"], 2)) + " m/s  "
        )
        current_pose = (
            "lat: "
            + str(round(farmworld_config.odom["position"]["latitude"], 6))
            + " lon: "
            + str(round(farmworld_config.odom["position"]["longitude"], 6))
            + " angle: "
            + str(round(farmworld_config.odom["orientation"], 3))
        )
        window["-POSE-"].update(current_pose)
        window["-STATUS-"].update(farmworld_config.stat)
        draw_pose = latlon_to_pixelXY(
            farmworld_config.odom["position"]["latitude"],
            farmworld_config.odom["position"]["longitude"],
        )
        position = graph.draw_circle(
            draw_pose, 3, fill_color="#1C1E23", line_color="white"
        )

        if event == "Return to Equipment Shed":
            graph_clean()
            send_goal(37.72488196909861, -120.99962795857607, 0)

        if event == "Start Tilling":
            graph_clean()
            window.perform_long_operation(tilling, "-tilling DONE-")

        if event == "STOP":
            graph_clean()
            api.cancel_prev_goal()

        if event == "graph":
            graph_clean()
            x, y = values["graph"]
            lat, lon = pixelXY_to_latlon(x, y)
            send_goal(
                lat, lon, yaw=0
            )  # NOTE: Clicking on the map always sends orientation 0!

    if event == "Connect":  # First time clicking the connect button, check we get UUID
        api = CaladanAPI.simple_api(url, values[1], values[0])
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
