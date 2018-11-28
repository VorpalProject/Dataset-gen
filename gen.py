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


def gen(letter, font, path, fontdir="fonts/", bindir="bin/"):
    img = Image.new('RGB', (512, 512), color=(255, 255, 255))
    
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(fontdir + font, 400)
    draw.text((0, 0), letter, (0, 0, 0), font=font)
    img.show()
    
    rstart, rend = seg(img)
    box = (rstart[0], rstart[1], rend[0] - rstart[0], rend[1] - rstart[1])
    img = img.resize((28, 28), resample=PIL.Image.BOX, box=box)
    
    

    img.save(bindir + path)


def main():
    ascii_table = []
    for i in range(97, 128):   #33
        ascii_table.append(i)
    for c in ascii_table:
        letter = chr(c)
        print("ascii: " + str(c) + "  " + letter)
        gen(letter, "sans-serif-Aaargh.ttf", "" + str(c) + ".png")
        return

if __name__ == "__main__":
    main()