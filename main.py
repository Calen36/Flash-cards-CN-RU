from tkinter import *
import pandas
import random

current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("chinese.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    root.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_txt, text=current_card["CN"], font=('Arial', 200))
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = root.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_txt, text=current_card["CN"] + '\n\n' + current_card["RU"].replace('; ', '\n'),
                      font=('Arial', 22))
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    pandas.DataFrame(to_learn).to_csv("words_to_learn.csv", index=False)
    next_card()


root = Tk()
root.title("Learn Chinese Characters")
root.iconbitmap('images/icon.ico')
root.config(padx=50, pady=50, bg="#B1DDC6")
root.resizable(height=False, width=False)

flip_timer = root.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_txt = canvas.create_text(400, 263, text="", font=('Arial', 120))
canvas.config(bg="#B1DDC6", highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()

root.mainloop()
