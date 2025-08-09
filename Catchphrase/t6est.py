import pygame as py
import sqlite3
import random
import time
from gpiozero import Button

class DatabaseManager:
    def __init__(self, db_file):
        self.connection = self.create_connection(db_file)
        self.cursor = self.connection.cursor()
        self.categories = self.load_categories()

    def create_connection(self, db_file):
        try:
            # Connection for testing
            # return sqlite3.connect("Catchphrase/" + db_file)
            # Connection for PI
            return sqlite3.connect("/home/johngruys/RasPi/Catchphrase/" + db_file, check_same_thread=False)
        except Exception as e:
            print(f"Failed to connect: {e}")
            return None

    def load_categories(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [cat[0] for cat in self.cursor.fetchall()]

    def get_word_count(self, category):
        self.cursor.execute(f"SELECT COUNT(*) AS total_items FROM {category}")
        return self.cursor.fetchall()[0][0]

    def get_word_by_id(self, category, word_id):
        self.cursor.execute(f"SELECT word FROM {category} WHERE id = {word_id}")
        return self.cursor.fetchall()[0][0]

class Timer:
    def __init__(self, duration, screen_width, screen_height):
        self.duration = duration
        self.start_time = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.outline_width = 300
        self.outline_height = 30
        self.outline_x = (screen_width / 2) - (self.outline_width / 2)
        self.outline_y = self.outline_height * 2
        self.progress_padding = 4
        self.round_ended = False

    def start(self):
        self.start_time = time.time()
        self.round_ended = False

    def update(self, screen):
        if self.round_ended:
            # Draw full red bar
            outline_dims = (self.outline_x, self.outline_y, self.outline_width, self.outline_height)
            py.draw.rect(screen, py.Color("darkseagreen"), outline_dims, 2)
            progress_bar_x = self.outline_x + self.progress_padding
            progress_bar_y = self.outline_y + self.progress_padding
            progress_bar_height = self.outline_height - (2 * self.progress_padding)
            progress_bar_width = self.outline_width - (2 * self.progress_padding)
            progress_bar_dims = (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height)
            py.draw.rect(screen, (255, 150, 150), progress_bar_dims)
            return False

        elapsed = time.time() - self.start_time
        pct_complete = min(elapsed / self.duration, 1)

        # Draw outline
        outline_dims = (self.outline_x, self.outline_y, self.outline_width, self.outline_height)
        py.draw.rect(screen, py.Color("darkseagreen"), outline_dims, 2)

        # Draw progress bar
        progress_bar_x = self.outline_x + self.progress_padding
        progress_bar_y = self.outline_y + self.progress_padding
        progress_bar_height = self.outline_height - (2 * self.progress_padding)
        max_progress_width = self.outline_width - (2 * self.progress_padding)
        progress_bar_width = pct_complete * max_progress_width
        progress_bar_dims = (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height)

        # Color transitions from green to red
        curr_red = int(255 * pct_complete)
        curr_red = max(0, min(255, curr_red))
        progress_color = (curr_red, 150, 150)
        py.draw.rect(screen, progress_color, progress_bar_dims)

        if pct_complete >= 1:
            self.round_ended = True
            return False
        return True

class CatchphraseGame:
    def __init__(self):
        py.init()
        self.screen = py.display.set_mode((120, 120), py.FULLSCREEN)
        py.display.set_caption("Catchphrase 2.0")
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.font = py.font.Font("freesansbold.ttf", 35)
        self.colors = {
            "background": "beige",  # Configurable background color
            "category": "cornflowerblue",    # Configurable category text color
            "word": "lightseagreen"   # Configurable word text color
        }
        self.db = DatabaseManager("first_database.db")
        self.timer = Timer(duration=30, screen_width=self.width, screen_height=self.height)
        self.selecting = True
        self.running = False
        self.round_ended = False
        self.current_cat_index = 0
        self.current_word = "hi"
        self.word_indices = []
        self.current_word_index = -1
        self.num_words = 0
        self.game_on = True
        
        ### Uncomment on Pi ###
        self.setup_gpio()

    def setup_gpio(self):
        # GPIO setup for Raspberry Pi
        self.ss_button = Button(20)
        self.ss_button.when_pressed = self.start_stop
        self.ss_button.when_released = self.start_stop
        self.back_button = Button(26)
        self.back_button.when_pressed = self.navigate_backward
        self.back_button.when_released = self.navigate_backward
        self.forward_button = Button(12)
        self.forward_button.when_pressed = self.navigate_forward
        self.forward_button.when_released = self.navigate_forward

    def navigate_forward(self):
        if self.selecting:
            self.current_cat_index = (self.current_cat_index + 1) % len(self.db.categories)
        elif self.running and self.current_word_index < len(self.word_indices) - 1:
            self.current_word_index += 1
            self.current_word = self.db.get_word_by_id(
                self.db.categories[self.current_cat_index], self.word_indices[self.current_word_index]
            )

    def navigate_backward(self):
        if self.selecting:
            self.current_cat_index = (self.current_cat_index - 1) % len(self.db.categories)
        elif self.running and self.current_word_index > 0:
            self.current_word_index -= 1
            self.current_word = self.db.get_word_by_id(
            self.db.categories[self.current_cat_index], self.word_indices[self.current_word_index]
            )

    def start_stop(self):
        if not self.running and not self.round_ended:
            self.selecting = False
            self.running = True
            self.num_words = self.db.get_word_count(self.db.categories[self.current_cat_index])
            self.word_indices = list(range(self.num_words))
            random.shuffle(self.word_indices)
            self.current_word_index = -1
            self.navigate_forward()  # Initialize first word
            self.timer.start()
        else:
            self.selecting = True
            self.running = False
            self.round_ended = False
            self.word_indices = []
            self.current_word_index = -1

    def render_text(self, text, color_key):
        rendered = self.font.render(text, True, py.Color(self.colors[color_key]))
        rectangle = rendered.get_rect(center=(self.width / 2, self.height / 2))
        return rendered, rectangle

    def handle_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
            if event.type == py.KEYDOWN:
                if event.key == py.K_s:
                    self.start_stop()
                elif event.key == py.K_c and not self.round_ended:
                    self.navigate_backward()
                elif event.key == py.K_n and not self.round_ended:
                    self.navigate_forward()
                elif event.key == py.K_ESCAPE:
                    return False
        return True

    def run(self):
        while self.game_on:
            self.screen.fill(py.Color(self.colors["background"]))

            if self.selecting:
                rendered, rectangle = self.render_text(self.db.categories[self.current_cat_index], "category")
                self.screen.blit(rendered, rectangle)
            elif self.running or self.round_ended:
                rendered, rectangle = self.render_text(self.current_word, "word")
                self.screen.blit(rendered, rectangle)
                if self.running and not self.timer.update(self.screen):
                    self.running = False
                    self.round_ended = True
                elif self.round_ended:
                    self.timer.update(self.screen)  # Display full red bar

            if not self.handle_events():
                break

            py.display.update()

        py.quit()

if __name__ == "__main__":
    game = CatchphraseGame()
    game.run()