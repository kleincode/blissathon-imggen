import requests
response = requests.request("GET", f"https://blissathon-jti4p3e3wa-oe.a.run.app/api/list",
    params={"key": "km5gzy6y"},
    #headers={"Content-Type": "application/json"}
)
print(response.text)
