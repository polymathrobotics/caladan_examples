#! /usr/bin/env python3

# Example Usage
import caladan_api

url = "https://beta-caladan.polymathrobotics.dev/api/"
# url = "https://webhook.site/d830f974-c83c-4764-afd7-437d696e3924/"

device_key = "psdf65eoh"
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InIwdDRQVnowQklGVjhOSFVhbU5ISyJ9.eyJpc3MiOiJodHRwczovL3BvbHltYXRocm9ib3RpY3MudXMuYXV0aDAuY29tLyIsInN1YiI6ImdCMjhGYUFHMjRnZXdmeGlGZE9zN3REUDFTTEJROExFQGNsaWVudHMiLCJhdWQiOiJodHRwOi8vb3BlbnNpbS1jdXN0b21lci1hcGkuY29tIiwiaWF0IjoxNjYzMzUyOTAzLCJleHAiOjE2NjU5NDQ5MDMsImF6cCI6ImdCMjhGYUFHMjRnZXdmeGlGZE9zN3REUDFTTEJROExFIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOltdfQ.Ne_5v5whfH67nO-UFQg7qQMlMbFx5MHqdJEL1smjRPJ1VehFKuceq0XpW4X3v0yNgoKjzzeK1R3JQgl2pA5GoLqAbfb_holPa2UHUU8c9se5ae_300YHIENcfLpuoVob0YYGErrbzNDOzrf4w_gqf58pApQC6MoGk-ZYFIlvc60SGilhYeYfm_670hd3OAXEBsd808xngZ3P0QtEdxP66TZlXOSpaTx9ua6lcdKnwlYIAL8xUu2yECuLto7kSAQ88Ru5m8WNz4JSuxrn_YmW9WbgvCpX6D89iu3_jj119Y0W1MATdBIeVGmljIMkTXzOmlGoznkok3xn8RR2_nuSnw"

api = caladan_api.SimpleAPI(url, device_key, token)

# print (api.get_uuid())

# print (api.send_gps_goal(37.72474,-120.998748,1.57))

goals = [[37.72474, -120.998748, 0], [37.725091, -120.998712, -1.57]]

print(api.send_waypoints(goals))
