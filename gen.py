import os
import PIL
import PIL.Image as Image
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw

#from PIL import Image
#from PIL import ImageFont
#from PIL import ImageDraw


def seg(img):
    start = [0, 0]
    end = [img.size[0], img.size[1]]
    x = 0
    y = 0
    while y != img.size[1] and img.getpixel((x, y)) == (255, 255, 255) \
            and x < img.size[0]:
        y += 1
        if img.size[1] == y:
            y = 0
            x += 1

    start[0] = x
    
    x = 0
    y = 0
    while x != img.size[0] and img.getpixel((x, y)) == (255, 255, 255) \
            and y < img.size[1]:
        x += 1
        if img.size[0] == x:
            x = 0
            y += 1
    start[1] = y

    x = img.size[0] - 1
    y = img.size[1] - 1
    while y != img.size[1] and img.getpixel((x, y)) == (255, 255, 255) \
            and x > 0:
        y -= 1
        if y < 0:
            y = img.size[1] - 1
            x -= 1

    end[0] = x
    
    x = img.size[0] - 1
    y = img.size[1] - 1
    while x != img.size[0] and img.getpixel((x, y)) == (255, 255, 255) \
            and y > 0:
        x -= 1
        if x < 0:
            x = img.size[0] - 1
            y -= 1
    end[1] = y
    
    return start, end


def gen(letter, fontname, path, fontdir="fonts/", bindir="bin/"):
    img = Image.new('RGB', (512, 512), color=(255, 255, 255))
    
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(fontdir + fontname, 256)
    draw.text((0, 0), letter, (0, 0, 0), font=font)
    
    rstart, rend = seg(img)
    cbox = (rstart[0], rstart[1], rend[0], rend[1])
    
    letter = img.crop(box=cbox)

    rbox = (0, 0) + letter.size
    mini = letter.resize((28, 28), PIL.Image.ANTIALIAS)
    
    #draw.line((rstart[0], rstart[1], rend[0], rstart[1]), fill=(0, 0, 0))
    #draw.line((rstart[0], rstart[1], rstart[0], rend[1]), fill=(0, 0, 0))
    #draw.line((rstart[0], rend[1], rend[0], rend[1]), fill=(0, 0, 0))
    #draw.line((rend[0], rstart[1], rend[0], rend[1]), fill=(0, 0, 0))
    
    mini.save(bindir + path, quality=100)


def main():
    fontdir = "fonts/"
    bindir = "bin/"
    fonts = os.listdir(fontdir)
    ascii_table = [i for i in range(33, 128)]

    for font in fonts:
        print("  FONT: " + font)
        for c in ascii_table:
            letter = chr(c)
            print("ascii: " + str(c) + "  " + letter)
            gen(letter, font, str(c) + "_" + font  + ".png", \
                    fontdir=fontdir, bindir=bindir)
        print("\n\n")

if __name__ == "__main__":
    main()
