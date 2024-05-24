import os
import moviepy.video.io.ImageSequenceClip
from moviepy.editor import *
import argparse

def combine_images(image_folder: str, audio_file: str):
    ZODIAC_SIGNS = "Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces".split(", ")

    fps=0.5
    image_files = [os.path.join(image_folder, f"{sign}.png")
                for sign in ["cover", *ZODIAC_SIGNS, "end"]
                if os.path.exists(os.path.join(image_folder, f"{sign}.png"))]
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
    audio_clip = AudioFileClip(audio_file)
    clip.audio = audio_clip
    clip.write_videofile(f'{image_folder}.mp4')

    print("Done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image_folder", type=str)
    parser.add_argument("audio_file", type=str)
    args = parser.parse_args()
    combine_images(args.image_folder, args.audio_file)