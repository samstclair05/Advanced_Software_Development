##by Htet Oo Wai - 24037079,  Samuel St Clair - 24022864
import tkinter as tk
from gui.dashboard_page import DashboardPage
from models.user import get_user

# color theme
NAVY = "#1E2A38"
BLUE = "#2F5D8C"
LIGHT_BG = "#F4F6F8"
WHITE = "#FFFFFF"
TEXT = "#222222"


class LoginPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=LIGHT_BG)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        # centered box to hold login form
        login_box = tk.Frame(self, bg=WHITE, bd=1, relief="solid")
        login_box.place(relx=0.5, rely=0.5, anchor="center", width=400, height=340)

        # page title
        title = tk.Label(
            login_box,
            text="PAMS Login",
            bg=WHITE,
            fg=NAVY,
            font=("Arial", 22, "bold")
        )
        title.pack(pady=(30, 20))

        # username input
        username_label = tk.Label(login_box, text="Username", bg=WHITE, fg=TEXT)
        username_label.pack(anchor="w", padx=40)

        self.username_entry = tk.Entry(login_box, width=30)
        self.username_entry.pack(pady=(5, 15))

        # password input
        password_label = tk.Label(login_box, text="Password", bg=WHITE, fg=TEXT)
        password_label.pack(anchor="w", padx=40)

        self.password_entry = tk.Entry(login_box, width=30, show="*")
        self.password_entry.pack(pady=(5, 10))

        # error message label
        self.error_label = tk.Label(login_box, text="", bg=WHITE, fg="red", font=("Arial", 10))
        self.error_label.pack()

        # login button
        login_button = tk.Button(
            login_box,
            text="Login",
            command=self.handle_login,
            bg=BLUE,
            fg="white",
            width=15
        )
        login_button.pack(pady=10)

        # allow pressing Enter to login
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
        self.username_entry.bind("<Return>", lambda e: self.handle_login())

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            self.error_label.config(text="Please enter both username and password.")
            return

        user = get_user(username)

        if user and user["password"] == password:
            self.go_to_dashboard(user)
        else:
            self.error_label.config(text="Invalid username or password.")
            self.password_entry.delete(0, tk.END)

    def go_to_dashboard(self, user):
        self.destroy()
        dashboard = DashboardPage(self.parent, user)
        dashboard.pack(fill="both", expand=True)