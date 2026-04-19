import tkinter as tk
from tkinter import messagebox
from models.tenant import add_tenant, update_tenant, delete_tenant, get_all_tenants

LIGHT_BG = "#F4F6F8"
WHITE = "#FFFFFF"
TEXT = "#222222"
SUBTEXT = "#6B7280"
BLUE = "#2F5D8C"
NAVY = "#1E2A38"
LIGHT_BUTTON = "#E5E7EB"
LIGHT_BUTTON_HOVER = "#D1D5DB"


class TenantPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=LIGHT_BG)
        self.create_widgets()
        self.load_records()

    def create_widgets(self):
        #page title
        title = tk.Label(
            self,
            text="Tenant Management",
            bg=LIGHT_BG,
            fg=TEXT,
            font=("Arial", 24, "bold")
        )
        title.pack(anchor="nw", padx=25, pady=(20, 5))

        #page subtitle
        subtitle = tk.Label(
            self,
            text="Add, update and manage tenant records",
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
        self.occupation_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.occupation_entry.grid(row=1, column=3, padx=15, pady=12)

        #row 3
        tk.Label(form_box, text="NI Number", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=2, column=0, padx=15, pady=12, sticky="w")
        self.ni_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.ni_entry.grid(row=2, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Lease Period", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=2, column=2, padx=15, pady=12, sticky="w")
        self.lease_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.lease_entry.grid(row=2, column=3, padx=15, pady=12)

        #row 4
        tk.Label(form_box, text="Reference", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=3, column=0, padx=15, pady=12, sticky="w")
        self.reference_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.reference_entry.grid(row=3, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Apartment Requirement", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=3, column=2, padx=15, pady=12, sticky="w")
        self.apartment_req_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.apartment_req_entry.grid(row=3, column=3, padx=15, pady=12)

        #button area
        button_frame = tk.Frame(self, bg=LIGHT_BG)
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

        #records box
        from tkinter import ttk
        records_box = tk.Frame(
            self,
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
        columns = ("id", "name", "phone", "email", "occupation", "ni_number", "lease_period")
        self.tree = ttk.Treeview(records_box, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("email", text="Email")
        self.tree.heading("occupation", text="Occupation")
        self.tree.heading("ni_number", text="NI Number")
        self.tree.heading("lease_period", text="Lease Period")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("name", width=150)
        self.tree.column("phone", width=110)
        self.tree.column("email", width=180)
        self.tree.column("occupation", width=120)
        self.tree.column("ni_number", width=100)
        self.tree.column("lease_period", width=100)

        self.tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    def load_records(self):
        #clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)
        #load from database
        for t in get_all_tenants():
            self.tree.insert("", "end", values=(
                t["tenant_id"], t["name"], t["phone"], t["email"],
                t["occupation"], t["ni_number"], t["lease_period"]
            ))

    def on_row_select(self, event):
        #populate form fields when a row is clicked
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        self.handle_clear()
        self.name_entry.insert(0, values[1])
        self.phone_entry.insert(0, values[2])
        self.email_entry.insert(0, values[3])
        self.occupation_entry.insert(0, values[4])
        self.ni_entry.insert(0, values[5])
        self.lease_entry.insert(0, values[6])

    def handle_add(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Missing Field", "Tenant Name is required.")
            return
        add_tenant(
            name,
            self.phone_entry.get(),
            self.email_entry.get(),
            self.occupation_entry.get(),
            self.ni_entry.get(),
            self.lease_entry.get(),
            self.reference_entry.get(),
            self.apartment_req_entry.get()
        )
        messagebox.showinfo("Success", "Tenant added successfully.")
        self.handle_clear()
        self.load_records()

    def handle_update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a tenant to update.")
            return
        tenant_id = self.tree.item(selected, "values")[0]
        update_tenant(
            tenant_id,
            self.name_entry.get(),
            self.phone_entry.get(),
            self.email_entry.get(),
            self.occupation_entry.get(),
            self.ni_entry.get(),
            self.lease_entry.get(),
            self.reference_entry.get(),
            self.apartment_req_entry.get()
        )
        messagebox.showinfo("Success", "Tenant updated successfully.")
        self.handle_clear()
        self.load_records()

    def handle_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a tenant to delete.")
            return
        tenant_id = self.tree.item(selected, "values")[0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this tenant?")
        if confirm:
            delete_tenant(tenant_id)
            messagebox.showinfo("Deleted", "Tenant deleted successfully.")
            self.handle_clear()
            self.load_records()

    def handle_clear(self):
        for entry in [
            self.name_entry, self.phone_entry, self.email_entry,
            self.occupation_entry, self.ni_entry, self.lease_entry,
            self.reference_entry, self.apartment_req_entry
        ]:
            entry.delete(0, tk.END)