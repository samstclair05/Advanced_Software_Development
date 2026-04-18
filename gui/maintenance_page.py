import tkinter as tk
from tkinter import ttk, messagebox

#Constants
LIGHT_BG = "#F4F6F8"
WHITE = "#FFFFFF"
TEXT = "#222222"
SUBTEXT = "#6B7280"
BLUE = "#2F5D8C"
DARK_BLUE = "#24496E"
NAVY = "#1E2A38"
LIGHT_BUTTON = "#E5E7EB"
LIGHT_BUTTON_HOVER = "#D1D5DB"
BORDER_COLOR = "#E0E0E0"
SUCCESS_GREEN = "#10B981"
WARNING_ORANGE = "#F59E0B"
ERROR_RED = "#EF4444"

class MaintenancePage(tk.Frame):
    
    #A page for managing maintenance issues reported by tenants.

    def __init__(self, parent):
        super().__init__(parent, bg=LIGHT_BG)
        
        # Sample data
        self.maintenance_issues = [
            {"id": 1, "apartment": "101A", "issue": "Leaky sink in kitchen", "priority": "High", "status": "Reported", "worker": "Unassigned", "cost": 0, "time": 0},
            {"id": 2, "apartment": "204B", "issue": "Broken window latch", "priority": "Medium", "status": "In Progress", "worker": "Bob", "cost": 0, "time": 0},
            {"id": 3, "apartment": "501C", "issue": "Heating not working", "priority": "High", "status": "Reported", "worker": "Unassigned", "cost": 0, "time": 0},
            {"id": 4, "apartment": "302A", "issue": "Clogged drain in bathroom", "priority": "Low", "status": "Resolved", "worker": "Alice", "cost": 50, "time": 1.5},
        ]
        self.workers = {"Alice": "Available", "Bob": "On-site", "Charlie": "Unavailable"}

        self.create_widgets()
        self.populate_issues_list()

    def create_widgets(self):
        """Creates and lays out the widgets for the page."""
        # Page Header
        title = tk.Label(self, text="Maintenance Management", bg=LIGHT_BG, fg=TEXT, font=("Arial", 24, "bold"))
        title.pack(anchor="nw", padx=25, pady=(20, 5))

        subtitle = tk.Label(self, text="Track, manage, and resolve maintenance issues.", bg=LIGHT_BG, fg=SUBTEXT, font=("Arial", 12))
        subtitle.pack(anchor="nw", padx=25, pady=(0, 20))

        # Main Container
        main_frame = tk.Frame(self, bg=LIGHT_BG)
        main_frame.pack(fill="both", expand=True, padx=25, pady=10)
        main_frame.grid_columnconfigure(0, weight=2) # Issues list takes more space
        main_frame.grid_columnconfigure(1, weight=1) # Details/actions take less space

        # Sections
        self.create_issues_section(main_frame)
        self.create_details_section(main_frame)
        self.create_worker_status_section(main_frame)

    def create_section_frame(self, parent, title_text):
        #Helper to create a styled section frame with a title
        frame = tk.Frame(parent, bg=WHITE, highlightbackground=BORDER_COLOR, highlightthickness=1)
        title = tk.Label(frame, text=title_text, bg=WHITE, fg=TEXT, font=("Arial", 14, "bold"))
        title.pack(anchor="nw", padx=15, pady=(15, 10))
        return frame

    def create_issues_section(self, parent):
        #Creates the list view for all maintenance issues
        issues_frame = self.create_section_frame(parent, "Maintenance Requests")
        issues_frame.grid(row=0, column=0, rowspan=2, padx=(0, 10), sticky="nsew")

        # Treeview for displaying issues
        columns = ("id", "apartment", "issue", "priority", "status")
        self.issues_tree = ttk.Treeview(issues_frame, columns=columns, show="headings", selectmode="browse")
        
        self.issues_tree.heading("id", text="ID")
        self.issues_tree.heading("apartment", text="Apartment")
        self.issues_tree.heading("issue", text="Issue")
        self.issues_tree.heading("priority", text="Priority")
        self.issues_tree.heading("status", text="Status")

        self.issues_tree.column("id", width=40, anchor="center")
        self.issues_tree.column("apartment", width=100, anchor="center")
        self.issues_tree.column("issue", width=250)
        self.issues_tree.column("priority", width=80, anchor="center")
        self.issues_tree.column("status", width=100, anchor="center")

        self.issues_tree.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        self.issues_tree.bind("<<TreeviewSelect>>", self.on_issue_select)

    def create_details_section(self, parent):
        #Creates the section for viewing and editing issue details.
        details_frame = self.create_section_frame(parent, "Issue Details & Actions")
        details_frame.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="nsew")

        content_frame = tk.Frame(details_frame, bg=WHITE)
        content_frame.pack(fill="x", padx=15, pady=5)

        # Labels and Controls
        tk.Label(content_frame, text="Priority:", bg=WHITE, font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.priority_var = tk.StringVar()
        priority_options = ["Low", "Medium", "High"]
        self.priority_menu = ttk.OptionMenu(content_frame, self.priority_var, priority_options[0], *priority_options)
        self.priority_menu.grid(row=0, column=1, sticky="ew", pady=5)

        tk.Label(content_frame, text="Status:", bg=WHITE, font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        self.status_var = tk.StringVar()
        status_options = ["Reported", "In Progress", "Resolved", "Cancelled"]
        self.status_menu = ttk.OptionMenu(content_frame, self.status_var, status_options[0], *status_options)
        self.status_menu.grid(row=1, column=1, sticky="ew", pady=5)

        tk.Label(content_frame, text="Assign Worker:", bg=WHITE, font=("Arial", 11, "bold")).grid(row=2, column=0, sticky="w", pady=5)
        self.worker_var = tk.StringVar()
        self.worker_menu = ttk.OptionMenu(content_frame, self.worker_var, "Unassigned", "Unassigned", *self.workers.keys())
        self.worker_menu.grid(row=2, column=1, sticky="ew", pady=5)

        tk.Label(content_frame, text="Cost (£):", bg=WHITE, font=("Arial", 11, "bold")).grid(row=3, column=0, sticky="w", pady=5)
        self.cost_entry = tk.Entry(content_frame, bg=WHITE, fg=TEXT, relief="solid", bd=1)
        self.cost_entry.grid(row=3, column=1, sticky="ew", pady=5)

        tk.Label(content_frame, text="Time (hours):", bg=WHITE, font=("Arial", 11, "bold")).grid(row=4, column=0, sticky="w", pady=5)
        self.time_entry = tk.Entry(content_frame, bg=WHITE, fg=TEXT, relief="solid", bd=1)
        self.time_entry.grid(row=4, column=1, sticky="ew", pady=5)

        content_frame.grid_columnconfigure(1, weight=1)

        # Action Buttons
        buttons_frame = tk.Frame(details_frame, bg=WHITE)
        buttons_frame.pack(fill="x", padx=15, pady=15)

        update_btn = tk.Button(buttons_frame, text="Update Issue", bg=BLUE, fg=WHITE, relief="flat", bd=0, font=("Arial", 10, "bold"), cursor="hand2", activebackground=DARK_BLUE, command=self.update_issue)
        update_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

        notify_btn = tk.Button(buttons_frame, text="Notify Tenant", bg=LIGHT_BUTTON, fg=TEXT, relief="flat", bd=0, font=("Arial", 10, "bold"), cursor="hand2", activebackground=LIGHT_BUTTON_HOVER, command=self.notify_tenant)
        notify_btn.pack(side="left", expand=True, fill="x", padx=(5, 0))

    def create_worker_status_section(self, parent):
        #Creates the section for managing worker availability
        worker_frame = self.create_section_frame(parent, "Worker Availability")
        worker_frame.grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky="nsew")

        self.worker_list_frame = tk.Frame(worker_frame, bg=WHITE)
        self.worker_list_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.update_worker_display()

    def populate_issues_list(self):
        #Clears and repopulates the issues treeview with current data
        for item in self.issues_tree.get_children():
            self.issues_tree.delete(item)
        for issue in self.maintenance_issues:
            self.issues_tree.insert("", "end", values=(issue["id"], issue["apartment"], issue["issue"], issue["priority"], issue["status"]))

    def on_issue_select(self, event):
        #Handles selection of an issue in the treeview, populating the details form
        selected_item = self.issues_tree.selection()
        if not selected_item:
            return
        
        item_values = self.issues_tree.item(selected_item, "values")
        issue_id = int(item_values[0])
        
        # Find the full issue dictionary
        selected_issue = next((issue for issue in self.maintenance_issues if issue["id"] == issue_id), None)
        
        if selected_issue:
            self.priority_var.set(selected_issue["priority"])
            self.status_var.set(selected_issue["status"])
            self.worker_var.set(selected_issue["worker"])
            self.cost_entry.delete(0, tk.END)
            self.cost_entry.insert(0, str(selected_issue["cost"]))
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, str(selected_issue["time"]))

    def update_issue(self):
        #Updates the selected maintenance issue with data from the form
        selected_item = self.issues_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a maintenance issue to update.")
            return

        item_values = self.issues_tree.item(selected_item, "values")
        issue_id = int(item_values[0])
        
        try:
            cost = float(self.cost_entry.get())
            time = float(self.time_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Cost and Time must be valid numbers.")
            return

        # Update the data source
        for issue in self.maintenance_issues:
            if issue["id"] == issue_id:
                issue["priority"] = self.priority_var.get()
                issue["status"] = self.status_var.get()
                issue["worker"] = self.worker_var.get()
                issue["cost"] = cost
                issue["time"] = time
                break
        
        self.populate_issues_list()
        messagebox.showinfo("Success", f"Issue #{issue_id} has been updated.")

    def notify_tenant(self):
        #Simulates sending a notification to the tenant
        selected_item = self.issues_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an issue to send a notification for.")
            return
        
        item_values = self.issues_tree.item(selected_item, "values")
        apartment = item_values[1]
        
        messagebox.showinfo("Notification Sent", f"A maintenance update has been sent to the tenant of apartment {apartment}.")

    def update_worker_display(self):
        #Updates the list of workers and their statuses
        for widget in self.worker_list_frame.winfo_children():
            widget.destroy()

        row = 0
        for worker, status in self.workers.items():
            tk.Label(self.worker_list_frame, text=worker, bg=WHITE, font=("Arial", 11)).grid(row=row, column=0, sticky="w", pady=2)
            
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