import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry


LIGHT_BG = "#F4F6F8"
WHITE = "#FFFFFF"
TEXT = "#222222"
SUBTEXT = "#6B7280"
LIGHT_BUTTON = "#E5E7EB"
LIGHT_BUTTON_HOVER = "#D1D5DB"


class PaymentPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=LIGHT_BG)
        self.create_widgets()

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
        tk.Label(form_box, text="Tenant ID", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=0, column=0, padx=15, pady=12, sticky="w")
        self.tenant_id_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.tenant_id_entry.grid(row=0, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Apartment ID", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=0, column=2, padx=15, pady=12, sticky="w")
        self.apartment_id_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.apartment_id_entry.grid(row=0, column=3, padx=15, pady=12)

        #row 2
        tk.Label(form_box, text="Amount", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=1, column=0, padx=15, pady=12, sticky="w")
        self.amount_entry = tk.Entry(form_box, width=25, bg="white", fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.amount_entry.grid(row=1, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Due Date", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=1, column=2, padx=15, pady=12, sticky="w")
        self.due_date_entry = DateEntry(
            form_box,
            width=23,
            background="#2F5D8C",
            foreground="white",
            borderwidth=1,
            date_pattern="yyyy-mm-dd"
        )
        self.due_date_entry.grid(row=1, column=3, padx=15, pady=12)

        #row 3
        tk.Label(form_box, text="Payment Date", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=2, column=0, padx=15, pady=12, sticky="w")
        self.payment_date_entry = DateEntry(
            form_box,
            width=23,
            background="#2F5D8C",
            foreground="white",
            borderwidth=1,
            date_pattern="yyyy-mm-dd"
        )
        self.payment_date_entry.grid(row=2, column=1, padx=15, pady=12)

        tk.Label(form_box, text="Payment Status", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=2, column=2, padx=15, pady=12, sticky="w")
        self.status_var = tk.StringVar(value="Pending")
        status_menu = tk.OptionMenu(form_box, self.status_var, "Pending", "Paid", "Late", "Overdue")
        status_menu.config(width=22, bg=WHITE, fg=TEXT, relief="solid", bd=1, highlightthickness=0)
        status_menu.grid(row=2, column=3, padx=15, pady=12, sticky="w")

        #row 4
        tk.Label(form_box, text="Invoice Number", bg=WHITE, fg=TEXT, font=("Arial", 11)).grid(row=3, column=0, padx=15, pady=12, sticky="w")
        self.invoice_entry = tk.Entry(form_box, width=25, bg="#F3F4F6", fg=TEXT, relief="solid", bd=1)
        self.invoice_entry.insert(0, "INV-001")
        self.invoice_entry.config(state="readonly")
        self.invoice_entry.grid(row=3, column=1, padx=15, pady=12)

        #button area
        button_frame = tk.Frame(self, bg=LIGHT_BG)
        button_frame.pack(anchor="w", padx=25, pady=12)

        tk.Button(
            button_frame,
            text="Record Payment",
            bg=LIGHT_BUTTON,
            fg=TEXT,
            activebackground=LIGHT_BUTTON_HOVER,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            width=16,
            height=2,
            font=("Arial", 11, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=6)

        tk.Button(
            button_frame,
            text="Update Status",
            bg=LIGHT_BUTTON,
            fg=TEXT,
            activebackground=LIGHT_BUTTON_HOVER,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            width=16,
            height=2,
            font=("Arial", 11, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=6)

        tk.Button(
            button_frame,
            text="Clear",
            bg=LIGHT_BUTTON,
            fg=TEXT,
            activebackground=LIGHT_BUTTON_HOVER,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            width=16,
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

        #records title
        records_title = tk.Label(
            records_box,
            text="Payment Records",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 14, "bold")
        )
        records_title.pack(anchor="w", padx=15, pady=(15, 10))

        #records table
        columns = ("payment_id", "tenant_id", "apartment_id", "amount", "payment_date", "status", "invoice_number")
        self.tree = ttk.Treeview(records_box, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("payment_id", text="Payment ID")
        self.tree.heading("tenant_id", text="Tenant ID")
        self.tree.heading("apartment_id", text="Apartment ID")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("payment_date", text="Payment Date")
        self.tree.heading("status", text="Status")
        self.tree.heading("invoice_number", text="Invoice Number")

        self.tree.column("payment_id", width=90, anchor="center")
        self.tree.column("tenant_id", width=90, anchor="center")
        self.tree.column("apartment_id", width=100, anchor="center")
        self.tree.column("amount", width=100, anchor="center")
        self.tree.column("payment_date", width=120, anchor="center")
        self.tree.column("status", width=100, anchor="center")
        self.tree.column("invoice_number", width=120, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def load_payment_history(self, payment_rows):
        #clear old rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        #insert new rows
        for payment in payment_rows:
            self.tree.insert("", "end", values=(
                payment.get("payment_id", ""),
                payment.get("tenant_id", ""),
                payment.get("apartment_id", ""),
                payment.get("amount", ""),
                payment.get("payment_date", ""),
                payment.get("status", ""),
                payment.get("invoice_number", "")
            ))