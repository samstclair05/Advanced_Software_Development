#by Htet Oo Wai - 24037079
import tkinter as tk
from tkinter import ttk, messagebox
from services.apartment_services import (
    service_get_all_apartments,
    service_add_apartment,
    service_update_apartment,
    service_delete_apartment,
    service_get_current_tenant,
    service_terminate_current_lease_for_apartment
)

LIGHT_BG = "#F4F6F8"
WHITE = "#FFFFFF"
TEXT = "#222222"
SUBTEXT = "#6B7280"
LIGHT_BUTTON = "#E5E7EB"
LIGHT_BUTTON_HOVER = "#D1D5DB"


class ApartmentPage(tk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent, bg=LIGHT_BG)
        self.current_user = user
        self.selected_apartment_id = None
        self.all_apartments = []
        self.user_location = self.current_user.get("location", "Bristol")

        self.setup_scrollable_area()
        self.create_widgets()
        self.load_records()

    def setup_scrollable_area(self):
        self.canvas = tk.Canvas(self, bg=LIGHT_BG, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=LIGHT_BG)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def enforce_location_lock(self, *args):
        if self.current_user.get("role") != "administrator":
            if self.location_var.get() != self.user_location:
                self.location_var.set(self.user_location)

    def sync_rooms(self, *args):
        mapping = {
            "Studio": 1,
            "1 Bedroom": 1,
            "2 Bedroom": 2,
            "3 Bedroom": 3
        }
        self.rooms_entry.config(state="normal")
        self.rooms_entry.delete(0, tk.END)
        self.rooms_entry.insert(0, mapping.get(self.type_var.get(), 1))
        self.rooms_entry.config(state="readonly")

    def suggest_rent(self, *args):
        base_prices = {
            "Studio": 700,
            "1 Bedroom": 900,
            "2 Bedroom": 1200,
            "3 Bedroom": 1600
        }

        location_multiplier = {
            "Bristol": 1.0,
            "Manchester": 0.9,
            "Cardiff": 0.85,
            "London": 1.6
        }

        apt_type = self.type_var.get()
        location = self.location_var.get()

        base = base_prices.get(apt_type, 800)
        multiplier = location_multiplier.get(location, 1.0)

        suggested = round(base * multiplier, 2)

        if not self.rent_entry.get().strip():
            self.rent_entry.insert(0, str(suggested))

    def create_widgets(self):
        container = self.scrollable_frame

        #page title
        title = tk.Label(
            container,
            text="Apartment Management",
            bg=LIGHT_BG,
            fg=TEXT,
            font=("Arial", 24, "bold")
        )
        title.pack(anchor="nw", padx=25, pady=(20, 5))

        #page subtitle
        subtitle = tk.Label(
            container,
            text="Add, update and manage apartment records",
            bg=LIGHT_BG,
            fg=SUBTEXT,
            font=("Arial", 12)
        )
        subtitle.pack(anchor="nw", padx=25, pady=(0, 15))

        #filter box
        filter_box = tk.Frame(container, bg=LIGHT_BG)
        filter_box.pack(anchor="w", padx=25, pady=(0, 10))

        tk.Label(
            filter_box,
            text="Filter by Status",
            bg=LIGHT_BG,
            fg=TEXT,
            font=("Arial", 11)
        ).pack(side="left", padx=(0, 10))

        self.filter_status_var = tk.StringVar(value="All")
        filter_menu = tk.OptionMenu(
            filter_box,
            self.filter_status_var,
            "All",
            "Vacant",
            "Occupied",
            "Reserved",
            "Under Maintenance",
            "Inactive",
            command=lambda _: self.apply_filter()
        )
        filter_menu.config(width=18, bg=WHITE, fg=TEXT, relief="solid", bd=1, highlightthickness=0)
        filter_menu.pack(side="left")

        #form box
        form_box = tk.Frame(
            container,
            bg=WHITE,
            highlightbackground="#E0E0E0",
            highlightthickness=1
        )
        form_box.pack(fill="x", padx=25, pady=10)

        form_box.grid_columnconfigure(0, weight=1)
        form_box.grid_columnconfigure(1, weight=1)
        form_box.grid_columnconfigure(2, weight=1)
        form_box.grid_columnconfigure(3, weight=1)

        #row 1
        tk.Label(form_box, text="Apartment ID", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=0, column=0, padx=15, pady=12, sticky="w")
        self.apartment_id_entry = tk.Entry(form_box, width=25, bg="#F3F4F6", fg=TEXT, relief="solid", bd=1)
        self.apartment_id_entry.config(state="readonly")
        self.apartment_id_entry.grid(row=0, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Location", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=0, column=2, padx=15, pady=12, sticky="w")
        self.location_var = tk.StringVar(value=self.user_location)
        self.location_menu = tk.OptionMenu(
            form_box,
            self.location_var,
            "Bristol",
            "Manchester",
            "Cardiff",
            "London"
        )
        self.location_menu.config(width=22, bg=WHITE, fg=TEXT, relief="solid", bd=1, highlightthickness=0)
        self.location_menu.grid(row=0, column=3, padx=15, pady=12, sticky="w")
        self.location_var.trace_add("write", self.enforce_location_lock)
        self.location_var.trace_add("write", self.suggest_rent)

        #row 2
        tk.Label(form_box, text="Apartment Type", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=1, column=0, padx=15, pady=12, sticky="w")
        self.type_var = tk.StringVar(value="Studio")
        type_menu = tk.OptionMenu(
            form_box,
            self.type_var,
            "Studio",
            "1 Bedroom",
            "2 Bedroom",
            "3 Bedroom"
        )
        type_menu.config(width=22, bg=WHITE, fg=TEXT, relief="solid", bd=1, highlightthickness=0)
        type_menu.grid(row=1, column=1, padx=15, pady=12, sticky="w")
        self.type_var.trace_add("write", self.sync_rooms)
        self.type_var.trace_add("write", self.suggest_rent)

        tk.Label(form_box, text="Monthly Rent", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=1, column=2, padx=15, pady=12, sticky="w")
        self.rent_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.rent_entry.grid(row=1, column=3, padx=15, pady=12)

        #row 3
        tk.Label(form_box, text="Number of Rooms", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=2, column=0, padx=15, pady=12, sticky="w")
        self.rooms_entry = tk.Entry(form_box, width=25, bg="#F3F4F6", fg=TEXT, relief="solid", bd=1)
        self.rooms_entry.grid(row=2, column=1, padx=15, pady=12)
        self.sync_rooms()

        tk.Label(form_box, text="Occupancy Status", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=2, column=2, padx=15, pady=12, sticky="w")
        self.status_var = tk.StringVar(value="Vacant")
        status_menu = tk.OptionMenu(
            form_box,
            self.status_var,
            "Vacant",
            "Occupied",
            "Reserved",
            "Under Maintenance",
            "Inactive"
        )
        status_menu.config(width=22, bg=WHITE, fg=TEXT, relief="solid", bd=1, highlightthickness=0)
        status_menu.grid(row=2, column=3, padx=15, pady=12, sticky="w")

        #row 4
        tk.Label(form_box, text="Floor Number", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=3, column=0, padx=15, pady=12, sticky="w")
        self.floor_var = tk.StringVar(value="1")
        floor_menu = tk.OptionMenu(
            form_box,
            self.floor_var,
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"
        )
        floor_menu.config(
            width=22,
            bg=WHITE,
            fg=TEXT,
            relief="solid",
            bd=1,
            highlightthickness=0
        )
        floor_menu.grid(row=3, column=1, padx=15, pady=12, sticky="w")

        tk.Label(form_box, text="Notes", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=3, column=2, padx=15, pady=12, sticky="w")
        self.notes_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.notes_entry.grid(row=3, column=3, padx=15, pady=12)

        #button area
        button_frame = tk.Frame(container, bg=LIGHT_BG)
        button_frame.pack(anchor="w", padx=25, pady=12)

        tk.Button(
            button_frame,
            text="Add Apartment",
            command=self.handle_add,
            bg=LIGHT_BUTTON,
            fg=TEXT,
            activebackground=LIGHT_BUTTON_HOVER,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            width=15,
            height=2,
            font=("Arial", 11, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=6)

        tk.Button(
            button_frame,
            text="Update",
            command=self.handle_update,
            bg=LIGHT_BUTTON,
            fg=TEXT,
            activebackground=LIGHT_BUTTON_HOVER,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            width=15,
            height=2,
            font=("Arial", 11, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=6)

        tk.Button(
            button_frame,
            text="Delete",
            command=self.handle_delete,
            bg=LIGHT_BUTTON,
            fg=TEXT,
            activebackground=LIGHT_BUTTON_HOVER,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            width=15,
            height=2,
            font=("Arial", 11, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=6)

        tk.Button(
            button_frame,
            text="Terminate Lease",
            command=self.handle_terminate_lease,
            bg=LIGHT_BUTTON,
            fg=TEXT,
            activebackground=LIGHT_BUTTON_HOVER,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            width=15,
            height=2,
            font=("Arial", 11, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=6)

        tk.Button(
            button_frame,
            text="Clear",
            command=self.handle_clear,
            bg=LIGHT_BUTTON,
            fg=TEXT,
            activebackground=LIGHT_BUTTON_HOVER,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            width=15,
            height=2,
            font=("Arial", 11, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=6)

        #current tenant box
        tenant_box = tk.Frame(
            container,
            bg=WHITE,
            highlightbackground="#E0E0E0",
            highlightthickness=1
        )
        tenant_box.pack(fill="x", padx=25, pady=10)

        tenant_title = tk.Label(
            tenant_box,
            text="Current Tenant",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 14, "bold")
        )
        tenant_title.pack(anchor="w", padx=15, pady=(15, 10))

        self.current_tenant_label = tk.Label(
            tenant_box,
            text="No apartment selected",
            bg=WHITE,
            fg=SUBTEXT,
            font=("Arial", 11)
        )
        self.current_tenant_label.pack(anchor="w", padx=15, pady=(0, 15))

        #records box
        records_box = tk.Frame(
            container,
            bg=WHITE,
            highlightbackground="#E0E0E0",
            highlightthickness=1
        )
        records_box.pack(fill="both", expand=True, padx=25, pady=10)

        records_title = tk.Label(
            records_box,
            text="Apartment Records",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 14, "bold")
        )
        records_title.pack(anchor="w", padx=15, pady=(15, 10))

        #records table
        columns = ("id", "location", "type", "rooms", "floor", "rent", "status")
        self.tree = ttk.Treeview(records_box, columns=columns, show="headings", selectmode="browse", height=8)

        self.tree.heading("id", text="ID")
        self.tree.heading("location", text="Location")
        self.tree.heading("type", text="Type")
        self.tree.heading("rooms", text="Rooms")
        self.tree.heading("floor", text="Floor")
        self.tree.heading("rent", text="Monthly Rent")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("location", width=150)
        self.tree.column("type", width=110)
        self.tree.column("rooms", width=70, anchor="center")
        self.tree.column("floor", width=70, anchor="center")
        self.tree.column("rent", width=120, anchor="center")
        self.tree.column("status", width=130, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        self.suggest_rent()

    def apply_filter(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        filter_value = self.filter_status_var.get()

        for a in self.all_apartments:
            if filter_value == "All" or a["occupancy_status"] == filter_value:
                self.tree.insert("", "end", values=(
                    a["apartment_id"],
                    a["location"],
                    a["apartment_type"],
                    a["num_rooms"],
                    a["floor_number"],
                    f"£{a['monthly_rent']:.2f}",
                    a["occupancy_status"]
                ))

    def load_records(self):
        response = service_get_all_apartments(self.current_user)

        if not response["success"]:
            messagebox.showerror("Error", response["error"])
            return

        self.all_apartments = response["data"]
        self.apply_filter()

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected, "values")
        self.handle_clear()

        self.selected_apartment_id = values[0]

        self.apartment_id_entry.config(state="normal")
        self.apartment_id_entry.delete(0, tk.END)
        self.apartment_id_entry.insert(0, values[0])
        self.apartment_id_entry.config(state="readonly")

        self.location_var.set(values[1])
        self.type_var.set(values[2])

        self.rooms_entry.config(state="normal")
        self.rooms_entry.delete(0, tk.END)
        self.rooms_entry.insert(0, values[3])
        self.rooms_entry.config(state="readonly")

        self.floor_var.set(str(values[4]))
        self.rent_entry.delete(0, tk.END)
        self.rent_entry.insert(0, values[5].replace("£", ""))
        self.status_var.set(values[6])

        tenant_response = service_get_current_tenant(self.current_user, self.selected_apartment_id)
        if tenant_response["success"] and tenant_response["data"]:
            tenant = tenant_response["data"]
            self.current_tenant_label.config(
                text=f"{tenant['name']} | Lease: {tenant['start_date']} to {tenant['end_date']} | Rent: £{tenant['lease_rent']}"
            )
        else:
            self.current_tenant_label.config(text="No active tenant for this apartment")

    def handle_add(self):
        location = self.location_var.get().strip()
        if not location:
            messagebox.showwarning("Missing Field", "Location is required.")
            return

        try:
            rooms = int(self.rooms_entry.get()) if self.rooms_entry.get().strip() else 0
            floor = int(self.floor_var.get())
            rent = float(self.rent_entry.get()) if self.rent_entry.get().strip() else 0.0
        except ValueError:
            messagebox.showerror("Invalid Input", "Rooms and Floor must be whole numbers, and Rent must be a number.")
            return

        response = service_add_apartment(
            self.current_user,
            location,
            self.type_var.get(),
            rooms,
            floor,
            rent,
            self.status_var.get(),
            self.notes_entry.get().strip()
        )

        if not response["success"]:
            messagebox.showerror("Error", response["error"])
            return

        messagebox.showinfo("Success", "Apartment added successfully.")
        self.handle_clear()
        self.load_records()

    def handle_update(self):
        if not self.selected_apartment_id:
            messagebox.showwarning("No Selection", "Please select an apartment to update.")
            return

        try:
            rooms = int(self.rooms_entry.get()) if self.rooms_entry.get().strip() else 0
            floor = int(self.floor_var.get())
            rent = float(self.rent_entry.get()) if self.rent_entry.get().strip() else 0.0
        except ValueError:
            messagebox.showerror("Invalid Input", "Rooms and Floor must be whole numbers, and Rent must be a number.")
            return

        response = service_update_apartment(
            self.current_user,
            self.selected_apartment_id,
            self.location_var.get().strip(),
            self.type_var.get(),
            rooms,
            floor,
            rent,
            self.status_var.get(),
            self.notes_entry.get().strip()
        )

        if not response["success"]:
            messagebox.showerror("Error", response["error"])
            return

        messagebox.showinfo("Success", "Apartment updated successfully.")
        self.handle_clear()
        self.load_records()

    def handle_delete(self):
        if not self.selected_apartment_id:
            messagebox.showwarning("No Selection", "Please select an apartment to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this apartment?")
        if not confirm:
            return

        response = service_delete_apartment(self.current_user, self.selected_apartment_id)

        if not response["success"]:
            messagebox.showerror("Error", response["error"])
            return

        messagebox.showinfo("Deleted", "Apartment deleted successfully.")
        self.handle_clear()
        self.load_records()

    def handle_terminate_lease(self):
        if not self.selected_apartment_id:
            messagebox.showwarning("No Selection", "Please select an apartment first.")
            return

        confirm = messagebox.askyesno(
            "Terminate Lease",
            "Are you sure you want to terminate the active lease for this apartment?"
        )
        if not confirm:
            return

        response = service_terminate_current_lease_for_apartment(
            self.current_user,
            self.selected_apartment_id
        )

        if not response["success"]:
            messagebox.showerror("Error", response["error"])
            return

        messagebox.showinfo("Success", response["message"])
        self.handle_clear()
        self.load_records()

    def handle_clear(self):
        self.selected_apartment_id = None

        self.apartment_id_entry.config(state="normal")
        self.apartment_id_entry.delete(0, tk.END)
        self.apartment_id_entry.config(state="readonly")

        self.location_var.set(self.user_location)
        self.type_var.set("Studio")

        self.rooms_entry.config(state="normal")
        self.rooms_entry.delete(0, tk.END)
        self.sync_rooms()

        self.floor_var.set("1")
        self.rent_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)

        self.status_var.set("Vacant")
        self.current_tenant_label.config(text="No apartment selected")
        self.suggest_rent()