from ctypes import windll, create_string_buffer

def getScreenSize():
    h = windll.kernel32.GetStdHandle(-12)
    csbi = create_string_buffer(22)
    res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    if res:
        import struct
        (bufx, bufy, curx, cury, wattr,
        left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        sizex = right - left
        sizey = bottom - top
    else:
        sizex, sizey = 80, 25 # Defaults

    return sizex, sizey