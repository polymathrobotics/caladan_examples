#! /usr/bin/env python3

# Copyright (c) 2022-present, Polymath Robotics, Inc.
# Example portworld UI for using the Caladan API in Python
# Designed as a simple teaching example, not feature complete or fully robust.

# GPS Coordinates hardcoded for example simplicity
# bottom left: 37.72475936903438, -120.99873450248205
# top right: 37.72600802278773, -121.00031316114797
# top left: 37.72475936903438, -121.00031316114797
# bottom right: 37.72600802278773, -120.99873450248205
# Hence, window will be 0.001248654 by 0.001578659 in lat/lon coordinates
# Multiplying by 400000 to get pixel space (so ~ 500 x 632)

import time
import math
import PySimpleGUI as sg
import caladan_api
import portworld_config

url = portworld_config.api_url
api = caladan_api.SimpleAPI("", "", "")
scale = 400000.0  # Used to change scale of drawing scene
font = ("Courier New", 6)

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
        sg.Button("Start Parking"),
        sg.Button("STOP", button_color=("white", "red")),
        sg.Button("Train Load"),
        sg.Button("Train Unload"),
    ],
    [
        sg.Button("Return to Equipment Shed"),
        sg.Button("Crane A"),
        sg.Button("Crane B"),
        sg.Button("Crane C"),
    ],
]


window = sg.Window(
    "Polymath Robotics Caladan Portworld Example",
    layout,
    icon="../images/icon.png",
    finalize=True,
)
graph = window["graph"]


def send_goal(lat, lon, yaw):
    api.send_gps_goal(lat, lon, yaw)


def update_loop():
    while True:
        time.sleep(1.2)
        portworld_config.odom = api.pose_with_odometry()
        quat = portworld_config.odom["orientation"]
        portworld_config.odom["orientation"] = math.atan2(
            2.0 * (quat["w"] * quat["z"]), 1.0 - 2.0 * (quat["z"] * quat["z"])
        )
        window.write_event_value("-UPDATE-", "updated")


def tolerance_check(goal, tol):
    if (
        abs(portworld_config.odom["position"]["latitude"] - goal[0]) < tol
        and abs(portworld_config.odom["position"]["longitude"] - goal[1]) < tol
    ):
        return False
    else:
        return True


def parking():
    for goal in portworld_config.parking_goals:
        send_goal(*goal)
        while tolerance_check(goal, 0.0001):
            time.sleep(0.5)


def clear_image():
    graph.Erase()
    image = graph.DrawImage(
        filename="../images/port_world.png", location=(0, 0.001578659 * scale - 1)
    )
    graph.DrawImage(filename="../images/port_world.png", location=(0, 0.001578659 * scale - 1))


clear_image()

while True:
    event, values = window.read()
    # print(event, values)
    graph.draw_rectangle(
        (1, 1), (0.001248654 * scale - 1, 0.001578659 * scale - 1), line_color="#719CDA"
    )

    if window["Connect"].get_text() == "Connected":  # Only update if connected
        # print(portworld_config.odom)
        window["-VEL-"].update(
            str(round(portworld_config.odom["odometry"]["linear.x"], 2)) + " m/s  "
        )
        current_pose = (
            "lat: "
            + str(round(portworld_config.odom["position"]["latitude"], 6))
            + " lon: "
            + str(round(portworld_config.odom["position"]["longitude"], 6))
            + " angle: "
            + str(round(portworld_config.odom["orientation"], 3))
        )
        window["-POSE-"].update(current_pose)
        draw_pose = (
            scale * (37.72600802278773 - portworld_config.odom["position"]["latitude"]),
            -scale
            * (-121.00031316114797 - portworld_config.odom["position"]["longitude"]),
        )
        position = graph.draw_circle(
            draw_pose, 3, fill_color="#1C1E23", line_color="white"
        )

    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if event == "Connect":
        api = caladan_api.SimpleAPI(url, values[1], values[0])
        uuid_response = api.get_uuid()
        if "uuid" in uuid_response:
            window["-PROMPT-"].update(
                "Successfully connected to vehicle " + uuid_response["uuid"]
            )
            window["Connect"].update(button_color=("black", "green"))
            window["Connect"].update("Connected")
            window.perform_long_operation(update_loop, "-OPERATION DONE-")
        else:
            window["-PROMPT-"].update(uuid_response)
    if (
        event == "Return to Equipment Shed"
        and window["Connect"].get_text() == "Connected"
    ):
        clear_image()
        send_goal(37.724982, -120.999135, 0)
    if event == "Crane A" and window["Connect"].get_text() == "Connected":
        clear_image()
        send_goal(37.725817, -120.99906, 3.14)
    if event == "Crane B" and window["Connect"].get_text() == "Connected":
        clear_image()
        send_goal(37.725608, -120.99908, 3.14)
    if event == "Crane C" and window["Connect"].get_text() == "Connected":
        clear_image()
        send_goal(37.725386, -120.99907, 3.14)
    if event == "Start Parking" and window["Connect"].get_text() == "Connected":
        clear_image()
        window.perform_long_operation(parking, "-parking DONE-")
    if event == "STOP" and window["Connect"].get_text() == "Connected":
        api.cancel_prev_goal()
        clear_image()
    if event == "graph" and window["Connect"].get_text() == "Connected":
        clear_image()
        x, y = values["graph"]
        lat, lon, yaw = (
            37.72600802278773 - x / scale,
            -121.00031316114797 - y / -scale,
            0,
        )  # NOTE: Clicking on the map always sends orientation 0!
        lat_lon_label = graph.DrawText(
            text=(round(lat, 5), round(lon, 5)),
            location=(x, y - 7),
            font=font,
            color="white",
        )
        target = graph.draw_circle((x, y), 3, fill_color="#1C1E23", line_color="red")
        send_goal(lat, lon, yaw)

window.close()
