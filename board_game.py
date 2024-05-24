from gemini.ask_gemini import ask_gemini
from imagen2.gen_img import gen_img
from PIL import Image, ImageDraw
import time
from math import floor

PROMPT = """
pick a random polictical conflict from the 20th or 21th century and describe in a few sentences how one could meme the conflict using an image of an existing board game where the most important persons are the game figures.""".strip()
FONT_SIZE = 80

gemini_out = ask_gemini(PROMPT)

print("gemini output:", gemini_out)

for i in range(3):
    print(f"Gen attempt #{i}")
    files = gen_img(gemini_out, 1)
    if files:
        img = Image.open(files[0])
        draw = ImageDraw.Draw(img)
        #draw.multiline_text((1536//2, 1536//2), "\n".join(lines[1:]), fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2, anchor="mm", font_size=FONT_SIZE, align="center")
        filename = f"board_game{floor(time.time()*1000)}.png"
        img.save(filename)
        print(f"Saved {filename}")
        break

print("Done!")