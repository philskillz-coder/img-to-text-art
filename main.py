import random
from PIL import Image, ImageDraw, ImageOps, ImageFont

CHARACTER_SPACING = 8
RESIZED_WIDTH = 500
BRIGHTNESS_LEVELS = 16
FONT_SIZE = 12
IMAGE_PATH = "img.png"
TEXT = "theskzforever"

filename = f"output/save.character_spacing-{CHARACTER_SPACING}.resized_width-{RESIZED_WIDTH}.brightness_levels-\
{BRIGHTNESS_LEVELS}.font_size-{FONT_SIZE}.text-{TEXT}.png "

font = ImageFont.truetype("arial.ttf", FONT_SIZE)

original = Image.open(IMAGE_PATH)

# original = ImageOps.invert(original)
original = ImageOps.grayscale(original)

w_pc = (RESIZED_WIDTH / float(original.size[0]))
hsize = int((float(original.size[1]) * float(w_pc)))
original = original.resize((RESIZED_WIDTH, hsize), Image.Resampling.LANCZOS)

pixels = list(original.getdata())
width, height = original.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

new = Image.new("RGB", (original.size[0] * CHARACTER_SPACING, original.size[1] * CHARACTER_SPACING), "WHITE")
draw = ImageDraw.Draw(new)


# base=4
# 0 -> 4
# 1 -> 3
# 2 -> 2
# 3 -> 1
# 4 -> 0
def invert_0(base: int, n: int) -> int:
    return int((n - base / 2) * -1 + base / 2)


def invert_1(base: int, n: int) -> int:
    return int((-1 - n) % base)


def chunks(base: int, n: int) -> int:
    return int(n // (256 / base))


def zero_if_negative(n: int) -> int:
    return int((abs(n) + n) / 2)


current_character = 0
for row, row_data in enumerate(pixels):
    print(f"ROW {row}/{(x:= len(pixels))}: {(row/x)*100:.2f}%")
    for pixel, pixel_data in enumerate(row_data):
        letters = invert_1(BRIGHTNESS_LEVELS, chunks(BRIGHTNESS_LEVELS, pixel_data)) + 1  # minimum=1
        offset_bounds = 2 * letters  # area of (2 * letters)^2

        # no random letter placement
        if letters == 1:
            draw.text(
                (pixel * CHARACTER_SPACING, row * CHARACTER_SPACING),
                TEXT[current_character],
                (0, 0, 0, 255),
                font=font,
            )
            current_character += 1
            current_character %= len(TEXT)

        # place the letters randomly within the offset bounds to create an effect of darkness
        else:
            for x in range(letters):
                offset_x = random.randint(-offset_bounds, offset_bounds) // 2
                offset_y = random.randint(-offset_bounds, offset_bounds) // 2

                draw.text(
                    (
                        zero_if_negative(pixel * CHARACTER_SPACING + offset_x),
                        zero_if_negative(row * CHARACTER_SPACING + offset_y)
                    ),
                    TEXT[current_character],
                    (0, 0, 0, 255),
                    font=font,
                )
                current_character += 1
                current_character %= len(TEXT)

new.show()
new.save(filename, format="png")
