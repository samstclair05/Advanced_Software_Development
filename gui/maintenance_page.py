import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from models.maintenance import get_all_requests, add_request, update_request, delete_request

LIGHT_BG = "#F4F6F8"
WHITE = "#FFFFFF"
TEXT = "#222222"
SUBTEXT = "#6B7280"
BLUE = "#2F5D8C"
DARK_BLUE = "#24496E"
BORDER_COLOR = "#E0E0E0"
SUCCESS_GREEN = "#10B981"
WARNING_ORANGE = "#F59E0B"
ERROR_RED = "#EF4444"


class MaintenancePage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=LIGHT_BG)
        self.workers = {"Alice": "Available", "Bob": "On-site", "Charlie": "Unavailable"}
        self.create_widgets()
        self.load_records()

    def create_widgets(self):
        # Header
        tk.Label(self, text="Maintenance Management", bg=LIGHT_BG, fg=TEXT, font=("Arial", 24, "bold")).pack(anchor="nw", padx=25, pady=(20, 5))
        tk.Label(self, text="Track, manage, and resolve maintenance issues.", bg=LIGHT_BG, fg=SUBTEXT, font=("Arial", 12)).pack(anchor="nw", padx=25, pady=(0, 10))

        # TOP: Add New Request - full width
        self.create_add_section()

        # BOTTOM: 2 columns - table left, details+workers right
        bottom_frame = tk.Frame(self, bg=LIGHT_BG)
        bottom_frame.pack(fill="both", expand=True, padx=25, pady=(0, 10))
        bottom_frame.grid_columnconfigure(0, weight=2)
        bottom_frame.grid_columnconfigure(1, weight=1)
        bottom_frame.grid_rowconfigure(0, weight=1)

        self.create_issues_section(bottom_frame)

        # Right column
        right_frame = tk.Frame(bottom_frame, bg=LIGHT_BG)
        right_frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        self.create_details_section(right_frame)
        self.create_worker_status_section(right_frame)

    def create_section_frame(self, parent, title_text):
        frame = tk.Frame(parent, bg=WHITE, highlightbackground=BORDER_COLOR, highlightthickness=1)
        tk.Label(frame, text=title_text, bg=WHITE, fg=TEXT, font=("Arial", 13, "bold")).pack(anchor="nw", padx=15, pady=(12, 8))
        return frame

    def create_add_section(self):
        # Full width, single compact row
        add_frame = tk.Frame(self, bg=WHITE, highlightbackground=BORDER_COLOR, highlightthickness=1)
        add_frame.pack(fill="x", padx=25, pady=(0, 10))

        inner = tk.Frame(add_frame, bg=WHITE)
        inner.pack(fill="x", padx=15, pady=10)
        inner.grid_columnconfigure(1, weight=1)
        inner.grid_columnconfigure(3, weight=1)
        inner.grid_columnconfigure(7, weight=3)

        tk.Label(inner, text="Add New Request", bg=WHITE, fg=TEXT, font=("Arial", 13, "bold")).grid(row=0, column=0, columnspan=9, sticky="w", pady=(0, 8))

        tk.Label(inner, text="Apt ID:", bg=WHITE, font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 4))
        self.new_apt_entry = tk.Entry(inner, width=8, bg=WHITE, fg=TEXT, relief="solid", bd=1)
        self.new_apt_entry.grid(row=1, column=1, sticky="ew", padx=(0, 12))

        tk.Label(inner, text="Tenant ID:", bg=WHITE, font=("Arial", 10, "bold")).grid(row=1, column=2, sticky="w", padx=(0, 4))
        self.new_tenant_entry = tk.Entry(inner, width=8, bg=WHITE, fg=TEXT, relief="solid", bd=1)
        self.new_tenant_entry.grid(row=1, column=3, sticky="ew", padx=(0, 12))

        tk.Label(inner, text="Priority:", bg=WHITE, font=("Arial", 10, "bold")).grid(row=1, column=4, sticky="w", padx=(0, 4))
        self.new_priority_var = tk.StringVar(value="Medium")
        ttk.OptionMenu(inner, self.new_priority_var, "Medium", "Low", "Medium", "High").grid(row=1, column=5, sticky="ew", padx=(0, 12))

        tk.Label(inner, text="Description:", bg=WHITE, font=("Arial", 10, "bold")).grid(row=1, column=6, sticky="w", padx=(0, 4))
        self.new_desc_entry = tk.Entry(inner, bg=WHITE, fg=TEXT, relief="solid", bd=1)
        self.new_desc_entry.grid(row=1, column=7, sticky="ew", padx=(0, 12))

        tk.Button(inner, text="Add Request", bg=BLUE, fg=WHITE, relief="flat", bd=0,
                  font=("Arial", 10, "bold"), cursor="hand2", activebackground=DARK_BLUE,
                  command=self.handle_add).grid(row=1, column=8, sticky="ew")

    def create_issues_section(self, parent):
        issues_frame = self.create_section_frame(parent, "Maintenance Requests")
        issues_frame.grid(row=0, column=0, sticky="nsew")

        columns = ("id", "apartment_id", "description", "priority", "status", "worker")
        self.issues_tree = ttk.Treeview(issues_frame, columns=columns, show="headings", selectmode="browse")

        self.issues_tree.heading("id", text="ID")
        self.issues_tree.heading("apartment_id", text="Apt ID")
        self.issues_tree.heading("description", text="Issue")
        self.issues_tree.heading("priority", text="Priority")
        self.issues_tree.heading("status", text="Status")
        self.issues_tree.heading("worker", text="Worker")

        self.issues_tree.column("id", width=40, anchor="center")
        self.issues_tree.column("apartment_id", width=70, anchor="center")
        self.issues_tree.column("description", width=200)
        self.issues_tree.column("priority", width=70, anchor="center")
        self.issues_tree.column("status", width=90, anchor="center")
        self.issues_tree.column("worker", width=90, anchor="center")

        self.issues_tree.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        self.issues_tree.bind("<<TreeviewSelect>>", self.on_issue_select)

    def create_details_section(self, parent):
        details_frame = self.create_section_frame(parent, "Issue Details & Actions")
        details_frame.pack(fill="x", pady=(0, 8))

        content = tk.Frame(details_frame, bg=WHITE)
        content.pack(fill="x", padx=15, pady=(0, 12))
        content.grid_columnconfigure(1, weight=1)

        tk.Label(content, text="Priority:", bg=WHITE, font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=3)
        self.priority_var = tk.StringVar()
        ttk.OptionMenu(content, self.priority_var, "Low", "Low", "Medium", "High").grid(row=0, column=1, sticky="ew", pady=3)

        tk.Label(content, text="Status:", bg=WHITE, font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w", pady=3)
        self.status_var = tk.StringVar()
        ttk.OptionMenu(content, self.status_var, "Reported", "Reported", "In Progress", "Resolved", "Cancelled").grid(row=1, column=1, sticky="ew", pady=3)

        tk.Label(content, text="Worker:", bg=WHITE, font=("Arial", 11, "bold")).grid(row=2, column=0, sticky="w", pady=3)
        self.worker_var = tk.StringVar()
        ttk.OptionMenu(content, self.worker_var, "Unassigned", "Unassigned", *self.workers.keys()).grid(row=2, column=1, sticky="ew", pady=3)

        tk.Label(content, text="Cost (£):", bg=WHITE, font=("Arial", 11, "bold")).grid(row=3, column=0, sticky="w", pady=3)
        self.cost_entry = tk.Entry(content, bg=WHITE, fg=TEXT, relief="solid", bd=1)
        self.cost_entry.grid(row=3, column=1, sticky="ew", pady=3)

        tk.Label(content, text="Time (hrs):", bg=WHITE, font=("Arial", 11, "bold")).grid(row=4, column=0, sticky="w", pady=3)
        self.time_entry = tk.Entry(content, bg=WHITE, fg=TEXT, relief="solid", bd=1)
        self.time_entry.grid(row=4, column=1, sticky="ew", pady=3)

        btn_frame = tk.Frame(content, bg=WHITE)
        btn_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(8, 0))

        tk.Button(btn_frame, text="Update", bg=BLUE, fg=WHITE, relief="flat", bd=0,
                  font=("Arial", 10, "bold"), cursor="hand2", activebackground=DARK_BLUE,
                  command=self.handle_update).pack(side="left", expand=True, fill="x", padx=(0, 5))

        tk.Button(btn_frame, text="Delete", bg=ERROR_RED, fg=WHITE, relief="flat", bd=0,
                  font=("Arial", 10, "bold"), cursor="hand2",
                  command=self.handle_delete).pack(side="left", expand=True, fill="x", padx=(5, 0))

    def create_worker_status_section(self, parent):
        worker_frame = self.create_section_frame(parent, "Worker Availability")
        worker_frame.pack(fill="x")

        self.worker_list_frame = tk.Frame(worker_frame, bg=WHITE)
        self.worker_list_frame.pack(fill="x", padx=15, pady=(0, 12))
        self.update_worker_display()

    def load_records(self):
        for item in self.issues_tree.get_children():
            self.issues_tree.delete(item)
        for r in get_all_requests():
            self.issues_tree.insert("", "end", values=(
                r["request_id"], r["apartment_id"], r["description"],
                r["priority"], r["status"], r["assigned_worker"]
            ))

    def on_issue_select(self, event):
        selected_item = self.issues_tree.selection()
        if not selected_item:
            return
        values = self.issues_tree.item(selected_item, "values")
        self.priority_var.set(values[3])
        self.status_var.set(values[4])
        self.worker_var.set(values[5])
        self.cost_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)

    def handle_add(self):
        apt_id = self.new_apt_entry.get().strip()
        desc = self.new_desc_entry.get().strip()
        if not apt_id or not desc:
            messagebox.showwarning("Missing Fields", "Apartment ID and Description are required.")
            return
        add_request(
            apartment_id=apt_id,
            tenant_id=self.new_tenant_entry.get().strip() or None,
            description=desc,
            priority=self.new_priority_var.get(),
            status="Reported",
            assigned_worker="Unassigned",
            cost=0,
            time_hours=0,
            created_date=str(date.today())
        )
        messagebox.showinfo("Success", "Maintenance request added.")
        self.new_apt_entry.delete(0, tk.END)
        self.new_tenant_entry.delete(0, tk.END)
        self.new_desc_entry.delete(0, tk.END)
        self.new_priority_var.set("Medium")
        self.load_records()

    def handle_update(self):
        selected_item = self.issues_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a maintenance issue to update.")
            return
        request_id = self.issues_tree.item(selected_item, "values")[0]
        try:
            cost = float(self.cost_entry.get()) if self.cost_entry.get() else 0.0
            time_hours = float(self.time_entry.get()) if self.time_entry.get() else 0.0
        except ValueError:
            messagebox.showerror("Invalid Input", "Cost and Time must be valid numbers.")
            return
        update_request(request_id, self.priority_var.get(), self.status_var.get(),
                       self.worker_var.get(), cost, time_hours)
        messagebox.showinfo("Success", f"Issue #{request_id} updated.")
        self.load_records()

    def handle_delete(self):
        selected_item = self.issues_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an issue to delete.")
            return
        request_id = self.issues_tree.item(selected_item, "values")[0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this request?")
        if confirm:
            delete_request(request_id)
            messagebox.showinfo("Deleted", "Maintenance request deleted.")
            self.load_records()

    def update_worker_display(self):
        for widget in self.worker_list_frame.winfo_children():
            widget.destroy()
        row = 0
        for worker, status in self.workers.items():
            tk.Label(self.worker_list_frame, text=worker, bg=WHITE, font=("Arial", 11)).grid(row=row, column=0, sticky="w", pady=3)
            status_color = TEXT
            if status == "Available": status_color = SUCCESS_GREEN
            if status == "On-site": status_color = WARNING_ORANGE
            if status == "Unavailable": status_color = ERROR_RED
            tk.Label(self.worker_list_frame, text=status, bg=WHITE, fg=status_color, font=("Arial", 11, "bold")).grid(row=row, column=1, sticky="e", padx=10)
            row += 1
        self.worker_list_frame.grid_columnconfigure(1, weight=1)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Maintenance Page Demo")
    root.geometry("1200x700")
    maintenance_page = MaintenancePage(root)
    maintenance_page.pack(fill="both", expand=True)
    root.mainloop()