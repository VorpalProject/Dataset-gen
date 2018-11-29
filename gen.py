import os
import time
import sys
import threading
import multiprocessing
import PIL
import PIL.Image as Image
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw


def seg(img):
    start = [0, 0]
    end = [img.size[0], img.size[1]]
    x = 0
    y = 0
    while y != img.size[1] and x < img.size[0] and \
            img.getpixel((x, y)) == (255, 255, 255):
        y += 1
        if img.size[1] == y:
            y = 0
            x += 1

    start[0] = x

    x = 0
    y = 0
    while x != img.size[0] and y < img.size[1] and \
            img.getpixel((x, y)) == (255, 255, 255):
        x += 1
        if img.size[0] == x:
            x = 0
            y += 1
    start[1] = y

    x = img.size[0] - 1
    y = img.size[1] - 1
    while y != img.size[1] and x > 0 and \
            img.getpixel((x, y)) == (255, 255, 255):
        y -= 1
        if y < 0:
            y = img.size[1] - 1
            x -= 1

    end[0] = x

    x = img.size[0] - 1
    y = img.size[1] - 1
    while x != img.size[0] and y > 0 and \
            img.getpixel((x, y)) == (255, 255, 255):
        x -= 1
        if x < 0:
            x = img.size[0] - 1
            y -= 1
    end[1] = y

    return start, end


def gen(letter, fontname, font, path, fontdir="fonts/", bindir="bin/"):
    if os.path.exists(bindir + path):
        return

    img = Image.new('RGB', (512, 512), color=(255, 255, 255))

    draw = ImageDraw.Draw(img)

    draw.text((0, 0), letter, (0, 0, 0), font=font)

    rstart, rend = seg(img)
    cbox = (rstart[0], rstart[1], rend[0], rend[1])

    letter = img.crop(box=cbox)

    rbox = (0, 0) + letter.size
    mini = letter.resize((28, 28), PIL.Image.ANTIALIAS)

    # draw.line((rstart[0], rstart[1], rend[0], rstart[1]), fill=(0, 0, 0))
    # draw.line((rstart[0], rstart[1], rstart[0], rend[1]), fill=(0, 0, 0))
    # draw.line((rstart[0], rend[1], rend[0], rend[1]), fill=(0, 0, 0))
    # draw.line((rend[0], rstart[1], rend[0], rend[1]), fill=(0, 0, 0))

    mini.save(bindir + path, quality=100)


class GenDataset(threading.Thread):
    fontlist = []
    rstart = 0
    end = 0
    ascii_table = []
    fontdir = ""
    bindir = ""

    def __init__(self, fontlist, rstart, end, ascii_table, fontdir, bindir):
        threading.Thread.__init__(self)
        self.fontlist = fontlist
        self.rstart = rstart
        self.end = end
        self.ascii_table = ascii_table
        self.bindir = bindir
        self.fontdir = fontdir

    def run(self):
        font_len = len(self.fontlist)
        self.end = self.end if self.end <= font_len else font_len
        for i in range(self.rstart, self.end):
            fontname = self.fontlist[i]
            font = ImageFont.truetype(self.fontdir + fontname, 256)
            for c in self.ascii_table:
                letter = chr(c)
                print("ascii: " + str(c) + "  " + letter + " with font " + fontname)
                gen(letter, fontname, font, str(c) + "_" + fontname + ".png", \
                    fontdir=self.fontdir, bindir=self.bindir)


def main():
    fontdir = "fonts/"
    bindir = "bin/"
    fonts = os.listdir(fontdir)
    len_fonts = len(fonts)
    ascii_table = [i for i in range(33, 128)]

    nbcore = multiprocessing.cpu_count()
    task = len_fonts // nbcore;

    threads = []
    start = 0
    end = task
    while end <= len_fonts:
        th = GenDataset(fonts, start, end, ascii_table, fontdir, bindir)
        print(th)
        threads.append(th)
        start = end
        end += task

    for th in threads:
        th.start()

    for th in threads:
        th.join()

    print("Done\n")


if __name__ == "__main__":
    main()
