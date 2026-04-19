import tkinter as tk
from tkinter import ttk, messagebox
from models.payment import add_payment, update_payment, delete_payment, get_all_payments

LIGHT_BG = "#F4F6F8"
WHITE = "#FFFFFF"
TEXT = "#222222"
SUBTEXT = "#6B7280"
BLUE = "#2F5D8C"
DARK_BLUE = "#24496E"
NAVY = "#1E2A38"
LIGHT_BUTTON = "#E5E7EB"
LIGHT_BUTTON_HOVER = "#D1D5DB"


class PaymentPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=LIGHT_BG)
        self.create_widgets()
        self.load_records()

    def create_widgets(self):
        #page title
        title = tk.Label(
            self,
            text="Payment Management",
            bg=LIGHT_BG,
            fg=TEXT,
            font=("Arial", 24, "bold")
        )
        title.pack(anchor="nw", padx=25, pady=(20, 5))

        #page subtitle
        subtitle = tk.Label(
            self,
            text="Track rent payments, invoices and payment status",
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
        tk.Label(form_box, text="Payment ID", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=0, column=0, padx=15, pady=12, sticky="w")
        self.payment_id_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.payment_id_entry.grid(row=0, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Tenant ID", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=0, column=2, padx=15, pady=12, sticky="w")
        self.tenant_id_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.tenant_id_entry.grid(row=0, column=3, padx=15, pady=12)

        #row 2
        tk.Label(form_box, text="Apartment ID", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=1, column=0, padx=15, pady=12, sticky="w")
        self.apartment_id_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.apartment_id_entry.grid(row=1, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Amount", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=1, column=2, padx=15, pady=12, sticky="w")
        self.amount_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.amount_entry.grid(row=1, column=3, padx=15, pady=12)

        #row 3
        tk.Label(form_box, text="Due Date", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=2, column=0, padx=15, pady=12, sticky="w")
        self.due_date_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.due_date_entry.grid(row=2, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Payment Date", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=2, column=2, padx=15, pady=12, sticky="w")
        self.payment_date_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.payment_date_entry.grid(row=2, column=3, padx=15, pady=12)

        #row 4
        tk.Label(form_box, text="Payment Status", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=3, column=0, padx=15, pady=12, sticky="w")
        self.status_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.status_entry.grid(row=3, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Invoice Number", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=3, column=2, padx=15, pady=12, sticky="w")
        self.invoice_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.invoice_entry.grid(row=3, column=3, padx=15, pady=12)

        #button area
        button_frame = tk.Frame(self, bg=LIGHT_BG)
        button_frame.pack(anchor="w", padx=25, pady=12)

        tk.Button(
            button_frame,
            text="Add Payment",
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
            text="Payment Records",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 14, "bold")
        )
        records_title.pack(anchor="w", padx=15, pady=(15, 10))

        #records table
        columns = ("id", "tenant_id", "apartment_id", "amount", "due_date", "payment_date", "status", "invoice")
        self.tree = ttk.Treeview(records_box, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("tenant_id", text="Tenant ID")
        self.tree.heading("apartment_id", text="Apt ID")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("due_date", text="Due Date")
        self.tree.heading("payment_date", text="Paid Date")
        self.tree.heading("status", text="Status")
        self.tree.heading("invoice", text="Invoice")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("tenant_id", width=80, anchor="center")
        self.tree.column("apartment_id", width=70, anchor="center")
        self.tree.column("amount", width=90, anchor="center")
        self.tree.column("due_date", width=100, anchor="center")
        self.tree.column("payment_date", width=100, anchor="center")
        self.tree.column("status", width=90, anchor="center")
        self.tree.column("invoice", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    def load_records(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in get_all_payments():
            self.tree.insert("", "end", values=(
                p["payment_id"], p["tenant_id"], p["apartment_id"],
                f"£{p['amount']:.2f}", p["due_date"], p["payment_date"],
                p["status"], p["invoice_number"]
            ))

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        self.handle_clear()
        self.payment_id_entry.insert(0, values[0])
        self.tenant_id_entry.insert(0, values[1])
        self.apartment_id_entry.insert(0, values[2])
        self.amount_entry.insert(0, values[3].replace("£", ""))
        self.due_date_entry.insert(0, values[4])
        self.payment_date_entry.insert(0, values[5])
        self.status_entry.insert(0, values[6])
        self.invoice_entry.insert(0, values[7])

    def handle_add(self):
        tenant_id = self.tenant_id_entry.get().strip()
        apartment_id = self.apartment_id_entry.get().strip()
        if not tenant_id or not apartment_id:
            messagebox.showwarning("Missing Fields", "Tenant ID and Apartment ID are required.")
            return
        try:
            amount = float(self.amount_entry.get()) if self.amount_entry.get() else 0.0
        except ValueError:
            messagebox.showerror("Invalid Input", "Amount must be a number.")
            return
        add_payment(
            tenant_id, apartment_id, amount,
            self.due_date_entry.get(),
            self.payment_date_entry.get(),
            self.status_entry.get() or "Pending",
            self.invoice_entry.get()
        )
        messagebox.showinfo("Success", "Payment added successfully.")
        self.handle_clear()
        self.load_records()

    def handle_update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a payment to update.")
            return
        payment_id = self.tree.item(selected, "values")[0]
        try:
            amount = float(self.amount_entry.get()) if self.amount_entry.get() else 0.0
        except ValueError:
            messagebox.showerror("Invalid Input", "Amount must be a number.")
            return
        update_payment(
            payment_id,
            self.tenant_id_entry.get(),
            self.apartment_id_entry.get(),
            amount,
            self.due_date_entry.get(),
            self.payment_date_entry.get(),
            self.status_entry.get(),
            self.invoice_entry.get()
        )
        messagebox.showinfo("Success", "Payment updated successfully.")
        self.handle_clear()
        self.load_records()

    def handle_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a payment to delete.")
            return
        payment_id = self.tree.item(selected, "values")[0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this payment?")
        if confirm:
            delete_payment(payment_id)
            messagebox.showinfo("Deleted", "Payment deleted successfully.")
            self.handle_clear()
            self.load_records()

    def handle_clear(self):
        for entry in [
            self.payment_id_entry, self.tenant_id_entry, self.apartment_id_entry,
            self.amount_entry, self.due_date_entry, self.payment_date_entry,
            self.status_entry, self.invoice_entry
        ]:
            entry.delete(0, tk.END)