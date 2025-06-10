# Import necessary libraries: tkinter for the GUI and random for food placement.
from tkinter import *
import random

""" --- CONSTANTS ---
These are the global settings for our game.
"""

GAME_WIDTH = 1000  # Width of the game window in pixels.
GAME_HEIGHT = 800  # Height of the game window in pixels.
SPEED = 70  # The initial speed of the snake (in milliseconds). Lower is faster.
SPACE_SIZE = 30  # The size of each grid space, and thus each part of the snake and food.
BODY_PARTS = 3  # The initial number of body parts the snake has.
SNAKE_COLOR = "#32CD32"  # A lime green color for the snake.
FOOD_COLOR = "#FA8072"  # A salmon color for the food.
BACKGROUND_COLOR = "#fff8e7"  # A light cream background color.


""" --- SNAKE CLASS ---
This class defines the snake object.
"""
class Snake:
    def __init__(self):
        # Initialize the snake's properties.
        self.body_size = BODY_PARTS
        self.coordinates = []  # A list to store the (x, y) coordinates of each body part.
        self.squares = []  # A list to store the rectangle objects drawn on the canvas.

        # Set the starting position of the snake at the top-left corner (0,0).
        # We create a list of coordinates for the snake's initial body parts.
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Draw the snake on the canvas.
        # We loop through the initial coordinates and create a rectangle for each body part.
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


""" --- FOOD CLASS ---
This class defines the food object.
"""
class Food:
    def __init__(self):
        # Calculate the maximum number of positions on the x and y axes.
        # This ensures the food appears perfectly within the grid.
        max_x_pos = int(GAME_WIDTH / SPACE_SIZE) - 1
        max_y_pos = int(GAME_HEIGHT / SPACE_SIZE) - 1

        # Generate a random x and y coordinate for the food.
        # We multiply by SPACE_SIZE to align it with the grid.
        x = random.randint(0, max_x_pos) * SPACE_SIZE
        y = random.randint(0, max_y_pos) * SPACE_SIZE

        # Store the food's coordinates.
        self.coordinates = [x, y]

        # Draw the food on the canvas as an oval.
        # We use a "food" tag to easily identify and delete it later.
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


""" --- GAME LOGIC FUNCTIONS ---
This function controls the game's flow for each turn.
"""
def next_turn(snake, food):
    global SPEED # Access the global SPEED variable to modify it.

    # Get the current coordinates of the snake's head.
    x, y = snake.coordinates[0]

    # Determine the new coordinates for the head based on the current direction.
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Insert the new head's coordinates at the beginning of the coordinates list.
    snake.coordinates.insert(0, (x, y))

    # Create a new rectangle for the new head on the canvas.
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    # Add the new head's square object to the beginning of the squares list.
    snake.squares.insert(0, square)

    # Check if the snake has eaten the food.
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score # Access the global score variable to modify it.
        score += 1
        
        # Update the score label.
        label.config(text="Score:{}".format(score))
        
        # Delete the old food from the canvas.
        canvas.delete("food")
        
        # Create a new food object at a new random location.
        food = Food()


    # If the snake did not eat the food, remove the last part of its body.
    else:
        # Delete the coordinates of the last body part.
        del snake.coordinates[-1]
        
        # Delete the corresponding square from the canvas.
        canvas.delete(snake.squares[-1])
        
        # Remove the square object from the list.
        del snake.squares[-1]

    # Check for collisions after moving.
    if check_collision(snake):
        game_over()
    # If no collision, schedule the next turn.
    else:
        # This line is the core of the game loop. It calls next_turn again after 'SPEED' milliseconds.
        window.after(SPEED, next_turn, snake, food)

# This function updates the snake's direction based on key presses.
def change_direction(new_direction):
    global direction # Access the global direction variable.

    # This logic prevents the snake from reversing on itself.
    # For example, if moving right, the direction cannot be changed to left.
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

# This function checks if the snake has collided with a wall or itself.
def check_collision(snake):
    x, y = snake.coordinates[0]

    # Check for collision with the window boundaries (walls).
    if x < 0 or x >= GAME_WIDTH:
        return True
    if y < 0 or y >= GAME_HEIGHT:
        return True

    # Check for collision with its own body.
    # We iterate through the body parts, starting from the second part (index 1).
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True # A collision is detected.
    
    # If no collisions are found, return False.
    return False

# This function is called when the game ends.
def game_over():
    # Clear everything from the canvas.
    canvas.delete(ALL)
    # Display a "GAME OVER" message in the center of the canvas.
    canvas.create_text(canvas.winfo_width() / 2,
                       canvas.winfo_height() / 2,
                       font=("consolas", 70),
                       text="GAME OVER",
                       fill="red",
                       tag="gameover")


""" --- WINDOW AND UI SETUP ---
Create the main window object.
"""
window = Tk()
window.title("Snake Game")
# Prevent the window from being resized.
window.resizable(False, False)

# Initialize game variables.
score = 0
direction = 'down'  # The snake will start by moving down.

# Create the score label.
label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

# Create the game canvas where everything will be drawn.
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Force the window to update to get its dimensions.
window.update()

# Get the window and screen dimensions to center the window.
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the x and y coordinates to center the window.
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

# Set the window's position on the screen.
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

""" --- KEY BINDINGS ---
Bind the arrow keys to the change_direction function.
A lambda function is used to pass the direction string as an argument.
"""
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))


""" --- START THE GAME ---
Create the initial snake and food objects.
"""
snake = Snake()
food = Food()

# Start the game loop by calling next_turn for the first time.
next_turn(snake, food)

# This function starts the tkinter event loop, listening for events like key presses and window closure.
# The program will stay in this loop until the window is closed.
window.mainloop()