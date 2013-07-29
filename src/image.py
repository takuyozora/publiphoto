# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math

import cairo
from gi.repository import Gdk, GdkPixbuf

from src.settings import load_settings

#######
# This module work on pictures
#  * Commented parts are some functionalities which can be reintroduce
#  * Kernel part is here to create an halo
#######
#######
# Ce module sert à traiter les images
#  * Les parties commentées dans la fonction de halo permettent l'écriture en verticale si besoin
#  * Le kernel sert à créer un effet de halo
####### 

# def pil_to_gdk(img):
#     arr = numpy.array(img)
#     return Gdk.pixbuf_new_from_array(arr, Gdk.COLORSPACE_RGBA, 16)

def gtk_to_pil(pb):
    width,height = pb.get_width(),pb.get_height()
    return Image.fromstring("RGB",(width,height),pb.get_pixels() )

def draw_label_cairo(img_path,label,font=False):
    sett = load_settings()
#     im=img_src
#     x = im.size[0]
#     y = im.size[1]
# 
#     im = pil_to_gdk(img_src)
    
#     if font is not False and font is not None:
#         f = ImageFont.truetype(font,f_size)
#     else:
#         f = ImageFont.truetype(sett.font["path"],f_size)
#     
#     im = draw_text_with_halo(im,label,f,0.3,sett.font["color"],sett.font["haloColor"])
    
    im = GdkPixbuf.Pixbuf.new_from_file(img_path)
    x = im.get_width()
    y = im.get_height()
    size = math.sqrt(x*y)
    f_size = (int)((size/60) * sett.font["scale"])
    surface = cairo.ImageSurface(0,x,y)
    
    ct = cairo.Context(surface)
    ct2 = Gdk.CairoContext(ct)
    ct2.set_source_pixbuf(im,0,0)

    
    drawable = GdkPixbuf.render_pixmap_and_mask(alpha_threshold=127)[0]
    
    context = Cairo.Context(im)
    
    return im

def draw_text_with_halo(img, text, font, halo_size, col, halo_col):
    sett = load_settings()
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
    w = img.size[0]  # (int)(img.size[0] * math.cos(sett.position["angle"]*(180/math.pi)))
    h = img.size[1]  # (int)(img.size[1] * math.sin(sett.position["angle"]*(180/math.pi)))
    if abs(sett.position["angle"]) >= 90:
        tmp = w
        w = h
        h = tmp
#     w = (int)(img.size[0] * math.cos(sett.position["angle"]*(180/math.pi))) + (int)(img.size[1] * math.sin(sett.position["angle"]*(180/math.pi)))
#     if w < 1: w *= -1
#     h = (int)(img.size[0] * math.sin(sett.position["angle"]*(180/math.pi))) + (int)(img.size[1] * math.cos(sett.position["angle"]*(180/math.pi)))
#     if h < 1 : h *= -1
    if "bottom" in sett.position["corner"]:
        p_y = (y / 1000) * 990 - font.getsize(text)[1]
    elif "top" in sett.position["corner"]:
        p_y = (y / 1000) * 10
    if "right" in sett.position["corner"]:
        p_x = (x/100) * 99 - font.getsize(text)[0]
    elif "left" in sett.position["corner"]:
        p_x = x/100
        
    if sett.position["corner"] == "center":
        p_x= x/2 - font.getsize(text)[0]/2
        p_y = y/2 - font.getsize(text)[1]/2
    
#     p_y = y/2
#     p_x = x/2
    position = ((int)(p_x),(int)(p_y))
    halo = Image.new('RGBA', (w,h), (0, 0, 0, 0))
    ImageDraw.Draw(halo).text(position, text, font = font, fill = halo_col)
#     halo2=halo
#     halo2.putalpha(mask)
#     if vertical:
#         halo=halo.rotate(90, expand=0)
    
    kernel = [
        4, 6, 8, 6, 4,
        6, 8, 12, 8, 6,
        8, 12, 16, 12, 8,
        6, 8, 12, 8, 6,
        4, 6, 8, 6, 4]
#     kernel = [
#     0, 0, 0, 0, 0,
#     0, 1, 3, 1, 0,
#     0, 3, 6, 3, 0,
#     0, 1, 3, 2, 0,
#     0, 0, 0, 0, 0]
    kernelsum = sum(kernel)
    myfilter = ImageFilter.Kernel((5, 5), kernel, scale = halo_size * sum(kernel))
    blurred_halo = halo.filter(myfilter)
    ImageDraw.Draw(blurred_halo).text(position, text, font = font, fill = col)
    if sett.position["angle"] != 0:
        blurred_halo=blurred_halo.rotate(sett.position["angle"], expand=0)
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
    sett = load_settings()
    im=img_src
    x = im.size[0]
    y = im.size[1]
    size = math.sqrt(x*y)
    f_size = (int)((size/60) * sett.font["scale"])
    
    if font is not False and font is not None:
        f = ImageFont.truetype(font,f_size)
    else:
        f = ImageFont.truetype(sett.font["path"],f_size)
    
    im = draw_text_with_halo(im,label,f,(-1*(sett.font["haloScale"]/4-0.5))+0.01,sett.font["color"],sett.font["haloColor"])
    
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
    




