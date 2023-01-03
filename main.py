from tkinter import *
import random
import PyPDF2
import time

FONT = ("Arial", 20, "")
wpm = []
correct_wpm = []
words_to_display = []
display = ''
timer_continue = False


def random_word_list(path):
    global display
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
                "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    word_list = []
    discard_words = []
    # extract text from pdf
    random_page_number = random.randint(7, 133)
    pdf_object = open(path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_object)
    page_object = pdf_reader.pages[random_page_number]
    page_text = page_object.extract_text()
    # get separate words
    split_words = page_text.split(" ")
    for word in split_words:
        word_list.append(word)
    # get rid of non-words
    for word in word_list:
        for char in word:
            if char not in alphabet:
                discard_words.append(word)
    final_words = [i for i in word_list if i not in discard_words]
    # randomise word order
    random_words = [random.choice(final_words) for i in final_words]
    return random_words


# gui setup
window = Tk()
window.minsize(1000, 500)
window.title("Typing Speed Test")
window.config(padx=20, pady=20, bg="black")
canvas = Canvas(width=1000, height=300, bg='white')
canvas.place(relx=0.5, rely=0.5, anchor='center')
canvas_display = canvas.create_text(400, 150, text="Words will appear hear after 'Start' is pressed "
                                                   "and the timer is started", font=FONT, fill='black')


def start_timer():
    global wpm, timer_continue, correct_wpm, words_to_display, display
    timer_continue = True
    wpm = []
    correct_wpm = []
    words_to_display = []
    display = ''
    type_space.focus()
    value_timer.config(text='60')
    run_timer(60)
    for word in random_word_list('othello.pdf'):
        words_to_display += word
        canvas.itemconfig(canvas_display, text=word, fill='black')


def run_timer(count):
    if not timer_continue:
        return
    if count > -1:
        window.after_id = window.after(1000, run_timer, count - 1)
    else:
        window.after_id = None
    if count == 0:
        finish_stats()
    value_timer.config(text=f"{count}")


def reset_timer():
    global words_to_display, wpm, timer_continue, correct_wpm, display
    timer_continue = False
    wpm = []
    correct_wpm = []
    words_to_display = []
    display = ''
    value_wpm.config(text=len(wpm))
    value_timer.config(text='60')
    canvas.itemconfig(corrected_wpm, text=f"Corrected words per minute: {len(correct_wpm)}", font=FONT, fill='white')
    canvas.itemconfig(final_wpm, text=f"Total words per minute: {len(wpm)}", font=FONT, fill='white')


def next_word(event):
    global words_to_display, display, wpm
    display = ''
    for word in random_word_list('othello.pdf'):
        # display += (word + ' ')
        words_to_display.append(word)
        canvas.itemconfig(canvas_display, text=word, fill='black')
    wpm.append(type_space.get())
    type_space.delete(0, END)
    value_wpm.config(text=str(len(wpm)))


def finish_stats():
    global wpm, correct_wpm
    correct_list = [i for i in wpm if i in words_to_display]
    correct_wpm = len(correct_list)
    canvas.itemconfig(corrected_wpm, text=f"Corrected words per minute: {correct_wpm}", font=FONT, fill='black')
    canvas.itemconfig(final_wpm, text=f"Total words per minute: {len(wpm)}", font=FONT, fill='black')


start_button = Button(window, text="Start", bd='5', width=10, font=("Arial", 40, ""), command=start_timer)
start_button.place(x=5, y=395, anchor='nw')
type_space = Entry(window, font=("Arial", 40, ""), bd='5', width=28)
type_space.place(x=300, y=395, anchor='nw')

label_wpm = Label(text="WPM: ", font=FONT, bg='white', fg='black')
label_wpm.place(relx=0.089, rely=0, anchor='nw')
value_wpm = Label(window, width=3, font=FONT, bg="white", fg="black", text='0')
value_wpm.place(relx=0.15, rely=0, anchor='nw')

label_timer = Label(text="Time Left: ", font=FONT, bg='white', fg='black')
label_timer.place(relx=0.4, rely=0, anchor='nw')
value_timer = Label(window, width=3, font=FONT, text='60', bg='white', fg='black')
value_timer.place(relx=0.5, rely=0, anchor='nw')

reset_button = Button(text="RESTART", background="white", fg="blue", width='10', font=("Arial", 20, ""),
                      command=reset_timer)
reset_button.place(relx=0.8, rely=0, anchor='nw')

corrected_wpm = canvas.create_text(150, 50)
final_wpm = canvas.create_text(150, 80)


window.bind('<space>', next_word)

window.mainloop()
