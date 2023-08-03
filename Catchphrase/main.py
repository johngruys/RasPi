import pygame as py
import sqlite3
import random
import time
from gpiozero import Button

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
        ### Connection for testing
#         connection = sqlite3.connect("Catchphrase/" + db_file)
        ### Connection for PI
        connection = sqlite3.connect("/home/johngruys/RasPi/Catchphrase/" + db_file)
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



### Event Handling for Testing (Comment on PI)    
# def handle_events():
#     for event in py.event.get():
#         if event.type == py.QUIT:
#             running = False
#             return False
# 
#         if event.type == py.KEYDOWN:
#             if event.key == py.K_s:
#                 ...
#             elif event.key == py.K_c:
#                 next_cat()
#             elif event.key == py.K_n:
#                 ...
#     return True
    

### Event Handling

ss = Button(20)
# ss.when_pressed = s
# ss.when_released = s

cat = Button(26)
cat.when_pressed = next_cat
cat.when_released = next_cat

ne = Button(12)
# ne.when_pressed = n
# ne.when_released = n


while running:

    ### Reset Screen
    screen.fill(black)

    if selecting == True:
        category = categories[current_cat]
        category_font = py.font.Font("freesansbold.ttf", 35)
        category_disp = category_font.render(category, True, white)
        screen.blit(category_disp, (177, 130))
              

    
    
    
    ### Uncomment for testing
#     if not handle_events():
#         break
            
    py.display.update()



### Closes when loop exits   
py.quit()
    

