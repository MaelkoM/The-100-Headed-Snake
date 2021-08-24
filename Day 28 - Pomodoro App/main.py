from tkinter import PhotoImage, Tk, Label, Button
import random

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Helvetica"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
TOMATO_START = "Artwork/susa_tomata_start.png"
TOMATO_WORK = "Artwork/susa_tomata_work.png"
TOMATO_LONG = "Artwork/susa_tomata_long.png"
TOMATO_SHORT_LIST = [
    "Artwork/susa_tomata_short_1.png",
    "Artwork/susa_tomata_short_2.png",
]
reps = 0
check_num = ""
timer = None
reset = False

# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    global reps
    global check_num
    timer_text.configure(text="00:00")
    timer_label.configure(text="Timer", fg=GREEN)
    start_button.configure(image=tomato_start)
    reps = 0
    window.after_cancel(timer)
    check_num = ""
    check_label.configure(text=check_num)


# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_all():
    global reset
    if not reset:
        reset = True
        start_timer()
    else:
        reset = False
        reset_timer()


def start_timer():
    global reps, check_num, TOMATO_SHORT_LIST, tomato_short
    random_tomato_short = random.choice(TOMATO_SHORT_LIST)
    tomato_short = PhotoImage(file=random_tomato_short)
    reps += 1
    if reps == 8:
        refresh_label(LONG_BREAK_MIN * 60)
        reps = 0
        check_num = ""
        check_label.configure(text=check_num)
        start_button.configure(image=tomato_long)
        timer_label.configure(text="Break", fg=RED)
    elif reps % 2 != 0:
        refresh_label(WORK_MIN * 60)
        start_button.configure(image=tomato_work)
        timer_label.configure(text="Work", fg=GREEN)
    else:
        refresh_label(SHORT_BREAK_MIN * 60)
        check_num += "✔"
        check_label.configure(text=check_num)
        start_button.configure(image=tomato_short)
        timer_label.configure(text="Break", fg=PINK)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def refresh_label(t):
    global timer
    if t > 0:
        mins, secs = divmod(t, 60)
        timer = "{:02d}:{:02d}".format(mins, secs)
        timer_text.configure(text=timer)
        timer = window.after(1000, refresh_label, t - 1)
        if t < 10:
            window.attributes("-topmost", True)
    else:
        start_timer()
        check_label.configure(text=check_num)
        window.attributes("-topmost", False)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Suso Pomodoro")
window.config(padx=100, pady=10, bg=YELLOW)

timer_text = Label(text="00:00", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 40, "bold"))
timer_text.grid(column=2, row=2)

timer_label = Label(text="Timer", font=(FONT_NAME, 40, "bold"), bg=YELLOW, fg=GREEN)
timer_label.grid(column=2, row=0)

tomato_start = PhotoImage(file=TOMATO_START)
tomato_work = PhotoImage(file=TOMATO_WORK)
tomato_long = PhotoImage(file=TOMATO_LONG)
tomato_short = PhotoImage(file=TOMATO_SHORT_LIST[0])

start_button = Button(
    image=tomato_start,
    activebackground=YELLOW,
    borderwidth=0,
    bg=YELLOW,
    font=(FONT_NAME, 10, "bold"),
    command=start_all,
)
start_button.grid(column=2, row=1)

check_label = Label(text=check_num, font=(FONT_NAME, 10, "bold"), bg=YELLOW, fg=GREEN)
check_label.grid(column=2, row=3)

window.mainloop()
