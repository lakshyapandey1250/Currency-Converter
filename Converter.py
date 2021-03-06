# ----- Imports -----
from openexchangerate import OpenExchangeRates
from tkinter import messagebox
from tkinter import *
import subprocess as sp
import json
import time

# ----- Global Variables -----
height = 600
width = 600
background_color = "#00FFFF"
latest = None
names = None

# Get Your API Key From openexchangerates.org
# pip install openexchangerates

# ----- Functions -----    
def helper():
    """Shows The Help Box For Instructions"""
    messagebox.showinfo("Help Text", "Welcome To The Currency Converter. Please Enter The 3 Letter Currency Codes Or The Full Name Of Currencies And Enter The Amount. To View Currency Codes, Click On The View Codes Button.")

def get_rates():
    """Getting And Formatting The Currency Rates"""
    global latest, names
    client = OpenExchangeRates(api_key="api_key")
    latest = str(client.latest())
    names = str(client.currencies())
    latest = latest.split(", frozendict", 1)[0]
    names = names.split(", frozendict", 1)[0]
    latest = latest.split("=", 1)[1]
    names = names.split("=", 1)[1]
    latest = latest.replace("'", '"')
    names = names.replace("'", '"')
    names = names.replace('Tongan Pa"anga', "Tongan Pa'anga")
    latest = dict(json.loads(latest))
    names = dict(json.loads(names))

def convert(input1, input2, amount):
    """Converting The Currencies"""
    if input1 == "" or input2 == "" or amount == "":
        messagebox.showerror("Empty Fields", "One Or More Fields Are Empty. Please Fill All Fields.")
    if amount.isnumeric() == False or int(amount) <= 0:
        messagebox.showerror("Wrong Input", "You Have Entered Negative Input. Please Enter Positive Input.")
    else:
        try:
            isfull1 = True
            isfull2 = True
            short1 = None
            short2 = None
            if len(input1) == 3:
                input1 = input1.upper()
                isfull1 = False
                num1 = latest[input1]
                short1 = input1
            if len(input2) == 3:
                input2 = input2.upper()
                isfull2 = False
                num2 = latest[input2]
                short2 = input2
            if isfull1:
                if input1.count(" ") > 0:
                    input1 = input1.split(" ")
                    for item in input1:
                        item.capitalize()
                    input1 = " ".join(input1)
                    for key, value in names.items():
                        if value == input1:
                            num1 = latest[key]
                            short1 = key
                else:
                    input1 = input1.capitalize()
                    for key, value in names.items():
                        if value == input1:
                            num1 = latest[key]
                            short1 = key
            if isfull2:
                if input2.count(" ") > 0:
                    input2 = input2.split(" ")
                    for item in input2:
                        item.capitalize()
                    input2 = " ".join(input2)
                    for key, value in names.items():
                        if value == input2:
                            num2 = latest[key]
                            short2 = key                    
                else:
                    input2 = input2.capitalize()
                    for key, value in names.items():
                        if value == input2:
                            num2 = latest[key]
                            short2 = key
            am = num2 / num1
            final = int(amount) * am
            final_text = str(str(amount)+" "+names[short1]+" Are \n"+str(final)+" "+names[short2]+" ")
            label2["text"] = final_text            
        except Exception as e: 
            messagebox.showerror("Wrong Codes", "You Have Entered Wrong Currency Codes Or Names. Please Check The Codes And Names From The Help File And Try Again.")
    
# ----- Main Code -----

# Initializing The Main Tkinter Window
root = Tk()
root.title("Currency Converter")
root.geometry(f"{width}x{height}")

# Initializing And Setting The Images
logo_image = PhotoImage(file="Logo.png")
root.iconphoto(False, logo_image)
background_image = PhotoImage(file="Background.png")
background_label = Label(root, image=background_image)
background_label.place(relheight=1, relwidth=1)
root.iconbitmap("Icon.ico")

# Creating The Main Window
frame1 = Frame(root, bg="white")
frame1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

label = Label(frame1, text="Currency Converter", font=("Times New Roman", 20), fg="Black", bg="White")
label.place(relwidth=0.5, relheight=0.08, relx=0.26, rely=0.055)

info1 = Button(frame1, relief=RIDGE, text="i", font=("Times New Roman", 20), fg="Black", bg="White", bd=5, command=helper, cursor="hand2")
info1.place(relwidth=0.1, relheight=0.08, relx=0.85, rely=0.05)

froml = Label(frame1, text="From:", font=("Times New Roman", 20), fg="Black", bg="White")
froml.place(relx=0.1, rely=0.2, relwidth=0.2, relheight=0.1)

entry1 = Entry(frame1, relief=RIDGE, bg="White", bd=7, font=("Times New Roman", 20), fg="Black")
entry1.place(relx=0.3, rely=0.2, relwidth=0.6, relheight=0.1)

from2 = Label(frame1, text="To:", font=("Times New Roman", 20), fg="Black", bg="White")
from2.place(relx=0.1, rely=0.375, relwidth=0.2, relheight=0.1)

entry2 = Entry(frame1, relief=RIDGE, bg="White", bd=7, font=("Times New Roman", 20), fg="Black")
entry2.place(relx=0.3, rely=0.375, relwidth=0.6, relheight=0.1)

from3 = Label(frame1, text="Amount:", font=("Times New Roman", 20), fg="Black", bg="White")
from3.place(relx=0.08, rely=0.55, relwidth=0.2, relheight=0.1)

entry3 = Entry(frame1, relief=RIDGE, bg="White", bd=7, font=("Times New Roman", 20), fg="Black")
entry3.place(relx=0.3, rely=0.55, relwidth=0.6, relheight=0.1)

button1 = Button(frame1, relief=RIDGE, text="Convert", font=("Times New Roman", 20), bd=7, bg="White", fg="Black", command=lambda:convert(entry1.get(), entry2.get(), entry3.get()), cursor="hand2")
button1.place(relx=0.1, rely=0.7, relwidth=0.35, relheight=0.1)

button2 = Button(frame1, relief=RIDGE, text="View Codes", font=("Times New Roman", 20), bd=7, bg="White", fg="Black", command=lambda:sp.Popen(["notepad.exe", "Codes.txt"]), cursor="hand2")
button2.place(relx=0.55, rely=0.7, relwidth=0.35, relheight=0.1)

label2 = Label(frame1, font=("Times New Roman", 20), fg="Black", bg="white")
label2.place(relx=0.05, rely=0.8, relwidth=0.9, relheight=0.2)    

# ----- Driver Code -----
if __name__ == "__main__":
    get_rates()
    root.mainloop()
