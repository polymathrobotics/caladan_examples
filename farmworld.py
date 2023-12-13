#! /usr/bin/env python3

# Copyright (c) 2022-present, Polymath Robotics, Inc.
# Example farmworld UI for using the Caladan API in Python
# Designed as a simple teaching example, not feature complete or fully robust.

import time  # used for sleep
import PySimpleGUI as sg  # used for the Gui
import caladan_api  # example API library
import config.farmworld_config as farmworld_config  # simple convenience, used to store config values
import base64  # Used to display images
from PIL import Image  # Used to display images
from io import BytesIO  # Used to display images

url = farmworld_config.api_url
token = farmworld_config.token
key = farmworld_config.key
scale = 335000.0  # Used to change drawing scale of the map
font = ("Courier New", 7)
latdiff = abs(farmworld_config.latlon_map[0][0] - farmworld_config.latlon_map[1][0])
londiff = abs(farmworld_config.latlon_map[0][1] - farmworld_config.latlon_map[1][1])
api = caladan_api.SimpleAPI("", "", "")  # Init to avoid flake8 issues

sg.theme("DarkGrey10")
layout = [
    [sg.Text("Please provide Token and Key below", key="-PROMPT-")],
    [sg.Input(token)],
    [sg.Input(key)],
    [sg.Button("Connect"), sg.Text("", key="-VEL-"), sg.Text("", key="-POSE-")],
    [
        sg.Graph(
            canvas_size=(londiff * scale, latdiff * scale),
            graph_bottom_left=(0, 0),
            graph_top_right=(londiff * scale, latdiff * scale),
            background_color="#1C1E23",
            enable_events=True,
            key="graph",
        )
    ],
    [
        # sg.Button("Start Tilling"),
        # sg.Button("Pause"),
        sg.Button("Resume"),
        sg.Button("STOP", button_color=("white", "red")),
        sg.Button("Snapshot"),
    ],
    [
        # sg.Button("Return to Equipment Shed"),
        sg.Input("lat", size=10, key="lat"),
        sg.Input("lon", size=10, key="lon"),
        sg.Input("ori", size=10, key="ori"),
        sg.Button("Send Goal"),
    ],
    [
        sg.Text("", key="-STATUS-", size=(45, None)),
    ],
]


window = sg.Window(
    "Polymath Robotics Caladan Farmworld Example",
    layout,
    icon="./images/icon.png",
    finalize=True,
)
graph = window["graph"]


def latlon_to_pixelXY(lat, lon):
    return (
        -scale * (farmworld_config.latlon_map[0][1] - lon),
        -scale * (farmworld_config.latlon_map[0][0] - lat),
    )


def pixelXY_to_latlon(x, y):
    return (
        farmworld_config.latlon_map[0][0] + y / scale,
        farmworld_config.latlon_map[0][1] + x / scale,
    )


def send_goal(lat, lon, yaw):
    x, y = latlon_to_pixelXY(lat, lon)
    graph.draw_circle((x, y), 3, fill_color="#1C1E23", line_color="red")
    graph.DrawText(
        text=(round(lat, 5), round(lon, 5)),
        location=(x, y - 7),
        font=font,
        color="white",
    )
    # print (lat,lon,yaw)
    api.post_gps_waypoints([[lat, lon, yaw]], 1)


def update_loop():
    while True:
        farmworld_config.stat = api.get_polymath_feedback()
        print(farmworld_config.stat)
        if farmworld_config.stat == "Input validation failed":
            print("Update Miss")
        else:
            farmworld_config.odom = farmworld_config.stat[
                "polymath_feedback"
            ]  # ['current_pose']['pose']
            window.write_event_value("-UPDATE-", "updated")
            time.sleep(1)
            window["-PROMPT-"].update(
                "Vehicle Status: "
                + farmworld_config.stat["polymath_feedback"]["cortex_status"][
                    "status_text"
                ]
            )


def tolerance_check(goal, tol):
    if (
        abs(
            farmworld_config.odom["current_pose"]["pose"]["position"]["latitude"]
            - goal[0]
        )
        < tol
        and abs(
            farmworld_config.odom["current_pose"]["pose"]["position"]["longitude"]
            - goal[1]
        )
        < tol
    ):
        return True
    else:
        return False


def tilling():
    for goal in farmworld_config.tilling_goals:
        send_goal(*goal)
        while not tolerance_check(goal, 0.00003):
            time.sleep(0.5)


def snapshot():
    snapshot = api.get_latest_image_frame()["image_base64"]
    image_data = base64.b64decode(snapshot)
    image_io = BytesIO(image_data)
    image = Image.open(image_io)
    image.show()


def graph_clean():
    graph.Erase()
    graph.DrawImage(filename="./images/forest.png", location=(0, latdiff * scale))


graph_clean()

while True:  # Main UI Loop
    event, values = window.read()

    if event == sg.WIN_CLOSED:  # Handle closing window
        break

    # Only update and accept other commands if already connected
    if window["Connect"].get_text() == "Connected":
        window["-VEL-"].update(
            "distance to goal: "
            + str(
                round(
                    farmworld_config.odom["navigation_feedback"][
                        "total_distance_remaining"
                    ],
                    2,
                )
            )
            + " m  "
        )
        current_pose = (
            "lat: "
            + str(
                round(
                    farmworld_config.odom["current_pose"]["pose"]["position"][
                        "latitude"
                    ],
                    6,
                )
            )
            + " lon: "
            + str(
                round(
                    farmworld_config.odom["current_pose"]["pose"]["position"][
                        "longitude"
                    ],
                    6,
                )
            )
            + " angle: "
            + str(
                round(
                    api.quaternion_to_euler(
                        farmworld_config.odom["current_pose"]["pose"]["orientation"]
                    )[2],
                    3,
                )
            )
        )
        window["-POSE-"].update(current_pose)
        window["-STATUS-"].update(farmworld_config.stat)
        draw_pose = latlon_to_pixelXY(
            farmworld_config.odom["current_pose"]["pose"]["position"]["latitude"],
            farmworld_config.odom["current_pose"]["pose"]["position"]["longitude"],
        )
        # print(draw_pose)
        position = graph.draw_circle(
            draw_pose, 3, fill_color="#1C1E23", line_color="white"
        )

        if event == "Return to Equipment Shed":
            graph_clean()
            send_goal(*farmworld_config.shed_goal)

        if event == "Start Tilling":
            graph_clean()
            window.perform_long_operation(tilling, "-tilling DONE-")

        if event == "Snapshot":
            window.perform_long_operation(snapshot, "-snapshot DONE-")

        if event == "STOP":
            graph_clean()
            api.post_motion_command(0, 1)

        if event == "Pause":
            # graph_clean()
            api.post_motion_command(1, 1)

        if event == "Resume":
            # graph_clean()
            api.post_motion_command(2, 0)

        if event == "Send Goal":
            graph_clean()
            try:
                lat, lon, ori = (
                    float(values["lat"]),
                    float(values["lon"]),
                    float(values["ori"]),
                )
                send_goal(lat, lon, ori)
            except ValueError:
                print(
                    "You need to provide latitude, longitude, and orientation values in the text boxes!"
                )

        if event == "graph":
            graph_clean()
            x, y = values["graph"]
            lat, lon = pixelXY_to_latlon(x, y)
            send_goal(
                lat, lon, yaw=1.57
            )  # NOTE: Clicking on the map always sends orientation NORTH!
            # print(lat,lon)

    if event == "Connect":  # First time clicking the connect button, check we get UUID
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
