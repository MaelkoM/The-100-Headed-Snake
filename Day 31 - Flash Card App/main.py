from tkinter import *
import pandas as pd
import random as rd

BACKGROUND_COLOR = "#B1DDC6"
KNOWN_LANGUAGE = "Deutsch"
UNKNOWN_LANGUAGE = "Portugiesisch"
LIST_FILEPATH = "data/word_list_pt-de.csv"
NEW_LIST_FILEPATH = "data/words_to_learn.csv"
word_tuple = ("", "")
word = word_tuple[0]
translation = word_tuple[1]

# ---------------------Vocabulary--------------------- #
try:
    VOCABULARY_DF = pd.read_csv(NEW_LIST_FILEPATH)
except FileNotFoundError:
    VOCABULARY_DF = pd.read_csv(LIST_FILEPATH)
    vocabulary_dict = dict(zip(VOCABULARY_DF.pt, VOCABULARY_DF.de))
else:
    vocabulary_dict = dict(zip(VOCABULARY_DF.pt, VOCABULARY_DF.de))


def get_random_word():
    global word_tuple, word, translation
    word_tuple = rd.choice(list(vocabulary_dict.items()))
    word = word_tuple[0]
    translation = word_tuple[1]


def next_card():
    global flip_timer
    window.after_cancel(flip_timer)
    get_random_word()
    canvas.itemconfigure(card_side, image=card_front)
    canvas.itemconfigure(language_txt, text=UNKNOWN_LANGUAGE, fill="black")
    canvas.itemconfigure(word_pt, text=word, fill="black")
    flip_timer = window.after(3000, turn_card)


def turn_card():
    canvas.itemconfigure(card_side, image=card_back)
    canvas.itemconfigure(language_txt, text=KNOWN_LANGUAGE, fill="white")
    canvas.itemconfigure(word_pt, text=translation, fill="white")

# ---------------------Button Logic--------------------- #


def unknown_action():
    next_card()


def known_action():
    del vocabulary_dict[word]
    new_vocabulary_df = pd.DataFrame(vocabulary_dict.items(), columns=["pt", "de"])
    new_vocabulary_df.to_csv(NEW_LIST_FILEPATH)
    next_card()


# ---------------------Window--------------------- #

window = Tk()
window.title("Flash Card App")
window.configure(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, turn_card)

# ---------------------Card--------------------- #

canvas = Canvas(width=820, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_side = canvas.create_image(420, 263, image=card_front)

# ---------------------Text--------------------- #

language_txt = canvas.create_text(410, 150, text=UNKNOWN_LANGUAGE, font=("Tahoma", 40, "italic"))
word_pt = canvas.create_text(410, 263, text=word, font=("Tahoma", 60, "bold"))

# ---------------------Buttons--------------------- #

wrong_img = PhotoImage(file="images/wrong.png")
button_unknown = Button(image=wrong_img, bd=0, command=unknown_action, highlightthickness=0)
button_unknown.grid(column=0, row=1)

right_img = PhotoImage(file="images/right.png")
button_known = Button(image=right_img, bd=0, command=known_action, highlightthickness=0)
button_known.grid(column=1, row=1)

# ---------------------Misc--------------------- #

next_card()
window.mainloop()
