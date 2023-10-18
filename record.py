import requests

# send an api request to all list of ip cameras to start recording

cameras = [ "http://192.168.0.97:8000/", "http://192.168.0.212:8000/","http://192.168.0.27:8000/"]

for camera in cameras:
    url = camera + "start_recording"
    print(url)
    r = requests.get(url)
    print(r.status_code)
    print(r.text)
    print(r.headers)
    print(r.encoding)
    print(r.json())