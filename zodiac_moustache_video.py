from gemini.ask_gemini import ask_gemini
from imagen2.gen_img import gen_img
from PIL import Image, ImageDraw
import os
import moviepy.video.io.ImageSequenceClip
import re

ZODIAC_PROMPT = """
Generate an Instagram post for me where each zodiac sign is assigned to a specific kind of moustache.

For example:
- Sagittarius: Handlebar
- Aquarius: English
Include all zodiac signs. Respond directly with the list, writing at most one zodiac sign per line.
""".strip()
OUTPUT_FOLDER = "moustache"

ZODIAC_SIGNS = "Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces".split(", ")
FONT_SIZE = 120

post_text = ask_gemini(ZODIAC_PROMPT)

print("Parsing texts")

def filter_line(line: str) -> str:
    line = re.sub(r":\w+:", "", line)
    return line.replace("*", "").replace(":fire:", "").replace(":heart:", "").replace(":bug:", "").replace(":beetle:", "").replace(":arrow:", "").replace(":mountain:", "").replace(":ocean:", "").replace(":music:", "")

lines = [filter_line(line) for line in post_text.splitlines(keepends=False)]

def find_line(sign: str) -> str | None:
    for line in lines:
        if sign.lower() in line.lower():
            return line

def extract_venue(line: str) -> str:
    line = "".join([i if i.isalnum() or ord(i) < 128 else ' ' for i in line])
    extra_text = ""
    col_index = line.index(":") if ":" in line else -1
    if 0 <= col_index + 2 < len(line):
        line = line[col_index+2:]
    hyphen_index = line.index("-") if "-" in line else -1
    if hyphen_index > 4:
        if hyphen_index + 1 < len(line):
            extra_text = line[hyphen_index+1:].strip()
        line = line[:hyphen_index]
    return line.strip(), extra_text

for sign in ZODIAC_SIGNS:
    sign_line = find_line(sign)
    venue, extra_text = extract_venue(sign_line)
    print(sign, venue)
    files = gen_img(f"{sign} man with a {venue} moustache", 1)
    if files:
        img = Image.open(files[0])
        draw = ImageDraw.Draw(img)
        txt = f"{sign}: {venue}"
        draw.text((1536//2, 1536//2), txt, fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2, anchor="mm", font_size=FONT_SIZE)
        draw.text((100, 1536 - 200), extra_text, fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2, font_size=FONT_SIZE // 3)
        img.save(f"{OUTPUT_FOLDER}/{sign}.png")
        print(f"Saved {OUTPUT_FOLDER}/{sign}.png")

while True:
    end_files = gen_img("Berlin TV tower with a moustache", 1)
    if end_files:
        img = Image.open(end_files[0])
        draw = ImageDraw.Draw(img)
        txt = f"What moustache fits your\nZODIAC SIGN?"
        draw.multiline_text((1536//2, 1536//2), txt, fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2, anchor="mm", font_size=FONT_SIZE, align="center")
        img.save(f"{OUTPUT_FOLDER}/cover.png")
        print(f"Saved {OUTPUT_FOLDER}/cover.png")
        break


while True:
    end_files = gen_img("Woman with giant moustache", 1)
    if end_files:
        img = Image.open(end_files[0])
        draw = ImageDraw.Draw(img)
        txt = f"Bring back moustaches!"
        draw.multiline_text((1536//2, 1536//2), txt, fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2, anchor="mm", font_size=FONT_SIZE, align="center")
        img.save(f"{OUTPUT_FOLDER}/end.png")
        print(f"Saved {OUTPUT_FOLDER}/end.png")
        break

print("Done!")
