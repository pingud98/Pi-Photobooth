#modified All Seeing Pi to remove overlay and overlay button.
from picamera import PiCamera
from gpiozero import Button
#from overlay_functions import *
from time import gmtime, strftime, sleep
import time
import string
import subprocess
from guizero import App, PushButton, Text, Picture, Window, info
#from twython import Twython
#from auth import (
#    consumer_key,
#    consumer_secret,
#    access_token,
#    access_token_secret
#)
from PIL import Image

###############CHANGE ME###########################
printer_MAC = "00:04:48:13:5E:8D"
####################################################
def print_photo():
    global printer_MAC
    print ("Print photo")
    commandtag ="obexftp --nopath --noconn --uuid none --bluetooth "+printer_MAC+" --channel 1 -p "+output
    #uncomment this for debugging
    #print (commandtag)
    p = subprocess.Popen(commandtag, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #uncomment these for debugging
    #for line in iter(p.stdout.readline, ''):
    #    print(line)
    #retval = p.wait()
    info("Printing", "Sending to printer. Please wait a minute.")
    
# Tell the take picture button what to do
def take_picture():
    q = subprocess.Popen('pkill fbcp', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    global output
    output = strftime("/home/pi/simplebooth/image-%d-%m%H:%M.jpg", gmtime())
    camera.stop_preview()
    your_pic.set(ready_photo)
    time.sleep(3)
    camera.capture(output)
    your_pic.set(black_photo)
    
    #camera.stop_preview()
    
#    remove_overlays(camera)
#    output_overlay(output)

    # Save a smaller gif
    size = 400, 600
    gif_img = Image.open(output)
    gif_img.thumbnail(size, Image.ANTIALIAS)
    gif_img.save(latest_photo, 'gif')

    # Set the gui picture to this picture
    window.show()
    app.hide()
    your_pic.set(latest_photo)
    your_picw.set(latest_photo)


def new_picture():
    window.hide()
    app.show()
    camera.start_preview()
    q = subprocess.Popen('/home/pi/simplebooth/./fbcp', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

#    preview_overlay(camera, overlay)


# Set up buttons
#next_overlay_btn = Button(23)
#next_overlay_btn.when_pressed = next_overlay
take_pic_btn = Button(21)
take_pic_btn.when_pressed = take_picture

# Set up camera (with resolution of the touchscreen)
camera = PiCamera()
camera.resolution = (1296, 730)
camera.hflip = True

# Start camera preview
#camera.start_preview()

# Set up filename
output = ""

latest_photo = '/home/pi/simplebooth/latest.gif'
ready_photo = '/home/pi/simplebooth/countdown.gif'
black_photo = '/home/pi/simplebooth/black.gif'

app = App("The JAM Wedding Photo Booth", 480, 320)
window = Window(app, title = "Backup")
window.hide()
#app.attributes("-fullscreen", True)
your_pic = Picture(app, latest_photo)
your_picw = Picture(window, latest_photo)
new_pic = PushButton(app, new_picture, text="New picture")
print_pic = PushButton(app, print_photo, text="Print picture")
new_picw = PushButton(window, new_picture, text="New picture")
print_picw = PushButton(window, print_photo, text="Print picture")
app.tk.attributes("-fullscreen",True)
window.tk.attributes("-fullscreen",True)
app.display()
