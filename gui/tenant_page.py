import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from services.tenant_services import (
    service_get_all_tenants,
    service_add_tenant,
    service_update_tenant,
    service_delete_tenant,
    service_assign_tenant_to_apartment
)

LIGHT_BG = "#F4F6F8"
WHITE = "#FFFFFF"
TEXT = "#222222"
SUBTEXT = "#6B7280"
LIGHT_BUTTON = "#E5E7EB"
LIGHT_BUTTON_HOVER = "#D1D5DB"


class TenantPage(tk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent, bg=LIGHT_BG)
        self.current_user = user
        self.selected_tenant_id = None
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

    def create_widgets(self):
        container = self.scrollable_frame

        #page title
        title = tk.Label(
            container,
            text="Tenant Management",
            bg=LIGHT_BG,
            fg=TEXT,
            font=("Arial", 24, "bold")
        )
        title.pack(anchor="nw", padx=25, pady=(20, 5))

        #page subtitle
        subtitle = tk.Label(
            container,
            text="Add, update and manage tenant records",
            bg=LIGHT_BG,
            fg=SUBTEXT,
            font=("Arial", 12)
        )
        subtitle.pack(anchor="nw", padx=25, pady=(0, 15))

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
        tk.Label(form_box, text="Tenant Name", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=0, column=0, padx=15, pady=12, sticky="w")
        self.name_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.name_entry.grid(row=0, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Phone Number", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=0, column=2, padx=15, pady=12, sticky="w")
        self.phone_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.phone_entry.grid(row=0, column=3, padx=15, pady=12)

        #row 2
        tk.Label(form_box, text="Email", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=1, column=0, padx=15, pady=12, sticky="w")
        self.email_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.email_entry.grid(row=1, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Occupation", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=1, column=2, padx=15, pady=12, sticky="w")
        self.occupation_var = tk.StringVar(value="Student")
        occupation_menu = tk.OptionMenu(
            form_box,
            self.occupation_var,
            "Student",
            "Employed",
            "Self-employed",
            "Unemployed",
            "Other"
        )
        occupation_menu.config(width=22, bg=WHITE, fg=TEXT, relief="solid", bd=1, highlightthickness=0)
        occupation_menu.grid(row=1, column=3, padx=15, pady=12, sticky="w")

        #row 3
        tk.Label(form_box, text="Lease Start Date", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=2, column=0, padx=15, pady=12, sticky="w")
        self.lease_start_entry = DateEntry(
            form_box,
            width=23,
            background="#2F5D8C",
            foreground="white",
            borderwidth=1,
            date_pattern="yyyy-mm-dd"
        )
        self.lease_start_entry.grid(row=2, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Lease End Date", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=2, column=2, padx=15, pady=12, sticky="w")
        self.lease_end_entry = DateEntry(
            form_box,
            width=23,
            background="#2F5D8C",
            foreground="white",
            borderwidth=1,
            date_pattern="yyyy-mm-dd"
        )
        self.lease_end_entry.grid(row=2, column=3, padx=15, pady=12)

        #row 4
        tk.Label(form_box, text="Reference", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=3, column=0, padx=15, pady=12, sticky="w")
        self.reference_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.reference_entry.grid(row=3, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Apartment Requirement", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=3, column=2, padx=15, pady=12, sticky="w")
        self.apartment_req_var = tk.StringVar(value="No Preference")
        apartment_req_menu = tk.OptionMenu(
            form_box,
            self.apartment_req_var,
            "No Preference",
            "Studio",
            "1 Bedroom",
            "2 Bedroom",
            "3 Bedroom"
        )
        apartment_req_menu.config(width=22, bg=WHITE, fg=TEXT, relief="solid", bd=1, highlightthickness=0)
        apartment_req_menu.grid(row=3, column=3, padx=15, pady=12, sticky="w")

        #button area
        button_frame = tk.Frame(container, bg=LIGHT_BG)
        button_frame.pack(anchor="w", padx=25, pady=12)

        tk.Button(
            button_frame,
            text="Add Tenant",
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

        #lease assignment box
        lease_box = tk.Frame(
            container,
            bg=WHITE,
            highlightbackground="#E0E0E0",
            highlightthickness=1
        )
        lease_box.pack(fill="x", padx=25, pady=10)

        lease_title = tk.Label(
            lease_box,
            text="Assign Apartment",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 14, "bold")
        )
        lease_title.grid(row=0, column=0, columnspan=4, sticky="w", padx=15, pady=(15, 10))

        lease_box.grid_columnconfigure(0, weight=1)
        lease_box.grid_columnconfigure(1, weight=1)
        lease_box.grid_columnconfigure(2, weight=1)
        lease_box.grid_columnconfigure(3, weight=1)

        tk.Label(lease_box, text="Apartment ID", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=1, column=0, padx=15, pady=12, sticky="w")
        self.assign_apartment_entry = tk.Entry(lease_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.assign_apartment_entry.grid(row=1, column=1, padx=15, pady=12)

        tk.Label(lease_box, text="Monthly Rent", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=1, column=2, padx=15, pady=12, sticky="w")
        self.assign_rent_entry = tk.Entry(lease_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.assign_rent_entry.grid(row=1, column=3, padx=15, pady=12)

        tk.Label(lease_box, text="Lease Start Date", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=2, column=0, padx=15, pady=12, sticky="w")
        self.assign_start_entry = DateEntry(
            lease_box,
            width=23,
            background="#2F5D8C",
            foreground="white",
            borderwidth=1,
            date_pattern="yyyy-mm-dd"
        )
        self.assign_start_entry.grid(row=2, column=1, padx=15, pady=12)

        tk.Label(lease_box, text="Lease End Date", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=2, column=2, padx=15, pady=12, sticky="w")
        self.assign_end_entry = DateEntry(
            lease_box,
            width=23,
            background="#2F5D8C",
            foreground="white",
            borderwidth=1,
            date_pattern="yyyy-mm-dd"
        )
        self.assign_end_entry.grid(row=2, column=3, padx=15, pady=12)

        tk.Button(
            lease_box,
            text="Assign Apartment",
            command=self.handle_assign_apartment,
            bg=LIGHT_BUTTON,
            fg=TEXT,
            activebackground=LIGHT_BUTTON_HOVER,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            width=18,
            height=2,
            font=("Arial", 11, "bold"),
            cursor="hand2"
        ).grid(row=3, column=0, columnspan=4, pady=(10, 15))

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
            text="Tenant Records",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 14, "bold")
        )
        records_title.pack(anchor="w", padx=15, pady=(15, 10))

        #records table
        columns = (
            "id",
            "name",
            "phone",
            "email",
            "occupation",
            "lease_period",
            "reference",
            "apartment_requirement"
        )
        self.tree = ttk.Treeview(records_box, columns=columns, show="headings", selectmode="browse", height=8)

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("email", text="Email")
        self.tree.heading("occupation", text="Occupation")
        self.tree.heading("lease_period", text="Lease Period")
        self.tree.heading("reference", text="Reference")
        self.tree.heading("apartment_requirement", text="Apartment Requirement")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("name", width=140)
        self.tree.column("phone", width=110)
        self.tree.column("email", width=170)
        self.tree.column("occupation", width=120)
        self.tree.column("lease_period", width=180)
        self.tree.column("reference", width=120)
        self.tree.column("apartment_requirement", width=150)

        self.tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    def load_records(self):
        response = service_get_all_tenants(self.current_user)

        if not response["success"]:
            messagebox.showerror("Error", response["error"])
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        for t in response["data"]:
            self.tree.insert("", "end", values=(
                t["tenant_id"],
                t["name"],
                t["phone"],
                t["email"],
                t["occupation"],
                t["lease_period"],
                t["reference"],
                t["apartment_requirement"]
            ))

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected, "values")
        self.handle_clear()

        self.selected_tenant_id = values[0]
        self.name_entry.insert(0, values[1])
        self.phone_entry.insert(0, values[2])
        self.email_entry.insert(0, values[3])
        self.occupation_var.set(values[4] if values[4] else "Student")

        lease_period = values[5]
        if " to " in lease_period:
            start_date, end_date = lease_period.split(" to ", 1)
            self.lease_start_entry.set_date(start_date)
            self.lease_end_entry.set_date(end_date)

        self.reference_entry.insert(0, values[6])
        self.apartment_req_var.set(values[7] if values[7] else "No Preference")

    def handle_add(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Missing Field", "Tenant Name is required.")
            return

        lease_period = f"{self.lease_start_entry.get()} to {self.lease_end_entry.get()}"

        response = service_add_tenant(
            self.current_user,
            name,
            self.phone_entry.get().strip(),
            self.email_entry.get().strip(),
            self.occupation_var.get().strip(),
            "",
            lease_period,
            self.reference_entry.get().strip(),
            self.apartment_req_var.get().strip()
        )

        if not response["success"]:
            messagebox.showerror("Error", response["error"])
            return

        messagebox.showinfo("Success", "Tenant added successfully.")

        self.load_records()
        if self.tree.get_children():
            last_item = self.tree.get_children()[-1]
            self.tree.selection_set(last_item)
            self.tree.focus(last_item)

            values = self.tree.item(last_item, "values")
            self.selected_tenant_id = values[0]

    def handle_update(self):
        if not self.selected_tenant_id:
            messagebox.showwarning("No Selection", "Please select a tenant to update.")
            return

        lease_period = f"{self.lease_start_entry.get()} to {self.lease_end_entry.get()}"

        response = service_update_tenant(
            self.current_user,
            self.selected_tenant_id,
            self.name_entry.get().strip(),
            self.phone_entry.get().strip(),
            self.email_entry.get().strip(),
            self.occupation_var.get().strip(),
            "",
            lease_period,
            self.reference_entry.get().strip(),
            self.apartment_req_var.get().strip()
        )

        if not response["success"]:
            messagebox.showerror("Error", response["error"])
            return

        messagebox.showinfo("Success", "Tenant updated successfully.")
        self.handle_clear()
        self.load_records()

    def handle_delete(self):
        if not self.selected_tenant_id:
            messagebox.showwarning("No Selection", "Please select a tenant to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this tenant?")
        if not confirm:
            return

        response = service_delete_tenant(self.current_user, self.selected_tenant_id)

        if not response["success"]:
            messagebox.showerror("Error", response["error"])
            return

        messagebox.showinfo("Deleted", "Tenant deleted successfully.")
        self.handle_clear()
        self.load_records()

    def handle_assign_apartment(self):
        if not self.selected_tenant_id:
            messagebox.showwarning("No Selection", "Please select a tenant from the table (or add one first).")
            return

        apartment_id = self.assign_apartment_entry.get().strip()
        start_date = self.assign_start_entry.get()
        end_date = self.assign_end_entry.get()
        monthly_rent_text = self.assign_rent_entry.get().strip()

        if not apartment_id or not monthly_rent_text:
            messagebox.showwarning("Missing Fields", "Apartment ID and Monthly Rent are required.")
            return

        try:
            monthly_rent = float(monthly_rent_text)
        except ValueError:
            messagebox.showerror("Invalid Input", "Monthly Rent must be a valid number.")
            return

        response = service_assign_tenant_to_apartment(
            self.current_user,
            self.selected_tenant_id,
            apartment_id,
            start_date,
            end_date,
            monthly_rent
        )

        if not response["success"]:
            messagebox.showerror("Error", response["error"])
            return

        messagebox.showinfo("Success", f"Apartment assigned successfully. Lease ID: {response['lease_id']}")
        self.assign_apartment_entry.delete(0, tk.END)
        self.assign_rent_entry.delete(0, tk.END)
        self.load_records()

    def handle_clear(self):
        self.selected_tenant_id = None

        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.reference_entry.delete(0, tk.END)

        self.occupation_var.set("Student")
        self.apartment_req_var.set("No Preference")
        self.lease_start_entry.set_date(self.lease_start_entry._date)
        self.lease_end_entry.set_date(self.lease_end_entry._date)

        self.assign_apartment_entry.delete(0, tk.END)
        self.assign_rent_entry.delete(0, tk.END)
        self.assign_start_entry.set_date(self.assign_start_entry._date)
        self.assign_end_entry.set_date(self.assign_end_entry._date)