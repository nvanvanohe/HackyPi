#Code to verify active IP's on the network using WSL and Bash, 20-03-2024 Nohé variation for version 9.0.0.
#From examples https://github.com/sbcshop/HackyPi-Software

import time
import usb_hid
import digitalio
import board
import busio
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_hid.keyboard import Keyboard, Keycode
from keyboard_layout_win_la import KeyboardLayout
from adafruit_st7789 import ST7789
from fourwire import FourWire

# First set some parameters used for shapes and text
BORDER = 12
FONTSCALE = 3
BACKGROUND_COLOR = 0xFF0000  # red
FOREGROUND_COLOR = 0xFFFF00  # Yellow
TEXT_COLOR = 0x0000ff        # Blue  

# Release any resources currently in use for the displays
displayio.release_displays()

tft_clk = board.GP10 # must be a SPI CLK
tft_mosi= board.GP11 # must be a SPI TX
tft_rst = board.GP12
tft_dc  = board.GP8
tft_cs  = board.GP9
spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)

# Make the displayio SPI bus and the GC9A01 display
display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
#display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst), versión 8
display = ST7789(display_bus, rotation=90, width=240, height=135, rowstart=40, colstart=53)

# Make the display context
splash = displayio.Group()
display.root_group = splash
#display.show(splash), versión 8

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR

#define led (as backlight) pin as output
tft_bl  = board.GP13 #GPIO pin to control backlight LED
led = digitalio.DigitalInOut(tft_bl)
led.direction = digitalio.Direction.OUTPUT
led.value=True

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

#Create the function of the rectangles with red and yellow color 
def inner_rectangle():
    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(display.width - BORDER * 2, display.height - BORDER * 2, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = FOREGROUND_COLOR
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER)
    splash.append(inner_sprite)
    
#Create the function that prints the data on the HackyPi screen
def print_onTFT(text, x_pos, y_pos): 
    text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
    text_group = displayio.Group(scale=FONTSCALE,x=x_pos,y=y_pos,)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)
    
#Draw the red and yellow rectangles
inner_rectangle()
#Print the texts on the screen
print_onTFT("Iniciando...", 16, 40)
print_onTFT("WSL, Bash", 30, 80)
time.sleep(3)

try:
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayout(keyboard)
    time.sleep(1)
    #Open the window to execute
    keyboard.send(Keycode.WINDOWS, Keycode.R)
    time.sleep(0.3)
    
    #Draw the red and yellow rectangles
    inner_rectangle()
    #Print the texts on the screen
    print_onTFT("Buscando...", 25, 30)
    print_onTFT("IP\'s", 90, 71)
    print_onTFT("Activas", 60, 110)
    
    #Open console
    keyboard_layout.write('cmd.exe')
    keyboard.send(Keycode.ENTER)
    time.sleep(0.9)
    keyboard.send(Keycode.F11)
    time.sleep(1.2)
    #Execute Windows Subsystem Linux on the console
    keyboard_layout.write("wsl") 
    keyboard.send(Keycode.ENTER)
    time.sleep(5)
    #Code Bash to searching IP active in the network
    keyboard_layout.write("for ip in {1..254};do (ping 192.168.1.$ip -c 1 -w 1 | awk \'NR==4, NR==5\' | grep \"192.168.1.$ip\" | awk \'{print $2}\'); done") 
    keyboard.send(Keycode.ENTER)
    time.sleep(5)

    led.value = True
    keyboard.release_all()

except Exception as ex:
    keyboard.release_all()
    raise ex
