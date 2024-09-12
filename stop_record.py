import requests

# send an api request to all list of ip cameras to stop recording

cameras = [ "http://192.168.0.97:8000/", "http://192.168.0.212:8000/","http://192.168.0.27:8000/"]

for camera in cameras:

    url = camera + "stop_recording"
    print(url)
    r = requests.get(url)
    print(r.status_code)
    print(r.text)
    print(r.headers)
    print(r.encoding)
    print(r.json())


## Output file: 19-09-2023 18:40:12__HG__0.mp4 night time

# Assign device ID to each camera

# cameras = [ "http://192.168.0.97:8000/", "http://192.168.0.212:8000/","http://192.168.0.27:8000/"]
#
# for i , camera in enumerate(cameras):
#
#     url = camera + "assign_device_id?device_id=" + str(i)
#     print(url)
#     r = requests.get(url)
#     print(r.status_code)
#     print(r.text)
#     print(r.headers)
#     print(r.encoding)
#     print(r.json())
