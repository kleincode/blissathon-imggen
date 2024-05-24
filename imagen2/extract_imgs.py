import json
import base64

with open("response.json") as f:
    response = json.load(f)

for i, prediction in enumerate(response["predictions"]):
    img = base64.b64decode(prediction["bytesBase64Encoded"])
    with open(f"img{i}.png", "wb") as f:
        f.write(img)

print("Done")