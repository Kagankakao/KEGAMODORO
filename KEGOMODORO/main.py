import os
import csv
import tkinter.messagebox
import math
import pandas as pd
import datetime as dt
import requests
import datetime
import time
import pygame
from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
from pyautogui import position
from time import sleep
from keyboard import is_pressed
from PIL import Image, ImageTk
from pathlib import Path
# ---------------------------- CONSTANTS AND SOME VARIABLES ------------------------------- #
# Change working directory to the script's location
os.chdir(os.path.dirname(os.path.abspath(__file__)))
BLACK = "#000000"
PINK = "#e2979c"
RED = "#000000"
GREEN = "#EB5B00"
YELLOW = "#8B0000"
ORANGE = "#fcba03"
DEEP_BLUE = "#000000"
DEEP_RED = "#cc2b33"
FONT_NAME = "Courier"
TOMATO_COLOR = "#f26849"
GRAY_COLOR = "#696969"
WHITE = "#feffff"
BUTTON_BACKGROUND_COLOR = BLACK
BUTTON_FOREGROUND_COLOR = WHITE
RADIO_BACKGROUND_COLOR = "#8B0000"
RADIO_FOREGROUND_COLOR = BLACK
SWITCH_BUTTON_DARK_BG_COLOR = BLACK
SWITCH_BUTTON_DARK_FG_COLOR = WHITE
SWITCH_BUTTON_LIGHT_BG_COLOR = WHITE
SWITCH_BUTTON_LIGHT_FG_COLOR = BLACK

#TODO: WHEN RESTING THE TIMER SAVE IT!
#TODO: UPDATE THE SAVE YOUR NOTE SECTION
#TODO: CHANGE THE THEMES
PIXELA_ENDPOINT = "https://pixe.la/v1/users" #! FILL HERE
USERNAME = "kegan"
TOKEN = "afhus8hj2phfb29nn821r"
GRAPH_ID = "graph1" #! FILL HERE

DEPENDENCIES = Path("dependencies/")
IMAGES = f"{DEPENDENCIES}/images"
AUDIOS = f"{DEPENDENCIES}/audios"
TEXTS = f"{DEPENDENCIES}/texts"

SAVE_FILE_NAME = f"{TEXTS}/KAÆ[Æß#.txt" # ! Change this to your desired file name
BREAK_SOUND_PATH = f"{AUDIOS}/ding.mp3"
APP_ICON_PATH = f"{IMAGES}/behelit.png" # ! THIS IS THE ICON STUFF SO CHANGE THIS
FLOATING_IMAGE_PATH = f"{IMAGES}/behelit.png"
LOGO_IMAGE_PATH = f"{IMAGES}/logo2.png"
MAIN_IMAGE_PATH = f"{IMAGES}/space_tomato2.png"
FLOATING_WINDOW_CHECKER_PATH = f"{TEXTS}/floating_window_checker.txt"
TIME_CSV_PATH = f"{TEXTS}/time.csv"
# Load to audio file
pygame.mixer.init()
BREAK_SOUND = pygame.mixer.Sound(BREAK_SOUND_PATH)
# Audio volume
BREAK_SOUND.set_volume(0.5)
#TODO: CHANGE THE SAVE NOTE ICON
# ----------------------------- TIMER VARIABLES ------------------------------- #
now = str(datetime.datetime.now())
DATE = now.split(" ")[0].replace("-", "")

saved_data = {
    "date": [],
    "time": [],
    "notes": []
}

# ----------------------------- TIMER CONFIGS ------------------------------- #
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 1
resume = 0
start_timer_checker = 0
second = 0
minute = 0
hours = 0
count_downer = 0
count_upper = 0
note_writer_first_gap = 0
MAIN_MINUTE_FONT_SIZE = 28
MAIN_HOUR_FONT_SIZE = 20
FLOATING_MINUTE_FONT_SIZE = 26
FLOATING_HOUR_FONT_SIZE = 23
HOURS_X=125
HOURS_Y=170
MINUTE_X=160
MINUTE_Y=168

