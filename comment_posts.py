import requests
import json
import random
from gemini.ask_gemini import ask_gemini
from texttospeech import generateSpeech
from PIL import Image as PILImage
from PIL import features
import io
from PIL import ImageDraw
from moviepy.editor import *
from publish import publish
import moviepy.video.io.ImageSequenceClip
from imagen2.gen_img import gen_img
from datetime import datetime


import vertexai
from vertexai.preview.generative_models import GenerativeModel, Image

random.seed(datetime.now().timestamp())
FONT_SIZE = 50

PROJECT_ID = "bliss-hack24ber-6526"
REGION = "us-central1"
vertexai.init(project=PROJECT_ID, location=REGION)

response = requests.request("GET", f"https://blissathon-jti4p3e3wa-oe.a.run.app/api/list",
    params={"key": "km5gzy6y"},
)
data = json.loads(response.text)

success = False
generative_multimodal_model = GenerativeModel("gemini-1.5-pro-preview-0409")
while not success:
    post = random.choice(data["posts"])
    if (post["type"] != "image"):
        continue

    print("Commenting on https://blissathon-jti4p3e3wa-oe.a.run.app/" + post["url"])
    
    image = requests.request("GET", f"https://blissathon-jti4p3e3wa-oe.a.run.app/" + post["url"],
        params={"key": "km5gzy6y"},
    ).content
    pilImage = PILImage.open(io.BytesIO(image))
    img_byte_arr = io.BytesIO()
    pilImage.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    loadedImage = Image.from_bytes(img_byte_arr)
    response = generative_multimodal_model.generate_content(["Roast this image", loadedImage])
    roastText = response.candidates[0].content.parts[0].text
    print(roastText)
    response = generative_multimodal_model.generate_content(["Is the following comment a roast? answer with 'True' or 'False'. Text: " + roastText])
    validRoast = response.candidates[0].content.parts[0].text
    print("valid? " + validRoast)
    response = generative_multimodal_model.generate_content(["Is the following comment funny? answer with 'True' or 'False'. Text: " + roastText])
    funnyRoast = response.candidates[0].content.parts[0].text
    print("funny? " + funnyRoast)
    if "True" in validRoast and "True" in funnyRoast:
        success = True
        audio = generateSpeech("<speak> " + roastText + "<break time='500ms'/> Like this post or you also get roasted!</speak>")
        with open("roastOutput.mp3", "wb") as out:
            out.write(audio)
            print('Audio content written to file "roastOutput.mp3"')

        ## Build image
        outputImage = PILImage.open(io.BytesIO(img_byte_arr))
        base = PILImage.new('RGBA', (outputImage.size[0] + 200, outputImage.size[1] + 200), (255,255,255,0))
        base.paste( (128, 8, 8), (0, 0, base.size[0], base.size[1]))
        base.paste(outputImage, (100, 100))
        draw = ImageDraw.Draw(base)
        draw.multiline_text((350,50), "ROAST-POST", fill=(255, 255, 255), stroke_width=2, anchor="mm", font_size=FONT_SIZE)
        base.save("roastImg.png")

        audio_clip = AudioFileClip("roastOutput.mp3")
        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(["roastImg.png"], durations=[audio_clip.duration + 1], fps=24)
        clip.audio = audio_clip
        clip.write_videofile('roastPost.mp4')

        sec = input('Publish? (Y/n)\n')

        if sec == "Y":
            print("Publishing...")
            publish("roastPost.mp4")