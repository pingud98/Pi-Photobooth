#!/usr/local/bin/python
#Written by Mari DeGrazia
#arizona4n6@gmail.com 
#Based off the All Seeing Pi by the Rasbperry Pi Foundation

from gpiozero import Button
from picamera import PiCamera
from time import gmtime, strftime,sleep
from overlay_functions import *
from shutil import copyfile
import subprocess
import Tkinter
import tkMessageBox
import ttk
from PIL import Image, ImageTk
import pygame
import time
from multiprocessing import Process

###############CHANGE ME###########################
printer_MAC = "00-04-48-13-5E-8D"
####################################################


def kill_keyboard():
    cmd = "sudo pkill -f matchbox-keyboard"
    k = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    message =  k.communicate(input)
    return

def next_overlay():
    global overlay
    global current_position
    current_position = current_position + 1
    if current_position >= len(overlays):
        current_position = 0
    overlay = overlays[current_position]
    if overlay == "":
        remove_overlays(camera)
    else:
        preview_overlay(camera, overlay)

def prev_overlay():
    global overlay
    global current_position
    
    current_position = current_position - 1
    overlay = overlays[current_position]
    if overlay == "":
        remove_overlays(camera)
    else:
        preview_overlay(camera, overlay)

def take_picture():
    global output
    global latest_photo
    global current_position
    global overlay
    
    output = strftime("/home/pi/Pi-Photobooth/photos/image-%d-%m_%H_%M_%S.png", gmtime())
    time.sleep(.3)
    camera.stop_preview()
    
    remove_overlays(camera)
    camera.hflip = False
    camera.capture(output)
    
    if overlay:
        output_overlay(output, overlays[current_position])
    else:
        output_no_overlay(output)
    size = 400, 400
    gif_img = Image.open(output)
    gif_img.thumbnail(size, Image.ANTIALIAS)
    
    gif_img.save(latest_photo, 'gif')
    loadImage(latest_photo)
    camera.hflip = True
    just_taken = True

def new_picture():
    global overlay  
    kill_keyboard()
    camera.start_preview()
    time.sleep(1)
    copyfile('/home/pi/Pi-Photobooth/images/loading.gif', '/home/pi/Pi-Photobooth/images/latest.gif')    
    remove_overlays(camera)
    current_position = 0
    loadImage(latest_photo)
    overlay = ""
    photo3 = Tkinter.PhotoImage(file='/home/pi/Pi-Photobooth/images/button_new.gif')
    b3 = Tkinter.Button(master, text="Take Picture",command=take_picture,image=photo3)
    b3.image = photo3
    b3.pack()


    
def remove():
    global overlay
    remove_overlays(camera)
    overlay = ""

def print_photo():
    global printer_MAC
    kill_keyboard()

    top = Tkinter.Tk()
    top.title("Printing")
    msg = Tkinter.Label(top, text="Sending to printer. Please wait a minute.",width=50,background='#B1B1B1')
    msg.pack()
    top.geometry("%dx%d%+d%+d" % (400, 100, 250, 125))
    top.configure(background='#B1B1B1')
    center(top)
   
    master.config(cursor="watch")
    top.config(cursor="watch")
    master.update()
    top.update()
 
    print ("Print photo")
    pp = subprocess.Popen(["obexftp --nopath --noconn --uuid none --bluetooth " +  printer_MAC +  " --channel 4 -p " + output],shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    message =  pp.communicate(input)
    master.config(cursor="")
    top.destroy()
    msg = "failed"
    if msg.encode('utf-8') in message[0]:
        tkMessageBox.showerror("Error", "Print failed. Check paper or make sure printer is on and paired and print again")
        
    else:
        tkMessageBox.showinfo("Printing", "Photo successfully sent. Now printing...")
        
    return True
    
def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2

    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

def lower(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2

    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y+150)))

    
def loadImage(latest_photo):
    global picture3
    picture3 = Tkinter.PhotoImage(file=latest_photo)
    c.itemconfigure(picture2, image = picture3)

  
current_position = 0


#reset image
copyfile('/home/pi/Pi-Photobooth/images/loading.gif', '/home/pi/Pi-Photobooth/images/latest.gif') 

    
overlay = ""
#no buttons connected.
#next_overlay_btn = Button(23)
#take_pic_btn = Button(11)


#next_overlay_btn.when_pressed = next_overlay
take_pic_btn.when_pressed = take_picture

camera = PiCamera()
camera.resolution = (800, 480)
camera.hflip = True


camera.start_preview()
output = ""
latest_photo = '/home/pi/Pi-Photobooth/images/latest.gif'

p = Process(target=start_wii_script)
p.start()
   
master = Tkinter.Tk()
master.wm_title(subject)
master.attributes("-fullscreen", True)
c = Tkinter.Canvas(master, width=400, height=300)

picture = Tkinter.PhotoImage(file=latest_photo)
picture2 = c.create_image(200,150,image=picture)
c.pack()

photo1 = Tkinter.PhotoImage(file='/home/pi/Pi-Photobooth/images/button_new.gif')
photo2 = Tkinter.PhotoImage(file='/home/pi/Pi-Photobooth/images/button_print.gif')

b1 = Tkinter.Button(master, text="New Picture",command=new_picture,image=photo1)
b2 = Tkinter.Button(master, text="Print Picture",command=print_photo,image=photo2)

b1.image = photo1
b2.image = photo2

b1.pack()
b2.pack()


Tkinter.mainloop( )