show_hours = False
pomodoro_mode_activate = False
crono_mode_activate = False
condition_checker = True
paused = False
start_short_break= False
start_long_break = False
open_floating_window = False
start_timer_checker_2 = False # FOR THE FIX FIRST SECOND GLITCH
#TODO: ADD A WARNING TO RESET BUTTON TO THIS "ARE YOU SURE?"
#TODO: CHANGE THE 00:00'S COLOR WHITE TO ANY COLOR
#TODO: LONG_BREAK 05:00 TEXTİNİ DİNAMİK YAP
#TODO: CHANGE THE COLORS NAME, THEY ARE WRONG

# ------------------------------ SOME BOOT-UPS --------------------------------- #

# Creating time.csv
try:
    with open(TIME_CSV_PATH, "r") as file:
        file.read()
except:
    with open(TIME_CSV_PATH, "w") as file:
        file.write("hours,minute,second\n0,0,0\n")

# -------------------------- CONECTION WITH PIXELA ------------------------------- #
def connect_to_pixela():
    global hours
    params = {
        "color": "momiji",
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes"
    }
    # creates user
    # response = requests.post(url=PIXELA_ENDPOINT, json=params)


    graphic_endpoint = f"{PIXELA_ENDPOINT}{USERNAME}/graphs"
    graphic_params = {
        "id": GRAPH_ID,
        "name": USERNAME,
        "unit": "hours",
        "type": "float",
    }
    headers = {
        "X-USER-TOKEN": TOKEN
    }

    # creates graph
    # graph_response = requests.post(url=graphic_endpoint, json=graphic_params, headers=headers)
    add_pixel_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}"
    pixels_params = {
        "date": DATE,
        "quantity": str(hours),
    }
    pixel_response = requests.post(url=add_pixel_endpoint, json=pixels_params, headers=headers)
    print(pixel_response.text)
    print(len(pixel_response.text))
    update_pixel_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}/{DATE}"
    update_pixel_params = {
        "quantity": str(hours),
    }
    # updates pixel quantity
    update_pixel_response = requests.put(url=update_pixel_endpoint, json=update_pixel_params, headers=headers)

    delete_pixel_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}/{DATE}"

    # delete_pixel_response = requests.delete(url=delete_pixel_endpoint, headers=headers)
    if len(pixel_response.text) == 341:
        print("Trying to connect to Pixela again...")
        time.sleep(0.5)
        connect_to_pixela()
# ----------------------------MODS---------------------------- #
def pomodoro_mode():
    global pomodoro_mode_activate, crono_mode_activate, hours, minute, second
    if crono_mode_activate:
        with open(TIME_CSV_PATH, mode='a') as file:
            file.write(f"{hours},{minute},{second}\n")
    reset()
    crono_mode_activate = False
    pomodoro_mode_activate = True


def crono_mode():
    global crono_mode_activate, pomodoro_mode_activate, second, minute, hours, show_hours, crono_reset
    reset()
    crono_mode_activate = True
    pomodoro_mode_activate = False

    # get's the time in time file
    df = pd.read_csv(TIME_CSV_PATH)
    second = df['second'].iloc[-1]
    minute = df['minute'].iloc[-1]
    hours = df['hours'].iloc[-1]
    if int(hours) != 0:
        show_hours = True

    if not show_hours:
        canvas.itemconfig(timer, text=f"{minute:02d}:{second:02d}")
        floating_timer_label.config(text=f"{minute:02d}:{second:02d}", font=(FONT_NAME, FLOATING_MINUTE_FONT_SIZE, "bold")) #! RELATIONAL WITH FLOATING TIMER BUT WHERE IDK
        floating_timer_label.place(x=MINUTE_X, y=MINUTE_Y)
    if show_hours:
        canvas.itemconfig(timer, text=f"{hours:02d}:{minute:02d}:{second:02d}", font=(FONT_NAME, MAIN_HOUR_FONT_SIZE, "bold")) #! RELATIONAL WITH MAIN SCREEN'S TIMER
        floating_timer_label.config(text=f"{hours:02d}:{minute:02d}:{second:02d}", font=(FONT_NAME, FLOATING_HOUR_FONT_SIZE, "bold")) #! RELATIONAL WITH FLOATING TIMER
        floating_timer_label.place(x=HOURS_X, y=HOURS_Y)
