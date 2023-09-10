import random, time, threading
from tkinter import *

# Setting variables

word_list = [
    "apple", "banana", "cat", "dog", "elephant",
    "friend", "happy", "house", "jump", "kitchen",
    "laugh", "milk", "orange", "park", "quiet",
    "river", "sun", "tree", "umbrella", "water",
    "yellow", "zebra", "book", "car", "door",
    "flower", "green", "hat", "ice", "juice",
    "key", "lamp", "moon", "notebook", "ocean",
    "pen", "quilt", "red", "shoes", "table",
    "umbrella", "vase", "window", "xylophone", "yogurt",
    "zeppelin", "bread", "chair", "desk", "egg",
    "fish", "grape", "hat", "island", "jacket",
    "kite", "lemon", "mirror", "nest", "owl",
    "pencil", "quill", "radio", "socks", "turtle",
    "unicorn", "violet", "whale", "xylophone", "yawn",
    "zebra", "bag", "candle", "duck", "ear",
    "feather", "guitar", "hammer", "ink", "jungle",
    "kite", "lemon", "magnet", "napkin", "oar",
    "pencil", "quilt", "rope", "socks", "television",
    "umbrella", "vase", "wagon", "xylophone", "yogurt",
    "zeppelin"
]
score = 0
playing = False
time_remaining = 5
character_count = 0

# Creating the GUI

window = Tk()
window.title("Typing Speed Test")
window.geometry("500x600")

# Creating a simple label to explain the rules

expl_label = Label(text=f"Start tyipng to start the timer.\nYou will have {time_remaining} seconds to do your best.")
expl_label.pack(pady=50)

# Creating 2 StringVar's to contain current and upcoming random words

selected_word = StringVar()
next_word = StringVar()

# At the start of the game we want to choose 2 random words,
# one for the current word and one for the next word
# this function is called only once at the start of the game

def choose_first_words():
    global selected_word, next_word
    selected_word.set(random.choice(word_list))
    next_word.set(random.choice(word_list))

# After first time, to select new words, this function is
# called instead. This function changes current word to
# reflect the previous next word and selects a new next word
# this function is called after every correct word

def choose_words():
    global selected_word, next_word
    selected_word.set(next_word.get())
    next_word.set(random.choice(word_list))

# Displaying current and next words as labels

word_label = Label(textvariable=selected_word, font="Arial, 30")
word_label.pack()

next_word_label = Label(textvariable=next_word, font="Arial, 15")
next_word_label.pack(pady=(5,35))

# Calling a function to check if entry and current word match
# also coloring the entry box fg accordingly

def check_match(event):
    global score, playing, character_count
    if playing == False:
        playing = True
        timer()

    if entry.get()[:len(entry.get())] == selected_word.get()[:len(entry.get())]:
        entry.config(foreground="green")
    else:
        entry.config(foreground="red")

    if entry.get() == selected_word.get():
        entry.delete(0, END)
        entry.config(foreground="black")
        choose_words()
        score += 1
        character_count += len(selected_word.get())
        score_var.set(f"Your current score is: {score}")

# Creating the entry box and a keyrelease bind attached to it
# that calls the check_match function after every key release

entry = Entry(justify="center", font="Arial, 30")
entry.pack()
entry.focus_force()
entry.bind("<KeyRelease>", check_match)

# Defining and displaying the score variable

score_var = IntVar()
score_var.set(f"Your current score is: {score}")

score_label = Label(textvariable=score_var)
score_label.pack(pady=20)

# Starting the timer with the first letter typed end stops the
# game when timer ends

def timer():
    global time_remaining, playing
    if time_remaining > 0:
        print(time_remaining)
        timer_var.set(f"Time remaining: {time_remaining}")
        time_remaining -= 1
        window.after(1000, timer)
    else:
        timer_var.set("Time's up!")
        timer_label.config(foreground="red")
        entry.config(state=DISABLED)
        score_var.set(f"You managed to type {score} words in 30 seconds!\nYour WPM is {score*60/30}\nYour CPM is {character_count*60/30}")
        replay.pack(pady=20)
        playing = False

timer_var = StringVar()
timer_var.set(f"Time remaining: {time_remaining}")

timer_label = Label(textvariable=timer_var)
timer_label.pack(pady=20)

# Setting all the variables to their original states and
# reseting the game

def reset():
    global time_remaining, score, character_count
    time_remaining = 30
    score = 0
    character_count = 0
    entry.delete(0, END)
    entry.config(state=NORMAL)
    score_var.set(f"Your current score is: {score}")
    timer_label.config(foreground="black")
    timer_var.set(f"Time remaining: {time_remaining}")
    replay.forget()
    choose_first_words()

# Replay button that only appears when game is over

replay = Button(text="Play Again?", command=reset)

choose_first_words()

window.mainloop()