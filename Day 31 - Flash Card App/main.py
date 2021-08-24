from tkinter import *
import pandas as pd
import random as rd

BACKGROUND_COLOR = "#81b29a"
KNOWN_LANGUAGE = "Deutsch"
UNKNOWN_LANGUAGE = "Portugiesisch"
LIST_FILEPATH = "Lists/word_list_pt-de.csv"
NEW_LIST_FILEPATH = "Lists/words_to_learn.csv"
COLUMN_NAMES_IN_FILE = ["pt", "de"]
CARD_FRONT_IMAGE = "Artwork/card_front.png"
CARD_BACK_IMAGE = "Artwork/card_back.png"
WINDOW_TITLE = "Flash Card App"
BUTTON_IMAGE_WRONG = "Artwork/wrong.png"
BUTTON_IMAGE_RIGHT = "Artwork/right.png"
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
    canvas.itemconfigure(language_txt, text=UNKNOWN_LANGUAGE, fill="midnight blue")
    canvas.itemconfigure(word_pt, text=word, fill="midnight blue")
    flip_timer = window.after(3000, turn_card)


def turn_card():
    canvas.itemconfigure(card_side, image=card_back)
    canvas.itemconfigure(language_txt, text=KNOWN_LANGUAGE, fill="grey10")
    canvas.itemconfigure(word_pt, text=translation, fill="grey10")

# ---------------------Button Logic--------------------- #


def unknown_action():
    next_card()


def known_action():
    del vocabulary_dict[word]
    new_vocabulary_df = pd.DataFrame(vocabulary_dict.items(), columns=COLUMN_NAMES_IN_FILE)
    new_vocabulary_df.to_csv(NEW_LIST_FILEPATH)
    next_card()


# ---------------------Window--------------------- #

window = Tk()
window.title(WINDOW_TITLE)
window.configure(bg=BACKGROUND_COLOR, padx=50, pady=40)

flip_timer = window.after(3000, turn_card)

# ---------------------Card--------------------- #

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2, pady=10)
card_front = PhotoImage(file=CARD_FRONT_IMAGE)
card_back = PhotoImage(file=CARD_BACK_IMAGE)
card_side = canvas.create_image(400, 263, image=card_front)

# ---------------------Text--------------------- #

language_txt = canvas.create_text(400, 75, text=UNKNOWN_LANGUAGE, font=("Lucida Handwriting", 40, "italic"))
word_pt = canvas.create_text(400, 295, text=word, font=("Lucida Handwriting", 60, "bold"))

# ---------------------Buttons--------------------- #

wrong_img = PhotoImage(file=BUTTON_IMAGE_WRONG)
button_unknown = Button(image=wrong_img, bd=0, bg=BACKGROUND_COLOR, command=unknown_action, highlightthickness=0)
button_unknown.grid(column=0, row=1, pady=10)

right_img = PhotoImage(file=BUTTON_IMAGE_RIGHT)
button_known = Button(image=right_img, bd=0, bg=BACKGROUND_COLOR, command=known_action, highlightthickness=0)
button_known.grid(column=1, row=1, pady=10)

# ---------------------Misc--------------------- #

next_card()
window.mainloop()
