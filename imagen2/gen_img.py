import requests
from argparse import ArgumentParser
import subprocess
import base64
import time
from math import floor
from typing import List

def get_access_token():
    result = subprocess.run(["gcloud", "auth", "print-access-token"], stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8").strip()

def gen_img(prompt: str, sample_count: int) -> List[str] | None:
    print("Prompt:", prompt)
    response = requests.request("POST", "https://us-central1-aiplatform.googleapis.com/v1/projects/bliss-hack24ber-6526/locations/us-central1/publishers/google/models/imagegeneration:predict",
        headers={
            "Authorization": f"Bearer {get_access_token()}",
            "Content-Type": "application/json; charset=utf-8"
        },
        json={
            "instances": [
                {
                    "prompt": prompt
                }
            ],
            "parameters": {
                "sampleCount": sample_count,
            }
        }
    ).json()
    if not "predictions" in response:
        print(response)
        return None
    
    timestamp = floor(time.time() * 1000)
    filenames = []
    for i, prediction in enumerate(response["predictions"]):
        img = base64.b64decode(prediction["bytesBase64Encoded"])
        filename = f"out{timestamp}_{i}.png"
        with open(filename, "wb") as f:
            f.write(img)
        print(f"Wrote {filename}")
        filenames.append(filename)
    return filenames


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("prompt", type=str, help="Prompt, use quotes")
    parser.add_argument("--samples", type=int, help="Sample count", default=1)
    args = parser.parse_args()
    gen_img(args.prompt, args.samples)