def floating_window(**kwargs):
    global open_floating_window, checked_state
    if open_floating_window == "True" or open_floating_window == "False":
        open_floating_window = open_floating_window.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
    open_floating_window = not open_floating_window
    try:
        kwargs["check"]
    except Exception as e:
        print(f"Error: {e}")
    else:
        open_floating_window = kwargs.get("check") 
    if open_floating_window == "True" or open_floating_window == True:
        window.deiconify()
        checked_state.set(1)
    elif open_floating_window == "False" or open_floating_window == False:
        window.withdraw()
        checked_state.set(0)
    with open(FLOATING_WINDOW_CHECKER_PATH, "w") as f:
        f.write(str(open_floating_window))




# ----------------------------TIMER RESET ------------------------------- #
def reset():
    global reps, count_downer, count_upper, start_timer_checker, minute, second, pause_checker, \
        condition_checker, pomodoro_mode_activate, crono_mode_activate, hours, show_hours, resume
    if pomodoro_mode_activate:
        try:
            root.after_cancel(count_downer)
        except Exception as e:
            print(f"Error: {e}")
    elif crono_mode_activate:
        try:
            root.after_cancel(count_upper)
        except Exception as e:
            print(f"Error: {e}")


    else:
        print("Error: No mode selected")
    timer_label.config(text="TIMER", fg=GREEN)
    check_mark.config(text="")
    reps = 1
    start_timer_checker = 0
    resume = 0
    hours = 0
    minute = 0
    second = 0
    condition_checker = True
    show_hours = False
    # pause_checker = 0
    pause_button.config(text=f"Pause")
    canvas.itemconfig(timer, text="00:00", font=(FONT_NAME, MAIN_MINUTE_FONT_SIZE, "bold"))
    floating_timer_label.config(text="00:00", font=(FONT_NAME, FLOATING_MINUTE_FONT_SIZE, "bold"))
    floating_timer_label.place(x=MINUTE_X, y=MINUTE_Y)
    

# ---------------------------- CRONOMETER MECHANISM ------------------------------- #
def crono():
    global count_upper, second, minute, hours, show_hours, start_timer_checker_2
    timer_label.config(text="WORK", fg=RED)
    # For the starting second, otherwise there will be a bug
    if not start_timer_checker_2:
        second +=1 
    if not show_hours:
        canvas.itemconfig(timer, text=f"{minute:02d}:{second:02d}")
        floating_timer_label.config(text=f"{minute:02d}:{second:02d}", font=(FONT_NAME, FLOATING_MINUTE_FONT_SIZE, "bold")) #? IS THIS EVEN WORKING??
        floating_timer_label.place(x=MINUTE_X, y=MINUTE_Y)
    # Update the timer display every second
 
    if second == 60:
        second = 0
        minute += 1
    elif minute == 60:
        minute = 0
        hours += 1
        show_hours = True
    if show_hours:
        canvas.itemconfig(timer, text=f"{hours:02d}:{minute:02d}:{second:02d}", font=(FONT_NAME, MAIN_HOUR_FONT_SIZE, "bold"))
        floating_timer_label.config(text=f"{hours:02d}:{minute:02d}:{second:02d}", font=(FONT_NAME, FLOATING_HOUR_FONT_SIZE, "bold"))
        floating_timer_label.place(x=HOURS_X, y=HOURS_Y)
    if start_timer_checker_2:
        second +1
        start_timer_checker_2 = False
    # You can change the speed of countup here
    count_upper = root.after(1000, crono)


