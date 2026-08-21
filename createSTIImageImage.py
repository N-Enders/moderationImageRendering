from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def wrap_text_pixel(draw, text, font, maxWidth):
    words = text.split(" ")
    lines = []
    current = None

    for word in words:
        if draw.textlength(word, font=font) > maxWidth:
            return None #This just means it automatically is too big, so it cancels

        if current is None:
            test_line = word
        else:
            test_line = current + " " + word

        #If its too big start new line and add the other one to lines var
        if draw.textlength(test_line, font=font) <= maxWidth:
            current = test_line
        else:
            lines.append(current)
            current = word
    if current is not None:
        lines.append(current)
    return lines



def draw_text_autosize_left(image, text, box_sizes, font_path,color="#000000",max_size=200, min_size=1):
    xpos, ypos, width, height = box_sizes

    draw = ImageDraw.Draw(image)

    low = min_size
    high = max_size
    best_fit_font = None
    best_lines = None

    while low <= high:
        size = (low + high) / 2 #This gets the middle of the 2 values
        font = ImageFont.truetype(font_path, size)

        lines = wrap_text_pixel(draw, text, font, width)
        if lines is None:
            #The text pixel wrap failed which means it is too big.
            high = size - 1
            continue

        bbox = draw.multiline_textbbox((0, 0), "\n".join(lines), font=font, align="center")
        box_height = bbox[3] - bbox[1]

        if box_height <= height: #If size is too small it will replace the current best
            best_fit_font = font
            best_lines = lines
            low = size + 1
        else:
            high = size - 1

    #Does the actual drawing
    draw.multiline_text((xpos, ypos + height / 2),"\n".join(best_lines),font=best_fit_font,fill=color,anchor="lm",align="left")
    #draw.rectangle([xpos, ypos, xpos + width, ypos + height],outline="red",width=1)


colorsToHex = {"Blue":"#2958A6", "Green":"#4B8312", "Red":"#791227", "Orange":"#A1640D", "Yellow":"#8F8713", "Purple":"#632595", "Pink":"#9A3C7A", "Teal":"#269484", "Gene":"#434343"}

box_x1, box_y1, box_x2, box_y2 = 415, 125, 790, 320
def buildSTIImage(image,twist,twisted_color,twisted_name):
    background = Image.open("./STIImages/background.png")

    font_path = "./STIImages/STITwistFont.ttf"

    draw_text_autosize_left(
        background,
        twist,
        box_sizes=(box_x1, box_y1, box_x2 - box_x1, box_y2 - box_y1),
        font_path=font_path
    )


    #background.paste(points,(0,0),points) will add when points are finalized
    photoName = "Dolphin"
    if Path(f"./STIPhotos/{image}.jpg").is_file():
        photoName = image
    photo = Image.open(f"./STIPhotos/{photoName}.jpg").convert("RGBA")
    photo = photo.resize((round(photo.width * 0.9), photo.height),Image.Resampling.LANCZOS)
    #icon = ImageOps.expand(icon, border=10, fill='white') didn't work

    background.paste(photo, (25, 28), photo)

    #Avatars
    avatar = Image.open(f"./STIImages/{twisted_color}.png").convert("RGBA")
    avatar = avatar.resize((85,85),Image.Resampling.LANCZOS)
    background.paste(avatar, (421, 32), avatar)

    draw = ImageDraw.Draw(background)
    name_size = 50 - (len(twisted_name)/12 * 28)
    draw.text((515,30), twisted_name, font=ImageFont.truetype("./STIImages/STIFont.ttf",name_size),fill=colorsToHex[twisted_color],anchor="lt",align="left")

    return background


buildSTIImage("Bear","I love big gay men.","Gene","Gene").save("testImage.png")