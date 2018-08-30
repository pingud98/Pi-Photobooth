# The Pi Simple Photobooth

This project is based off the All Seeing Pi project by the Raspberry Pi Foundation and the changes by @mdegrazia.

![The finished article](https://github.com/pingud98/simplebooth/raw/master/IMG_20180828_092642.jpg)

In general, the changes/additions I made to the changes that were made by @mdegrazia were:

1) removed the audio
2) removed the wii functions
3) added an on screen button to take photos/set up for the photos
4) removed the GPIO functions for buttons apart from the shutter trigger
5) killed the kill button functionality

The hardware for this project:
A hardboard crate of blueberries (minus blueberries)
A Raspberry Pi 3B with an 8GB SD card
A cheap SPI 3.5" TFT screen (hence the framebuffer copy utility, not required for luxury HDMI screens) from Aliexpress
https://www.aliexpress.com/item/3-5-Inch-TFT-LCD-Module-For-Raspberry-Pi-2-Model-B-RPI-B-raspberry-pi/32631471521.html
A knock-off 5MP V1.3 Pi Cam from Aliexpress
https://www.aliexpress.com/item/Free-Shipping-raspberry-pi-camera-5mp-pixels-RASPBERRY-PI-CAMERA/32293433078.html
A button I had in the draw
A Polaroid Pogo bluetooth printer (you can even see the MAC address in the source...) which I was given by a couple of friends for a previous wedding photobooth project. It turns out that you can use Zink papers for the Pryntr range (or the slightly more expensive HP Sprocket) in this unit without any modifications. However, it won't print .png's so the source code is modified to save as .jpg.
https://www.amazon.com/Polaroid-CZA10011-Instant-Mobile-Printer/dp/B001APNVTQ

In addition to the hardware listed, you'll also need to prepare your Pi with drivers for the screen. I used the ones from goodtft:
https://github.com/goodtft/LCD-show
Since the framebuffer doesn't auto-copy itself to the SPI display, you will also need the framebuffer copy util from @tasanakorn. I've included the binary I compiled on my Pi in this folder, but if you need to re-compile the source is here:
https://github.com/tasanakorn/rpi-fbcp



See the original blog post here for details https://anotherpiblog.blogspot.com/2017/06/raspberry-pi-photobooth-with-bluetooth.html
## License

Unless otherwise specified, everything in this repository is covered by the following license:

[![Creative Commons License](http://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

***The Pi Photobooth*** by [Mari DeGrazia](http://anotherpiblog.blogspot.com/) is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

Based on a work at https://github.com/raspberrypilearning/the-all-seeing-pi