# --------------------------- COUNTDOWN MECHANISM ------------------------------- #
def start_timer():
    global start_timer_checker, pause_checker, condition_checker, pomodoro_mode_activate, crono_mode_activate, start_short_break, start_long_break, start_timer_checker_2
    condition_checker = False
    start_timer_checker_2 = True
    if pomodoro_mode_activate:
        start_timer_checker += 1
        pause_checker = 1
        if start_timer_checker == 1:
            global reps
            condition_checker = False
            work_sec = WORK_MIN * 60
            short_break_sec = SHORT_BREAK_MIN * 60
            long_break_sec = LONG_BREAK_MIN * 60
            if reps % 8 == 0:
                BREAK_SOUND.play()
                variable = condition_checker
                condition_checker = False
                start_long_break = True
                pause_timer()
                condition_checker = variable
                timer_label.config(text="Break", fg=PINK)
                canvas.itemconfig(timer, text=f"20:00")
                floating_timer_label.config(text="20:00")
                floating_timer_label.place(x=MINUTE_X, y=MINUTE_Y)
                condition_checker = variable
                check_mark.config(text="✔✔✔✔")
                check_mark.place(x=60, y=290)
                reps = 1
            elif reps % 2 == 1:
                if reps == 1:
                    check_mark.config(text="")
                timer_label.config(text="Work", fg=RED)
                count_down(work_sec)
                reps += 1

            else:
                if reps == 2:
                    check_mark.config(text="✔")
                    check_mark.place(x=90, y=290)
                elif reps == 4:
                    check_mark.config(text="✔✔")
                    check_mark.place(x=80, y=290)
                elif reps == 6:
                    check_mark.config(text="✔✔✔")
                    check_mark.place(x=70, y=290)
                BREAK_SOUND.play()
                variable = condition_checker
                condition_checker = False
                start_short_break = True
                pause_timer()
                condition_checker = variable
                timer_label.config(text="Break", fg=PINK)
                canvas.itemconfig(timer, text=f"05:00")
                floating_timer_label.config(text="05:00")
                floating_timer_label.place(x=MINUTE_X, y=MINUTE_Y)
                reps += 1
    elif crono_mode_activate:
        start_timer_checker += 1
        pause_checker = 1
        condition_checker = False
        if start_timer_checker == 1:
            crono()
    else:
        tkinter.messagebox.showerror("Error", "No mode selected!")


def count_down(count):
    global second, minute, count_downer
    second = count % 60
    minute = math.floor(count / 60)
    second_int = count % 60
    minute_int = math.floor(count / 60)
    canvas.itemconfig(timer, text=f"{minute:02d}:{second:02d}")
    floating_timer_label.config(text=f"{minute:02d}:{second:02d}")
    floating_timer_label.place(x=MINUTE_X, y=MINUTE_Y)

    second = second_int
    minute = minute_int
    if count > 0:
        global count_downer
        # you can change the speed of countdown here
        count_downer = root.after(1000, count_down, count - 1)
    else:
        global start_timer_checker
        start_timer_checker = 0
        start_timer()
#TODO: SOMETIMES, WHEN YOU PAUSE THEN START TIMER SKIPS THE ANOTHER SECOND, FIX IT

