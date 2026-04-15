import tkinter as tk
from gui.dashboard_page import DashboardPage

#color theme
NAVY = "#1E2A38"
BLUE = "#2F5D8C"
LIGHT_BG = "#F4F6F8"
WHITE = "#FFFFFF"
TEXT = "#222222"

class LoginPage(tk.Frame):
    def __init__(self, parent):
        #inherit Tk frame to be placed inside the main window
        super().__init__(parent, bg=LIGHT_BG)
        self.parent = parent

        #Build UI
        self.create_widgets()

    def create_widgets(self):
        # a centered box to hold login form
        login_box = tk.Frame(self, bg=WHITE, bd=1, relief="solid")
        login_box.place(relx=0.5, rely=0.5, anchor="center", width=400, height=320)

        #page title
        title = tk.Label(
            login_box,
            text="PAMS Login",
            bg=WHITE,
            fg=NAVY,
            font=("Arial", 22, "bold")
        )
        title.pack(pady=(30,20))

        #username input
        username_label = tk.Label(login_box, text="Username", bg=WHITE, fg=TEXT)
        username_label.pack(anchor="w", padx=40)

        self.password_entry = tk.Entry(login_box, width=30, show="*")
        self.password_entry.pack(pady=(5, 20))

        #login button
        login_button = tk.Button(
            login_box,
            text="Login",
            bg=BLUE,
            fg="white",
            width=15,
            command=self.go_to_dashboard
        )
        login_button.pack(pady=10)

    def go_to_dashboard(self):
        #for now, skip validation to go to dashboard
        #add authentication later

        #remove login screen
        self.destroy()

        #load dashboard page
        dashboard = DashboardPage(self.parent)
        dashboard.pack(fill="both", expand=True)