#! /usr/bin/env python3

# Copyright (c) 2022-present, Polymath Robotics, Inc.
# Example small API library for using the API in Python
# Designed as a simple teaching example, not feature complete or fully robust.

import requests
import json
import math


class SimpleAPI:
    def __init__(self, url, key, token):
        self.token = token
        self.key = key
        self.url = url
        self.headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + token,
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def status_check(self, data):
        if "status" in data:
            if data["status"] == "success":
                return (data)["data"]
            else:
                return data["message"]
        else:
            return data

    def get_uuid(self):
        api_url = self.url + "uuid?device_key=" + self.key
        response = requests.get(api_url, headers=self.headers, timeout=10)
        return self.status_check(response.json())

    def get_polymath_feedback(self):
        api_url = self.url + "polymath-feedback?device_key=" + self.key
        response = requests.get(api_url, headers=self.headers, timeout=10)
        return self.status_check(response.json())

    def get_latest_image_frame(self):
        api_url = self.url + "latest-image-frame?device_key=" + self.key
        response = requests.get(api_url, headers=self.headers, timeout=10)
        return self.status_check(response.json())

    def post_motion_command(self, motion_command, mode):
        api_url = self.url + "motion-command?device_key=" + self.key
        r = {
            "motion_command": motion_command,  # 0 for STOP, 1 for PAUSE, 2 for RESUME
            "mode": mode,  # 1 for PREEMPT, 0 for ADD
        }
        self.headers["Content-Type"] = "application/json"
        response = requests.post(
            api_url,
            headers=self.headers,
            json=r,
            timeout=10,
        )
        return self.status_check(response.json())

    def post_gps_waypoints(self, goals, preempt):  # Expect an array of 3 entry sets
        api_url = self.url + "gps-waypoints?device_key=" + self.key
        r = {
            "goals": [],
            "navigation_options": {"mode": preempt},  # 1 for PREEMPT, 0 for ADD
        }
        for waypoint in goals:
            r["goals"].append(
                {
                    "lat": json.dumps(waypoint[0]),
                    "lon": json.dumps(waypoint[1]),
                    "yaw": json.dumps(waypoint[2]),
                }
            )
        self.headers["Content-Type"] = "application/json"
        response = requests.post(
            api_url,
            headers=self.headers,
            json=r,
            timeout=10,
        )
        # print (response.json())
        return self.status_check(response.json())

    def post_relative_waypoints(
        self, goals, preempt
    ):  # Expect goals to be an array of 4 entry sets
        api_url = self.url + "relative-waypoints?device_key=" + self.key
        r = {
            "relative_to": "current_position",
            "move_to": [],
            "mode": preempt,  # 1 for PREEMPT, 0 for ADD
        }
        for waypoint in goals:
            r["move_to"].append(
                {
                    "x": json.dumps(waypoint[0]),
                    "y": json.dumps(waypoint[1]),
                    "z": json.dumps(waypoint[2]),
                    "yaw": json.dumps(waypoint[3]),
                }
            )
        self.headers["Content-Type"] = "application/json"
        response = requests.post(
            api_url,
            headers=self.headers,
            json=r,
            timeout=10,
        )
        return self.status_check(response.json())

    def quaternion_to_euler(self, quaternion_dict):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        x = quaternion_dict["x"]
        y = quaternion_dict["y"]
        z = quaternion_dict["z"]
        w = quaternion_dict["w"]

        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)

        return roll_x, pitch_y, yaw_z  # in radians


# Example Usage
# import caladan_api
# url = "https://synapse.api.polymathrobotics.dev/v2/"
# device_key = "*******"
# token = "*****"
# api = SimpleAPI(url, device_key, token)
# print(api.get_uuid())
# print()
# print(api.get_polymath_feedback())
# print()
# print (api.post_gps_waypoints([[37.72521,-120.99957,3.14]],1))
# print()
# print (api.post_relative_waypoints([[1,0,0,0],[1,0,0,0]],0))
# print()
# api.get_latest_image_frame() # Don't print this, it will be huge
