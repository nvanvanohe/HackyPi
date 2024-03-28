# The connections about hardware https://how2electronics.com/interfacing-16x2-lcd-display-with-raspberry-pi-pico/
# The software is variation from https://www.rototron.info/lcd-display-tutorial-for-raspberry-pi/
# Tested Raspberry Pi Pico W with CircuitPython 9.0.1, 27-03-2024

import time
import board
import digitalio
from adafruit_character_lcd.character_lcd import Character_LCD_Mono

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

lcd_rs = digitalio.DigitalInOut(board.GP16)
lcd_en = digitalio.DigitalInOut(board.GP17)
lcd_d4 = digitalio.DigitalInOut(board.GP18)
lcd_d5 = digitalio.DigitalInOut(board.GP19)
lcd_d6 = digitalio.DigitalInOut(board.GP20)
lcd_d7 = digitalio.DigitalInOut(board.GP21)

# Initialise the LCD class
lcd = Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows
)
# display text on LCD display \n = new line
lcd.clear()
time.sleep(1)
lcd.message = "Adafruit CharLCD\nCP Raspberry Pi"
time.sleep(3)
lcd.clear()
lcd.message = "      Hola\n     Mundo!"
time.sleep(3)

# scroll text off display
for x in range(0, 16):
    lcd.move_right()
    time.sleep(.2)
time.sleep(2)
# scroll text on display
for x in range(0, 16):
    lcd.move_left()
    time.sleep(.2)
time.sleep(2)
# scroll text on display
for x in range(0, 16):
    lcd.move_left()
    time.sleep(.2)
    
"""
Connections LCD 16x2 to Raspberry Pi Pico W
VBUS = 5V (40)
Ground = GND (38)

Pin 1 to Ground (GND 38)
Pin 2 to 5V (VBUS 40)
Pin 3 to Potentiometer 10K
Pin 4 to GP16
Pin 5 to Ground (GND 38)
Pin 6 to GP17
Pin 11 to GP18
Pin 12 to GP19
Pin 13 to GP20
Pin 14 to GP21
Pin 15 to 5V (VBUS 40)
Pin 16 to Ground (GND 38)
"""
