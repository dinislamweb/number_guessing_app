import tkinter as tk
from tkinter import messagebox
from random import randint
import pygame
import os

# Initialize pygame mixer for sound
pygame.mixer.init()

SOUND_MISS = os.path.join(os.path.dirname(__file__), 'soft_buzz.wav')  # Use a soft buzz for miss
SOUND_WIN = os.path.join(os.path.dirname(__file__), 'cheer.wav')      # Use a cheerful sound for win

# Generate random number
def new_game():
    global random_num, attempts, guess_history
    random_num = randint(1, 100)
    attempts = 0
    guess_history = []
    entry_var.set("")
    feedback_var.set("Guess a number between 1 and 100!")
    attempts_var.set("Attempts: 0")
    history_var.set("")
    emoji_var.set("")
    guess_btn.config(state=tk.NORMAL)
    restart_btn.config(state=tk.DISABLED)
    entry.config(state=tk.NORMAL)
    entry.focus()
    hide_congrats_area()

def play_sound(sound_path):
    try:
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
    except Exception:
        pass

def check_guess():
    global attempts, guess_history
    try:
        guess = int(entry_var.get())
    except ValueError:
        feedback_var.set("Please enter a valid number!")
        emoji_var.set("😞")  # Colorful sad emoji
        play_sound(SOUND_MISS)
        entry_var.set("")
        return
    if guess < 1 or guess > 100:
        feedback_var.set("Number must be between 1 and 100!")
        emoji_var.set("😞")  # Colorful sad emoji
        play_sound(SOUND_MISS)
        entry_var.set("")
        return
    attempts += 1
    guess_history.append(guess)
    attempts_var.set(f"Attempts: {attempts}")
    history_var.set(f"Your guesses: {', '.join(map(str, guess_history))}")
    if guess < random_num:
        feedback_var.set("⬆️ Too Low! Try a higher number.")
        emoji_var.set("😞")  # Colorful sad emoji
        play_sound(SOUND_MISS)
        entry_var.set("")
    elif guess > random_num:
        feedback_var.set("⬇️ Too High! Try a lower number.")
        emoji_var.set("😞")  # Colorful sad emoji
        play_sound(SOUND_MISS)
        entry_var.set("")
    else:
        feedback_var.set(f"🎉 Congratulations! You guessed it in {attempts} attempts!")
        emoji_var.set("🥳")  # Colorful happy emoji
        play_sound(SOUND_WIN)
        guess_btn.config(state=tk.DISABLED)
        restart_btn.config(state=tk.NORMAL)
        entry.config(state=tk.DISABLED)
        # Show a bottom congratulation area with emoji and sound
        show_congrats_area()
        messagebox.showinfo("Winner!", f"You guessed the number in {attempts} attempts!\n\nYour guesses: {', '.join(map(str, guess_history))}")

def show_hint():
    hints = []
    if random_num % 2 == 0:
        hints.append("even")
    else:
        hints.append("odd")
    if random_num > 50:
        hints.append("greater than 50")
    else:
        hints.append("50 or less")
    messagebox.showinfo("Hint", f"The number is {hints[0]} and {hints[1]}.")

# --- UI COLORS ---
BG_GRADIENT_TOP = "#f7cac9"   # Light pink
BG_GRADIENT_BOTTOM = "#92a8d1" # Soft blue
CARD_BG = "seashell"              # Card background (was tomato)
CARD_BORDER = "#e0e1dd"       # Card border
FG_MAIN = "#22223b"           # Deep blue-black for text
ACCENT = "#ff6f3c"            # Orange-red for buttons
BTN_BG = ACCENT
BTN_FG = "#fff"                # White text for buttons
BTN_ACTIVE_BG = "#ff922b"     # Lighter orange-red
ENTRY_BG = "#f8f9fa"          # Light entry
ENTRY_FG = FG_MAIN
HISTORY_FG = "#3a86ff"         # Blue for history

# --- Fonts ---
font_title = ("Poppins", 22, "bold")  # Reduced font size for better fit
font_label = ("Poppins", 15)
font_btn = ("Poppins", 15, "bold")
font_emoji = ("Arial", 38)

root = tk.Tk()
root.title("Number Guessing Game")
root.geometry("520x540")
root.resizable(False, False)

# Gradient background using a Canvas
canvas = tk.Canvas(root, width=520, height=540, highlightthickness=0)
canvas.pack(fill="both", expand=True)
for i in range(0, 540):
    r1, g1, b1 = 247, 202, 201  # top
    r2, g2, b2 = 146, 168, 209  # bottom
    r = int(r1 + (r2 - r1) * i / 540)
    g = int(g1 + (g2 - g1) * i / 540)
    b = int(b1 + (b2 - b1) * i / 540)
    color = f'#{r:02x}{g:02x}{b:02x}'
    canvas.create_line(0, i, 520, i, fill=color)

