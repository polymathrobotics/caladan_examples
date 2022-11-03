#! /usr/bin/env python3

# Copyright (c) 2022-present, Polymath Robotics, Inc.
# Example small API library for using the API in Python
# Designed as a simple teaching example, not feature complete or fully robust.

import requests
import json


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
        response = requests.get(api_url, headers=self.headers, timeout=30)
        return self.status_check(response.json())
        

    def get_position(self):
        api_url = self.url + "position?device_key=" + self.key
        response = requests.get(api_url, headers=self.headers, timeout=30)
        return self.status_check(response.json())

    def pose_with_odometry(self):
        api_url = self.url + "pose-with-odometry?device_key=" + self.key
        response = requests.get(api_url, headers=self.headers, timeout=30)
        return self.status_check(response.json())

    def goal_status(self):
        api_url = self.url + "goal-status?device_key=" + self.key
        response = requests.get(api_url, headers=self.headers, timeout=30)
        return self.status_check(response.json())

    def send_gps_goal(self, lat, lon, yaw):
        api_url = self.url + "send-gps-goal?device_key=" + self.key
        response = requests.post(
            api_url,
            headers=self.headers,
            data={"lat": lat, "lon": lon, "yaw": yaw},
            timeout=10,
        )
        return self.status_check(response.json())
    
    def send_waypoints(self, goals): #Expect an array of 3 entry sets
        api_url = self.url + "send-waypoints?device_key=" + self.key
        r = {"goals":[]}
        for waypoint in goals:
            print(json.dumps(waypoint[2]))
            r["goals"].append({"lat":json.dumps(waypoint[0]),"lon":json.dumps(waypoint[1]),"yaw":json.dumps(waypoint[2])})
        print (r)
        self.headers["Content-Type"] = "application/json"
        response = requests.post(
            api_url,
            headers=self.headers,
            json=r,
            timeout=10,
        )
        self.headers["Content-Type"] = "application/x-www-form-urlencoded"
        return self.status_check(response.json())    

    def cancel_prev_goal(self):
        api_url = self.url + "cancel-prev-goal?device_key=" + self.key
        response = requests.post(api_url, headers=self.headers, timeout=30)
        return self.status_check(response.json())


# Example Usage in 
# import caladan_api
# url = "https://beta-caladan.polymathrobotics.dev/api/"
# device_key = "*******"
# token= "*******"
# api = SimpleAPI(url,device_key,token)
# print (api.get_uuid())
# print (api.get_position())
# print (api.send_gps_goal(37.72521,-120.99957,3.14))
# print (api.pose_with_odometry())
# print (api.cancel_prev_goal())
# print (api.send_waypoints([[37.725017,-120.998852,None],[37.72519,-120.998815,3.14]]))
# print (api.goal_status()) # Note: that goal status will take a few seconds to change when a new goal is sent
