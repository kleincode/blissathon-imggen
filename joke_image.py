from gemini.ask_gemini import ask_gemini
from imagen2.gen_img import gen_img
from PIL import Image, ImageDraw
import time
from math import floor

PROMPT = """
Pick a really random subject to write a poem about, something with a sausage. Write down your choice. Then write a short, funny poem about it, each verse on a new line. It should be a maximum of 6 verses.
""".strip()
FONT_SIZE = 80

lines = [line.replace("*", "").strip() for line in ask_gemini(PROMPT).splitlines() if line.strip() != ""]

subject = lines[0]
if ":" in subject:
    col_idx = subject.index(":")
    if col_idx + 1 < len(subject):
        subject = subject[col_idx+1:]
subject = subject.strip()

print("subject:", subject)
print(lines[1:])

for i in range(3):
    print(f"Gen attempt #{i}")
    files = gen_img(subject, 1)
    if files:
        img = Image.open(files[0])
        draw = ImageDraw.Draw(img)
        # adaptive font size
        font_size = FONT_SIZE
        while True:
            text_width = max(draw.textlength(line, font_size=FONT_SIZE) for line in lines[1:])
            if text_width < 1500:
                break
            else:
                font_size -= 5
        # draw text
        draw.multiline_text((1536//2, 1536//2), "\n".join(lines[1:]), fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2, anchor="mm", font_size=FONT_SIZE, align="center")
        filename = f"joke{floor(time.time()*1000)}.png"
        img.save(filename)
        print(f"Saved {filename}")
        break

print("Done!")