# Card-like main frame
main_frame = tk.Frame(root, bg=CARD_BG, bd=0, highlightbackground=CARD_BORDER, highlightthickness=3)
main_frame.place(relx=0.5, rely=0.5, anchor='center', width=440, height=470)

# --- Define all StringVars and widgets before using them in functions ---
emoji_var = tk.StringVar(value="")
feedback_var = tk.StringVar(value="Guess a number between 1 and 100!")
entry_var = tk.StringVar()
attempts_var = tk.StringVar(value="Attempts: 0")
history_var = tk.StringVar(value="")

# Add congratulation area widgets after main_frame and CARD_BG are defined
congrats_frame = tk.Frame(main_frame, bg=CARD_BG)
congrats_label = tk.Label(congrats_frame, text="", font=("Arial", 30), bg=CARD_BG)
congrats_label.pack(pady=4)
congrats_msg = tk.Label(congrats_frame, text="", font=("Poppins", 16, "bold"), fg="#43aa8b", bg=CARD_BG)
congrats_msg.pack(pady=2)

# Title
tk.Label(main_frame, text="🎲 Number Guessing Game", font=font_title, fg=ACCENT, bg=CARD_BG, wraplength=400, justify='center').pack(pady=(18, 8))

# Emoji feedback
emoji_label = tk.Label(main_frame, textvariable=emoji_var, font=font_emoji, bg=CARD_BG)
emoji_label.pack(pady=2)

# Feedback
tk.Label(main_frame, textvariable=feedback_var, font=font_label, fg=FG_MAIN, bg=CARD_BG).pack(pady=6)

# Entry
entry = tk.Entry(main_frame, textvariable=entry_var, font=font_label, width=14, justify='center', bg=ENTRY_BG, fg=ENTRY_FG, relief=tk.FLAT, bd=3, insertbackground=ENTRY_FG, highlightbackground=ACCENT, highlightcolor=ACCENT, highlightthickness=2)
entry.pack(pady=8)
entry.focus()

# Attempts
tk.Label(main_frame, textvariable=attempts_var, font=font_label, fg=ACCENT, bg=CARD_BG).pack(pady=4)

# Guess history
history_label = tk.Label(main_frame, textvariable=history_var, font=("Poppins", 12), fg=HISTORY_FG, bg=CARD_BG)
history_label.pack(pady=2)

# Buttons
btn_frame = tk.Frame(main_frame, bg=CARD_BG)
btn_frame.pack(pady=(22, 10))  # Add more bottom padding to keep buttons from touching the board

# Guess Button: Orange, white text
guess_btn = tk.Button(
    btn_frame, text="Guess", font=font_btn, bg="#ff6600", fg="#fff", activebackground="#ff922b", activeforeground="#fff", width=10, height=1, bd=0, relief=tk.FLAT, padx=8, pady=8, command=check_guess, cursor="hand2"
)
guess_btn.grid(row=0, column=0, padx=(18, 8), pady=7, ipadx=2, ipady=2)

# Hint Button: Blue, white text
hint_btn = tk.Button(
    btn_frame, text="Hint", font=font_btn, bg="#0057b7", fg="#fff", activebackground="#339cff", activeforeground="#fff", width=10, height=1, bd=0, relief=tk.FLAT, padx=8, pady=8, command=show_hint, cursor="hand2"
)
hint_btn.grid(row=0, column=1, padx=(8, 18), pady=7, ipadx=2, ipady=2)

# Restart Button: Green, white text, normal font size for best readability
restart_btn = tk.Button(
    btn_frame, text="Restart", font=font_btn, bg="cyan", fg="white", activebackground="#ff4d8b", activeforeground="white", width=10, height=1, bd=0, relief=tk.FLAT, padx=8, pady=8, command=new_game, state=tk.DISABLED, cursor="hand2"
)
restart_btn.grid(row=1, column=0, columnspan=2, pady=(14, 0), ipadx=2, ipady=2)

def show_congrats_area():
    congrats_label.config(text="🎉🥳🎉")
    congrats_msg.config(text="Congratulations! You Win!")
    congrats_frame.pack(side="bottom", pady=10)

def hide_congrats_area():
    congrats_label.config(text="")
    congrats_msg.config(text="")
    congrats_frame.pack_forget()

# Keyboard enter triggers guess
def on_enter(event):
    if guess_btn['state'] == tk.NORMAL:
        check_guess()
root.bind('<Return>', on_enter)

new_game()
root.mainloop()
