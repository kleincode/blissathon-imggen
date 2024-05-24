from imagen2.gen_img import gen_img
from PIL import Image, ImageDraw
import os

FONT_SIZE = 250

# Picasso sometimes has difficulties generating images, same with Michelangelo, Andy Warhol, Hundertwasser, Gerhard Richter
# Manet works but images are not great
# Van Gogh is nice
# Monet works well
# Salvador Dali works too
# Franz Marc works too
# Da Vinci works
# Cave Painting ist supi
# Roy Lichtenstein auch cool
# Miro not so good
# Medieval Art is ok
# "Van Gogh", "Cave Painting", "Da Vinci", "Salvador Dali", "Monet", 

for artist in (["Franz Marc"]):
    # generate 4 images
    for i, prompt in enumerate([f"Cute moment in a cafe with friends in the style of {artist}", f"Working on a computer in the style of {artist}", f"Reading a book in the livingroom in the style of {artist}", f"Partying in Berlin with friends the style of {artist}"]):
        files = gen_img(prompt, 1)
        if files:
            img = Image.open(files[0])
            img.save(f"vangogh/{artist}_{i}.png")
            print(f"Saved vangogh/{artist}_{i}.png")

    # Merge images
    image_0 = Image.open(f"vangogh/{artist}_0.png")
    image_1 = Image.open(f"vangogh/{artist}_1.png")
    image_2 = Image.open(f"vangogh/{artist}_2.png")
    image_3 = Image.open(f"vangogh/{artist}_3.png")
    image_size = image_0.size
    new_image = Image.new('RGB',(2*image_size[0], 2*image_size[1]), (250,250,250))
    new_image.paste(image_0,(0,0))
    new_image.paste(image_1,(0, image_size[1]))
    new_image.paste(image_2,(image_size[0], image_size[1]))
    new_image.paste(image_3,(image_size[0],0))

    # Draw text: Van Gogh Dump
    draw = ImageDraw.Draw(new_image)
    draw.multiline_text((1536,1536), f"{artist} Dump", fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2, anchor="mm", font_size=FONT_SIZE)

    # Save merged and described image
    new_image.save(f"dump_post/dump_image_{artist}.jpg","JPEG")
    new_image.show()

print("Done!")