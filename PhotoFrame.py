##copy folder photoframe to /home/pi
##To install PIL for image work on raspbian buster 2/2020
##sudo apt-get install python-imaging-tk
##sudo apt-get install python3-pil python3-pil.imagetk
# To setup autostart of this program
# add last lines to /home/pi/.bashrc
# echo Running at boot
# sudo python3 /home/pi/photoframe/PhotoFrame.py
# This only runs when terminal is opened so add last line by
# changing global autostart add last line
# sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# @lxterminal
# " on a4tech keyboard
# must give graphics time to load so add to start of program
# import time
# time.sleep(20)
# To stop restart kill terminal when it appears
# To restore terminal change .brashrc to unknown file
##To ensure 24/7 operation
##sudo apt-get install xscreensaver
##set mode disable screen saver

from tkinter import *
from PIL import ImageTk,Image
import time
from threading import Thread  
import os

time.sleep(20)

photo_paths = []
for root, dirs, files in os.walk('/media/pi'):
  for file in files:
    if file.endswith('.jpg'):
##can use PPM PNG JPEG GIF TIFF and BMP
      photo_paths.append(os.path.join(root, file))
if len(photo_paths) == 0:
  photo_paths.append('/home/pi/photoframe/nojpgfiles.jpg')

photo_number = [-1,1]  ##current number,maximun number
photo_number[1] = len(photo_paths) 
def run_thread(cv,page):
    t = Thread(target=next_image, name = 'cd')
    t.daemon = True  #on completion the thread will be killed
    t.start()
        
def resize_image(path):
    with Image.open(path) as nimg:  
      asp = nimg.size[0]/nimg.size[1]
      if asp < screen_data[2]:   #narrower than screen
          mult = screen_data[1]/nimg.size[1]
      else:          #wider than screen
          mult = screen_data[0]/nimg.size[0]
      pic_w = (int)(nimg.size[0]*mult)
      pic_h = (int)(nimg.size[1]*mult)
      rz = nimg.resize((pic_w,pic_h),Image.ANTIALIAS)
      gap_down = (int)((screen_data[1] - rz.size[1])/2.0)
      gap_left = (int)((screen_data[0] - rz.size[0])/2.0)
      return rz,gap_left,gap_down
  
move_display = [0,0]
def next_image():
    (sw,sh,aps,cv,current_page) = screen_data
    while True: #run always
##      set time for each photo here
      time.sleep(5) #display time
      try:
        rz,gl,gd = resize_image(photo_paths[photo_number[0]])
      except:  #removed USB ?
        del photo_paths[:]
        photo_paths.append('/home/pi/photoframe/nojpgfiles.jpg')
        photo_number[1] = 1
        photo_number[0] = 0
      rzimg = ImageTk.PhotoImage(rz)
      cv.itemconfigure(current_page,image=rzimg)
      cv.move(current_page,gl-move_display[0],gd-move_display[1])
      move_display[0] = gl
      move_display[1] = gd
      photo_number[0] += 1 ##go to the next number
      if photo_number[0] == photo_number[1]:
          photo_number[0] = 0

screen_data = []  ##the display screen data
root = Tk()
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
screen_data.append(sw)
screen_data.append(sh)
aspect_screen = sw/sh
screen_data.append(aspect_screen)
##uncomment to allow full screen
##root.attributes('-fullscreen',True)
cv = Canvas(root,width=sw,height=sh,bg='black')
screen_data.append(cv)
cv.pack()
simg,sl,sd = resize_image('/home/pi/photoframe/photoframe.jpg')
rsimg = ImageTk.PhotoImage(simg)
first_page = cv.create_image(sl, sd, anchor=NW, image=rsimg)
move_display[0] = sl
move_display[1] = sd  ##reset the first image location
screen_data.append(first_page)
run_thread(cv,first_page)
root.mainloop()
