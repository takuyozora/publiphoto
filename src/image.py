from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math

from src import config


#######
# Ce module sert à traiter les images
#  * Les parties commentées dans la fonction de halo permettent l'écriture en verticale si besoin
#  * Le kernel sert à créer un effet de halo
####### 


def draw_text_with_halo(img, text, font, halo_size, col, halo_col):
    vertical = False
    x = img.size[0]
    y = img.size[1]
#     if img.size[1] > img.size[0]:
#         vertical = True
#         w = img.size[1]
#         h = img.size[0]
#         p_x = y/100
#         p_y = (x / 100 ) * 95
#     else:
#         w = img.size[0]
#         h = img.size[1]
#         p_y = (y / 1000) * 970
#         p_x = x/100
    ## Calcul des positions pour le text
    w = img.size[0]
    h = img.size[1]
    p_y = (y / 1000) * 970
    p_x = x/100
    position = (p_x,p_y)
    halo = Image.new('RGBA', (w,h), (0, 0, 0, 0))
    ImageDraw.Draw(halo).text(position, text, font = font, fill = halo_col)
#     halo2=halo
#     halo2.putalpha(mask)
#     if vertical:
#         halo=halo.rotate(90, expand=0)
    
    kernel = [
    0, 0, 0, 0, 0,
    0, 1, 3, 1, 0,
    0, 3, 6, 3, 0,
    0, 1, 3, 2, 0,
    0, 0, 0, 0, 0]
    kernelsum = sum(kernel)
    myfilter = ImageFilter.Kernel((5, 5), kernel, scale = halo_size * sum(kernel))
    blurred_halo = halo.filter(myfilter)
    ImageDraw.Draw(blurred_halo).text(position, text, font = font, fill = col)
#     if vertical:
#         blurred_halo=blurred_halo.rotate(90, expand=0)
    compo_mask = ImageChops.invert(blurred_halo)
    return Image.composite(img, blurred_halo, compo_mask) 

# def draw_text_with_halo(img, position, text, font, halo_size, col, halo_col):
#     halo = Image.new('RGBA', img.size, (0, 0, 0, 0))
#     ImageDraw.Draw(halo).text(position, text, font = font, fill = halo_col)
#     kernel = [
#     0, 1, 2, 1, 0,
#     1, 2, 4, 2, 1,
#     2, 4, 8, 4, 1,
#     1, 2, 4, 2, 1,
#     0, 1, 2, 1, 0]
#     kernelsum = sum(kernel)
#     myfilter = ImageFilter.Kernel((5, 5), kernel, scale = halo_size * sum(kernel))
#     blurred_halo = halo.filter(myfilter)
#     ImageDraw.Draw(blurred_halo).text(position, text, font = font, fill = col)
#     return Image.composite(img, blurred_halo, ImageChops.invert(blurred_halo))

def draw_label(img_src,label,font=False):
    im=img_src
    x = im.size[0]
    y = im.size[1]
    size = math.sqrt(x*y)
    f_size = (int)(size/60)
    
    if font is not False and font is not None:
        f = ImageFont.truetype(font,f_size)
    else:
        f = ImageFont.truetype(config.DEFAULT_FONT,f_size)
    
    im = draw_text_with_halo(im,label,f,0.3,config.COLOR_TEXT,config.COLOR_HALO)
    
    return im
    
def resize_img(img_src,x,y,ratio):
    img = img_src
    if x is None:
        x = img.size[0]
    else:
        x = (int)(x)
    if y is None:
        y = img.size[1]
    else:
        y = (int)(y)
    if ratio is True:
        if x/img.size[0] < y/img.size[1]:
            y = (int)(img.size[1] * (x/img.size[0]))
        else:
            x = (int)(img.size[0] * (y/img.size[1]))
    else:
        if img.size[0] < img.size[1]:
            tmp = x
            x = y
            y = tmp
             
    img = img.resize((x,y),Image.ANTIALIAS)
    return img

def open_img(path):
    return Image.open(path)

def save_img(img,path):
    img.save(path)
    




