#TO DO
# 1: set up framework for keys
# 2: set up framework for encoder/
# 2.5: set up different modes for different softwares
# 3: set up framework for OLED/
# 4: fill in pin values/
# 5: design display UIs/
# 6: try to fit it into at least 14 hrs (if less, then add more features)


import board
import digitalio
import time
import keypad
import bitmap
import displayio
import rotaryio
import usb_hid
from adafruit_hid.keyboard import keyboard
from adafruit_hid.keyboard import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import math
import terminalio
import adafruit_displayio_ssd1306

#matrix pin declarations
row_zero = board.GPIO7
row_one = board.GPIO8
row_two = board.GPIO10
row_three = board.GPIO9
col_zero = board.GPIO1
col_one = board.GPIO6



keys = keypad.KeyMatrix(
    row_pins=(row_zero, row_one, row_two, row_three),
    col_pins=(col_zero, col_one),
    columns_to_anodes=True,
)

kpd = Keyboard(usb_hid.devices)
layout = KeyboardLayouts(kpd)


#Blender Shortcuts
blender_mode_change=(Keycode.TAB)
blender_grab=(Keycode.G)
blender_delete=(Keycode.X)
blender_add=(Keycode.SHIFT, Keycode.A)
blender_viewport_change=(Keycode.Z)
blender_front_view=(Keycode.KEYPAD_ONE)
blender_side_view=(Keycode.KEYPAD_THREE)
blender_top_view=(Keycode.KEYPAD_SEVEN)

#VSCode Hotkeys
vsc_cut= (Keycode.COMMAND, Keycode.X)
vsc_copy=(Keycode.COMMAND, Keycode.C)
vsc_paste=(Keycode.COMMAND, Keycode.V)
vsc_undo=(Keycode.COMMAND, Keycode.Z)
vsc_redo=(Keycode.COMMAND, Keycode.Y)
vsc_find=(Keycode.COMMAND, Keycode.F)
vsc_save =(Keycode.COMMAND, Keycode.S)
vsc_debug =(Keycode.F5)

matrix_case = 1

match matrix_case:
    case 1: #Unity
        KEYMATRIX = [
            (Keycode.COMMAND, Keycode.D), (Keycode.COMMAND, Keycode.P),
            (Keycode.W), (Keycode.E)
            (Keycode.R), (Keycode.COMMAND, Keycode.SHIFT, Keycode.C)
            (Keycode.COMMAND, Keycode.Z), (Keycode.COMMAND, Keycode.A)

        ]
    case 2: #Blender
        KEYMATRIX = [
            blender_add, blender_delete,
            blender_viewport_change, blender_mode_change,
            blender_grab, blender_front_view,
            blender_side_view, blender_top_view,
        ]
    case 3: #VS Code
        KEYMATRIX = [
            vsc_copy, vsc_paste,
            vsc_cut, vsc_debug,
            vsc_undo, vsc_redo,
            vsc_save, vsc_find,
        ]




#OLED Setup
displayio.release_displays()
i2c = board.I2c()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3d, reset=None)

WIDTH = 128
HEIGHT = 64
BORDER = 5

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)


rot_encoder = rotaryio.IncrementalEncoder() #add encoder pins here
rot_prev = 0



# and this is loop()
while True:
    event = keys.events.get()
    if event:
        print(event)

    rot_current = rot_encoder.position

    rot_angle = (rot_current / 20) * 360
   


    if rot_angle > 0 and rot_angle <= 120:
        print("Unity")
        matrix_case = 1
    elif rot_angle > 120 and rot_angle <= 240:
        print("Blender")
        matrix_case = 2
    elif rot_angle > 240 and rot_angle <= 360:
        print("VS Code")
        matrix_case = 3

    if rot_angle > 360:# resets the count if you turn the EC11 a full 360
        rot_angle = 0

    #keypad code
    event = keys.events.get()
    if event:
        key_number = event.key_number
        keycode = KEYMATRIX[key_number]

        if event.pressed:
            kpd.press(keycode)

        if event.released:
            kpd.released(keycode)
