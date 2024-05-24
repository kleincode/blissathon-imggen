import requests
from argparse import ArgumentParser

def publish(file: str, api_key: str = "km5gzy6y"):
    with open(file, "rb") as f:
        response = requests.request("POST", f"https://blissathon-jti4p3e3wa-oe.a.run.app/api/upload",
            #data=file,
            #params={"key": "km5gzy6y"},
            files={"file": f},
            #json={"key": "km5gzy6y"},
            data={"key": api_key},
            #headers={"Content-Type": "application/json"}
        )
    print(response.text)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file", type=str)
    args = parser.parse_args()
    publish(args.file)