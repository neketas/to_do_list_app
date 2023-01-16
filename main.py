import random
from tkinter import *

snake_size = 4
snake_speed = 100
snake_color = "white"
space_size = 20
window_width = 500
window_height = 500
collectible_color = "green"
background_color = "black"


class Snake:
    def __init__(self) -> None:
        self.body_size = snake_size
        self.coordinates = []
        self.squares = []

        for i in range(0, snake_size):
            self.coordinates.append([0,0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x,y, x + space_size, y + space_size)
            self.squares.append(square)

class Collectible:
    def __init__(self) -> None:
        x = random.randint(0, (window_width/space_size) - 1) * space_size
        y = random.randint(0, (window_height/space_size) - 1) * space_size

        self.coordinates = [x,y]

        canvas.create_oval(x, y, x + space_size, y + space_size, fill = collectible_color, tag = "collectible")

def turn(snake, collectible):
    x, y = snake.coordinates[0]

    if entry_direction == "up":
        y -= space_size
    elif entry_direction == "down":
        y += space_size
    elif entry_direction == "left":
        x -= space_size
    elif entry_direction == "right":
        x += space_size

    snake.coordinates.insert(0,(x,y))
    square = canvas.create_rectangle(x,y, x + space_size, y + space_size)
    
    snake.squares.insert(0, square)

    if x == collectible.coordinates[0] and y == collectible.coordinates[1]:
        global score
        score += 1
        lb.config(text = "Score:{}".format(score))
        canvas.delete("collectible")
        collectible = Collectible()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    if check_collisions(snake):
        dead()
    else:
        root.after(snake_speed, turn, snake, collectible)

def change_direction(new_direction):
    global entry_direction 

    if new_direction == "left":
        if entry_direction != "right":
            entry_direction = new_direction
    elif new_direction == "right":
        if entry_direction != "left":
            entry_direction = new_direction
    elif new_direction == "up":
        if entry_direction != "down":
            entry_direction = new_direction
    elif new_direction == "down":
        if entry_direction != "up":
            entry_direction = new_direction

def check_collisions(snake):
    x,y = snake.coordinates[0]

    if x < 0 or x >= window_width:
        return True
    elif y < 0 or y >= window_height:  
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def dead():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font = ("Arial", 40), text = "YOU LOSE", fill = "red", tag = "GameOver")
    
root = Tk()
root.title("Snake")
root.resizable(False,False)

score = 0
entry_direction = "down"

lb = Label(root, text = "Score: {}".format(score), font = ("Arial", 18))
lb.pack()

canvas = Canvas(root, bg = background_color, height = window_height, width = window_width)
canvas.pack()

root.update()

root_width = root.winfo_width()
root_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = int((screen_width/2) - (root_width/2))
y = int((screen_height/2) - (root_height/2))

snake = Snake()
collectible = Collectible()

turn(snake, collectible)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

root.bind("<Left>", lambda event: change_direction("left"))
root.bind("<Right>", lambda event: change_direction("right"))
root.bind("<Up>", lambda event: change_direction("up"))
root.bind("<Down>", lambda event: change_direction("down"))

root.mainloop()