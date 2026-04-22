import tkinter as tk
from gui.tenant_page import TenantPage
from gui.apartment_page import ApartmentPage
from gui.payment_page import PaymentPage
from gui.maintenance_page import MaintenancePage
from gui.report_page import ReportPage
from PIL import Image, ImageTk
from database.db_connection import get_connection


NAVY = "#1E2A38"
BLUE = "#2F5D8C"
LIGHT_BG = "#F4F6F8"
WHITE = "#FFFFFF"
TEXT = "#222222"
SUBTEXT = "#6B7280"

ROLE_LABELS = {
    "front_desk": "Front Desk Staff",
    "finance_manager": "Finance Manager",
    "maintenance_staff": "Maintenance Staff",
    "administrator": "Administrator",
    "manager": "Manager"
}

LOCATION_LABELS = {
    "bristol": "Bristol",
    "cardiff": "Cardiff",
    "manchester": "Manchester",
    "london": "London",

}

ROLE_ACCESS = {
    "front_desk": ["dashboard", "tenant", "maintenance"],
    "finance_manager": ["dashboard", "payment", "report"],
    "maintenance_staff": ["dashboard", "maintenance"],
    "administrator": ["dashboard", "tenant", "apartment", "payment", "maintenance", "report"],
    "manager": ["dashboard", "report"]
}


class DashboardPage(tk.Frame):

    def get_stats(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM tenants")
        total_tenants = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM apartments WHERE occupancy_status = 'Occupied'")
        occupied = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM payments WHERE status = 'Pending'")
        pending_payments = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM maintenance_requests WHERE status NOT IN ('Resolved', 'Cancelled')")
        open_requests = cursor.fetchone()[0]
        
        conn.close()
        return total_tenants, occupied, pending_payments, open_requests

    def __init__(self, parent, user):
        super().__init__(parent, bg=LIGHT_BG)
        self.parent = parent
        self.current_page = None
        self.user = user
        self.role = user.get("role", "front_desk")
        self.role_display = ROLE_LABELS.get(self.role, "Front Desk Staff")
        self.location = user.get("location", "Bristol")
        self.location_display = self.location
        self.allowed_pages = ROLE_ACCESS.get(self.role, ["dashboard"])
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
            text=f"Role: {self.role_display}",
            bg=NAVY,
            fg="white",
            font=("Arial", 11)
        )
        role_label.pack(side="right", padx=20)

        #location label
        location_label = tk.Label(
            self.topbar,
            text=f"Location: {self.location_display}",
            bg=NAVY,
            fg="white",
            font=("Arial", 11)
        )
        location_label.pack(side="bottom", padx=20)

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
        if "dashboard" in self.allowed_pages:
            self.add_nav_button("Dashboard", lambda: self.show_page("dashboard"))

        if "tenant" in self.allowed_pages:
            self.add_nav_button("Tenants", lambda: self.show_page("tenant"))

        if "apartment" in self.allowed_pages:
            self.add_nav_button("Apartments", lambda: self.show_page("apartment"))

        if "payment" in self.allowed_pages:
            self.add_nav_button("Payments", lambda: self.show_page("payment"))

        if "maintenance" in self.allowed_pages:
            self.add_nav_button("Maintenance", lambda: self.show_page("maintenance"))

        if "report" in self.allowed_pages:
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
        logout_label.bind("<Enter>", lambda event: logout_label.config(bg=BLUE))
        logout_label.bind("<Leave>", lambda event: logout_label.config(bg=NAVY))
        logout_label.bind("<Button-1>", lambda event: self.logout())

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
            self.sidebar.pack(side="left", fill="y", before=self.content_frame)
            self.sidebar.config(width=240)
            self.sidebar.pack_propagate(False)
            self.sidebar_visible = True

    def logout(self):
        from gui.login_page import LoginPage
        self.destroy()
        login_page = LoginPage(self.parent)
        login_page.pack(fill="both", expand=True)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_page(self, page_name):
        if page_name not in self.allowed_pages:
            self.show_unauthorized(page_name)
            return

        self.clear_content()

        if page_name == "dashboard":
            self.show_dashboard_home()
        elif page_name == "tenant":
            page = TenantPage(self.content_frame, self.user)
            page.pack(fill="both", expand=True, padx=20, pady=20)
        elif page_name == "apartment":
            page = ApartmentPage(self.content_frame, self.user)
            page.pack(fill="both", expand=True, padx=20, pady=20)
        elif page_name == "payment":
            page = PaymentPage(self.content_frame, self.user)
            page.pack(fill="both", expand=True, padx=20, pady=20)
        elif page_name == "maintenance":
            page = MaintenancePage(self.content_frame)
            page.pack(fill="both", expand=True, padx=20, pady=20)
        elif page_name == "report":
            page = ReportPage(self.content_frame, self.user)
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
        total_tenants, occupied, pending_payments, open_requests = self.get_stats()

        self.create_card(cards_frame, "Total Tenants", str(total_tenants))
        self.create_card(cards_frame, "Occupied Apartments", str(occupied))
        self.create_card(cards_frame, "Pending Payments", str(pending_payments))
        self.create_card(cards_frame, "Open Requests", str(open_requests))

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

    def show_placeholder(self, title_text, message):
        #page title
        title = tk.Label(
            self.content_frame,
            text=title_text,
            bg=LIGHT_BG,
            fg=TEXT,
            font=("Arial", 22, "bold")
        )
        title.pack(anchor="nw", padx=20, pady=(20, 10))

        #placeholder box
        box = tk.Frame(
            self.content_frame,
            bg=WHITE,
            highlightbackground="#E0E0E0",
            highlightthickness=1
        )
        box.pack(fill="both", expand=True, padx=20, pady=20)

        #placeholder text
        msg = tk.Label(
            box,
            text=message,
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 12)
        )
        msg.pack(pady=40)

    def show_unauthorized(self, page_name):
        self.clear_content()

        #page title
        title = tk.Label(
            self.content_frame,
            text="Access Denied",
            bg=LIGHT_BG,
            fg=TEXT,
            font=("Arial", 22, "bold")
        )
        title.pack(anchor="nw", padx=20, pady=(20, 10))

        #message box
        box = tk.Frame(
            self.content_frame,
            bg=WHITE,
            highlightbackground="#E0E0E0",
            highlightthickness=1
        )
        box.pack(fill="both", expand=True, padx=20, pady=20)

        msg = tk.Label(
            box,
            text=f"You do not have permission to access: {page_name}",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 12)
        )
        msg.pack(pady=40)