def pause_timer():
    global pomodoro_mode_activate, crono_mode_activate, resume, count_downer, count_upper, minute, second, paused,start_short_break, start_long_break,short_break_sec, long_break_sec, condition_checker
    if pomodoro_mode_activate:
        if not condition_checker:
            root.after_cancel(count_downer)
            second_int = second
            minute_int = minute
            paused = True
            resume += 1
            canvas.itemconfig(timer, text=f"{minute:02d}:{second:02d}")
            floating_timer_label.config(text=f"{minute:02d}:{second:02d}", font=(FONT_NAME, FLOATING_MINUTE_FONT_SIZE, "bold"))
            floating_timer_label.place(x=MINUTE_X, y=MINUTE_Y)

            second = second_int
            minute = minute_int
            timer_label.config(text=f"Paused", fg=DEEP_BLUE)
            pause_button.config(text=f"Resume")
            if resume == 2:
                paused = False
                resume = 0
                pause_button.config(text=f"Pause")
                if start_short_break:
                    start_short_break = False
                    count_down(SHORT_BREAK_MIN * 60 + second)
                    timer_label.config(text="Break", fg=PINK)
                    root.after(301000, pause_timer)
                elif start_long_break:
                    start_long_break = False
                    count_down(LONG_BREAK_MIN * 60 + second)
                    timer_label.config(text="Break", fg=PINK)
                    root.after(1201000, pause_timer)
                else:
                    count_down(minute * 60 + second)
                    timer_label.config(text="Work", fg=RED)

    elif crono_mode_activate:
        if not condition_checker:
            root.after_cancel(count_upper)
            timer_label.config(text=f"Paused", fg=DEEP_BLUE) 
            pause_button.config(text=f"Resume")
            second_int = second
            minute_int = minute
            paused = True
            resume += 1
            if show_hours:
                canvas.itemconfig(timer, text=f"{hours:02d}:{minute:02d}:{second:02d}")
                floating_timer_label.config(text=f"{hours:02d}:{minute:02d}:{second:02d}", font=(FONT_NAME, FLOATING_HOUR_FONT_SIZE, "bold"))
                floating_timer_label.place(x=HOURS_X, y=HOURS_Y)
            elif not show_hours:
                canvas.itemconfig(timer, text=f"{minute:02d}:{second:02d}")
                floating_timer_label.config(text=f"{minute:02d}:{second:02d}", font=(FONT_NAME, FLOATING_MINUTE_FONT_SIZE, "bold"))
                floating_timer_label.place(x=MINUTE_X, y=MINUTE_Y)
            else:
                print("Error: There's a problem with the show_hours")
                return
            if resume == 2:
                paused = False
                resume = 0
                timer_label.config(text="WORK", fg=RED)
                pause_button.config(text=f"Pause")
                count_upper = root.after(1000, crono)
    else:
        print("Error: No mode selected")


def save_data():
    global hours, minute, second, crono_mode_activate, show_hours, saved_data, crono_reset, paused, note_writer_first_gap
    if not paused:
        pause_timer()
    if crono_mode_activate:
        crono_reset = False
        with open(TIME_CSV_PATH, mode='a') as file:
            file.write(f"{hours},{minute},{second}\n")

        if show_hours:
            saved_note = askstring('', 'Write your note:')
            if saved_note == "pass" or saved_note == "" or saved_note=="None":
                return
            else: 
                showinfo("Saved!", 'Your note: {}'.format(saved_note))
            saved_data["date"].append(dt.datetime.now().strftime("%Y-%m-%d"))
            saved_data["time"].append(f"{hours:02d}:{minute:02d}:{second:02d}")
            saved_data["notes"].append(saved_note)
        else:
            saved_note = askstring('Save your note', 'Write your note:')
            if saved_note == "pass" or saved_note == "" or saved_note=="None":
                return
            else: 
                showinfo("Saved!", 'Your note: {}'.format(saved_note))
            saved_data["date"].append(dt.datetime.now().strftime("%Y-%m-%d"))
            saved_data["time"].append(f"{minute:02d}:{second:02d}")
            saved_data["notes"].append(saved_note)
        # when pressing the 'Save' button, it saves the data to a CSV file and for not to do overwrite the file:
        try:
            if note_writer_first_gap == 0:
                note_writer_first = ""
            else:
                note_writer_first = "\n"
            note_writer_first_gap = None
            with open(SAVE_FILE_NAME, 'a', encoding='utf-8') as file:
                if not show_hours:
                    file.write(
                        f"{note_writer_first}{dt.datetime.now().strftime("%m/%d/%Y")}\n{minute:02d}:{second:02d} {saved_note}\n")
                else: # ? 'Save your note', 'Write your note: ")'
                    file.write(
                        f"{note_writer_first}{dt.datetime.now().strftime("%m/%d/%Y")}\n{hours:02d}:{minute:02d}:{second:02d} {saved_note}\n")
        except e:
            print(e)
    else:
        tkinter.messagebox.showerror("Error", "You need to be in stopwatch mode to use save button.")
    # save this data to a pixela website
    try:
        if crono_mode_activate:
            connect_to_pixela()
    except requests.exceptions.ConnectionError:
        print("Connection Error: Unable to connect to Pixela.")
        time.sleep(1)
        connect_to_pixela()
    except Exception as e:
        print(f"An error occurred: {e}")
