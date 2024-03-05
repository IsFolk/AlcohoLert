import tkinter as tk
from tkinter import ttk
    
class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)
        
        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)
        
        # Create widgets :)
        self.setup_widgets()
    def setup_widgets(self):
        # Create a Frame for the CarIndex
        self.check_frame = ttk.LabelFrame(self, text="Car Index", padding=(20, 10))
        self.check_frame.grid(
            row=0, column=1, columnspan=2, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )
        
        # Make the app responsive
        for index in [0, 1, 2]:
            self.check_frame.columnconfigure(index=index, weight=1)
            self.check_frame.rowconfigure(index=index, weight=1)
        
        # Entry
        self.entry = ttk.Entry(self.check_frame)
        self.entry.grid(row=1, column=1, padx=10, pady=2, sticky="nsew")

        # Create a Frame for the CarIndex
        self.check_frame2 = ttk.LabelFrame(self, text="Plate Number", padding=(20, 10))
        self.check_frame2.grid(
            row=1, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )
        
        # Make the app responsive
        for index in [0, 1, 2]:
            self.check_frame2.columnconfigure(index=index, weight=1)
            self.check_frame2.rowconfigure(index=index, weight=1)
        
        # Entry
        self.entry = ttk.Entry(self.check_frame2)
        self.entry.grid(row=1, column=1, padx=10, pady=2, sticky="nsew")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("")
    

    root.geometry("500x500")
    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    root.mainloop()
