import tkinter as tk
from gui.login_page import LoginPage

def main():
    print("App starting...")
    #create the main application window
    root = tk.Tk()

    #set window title and size
    root.title("Paragon Apartment Management System")
    root.state("zoomed")

    #disable resizing for now to keep layout consistent
    root.resizable(False, False)

    #load the login page as the first screen
    app = LoginPage(root)
    app.pack(fill="both", expand=True)

    #start the tkinter event loop
    root.mainloop()

#Python entry point
if __name__ == "__main__":
    main()