import pygame as py
import sqlite3
import random
import time
# from gpiozero import Button

### Initialize
py.init()

screen = py.display.set_mode((0, 0), py.FULLSCREEN)

py.display.set_caption("Catchprase 2.0")

game_on = True
# Start time for round timer (global)
start_time = 0

width = screen.get_width();
height = screen.get_height();

# Colors #
white = (255, 255, 255)
black = (0, 0, 0)
beige = (246, 236, 215)

# Font
font = py.font.Font("freesansbold.ttf", 35)

def create_connection(db_file):
    connection = None
    try:
        ### Connection for testing
        connection = sqlite3.connect("Catchphrase/" + db_file)
        
        ### Connection for PI
        # connection = sqlite3.connect("/home/johngruys/RasPi/Catchphrase/" + db_file, check_same_thread=False)
    except:
        print("Failed to connect")

    return connection

### Access Database
database_name = "first_database.db"
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
    if selecting == True:
        if current_cat < num_cat - 1:
            current_cat += 1
        else:
            current_cat = 0


### To be set when start button pressed
num_words = 0
current_word = "hi"

running = False

##############################################################################################
### Main functions for game operation
def start_stop():
    global running
    global selecting
    global num_words
    global start_time
    
    if running == False:
        selecting = False
        running = True
        cursor.execute("SELECT COUNT(*) AS total_items FROM " + categories[current_cat])
        num_words = cursor.fetchall()[0][0]
        skip()

        ### Start timer
        start_time = time.time()
        

    elif running == True:
        selecting = True
        running = False

ids_used = []
def next_word():
    global ids_used
    if num_words > 0:
        while True:
            rand_id = random.randint(0, num_words - 1)
            if rand_id not in ids_used:
                ids_used.append(rand_id)
                cursor.execute("SELECT word FROM " + categories[current_cat] + " WHERE id = " + str(rand_id))
                word = cursor.fetchall()
                return word[0][0]

def skip():
    if running:
        global current_word
        current_word = next_word()
    
##############################################################################################


### Function for writing the words
def write(text, color):
    rendered = font.render(text, True, py.Color(color))
    rectangle = rendered.get_rect(center=(width/2, height/2))
    return rendered, rectangle


### Functions for timing bar along top
def update_timer():
    global start_time
    game_duration = 10
    
    # Dimensions/location for progress bar
    outline_width = 300
    outline_height = 30
    outline_x = (width/2) - (outline_width/2)
    outline_y = outline_height * 2
    
    # Draw outline for loading bar (x, y, width, height, border_thickness)
    outline_dims = (outline_x, outline_y, outline_width, outline_height)
    py.draw.rect(screen, py.Color("darkseagreen"), outline_dims, 2)
    
    # Make progress bar to fill
    progress_padding = 4
    
    current_time = time.time()
    elapsed = current_time - start_time
    pct_complete = elapsed/game_duration
    
    if pct_complete >= 1:
        pct_complete = 1
    
    progress_bar_x = outline_x + progress_padding
    progress_bar_y = outline_y + progress_padding
    
    progress_bar_height = outline_height - (2 * progress_padding)
    max_progress_width = outline_width - (2 * progress_padding)
    progress_bar_width = pct_complete * max_progress_width
    
    progress_bar_dims = (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height)
    
    # Fill bar depending on progess, color gradually becomes more red
    # Ensure value is an int between 0-255
    curr_red = int(255 * pct_complete)
    curr_red = max(0, min(255, curr_red))
    progress_color = (curr_red, 150, 150)
    py.draw.rect(screen, progress_color, progress_bar_dims)
    
    # Return t/f if round still running
    if pct_complete < 1:
        return True
    else: 
        return False
    
    
    # pygame.draw.rect(screen, GREEN, (50, 200, 150, 100)) # Green filled rectangle
    # pygame.draw.rect(screen, RED, (50, 50, 100, 75), 2)  # Red outline, 2 pixels thick

### Event Handling for Testing (Comment on PI)    
def handle_events():
    for event in py.event.get():
        if event.type == py.QUIT:
            return False

        if event.type == py.KEYDOWN:
            if event.key == py.K_s:
                start_stop()
            elif event.key == py.K_c:
                next_cat()
            elif event.key == py.K_n:
                skip()
                
            # Esc to end game
            elif event.key == py.K_ESCAPE:
                return False
    return True
    

### Event Handling for PI (Uncomment on PI)

# ss = Button(20)
# ss.when_pressed = start_stop
# ss.when_released = start_stop

# cat = Button(26)
# cat.when_pressed = next_cat
# cat.when_released = next_cat

# ne = Button(12)
# ne.when_pressed = skip
# ne.when_released = skip


while game_on:

    ### Reset Screen
    screen.fill(beige)
    

    if selecting == True:
        category = categories[current_cat]
        rendered, rectangle = write(category, "blue4")
        screen.blit(rendered, rectangle)
        

    if running == True:
        rendered, rectangle = write(current_word, "aquamarine3")
        screen.blit(rendered, rectangle)
        
        # Update timer and check if game still going
        still_running = update_timer()
        if not still_running:
            start_stop()


            
    ### Uncomment for testing
    if not handle_events():
        break
            
    py.display.update()


 
### Closes when loop exits   
py.quit()
    

