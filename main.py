from tkinter import *
from pandas import read_csv, DataFrame
from random import choice
BACKGROUND_COLOR = "#B1DDC6"
FONT = "Arial"
WORDS_FILE = "data/french_words.csv"
LEARN_FILE = "data/words_to_learn.csv"

try:
    study_dataset = read_csv(LEARN_FILE)
except FileNotFoundError:
    study_dataset = read_csv(WORDS_FILE)
finally:
    study_list = study_dataset.to_dict(orient="records")
current_card = {}
# ---------------------------- FUNCTIONS  ------------------------------ #


def remove_card():
    study_list.remove(current_card)
    DataFrame(study_list).to_csv(LEARN_FILE, index=False)
    next_card()


def next_card():
    global current_card, timer
    window.after_cancel(timer)
    current_card = choice(study_list)
    canvas.itemconfig(canvas_image, image=card_front_image)
    canvas.itemconfig(language_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=current_card["French"], fill="black")
    timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

#Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_image)

#Canvas text x2
language_text = canvas.create_text(400, 150, text="", fill="black",
                                font=(FONT, 40, "italic"))
word_text = canvas.create_text(400, 263, text="", fill="black",
                                font=(FONT, 60, "bold"))

#Buttons x2
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0,
                      command=next_card)
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0,
                      command=remove_card)

#Layout
canvas.grid(row=0, column=0, columnspan=2)
wrong_button.grid(row=1, column=0)
right_button.grid(row=1, column=1)

timer = window.after(3000, flip_card)
next_card()

window.mainloop()
