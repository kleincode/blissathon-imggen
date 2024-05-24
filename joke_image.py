from gemini.ask_gemini import ask_gemini
from imagen2.gen_img import gen_img
from PIL import Image, ImageDraw
import time
from math import floor
from argparse import ArgumentParser

PROMPT = """
Pick a really random subject to write a poem about{suffix}. Write down your choice. Then write a short, funny poem about it, each verse on a new line. It should be a maximum of 6 verses.
""".strip()
FONT_SIZE = 120

def write_joke(subject: str | None = None) -> str | None:
    suffix = "" if subject is None else f", something with a {subject}"
    prompt = PROMPT.replace("{suffix}", suffix)
    lines = [line.replace("*", "").strip() for line in ask_gemini(prompt).splitlines() if line.strip() != ""]

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
                text_width = max(draw.textlength(line, font_size=font_size) for line in lines[1:])
                if text_width < 1500:
                    break
                else:
                    font_size -= 5
            # draw text
            draw.multiline_text((1536//2, 1536//2), "\n".join(lines[1:]), fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2, anchor="mm", font_size=font_size, align="center")
            filename = f"joke{floor(time.time()*1000)}.png"
            img.save(filename)
            print(f"Saved {filename}")
            return filename

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--subject", type=str, default="")
    args = parser.parse_args()
    write_joke(args.subject)
    print("Done!")