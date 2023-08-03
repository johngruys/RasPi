import pygame as py
import sqlite3
import random
import time
from gpiozero import Button
from pynput.keyboard import Key, Controller

### Button input for pi
keyboard = Controller()

def s():
     print("s")
     keyboard.press("s")
     keyboard.release("s")
     
def c():
    print("c")
    keyboard.press("c")
    keyboard.release("c")
    
def n():
    print("n")
    keyboard.press("n")
    keyboard.release("n")
     
# ss = Button(20)
# ss.when_pressed = s
# ss.when_released = s

# cat = Button(26)
# cat.when_pressed = c
# cat.when_released = c

# ne = Button(12)
# ne.when_pressed = n
# ne.when_released = n


### Initialize
py.init()

screen = py.display.set_mode((480, 320))

py.display.set_caption("Catchprase 2.0")

running = True

# Colors #
white = (255, 255, 255)
black = (0, 0, 0)

def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect("Catchphrase/" + db_file)
    except:
        print("Failed to connect")

    return connection

### Access Database
database_name = "words.db"
connection = create_connection(database_name)
cursor = connection.cursor()

# Compile category names and store in "categories"
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
categories = []
for cat in tables:
    categories += cat

### Starting game + selection process
selecting = True
num_cat = len(categories)
current_cat = 0

def next_cat():
    global current_cat
    if current_cat < num_cat - 1:
        current_cat += 1
    else:
        current_cat = 0



while running:

    ### Reset Screen
    screen.fill(black)

    if selecting == True:
        category = categories[current_cat]
        category_font = py.font.Font("freesansbold.ttf", 35)
        category_disp = category_font.render(category, True, white)
        screen.blit(category_disp, (177, 130))
              
        

    
    # hello = "hello"
    # hello_font = py.font.Font("freesansbold.ttf", 35)
    # hello_disp = hello_font.render(hello, True, white)
    # screen.blit(hello_disp, (50, 50))

    
    
    for event in py.event.get():
        ### Input Checking
        if event.type == py.QUIT:
            running = False

        if event.type == py.KEYDOWN:
            if event.key == py.K_s:
                ...
            elif event.key == py.K_c:
                next_cat()
            elif event.key == py.K_n:
                ...

    
            
    py.display.update()
            
py.quit()
    