# def toggle():
#     if switch_button.config('text')[-1] == 'DARK':
#         switch_button.config(text='LIGHT', bg=SWITCH_BUTTON_LIGHT_BG_COLOR, fg=SWITCH_BUTTON_LIGHT_FG_COLOR)
#     else:
#         switch_button.config(text='DARK', bg=SWITCH_BUTTON_DARK_BG_COLOR, fg=SWITCH_BUTTON_DARK_FG_COLOR)
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def on_closing():
    with open(TIME_CSV_PATH, mode='a') as file:
        file.write(f"{hours},{minute},{second}\n")
        root.destroy()
# ---------------------------- UI SETUP ------------------------------- #
root = Tk()
root.title("KEGOMODORO")
root.config(padx=100, pady=50, bg=YELLOW)
root.resizable(False, False)
ico = Image.open(APP_ICON_PATH) 
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)
root.geometry("+700+300") #! ADJUSTS THE STARTING LOCATION OF WINDOW
# ---------------------------- FLOATING WINDOW SETUP ------------------------------- #
class DraggableWindow(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Draggable Window")
        # self.geometry("300x300")
        
        # Bind mouse events to the window
        self.bind("<Button-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_drag)
        
        # Load the image and keep a reference to it
        self.image = ImageTk.PhotoImage(Image.open(FLOATING_IMAGE_PATH))
        label = Label(self, image=self.image, bg='white', highlightthickness=0) #! Adjust the frame color of image
        self.overrideredirect(True)
        self.geometry("+250+250")
        self.lift()
        self.wm_attributes("-topmost", True)
        # self.wm_attributes("-disabled", True)
        self.wm_attributes("-transparentcolor", "white")
        label.pack()

        self.start_x = 0
        self.start_y = 0

    def on_press(self, event):
        # Record the start position of the mouse
        self.start_x = event.x_root
        self.start_y = event.y_root

    def on_drag(self, event):
        # Calculate the distance moved
        delta_x = event.x_root - self.start_x
        delta_y = event.y_root - self.start_y
        
        # Move the window
        new_x = self.winfo_x() + delta_x
        new_y = self.winfo_y() + delta_y
        
        self.geometry(f"+{new_x}+{new_y}")
        
        # Update the start position
        self.start_x = event.x_root
        self.start_y = event.y_root

# Create the window
window = DraggableWindow()  # Hide the main window
window.configure(bg='')
window.overrideredirect(True)
window.resizable(False, False)
window.geometry("+1150+440")

floating_timer_label = Label(window, text="00:00", font=(FONT_NAME, FLOATING_MINUTE_FONT_SIZE, "bold"), foreground=WHITE, bg=DEEP_RED)
floating_timer_label.pack()
floating_timer_label.place(x=MINUTE_X, y=MINUTE_Y)

# Kegan Software
logo = Canvas(width=600, height=224, bg=YELLOW, highlightthickness=0)
logo_img = PhotoImage(file=LOGO_IMAGE_PATH)
logo.create_image(300, 112, image=logo_img)
logo.grid(column=1, row=0)
logo.place(x=-300, y=230)

# Tomato
canvas = Canvas(width=200, height=240, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file=MAIN_IMAGE_PATH)
canvas.create_image(100, 120, image=tomato_img) #? IT'S CENTER THE IMAGE
timer = canvas.create_text(100, 130, text="00:00", font=(FONT_NAME, MAIN_MINUTE_FONT_SIZE, "bold"), fill="white")
canvas.grid(column=1, row=1)

# labels
timer_label = Label(text="TIMER", font=(FONT_NAME, 40, "bold"), bg=YELLOW, fg=GREEN)
timer_label.grid(column=1, row=0)

modes_label = Label(text="Modes", font=(FONT_NAME, 20, "bold"), bg=YELLOW, fg=ORANGE)
modes_label.grid(column=1, row=0)
modes_label.place(x=200, y=-50)

check_mark = Label(font=(FONT_NAME, 15, "bold"), bg=YELLOW, fg=GREEN)
check_mark.grid(column=1, row=3)
check_mark.place(x=120, y=300)

# buttons
start_button = Button(text="Start", command=start_timer, highlightthickness=0, 
                      background=BUTTON_BACKGROUND_COLOR, foreground=BUTTON_FOREGROUND_COLOR,
                      activebackground=BUTTON_BACKGROUND_COLOR, activeforeground=BUTTON_FOREGROUND_COLOR)
start_button.grid(column=0, row=2)
start_button.place(x=-30, y=291)

pause_button = Button(text="Pause", command=pause_timer, highlightthickness=0, 
                      background=BUTTON_BACKGROUND_COLOR, foreground=BUTTON_FOREGROUND_COLOR,
                      activebackground=BUTTON_BACKGROUND_COLOR, activeforeground=BUTTON_FOREGROUND_COLOR)
pause_button.grid(column=0, row=2)
pause_button.place(x=4, y=291)

reset_button = Button(text="Reset", highlightthickness=0, command=reset, 
                      background=BUTTON_BACKGROUND_COLOR, foreground=BUTTON_FOREGROUND_COLOR,
                      activebackground=BUTTON_BACKGROUND_COLOR, activeforeground=BUTTON_FOREGROUND_COLOR)
reset_button.grid(column=2, row=2)
reset_button.place(x=175, y=291)

save_button = Button(text="Save", highlightthickness=0, command=save_data, 
                      background=BUTTON_BACKGROUND_COLOR, foreground=BUTTON_FOREGROUND_COLOR,
                      activebackground=BUTTON_BACKGROUND_COLOR, activeforeground=BUTTON_FOREGROUND_COLOR)
save_button.grid(column=2, row=2)
save_button.place(x=213, y=291)

checked_state = IntVar()
checkbutton = Checkbutton(text="SmallWindow", variable=checked_state, command=floating_window, 
                           background=RADIO_BACKGROUND_COLOR, foreground=RADIO_FOREGROUND_COLOR,
                           activebackground=RADIO_BACKGROUND_COLOR, activeforeground=RADIO_FOREGROUND_COLOR)
checkbutton.place(x=200, y=20)

# radio buttons
radio_state = IntVar()
radiobutton1 = Radiobutton(text="Pomodoro", value=1, variable=radio_state, command=pomodoro_mode,
                           highlightthickness=0, 
                           background=RADIO_BACKGROUND_COLOR, foreground=RADIO_FOREGROUND_COLOR,
                           activebackground=RADIO_BACKGROUND_COLOR, activeforeground=RADIO_FOREGROUND_COLOR)
radiobutton2 = Radiobutton(text="Stopwatch", value=2, variable=radio_state, command=crono_mode,
                           highlightthickness=0, 
                           background=RADIO_BACKGROUND_COLOR, foreground=RADIO_FOREGROUND_COLOR,
                           activebackground=RADIO_BACKGROUND_COLOR, activeforeground=RADIO_FOREGROUND_COLOR)
radiobutton1.place(x=200, y=-20) 
radiobutton2.place(x=200, y=-0)

# switch_button = Button(root, text="DARK", bg=SWITCH_BUTTON_DARK_BG_COLOR, fg=SWITCH_BUTTON_DARK_FG_COLOR, width=5, height=1, command=toggle)
# switch_button.place(x=226, y=40)

# Floating timer remebers the mode
window.withdraw()
try:
    with open(FLOATING_WINDOW_CHECKER_PATH, "r") as file:
        floating_window_boolean = file.readline()
        floating_window(check = floating_window_boolean)
except FileNotFoundError as e:
    with open(FLOATING_WINDOW_CHECKER_PATH, "w") as file:
        file.write("")

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()