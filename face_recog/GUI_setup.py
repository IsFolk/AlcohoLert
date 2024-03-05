#!usr/bin/env python3
#Import the required Libraries
from tkinter import *
from tkinter import ttk
import json
import upload_carstatus as uc



#Create an instance of Tkinter frame
win= Tk()

win.title("Alcoholert Interface")

# Simply set the theme
win.tk.call("source", "azure.tcl")
win.tk.call("set_theme", "dark")

#Set the geometry of Tkinter frame
win.update()
win.minsize(win.winfo_width(), win.winfo_height())
x_cordinate = int((win.winfo_screenwidth() / 2) - (win.winfo_width() / 2))
y_cordinate = int((win.winfo_screenheight() / 2) - (win.winfo_height() / 2))
win.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))


def display_text():
   global entry
   index_num= index.get()
   plate_num= plate.get()
   
   data = {"Index":index_num, "Plate_num":plate_num}
   json_data = json.dumps(data, indent=4)
   
   file = open("Index.json", "w")  
   file.write(json_data)
   file.close()
   
   win.destroy()
   
   uc.uploadPlateNum()

#Initialize a Label to display the User Input
label=Label(win, text="Car Index", font=("Arial 22 bold"))
label.pack()

#Create an Entry widget to accept User Input
index= Entry(win, width= 40)
index.focus_set()
#index.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="ew")
index.pack()

label2=Label(win, text="Plate Number", font=("Arial 22 bold"))
label2.pack()

plate= Entry(win, width= 40)
plate.focus_set()
plate.pack()

#Create a Button to validate Entry Widget
ttk.Button(win, text= "Okay",width= 20, command= display_text).pack(pady=20)

win.mainloop()