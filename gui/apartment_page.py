import tkinter as tk
from tkinter import ttk, messagebox
from models.apartment import add_apartment, update_apartment, delete_apartment, get_all_apartments

LIGHT_BG = "#F4F6F8"
WHITE = "#FFFFFF"
TEXT = "#222222"
SUBTEXT = "#6B7280"
BLUE = "#2F5D8C"
DARK_BLUE = "#24496E"
NAVY = "#1E2A38"
LIGHT_BUTTON = "#E5E7EB"
LIGHT_BUTTON_HOVER = "#D1D5DB"


class ApartmentPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=LIGHT_BG)
        self.create_widgets()
        self.load_records()

    def create_widgets(self):
        #page title
        title = tk.Label(
            self,
            text="Apartment Management",
            bg=LIGHT_BG,
            fg=TEXT,
            font=("Arial", 24, "bold")
        )
        title.pack(anchor="nw", padx=25, pady=(20, 5))

        #page subtitle
        subtitle = tk.Label(
            self,
            text="Add, update and manage apartment records",
            bg=LIGHT_BG,
            fg=SUBTEXT,
            font=("Arial", 12)
        )
        subtitle.pack(anchor="nw", padx=25, pady=(0, 15))

        #form box
        form_box = tk.Frame(
            self,
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
        self.apartment_id_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.apartment_id_entry.grid(row=0, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Location", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=0, column=2, padx=15, pady=12, sticky="w")
        self.location_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.location_entry.grid(row=0, column=3, padx=15, pady=12)

        #row 2
        tk.Label(form_box, text="Apartment Type", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=1, column=0, padx=15, pady=12, sticky="w")
        self.type_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.type_entry.grid(row=1, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Monthly Rent", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=1, column=2, padx=15, pady=12, sticky="w")
        self.rent_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.rent_entry.grid(row=1, column=3, padx=15, pady=12)

        #row 3
        tk.Label(form_box, text="Number of Rooms", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=2, column=0, padx=15, pady=12, sticky="w")
        self.rooms_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.rooms_entry.grid(row=2, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Occupancy Status", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=2, column=2, padx=15, pady=12, sticky="w")
        self.status_var = tk.StringVar(value="Vacant")
        status_menu = tk.OptionMenu(form_box, self.status_var, "Vacant", "Occupied", "Reserved", "Under Maintenance")
        status_menu.config(width=22, bg=WHITE, fg=TEXT, relief="solid", bd=1, highlightthickness=0)
        status_menu.grid(row=2, column=3, padx=15, pady=12, sticky="w")

        #row 4
        tk.Label(form_box, text="Floor Number", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=3, column=0, padx=15, pady=12, sticky="w")
        self.floor_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.floor_entry.grid(row=3, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Notes", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=3, column=2, padx=15, pady=12, sticky="w")
        self.notes_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.notes_entry.grid(row=3, column=3, padx=15, pady=12)

        #button area
        button_frame = tk.Frame(self, bg=LIGHT_BG)
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

        #records box
        records_box = tk.Frame(
            self,
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
        self.tree = ttk.Treeview(records_box, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("location", text="Location")
        self.tree.heading("type", text="Type")
        self.tree.heading("rooms", text="Rooms")
        self.tree.heading("floor", text="Floor")
        self.tree.heading("rent", text="Monthly Rent")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("location", width=150)
        self.tree.column("type", width=100)
        self.tree.column("rooms", width=60, anchor="center")
        self.tree.column("floor", width=60, anchor="center")
        self.tree.column("rent", width=110, anchor="center")
        self.tree.column("status", width=110, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    def load_records(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for a in get_all_apartments():
            self.tree.insert("", "end", values=(
                a["apartment_id"],
                a["location"],
                a["apartment_type"],
                a["num_rooms"],
                a["floor_number"],
                f"£{a['monthly_rent']:.2f}",
                a["occupancy_status"]
            ))

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected, "values")
        self.handle_clear()

        self.apartment_id_entry.insert(0, values[0])
        self.location_entry.insert(0, values[1])
        self.type_entry.insert(0, values[2])
        self.rooms_entry.insert(0, values[3])
        self.floor_entry.insert(0, values[4])
        self.rent_entry.insert(0, values[5].replace("£", ""))
        self.status_var.set(values[6])

    def handle_add(self):
        location = self.location_entry.get().strip()
        if not location:
            messagebox.showwarning("Missing Field", "Location is required.")
            return

        try:
            rooms = int(self.rooms_entry.get()) if self.rooms_entry.get() else 0
            floor = int(self.floor_entry.get()) if self.floor_entry.get() else 0
            rent = float(self.rent_entry.get()) if self.rent_entry.get() else 0.0
        except ValueError:
            messagebox.showerror("Invalid Input", "Rooms and Floor must be whole numbers, Rent must be a number.")
            return

        add_apartment(
            location,
            self.type_entry.get(),
            rooms,
            floor,
            rent,
            self.status_var.get() or "Vacant",
            self.notes_entry.get()
        )

        messagebox.showinfo("Success", "Apartment added successfully.")
        self.handle_clear()
        self.load_records()

    def handle_update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an apartment to update.")
            return

        apartment_id = self.tree.item(selected, "values")[0]

        try:
            rooms = int(self.rooms_entry.get()) if self.rooms_entry.get() else 0
            floor = int(self.floor_entry.get()) if self.floor_entry.get() else 0
            rent = float(self.rent_entry.get()) if self.rent_entry.get() else 0.0
        except ValueError:
            messagebox.showerror("Invalid Input", "Rooms and Floor must be whole numbers, Rent must be a number.")
            return

        update_apartment(
            apartment_id,
            self.location_entry.get(),
            self.type_entry.get(),
            rooms,
            floor,
            rent,
            self.status_var.get(),
            self.notes_entry.get()
        )

        messagebox.showinfo("Success", "Apartment updated successfully.")
        self.handle_clear()
        self.load_records()

    def handle_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an apartment to delete.")
            return

        apartment_id = self.tree.item(selected, "values")[0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this apartment?")

        if confirm:
            delete_apartment(apartment_id)
            messagebox.showinfo("Deleted", "Apartment deleted successfully.")
            self.handle_clear()
            self.load_records()

    def handle_clear(self):
        for entry in [
            self.apartment_id_entry,
            self.location_entry,
            self.type_entry,
            self.rooms_entry,
            self.floor_entry,
            self.rent_entry,
            self.notes_entry
        ]:
            entry.delete(0, tk.END)

        self.status_var.set("Vacant")