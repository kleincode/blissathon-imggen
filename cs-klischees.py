from gemini.ask_gemini import ask_gemini
from imagen2.gen_img import gen_img
from PIL import Image, ImageDraw
import os
import moviepy.video.io.ImageSequenceClip
import re

ZODIAC_PROMPT = """
Generate an Instagram post for me where each zodiac sign is assigned to a different programmer type. Use klischees, be funny and be provocative.

For example:
- Sagittarius: weird Linux-Nerd
- Aquarius: outgoing sleek Apple-User
Include all zodiac signs. Respond directly with the list, writing at most one zodiac sign per line.
""".strip()

ZODIAC_SIGNS = "Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces".split(", ")
FONT_SIZE = 95
OUT_FOLDER = "computer-scientists"

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
    image_prompt = ask_gemini("Write an image prompt for drawing a computer scientist. Describe the following klischee: " + venue)
    print("prompt: " + image_prompt)
    files = gen_img(f"{image_prompt}", 1)
    if files:
        img = Image.open(files[0])
        draw = ImageDraw.Draw(img)
        txt = f"{sign}:{venue}"
        # adaptive font size
        font_size = FONT_SIZE
        while True:
            text_width = draw.textlength(txt, font_size=font_size)
            if text_width < 1500:
                break
            else:
                font_size -= 5
        draw.text((1536//2, 1536//2), extra_text, fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2, anchor="mm", font_size=font_size, align="center")
        while True:
            text_width = draw.textlength(extra_text, font_size=font_size)
            if text_width < 1500:
                break
            else:
                font_size -= 5
        draw.text((100, 1536 - 200), extra_text, fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2, font_size=font_size // 2)
        img.save(f"{OUT_FOLDER}/{sign}.png")
        print(f"Saved {OUT_FOLDER}/{sign}.png")

while True:
    end_files = gen_img("Group of people coding", 1)
    if end_files:
        img = Image.open(end_files[0])
        draw = ImageDraw.Draw(img)
        txt = f"Your type of programmer\nbased on your zodiac sign!!!"
        draw.multiline_text((1536//2, 1536//2), txt, fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2, anchor="mm", font_size=FONT_SIZE, align="center")
        img.save(f"{OUT_FOLDER}/cover.png")
        print(f"Saved {OUT_FOLDER}/cover.png")
        break


while True:
    end_files = gen_img("Group of people coding", 1)
    if end_files:
        img = Image.open(end_files[0])
        draw = ImageDraw.Draw(img)
        txt = f"PS: How did it fit you?"
        draw.multiline_text((1536//2, 1536//2), txt, fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2, anchor="mm", font_size=FONT_SIZE, align="center")
        img.save(f"{OUT_FOLDER}/end.png")
        print(f"Saved {OUT_FOLDER}/end.png")
        break

print("Done!")
