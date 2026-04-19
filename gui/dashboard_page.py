import tkinter as tk
from gui.tenant_page import TenantPage
from gui.apartment_page import ApartmentPage
from gui.payment_page import PaymentPage
from gui.maintenance_page import MaintenancePage
from gui.report_page import ReportPage
from PIL import Image, ImageTk


NAVY = "#1E2A38"
BLUE = "#2F5D8C"
LIGHT_BG = "#F4F6F8"
WHITE = "#FFFFFF"
TEXT = "#222222"
SUBTEXT = "#6B7280"


class DashboardPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=LIGHT_BG)
        self.parent = parent
        self.current_page = None
        self.role = "Front Desk Staff"
        self.sidebar_visible = True

        self.create_layout()
        self.show_page("dashboard")

    def create_layout(self):
        #top bar
        self.topbar = tk.Frame(self, bg=NAVY, height=60)
        self.topbar.pack(side="top", fill="x")
        self.topbar.pack_propagate(False)

        #menu button
        menu_btn = tk.Label(
            self.topbar,
            text="☰",
            bg=NAVY,
            fg="white",
            font=("Arial", 18, "bold"),
            cursor="hand2"
        )
        menu_btn.pack(side="left", padx=10)
        menu_btn.bind("<Button-1>", lambda e: self.toggle_sidebar())

        #system title
        title_label = tk.Label(
            self.topbar,
            text="Paragon Apartment Management System",
            bg=NAVY,
            fg="white",
            font=("Arial", 18, "bold")
        )
        title_label.pack(side="left", padx=20)

        #role label
        role_label = tk.Label(
            self.topbar,
            text=f"Role: {self.role}",
            bg=NAVY,
            fg="white",
            font=("Arial", 11)
        )
        role_label.pack(side="right", padx=20)

        #main area
        self.main_area = tk.Frame(self, bg=LIGHT_BG)
        self.main_area.pack(fill="both", expand=True)

        #sidebar
        self.sidebar = tk.Frame(
            self.main_area,
            bg=NAVY,
            width=240,
            highlightbackground="#2A3A4A",
            highlightthickness=1
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        #content area
        self.content_frame = tk.Frame(self.main_area, bg=LIGHT_BG)
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.create_sidebar_buttons()

    def create_sidebar_buttons(self):
        #heading
        heading = tk.Label(
            self.sidebar,
            text="Navigation",
            bg=NAVY,
            fg="white",
            font=("Arial", 16, "bold")
        )
        heading.pack(anchor="w", padx=25, pady=(20, 25))

        #nav items
        self.add_nav_button("Dashboard", lambda: self.show_page("dashboard"))
        self.add_nav_button("Tenants", lambda: self.show_page("tenant"))
        self.add_nav_button("Apartments", lambda: self.show_page("apartment"))
        self.add_nav_button("Payments", lambda: self.show_page("payment"))
        self.add_nav_button("Maintenance", lambda: self.show_page("maintenance"))
        self.add_nav_button("Reports", lambda: self.show_page("report"))

        #logout
        logout_label = tk.Label(
            self.sidebar,
            text="Logout",
            bg=NAVY,
            fg="white",
            font=("Arial", 13, "bold"),
            anchor="w",
            padx=25,
            pady=10,
            cursor="hand2"
        )
        logout_label.pack(side="bottom", fill="x", pady=20)

    def add_nav_button(self, text, command):
        nav_label = tk.Label(
            self.sidebar,
            text=text,
            bg=NAVY,
            fg="white",
            font=("Arial", 13, "bold"),
            anchor="w",
            padx=25,
            pady=10,
            cursor="hand2"
        )
        nav_label.pack(fill="x", pady=6)

        #click to open page
        nav_label.bind("<Button-1>", lambda event: command())

        #hover effect
        nav_label.bind("<Enter>", lambda event: nav_label.config(bg=BLUE))
        nav_label.bind("<Leave>", lambda event: nav_label.config(bg=NAVY))

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.pack_forget()
            self.sidebar_visible = False
        else:
            self.sidebar.pack(side="left", fill="y")
            self.sidebar_visible = True

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_page(self, page_name):
        self.clear_content()

        if page_name == "dashboard":
            self.show_dashboard_home()
        elif page_name == "tenant":
            page = TenantPage(self.content_frame)
            page.pack(fill="both", expand=True, padx=20, pady=20)
        elif page_name == "apartment":
            page = ApartmentPage(self.content_frame)
            page.pack(fill="both", expand=True, padx=20, pady=20)
        elif page_name == "payment":
            page = PaymentPage(self.content_frame)
            page.pack(fill="both", expand=True, padx=20, pady=20)
        elif page_name == "maintenance":
            page = MaintenancePage(self.content_frame)
            page.pack(fill="both", expand=True, padx=20, pady=20)
        elif page_name == "report":
            page = ReportPage(self.content_frame)
            page.pack(fill="both", expand=True, padx=20, pady=20)

    def show_dashboard_home(self):
        #hero image section
        img = Image.open("assets/apartment.jpg")
        img = img.resize((1100, 220))

        photo = ImageTk.PhotoImage(img)

        img_label = tk.Label(self.content_frame, image=photo, bg=LIGHT_BG)
        img_label.image = photo
        img_label.pack(fill="x", padx=20, pady=(20, 15))

        #page title
        title = tk.Label(
            self.content_frame,
            text="Dashboard",
            bg=LIGHT_BG,
            fg=TEXT,
            font=("Arial", 24, "bold")
        )
        title.pack(anchor="nw", padx=25, pady=(10, 5))

        #page subtitle
        subtitle = tk.Label(
            self.content_frame,
            text="Welcome to the Paragon Apartment Management System",
            bg=LIGHT_BG,
            fg=SUBTEXT,
            font=("Arial", 12)
        )
        subtitle.pack(anchor="nw", padx=25, pady=(0, 15))

        #stats
        cards_frame = tk.Frame(self.content_frame, bg=LIGHT_BG)
        cards_frame.pack(pady=20)

        self.create_card(cards_frame, "Total Tenants", "128")
        self.create_card(cards_frame, "Occupied Apartments", "94")
        self.create_card(cards_frame, "Pending Payments", "12")
        self.create_card(cards_frame, "Open Requests", "8")

    def create_card(self, parent, title, value):
        #card box
        card = tk.Frame(
            parent,
            bg=WHITE,
            width=200,
            height=120,
            highlightbackground="#E0E0E0",
            highlightthickness=1
        )
        card.pack(side="left", padx=12, pady=5)
        card.pack_propagate(False)

        #card title
        title_label = tk.Label(
            card,
            text=title,
            bg=WHITE,
            fg=SUBTEXT,
            font=("Arial", 11)
        )
        title_label.pack(anchor="w", padx=15, pady=(20, 5))

        #card value
        value_label = tk.Label(
            card,
            text=value,
            bg=WHITE,
            fg=BLUE,
            font=("Arial", 22, "bold")
        )
        value_label.pack(anchor="w", padx=15)