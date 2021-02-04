from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
check_num = ""
timer = None
reset = False

# # ---------------------------- TIMER RESET ------------------------------- #
#
#
# def reset_timer():
#     global reps
#     global check_num
#     timer_text.configure(text="25:00")
#     timer_label.configure(text="Timer", fg=GREEN)
#     reps = 0
#     window.after_cancel(timer)
#     check_num = ""
#     start_button["state"] = NORMAL
#
# # ---------------------------- TIMER MECHANISM ------------------------------- #
#
#
# def start_all():
#     start_button["state"] = DISABLED
#     start_timer()
#
#
# def start_timer():
#     global reps
#     global check_num
#     reps += 1
#     if reps == 8:
#         refresh_label(LONG_BREAK_MIN)
#         reps = 0
#         check_num = ""
#         timer_label.configure(text="Break", fg=RED)
#         return
#     elif reps % 2 != 0:
#         refresh_label(WORK_MIN)
#         timer_label.configure(text="Work", fg=GREEN)
#     else:
#         refresh_label(SHORT_BREAK_MIN)
#         check_num += "✔"
#         timer_label.configure(text="Break", fg=PINK)
#
#
# # ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
#
#
# def refresh_label(t):
#     global timer
#     if t > 0:
#         mins, secs = divmod(t, 60)
#         timer = "{:02d}:{:02d}".format(mins, secs)
#         timer_text.configure(text=timer)
#         timer = window.after(1000, refresh_label, t-1)
#     else:
#         start_timer()
#         check_label.configure(text=check_num)
#
#
# # ---------------------------- UI SETUP ------------------------------- #
#
# window = Tk()
# window.title("Pomodoro")
# window.config(padx=100, pady=50, bg=YELLOW)
#
# canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
# tomato_img = PhotoImage(file="Suse_Tomate.png")
# canvas.create_image(100, 112, image=tomato_img)
# canvas.grid(column=2, row=1)
#
#
# timer_text = Label(text="25:00", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 40, "bold"))
# timer_text.grid(column=2, row=2)
#
# timer_label = Label(text="Timer", font=(FONT_NAME, 40, "bold"), bg=YELLOW, fg=GREEN)
# timer_label.grid(column=2, row=0)
#
# start_button = Button(text="Start", relief="groove", padx=10, bg=YELLOW, activebackground=GREEN, font=(FONT_NAME, 10,
#                                                                                                        "bold"),
#                       command=start_all)
# start_button.grid(column=1, row=3)
#
# reset_button = Button(text="Reset", relief="groove", padx=10, bg=YELLOW, activebackground=GREEN, font=(FONT_NAME, 10,
#                                                                                                        "bold"),
#                       command=reset_timer)
# reset_button.grid(column=3, row=3)
#
# check_label = Label(text=check_num, font=(FONT_NAME, 10, "bold"), bg=YELLOW, fg=GREEN)
# check_label.grid(column=2, row=3)
#
# window.mainloop()

# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    global reps
    global check_num
    timer_text.configure(text="00:00")
    timer_label.configure(text="Timer", fg=GREEN)
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
    global reps
    global check_num
    reps += 1
    if reps == 8:
        refresh_label(LONG_BREAK_MIN * 60)
        reps = 0
        check_num = ""
        check_label.configure(text=check_num)
        timer_label.configure(text="Break", fg=RED)
    elif reps % 2 != 0:
        refresh_label(WORK_MIN * 60)
        timer_label.configure(text="Work", fg=GREEN)
    else:
        refresh_label(SHORT_BREAK_MIN * 60)
        check_num += "✔"
        check_label.configure(text=check_num)
        timer_label.configure(text="Break", fg=PINK)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def refresh_label(t):
    global timer
    if t > 0:
        mins, secs = divmod(t, 60)
        timer = "{:02d}:{:02d}".format(mins, secs)
        timer_text.configure(text=timer)
        timer = window.after(1000, refresh_label, t-1)
        if t < 10:
            window.attributes("-topmost", True)
    else:
        start_timer()
        check_label.configure(text=check_num)
        window.attributes("-topmost", False)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=10, bg=YELLOW)

timer_text = Label(text="00:00", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 40, "bold"))
timer_text.grid(column=2, row=2)

timer_label = Label(text="Timer", font=(FONT_NAME, 40, "bold"), bg=YELLOW, fg=GREEN)
timer_label.grid(column=2, row=0)

tomato = PhotoImage(file=r"Suse_Tomate.png")
start_button = Button(image=tomato, activebackground=YELLOW, borderwidth=0, bg=YELLOW, font=(FONT_NAME, 10, "bold"),
                      command=start_all)
start_button.grid(column=2, row=1)

check_label = Label(text=check_num, font=(FONT_NAME, 10, "bold"), bg=YELLOW, fg=GREEN)
check_label.grid(column=2, row=3)

window.mainloop()
