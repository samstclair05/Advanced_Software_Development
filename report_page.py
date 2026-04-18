import tkinter as tk
from tkinter import ttk, messagebox


LIGHT_BG = "#F4F6F8"
WHITE = "#FFFFFF"
TEXT = "#222222"
SUBTEXT = "#6B7280"
BLUE = "#2F5D8C"
DARK_BLUE = "#24496E"
NAVY = "#1E2A38"
LIGHT_BUTTON = "#E5E7EB"
LIGHT_BUTTON_HOVER = "#D1D5DB"


class ReportPage:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Operational Reports")
        self.root.configure(bg=LIGHT_BG)
        self.root.geometry("1280x840")
        self.root.minsize(1180, 760)

        self.occupancy_rows = []
        self.financial_rows = []
        self.maintenance_rows = []

        self.selected_occupancy_index = None
        self.selected_financial_index = None
        self.selected_maintenance_index = None

        self._configure_styles()
        self._build_layout()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Card.TFrame", background=WHITE)
        style.configure("Header.TLabel", background=LIGHT_BG, foreground=NAVY, font=("Segoe UI", 18, "bold"))
        style.configure("SectionTitle.TLabel", background=WHITE, foreground=TEXT, font=("Segoe UI", 14, "bold"))
        style.configure("Body.TLabel", background=WHITE, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Sub.TLabel", background=WHITE, foreground=SUBTEXT, font=("Segoe UI", 9))
        style.configure("Metric.TLabel", background=WHITE, foreground=BLUE, font=("Segoe UI", 11, "bold"))
        style.configure("TEntry", fieldbackground=WHITE, foreground=TEXT)
        style.configure("Treeview", rowheight=24, font=("Segoe UI", 9), background=WHITE, foreground=TEXT)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background=LIGHT_BUTTON, foreground=TEXT)

    def _build_layout(self):
        container = ttk.Frame(self.root, style="Card.TFrame", padding=18)
        container.pack(fill="both", expand=True, padx=16, pady=16)

        ttk.Label(container, text="Operational Insights Report", style="Header.TLabel").pack(anchor="w", pady=(0, 12))

        content = ttk.Frame(container, style="Card.TFrame")
        content.pack(fill="both", expand=True)

        self._build_occupancy_section(content)
        self._build_financial_section(content)
        self._build_maintenance_section(content)

    def _make_button(self, parent, text, command, primary=False):
        bg = BLUE if primary else LIGHT_BUTTON
        fg = WHITE if primary else TEXT
        active_bg = DARK_BLUE if primary else LIGHT_BUTTON_HOVER
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=fg,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            padx=12,
            pady=6,
        )
        return button

    def _section_card(self, parent, title, row):
        frame = ttk.Frame(parent, style="Card.TFrame", padding=14)
        frame.grid(row=row, column=0, sticky="nsew", pady=(0, 12))
        ttk.Label(frame, text=title, style="SectionTitle.TLabel").pack(anchor="w", pady=(0, 10))
        return frame

    def _build_occupancy_section(self, parent):
        card = self._section_card(parent, "Occupancy Reports", 0)

        form = ttk.Frame(card, style="Card.TFrame")
        form.pack(fill="x")
        form.columnconfigure((0, 1, 2, 3), weight=1)

        ttk.Label(form, text="Apartment", style="Body.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Label(form, text="City", style="Body.TLabel").grid(row=0, column=1, sticky="w", padx=(0, 8))
        ttk.Label(form, text="Units", style="Body.TLabel").grid(row=0, column=2, sticky="w", padx=(0, 8))
        ttk.Label(form, text="Occupied", style="Body.TLabel").grid(row=0, column=3, sticky="w")

        self.occ_apartment = ttk.Entry(form)
        self.occ_city = ttk.Entry(form)
        self.occ_units = ttk.Entry(form)
        self.occ_occupied = ttk.Entry(form)
        self.occ_apartment.grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(0, 10))
        self.occ_city.grid(row=1, column=1, sticky="ew", padx=(0, 8), pady=(0, 10))
        self.occ_units.grid(row=1, column=2, sticky="ew", padx=(0, 8), pady=(0, 10))
        self.occ_occupied.grid(row=1, column=3, sticky="ew", pady=(0, 10))

        filters = ttk.Frame(card, style="Card.TFrame")
        filters.pack(fill="x", pady=(0, 8))
        ttk.Label(filters, text="Filter by Apartment", style="Sub.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(filters, text="Filter by City", style="Sub.TLabel").grid(row=0, column=1, sticky="w", padx=(8, 0))
        self.filter_apartment = ttk.Entry(filters)
        self.filter_city = ttk.Entry(filters)
        self.filter_apartment.grid(row=1, column=0, sticky="ew")
        self.filter_city.grid(row=1, column=1, sticky="ew", padx=(8, 0))
        filters.columnconfigure((0, 1), weight=1)

        btns = tk.Frame(card, bg=WHITE)
        btns.pack(fill="x", pady=(0, 10))
        self._make_button(btns, "Add", self.add_occupancy, primary=True).pack(side="left", padx=(0, 6))
        self._make_button(btns, "Update", self.update_occupancy).pack(side="left", padx=(0, 6))
        self._make_button(btns, "Delete", self.delete_occupancy).pack(side="left", padx=(0, 6))
        self._make_button(btns, "Clear", self.clear_occupancy).pack(side="left", padx=(0, 6))
        self._make_button(btns, "Apply Filters", self.refresh_occupancy_view).pack(side="left")

        metrics = ttk.Frame(card, style="Card.TFrame")
        metrics.pack(fill="x", pady=(0, 8))
        self.occ_total_label = ttk.Label(metrics, text="Total Units: 0", style="Metric.TLabel")
        self.occ_occ_label = ttk.Label(metrics, text="Occupied Units: 0", style="Metric.TLabel")
        self.occ_rate_label = ttk.Label(metrics, text="Occupancy Rate: 0.00%", style="Metric.TLabel")
        self.occ_total_label.grid(row=0, column=0, sticky="w", padx=(0, 14))
        self.occ_occ_label.grid(row=0, column=1, sticky="w", padx=(0, 14))
        self.occ_rate_label.grid(row=0, column=2, sticky="w")

        self.occ_tree = ttk.Treeview(card, columns=("apartment", "city", "units", "occupied", "status"), show="headings", height=6)
        for col, title in (("apartment", "Apartment"), ("city", "City"), ("units", "Units"), ("occupied", "Occupied"), ("status", "Status")):
            self.occ_tree.heading(col, text=title)
            self.occ_tree.column(col, anchor="w", width=150)
        self.occ_tree.pack(fill="x")
        self.occ_tree.bind("<<TreeviewSelect>>", self.on_occupancy_select)

    def _build_financial_section(self, parent):
        card = self._section_card(parent, "Financial Summary", 1)

        form = ttk.Frame(card, style="Card.TFrame")
        form.pack(fill="x")
        form.columnconfigure((0, 1, 2, 3), weight=1)

        ttk.Label(form, text="Apartment", style="Body.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Label(form, text="Collected Rent", style="Body.TLabel").grid(row=0, column=1, sticky="w", padx=(0, 8))
        ttk.Label(form, text="Pending Rent", style="Body.TLabel").grid(row=0, column=2, sticky="w", padx=(0, 8))
        ttk.Label(form, text="Payment Status", style="Body.TLabel").grid(row=0, column=3, sticky="w")

        self.fin_apartment = ttk.Entry(form)
        self.fin_collected = ttk.Entry(form)
        self.fin_pending = ttk.Entry(form)
        self.fin_status = ttk.Entry(form)
        self.fin_apartment.grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(0, 10))
        self.fin_collected.grid(row=1, column=1, sticky="ew", padx=(0, 8), pady=(0, 10))
        self.fin_pending.grid(row=1, column=2, sticky="ew", padx=(0, 8), pady=(0, 10))
        self.fin_status.grid(row=1, column=3, sticky="ew", pady=(0, 10))

        btns = tk.Frame(card, bg=WHITE)
        btns.pack(fill="x", pady=(0, 10))
        self._make_button(btns, "Add", self.add_financial, primary=True).pack(side="left", padx=(0, 6))
        self._make_button(btns, "Update", self.update_financial).pack(side="left", padx=(0, 6))
        self._make_button(btns, "Delete", self.delete_financial).pack(side="left", padx=(0, 6))
        self._make_button(btns, "Clear", self.clear_financial).pack(side="left")

        metrics = ttk.Frame(card, style="Card.TFrame")
        metrics.pack(fill="x", pady=(0, 8))
        self.fin_collected_label = ttk.Label(metrics, text="Collected Total: $0.00", style="Metric.TLabel")
        self.fin_pending_label = ttk.Label(metrics, text="Pending Total: $0.00", style="Metric.TLabel")
        self.fin_ratio_label = ttk.Label(metrics, text="Collection Ratio: 0.00%", style="Metric.TLabel")
        self.fin_collected_label.grid(row=0, column=0, sticky="w", padx=(0, 14))
        self.fin_pending_label.grid(row=0, column=1, sticky="w", padx=(0, 14))
        self.fin_ratio_label.grid(row=0, column=2, sticky="w")

        self.fin_tree = ttk.Treeview(card, columns=("apartment", "collected", "pending", "status"), show="headings", height=6)
        for col, title in (("apartment", "Apartment"), ("collected", "Collected"), ("pending", "Pending"), ("status", "Status")):
            self.fin_tree.heading(col, text=title)
            self.fin_tree.column(col, anchor="w", width=170)
        self.fin_tree.pack(fill="x")
        self.fin_tree.bind("<<TreeviewSelect>>", self.on_financial_select)

    def _build_maintenance_section(self, parent):
        card = self._section_card(parent, "Maintenance Costs", 2)

        form = ttk.Frame(card, style="Card.TFrame")
        form.pack(fill="x")
        form.columnconfigure((0, 1, 2, 3), weight=1)

        ttk.Label(form, text="Apartment", style="Body.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Label(form, text="Category", style="Body.TLabel").grid(row=0, column=1, sticky="w", padx=(0, 8))
        ttk.Label(form, text="Cost", style="Body.TLabel").grid(row=0, column=2, sticky="w", padx=(0, 8))
        ttk.Label(form, text="Details", style="Body.TLabel").grid(row=0, column=3, sticky="w")

        self.maint_apartment = ttk.Entry(form)
        self.maint_category = ttk.Entry(form)
        self.maint_cost = ttk.Entry(form)
        self.maint_details = ttk.Entry(form)
        self.maint_apartment.grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(0, 10))
        self.maint_category.grid(row=1, column=1, sticky="ew", padx=(0, 8), pady=(0, 10))
        self.maint_cost.grid(row=1, column=2, sticky="ew", padx=(0, 8), pady=(0, 10))
        self.maint_details.grid(row=1, column=3, sticky="ew", pady=(0, 10))

        btns = tk.Frame(card, bg=WHITE)
        btns.pack(fill="x", pady=(0, 10))
        self._make_button(btns, "Add", self.add_maintenance, primary=True).pack(side="left", padx=(0, 6))
        self._make_button(btns, "Update", self.update_maintenance).pack(side="left", padx=(0, 6))
        self._make_button(btns, "Delete", self.delete_maintenance).pack(side="left", padx=(0, 6))
        self._make_button(btns, "Clear", self.clear_maintenance).pack(side="left")

        metrics = ttk.Frame(card, style="Card.TFrame")
        metrics.pack(fill="x", pady=(0, 8))
        self.maint_total_label = ttk.Label(metrics, text="Maintenance Total: $0.00", style="Metric.TLabel")
        self.maint_count_label = ttk.Label(metrics, text="Entries: 0", style="Metric.TLabel")
        self.maint_total_label.grid(row=0, column=0, sticky="w", padx=(0, 14))
        self.maint_count_label.grid(row=0, column=1, sticky="w")

        self.maint_tree = ttk.Treeview(card, columns=("apartment", "category", "cost", "details"), show="headings", height=6)
        for col, title in (("apartment", "Apartment"), ("category", "Category"), ("cost", "Cost"), ("details", "Details")):
            self.maint_tree.heading(col, text=title)
            self.maint_tree.column(col, anchor="w", width=170)
        self.maint_tree.pack(fill="x")
        self.maint_tree.bind("<<TreeviewSelect>>", self.on_maintenance_select)

    @staticmethod
    def _to_float(value, field_name):
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"{field_name} must be a number.")

    @staticmethod
    def _to_int(value, field_name):
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"{field_name} must be an integer.")

    def add_occupancy(self):
        apartment = self.occ_apartment.get().strip()
        city = self.occ_city.get().strip()
        units = self.occ_units.get().strip()
        occupied = self.occ_occupied.get().strip()
        if not (apartment and city and units and occupied):
            messagebox.showwarning("Missing data", "Please fill all Occupancy fields.")
            return
        try:
            units_val = self._to_int(units, "Units")
            occupied_val = self._to_int(occupied, "Occupied")
            if units_val < 0 or occupied_val < 0 or occupied_val > units_val:
                raise ValueError("Occupied must be between 0 and Units.")
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))
            return

        status = "Full" if occupied_val == units_val else "Partial" if occupied_val > 0 else "Vacant"
        self.occupancy_rows.append({"apartment": apartment, "city": city, "units": units_val, "occupied": occupied_val, "status": status})
        self.clear_occupancy(clear_selection=False)
        self.refresh_occupancy_view()

    def update_occupancy(self):
        if self.selected_occupancy_index is None:
            messagebox.showinfo("Select record", "Please select an occupancy record to update.")
            return

        apartment = self.occ_apartment.get().strip()
        city = self.occ_city.get().strip()
        units = self.occ_units.get().strip()
        occupied = self.occ_occupied.get().strip()
        if not (apartment and city and units and occupied):
            messagebox.showwarning("Missing data", "Please fill all Occupancy fields.")
            return

        try:
            units_val = self._to_int(units, "Units")
            occupied_val = self._to_int(occupied, "Occupied")
            if units_val < 0 or occupied_val < 0 or occupied_val > units_val:
                raise ValueError("Occupied must be between 0 and Units.")
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))
            return

        status = "Full" if occupied_val == units_val else "Partial" if occupied_val > 0 else "Vacant"
        self.occupancy_rows[self.selected_occupancy_index] = {
            "apartment": apartment,
            "city": city,
            "units": units_val,
            "occupied": occupied_val,
            "status": status,
        }
        self.clear_occupancy()
        self.refresh_occupancy_view()

    def delete_occupancy(self):
        if self.selected_occupancy_index is None:
            messagebox.showinfo("Select record", "Please select an occupancy record to delete.")
            return
        del self.occupancy_rows[self.selected_occupancy_index]
        self.clear_occupancy()
        self.refresh_occupancy_view()

    def clear_occupancy(self, clear_selection=True):
        for entry in (self.occ_apartment, self.occ_city, self.occ_units, self.occ_occupied):
            entry.delete(0, tk.END)
        if clear_selection:
            self.selected_occupancy_index = None

    def refresh_occupancy_view(self):
        for item in self.occ_tree.get_children():
            self.occ_tree.delete(item)

        apt_filter = self.filter_apartment.get().strip().lower()
        city_filter = self.filter_city.get().strip().lower()

        total_units = 0
        total_occupied = 0
        for i, row in enumerate(self.occupancy_rows):
            if apt_filter and apt_filter not in row["apartment"].lower():
                continue
            if city_filter and city_filter not in row["city"].lower():
                continue
            self.occ_tree.insert("", "end", iid=str(i), values=(row["apartment"], row["city"], row["units"], row["occupied"], row["status"]))
            total_units += row["units"]
            total_occupied += row["occupied"]

        rate = (total_occupied / total_units * 100) if total_units else 0
        self.occ_total_label.config(text=f"Total Units: {total_units}")
        self.occ_occ_label.config(text=f"Occupied Units: {total_occupied}")
        self.occ_rate_label.config(text=f"Occupancy Rate: {rate:.2f}%")

    def on_occupancy_select(self, _event):
        selected = self.occ_tree.selection()
        if not selected:
            return
        index = int(selected[0])
        row = self.occupancy_rows[index]
        self.selected_occupancy_index = index
        self.clear_occupancy(clear_selection=False)
        self.occ_apartment.insert(0, row["apartment"])
        self.occ_city.insert(0, row["city"])
        self.occ_units.insert(0, str(row["units"]))
        self.occ_occupied.insert(0, str(row["occupied"]))

    def add_financial(self):
        apartment = self.fin_apartment.get().strip()
        collected = self.fin_collected.get().strip()
        pending = self.fin_pending.get().strip()
        status = self.fin_status.get().strip()
        if not (apartment and collected and pending and status):
            messagebox.showwarning("Missing data", "Please fill all Financial fields.")
            return

        try:
            collected_val = self._to_float(collected, "Collected Rent")
            pending_val = self._to_float(pending, "Pending Rent")
            if collected_val < 0 or pending_val < 0:
                raise ValueError("Rent values cannot be negative.")
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))
            return

        self.financial_rows.append(
            {
                "apartment": apartment,
                "collected": collected_val,
                "pending": pending_val,
                "status": status,
            }
        )
        self.clear_financial(clear_selection=False)
        self.refresh_financial_view()

    def update_financial(self):
        if self.selected_financial_index is None:
            messagebox.showinfo("Select record", "Please select a financial record to update.")
            return

        apartment = self.fin_apartment.get().strip()
        collected = self.fin_collected.get().strip()
        pending = self.fin_pending.get().strip()
        status = self.fin_status.get().strip()
        if not (apartment and collected and pending and status):
            messagebox.showwarning("Missing data", "Please fill all Financial fields.")
            return

        try:
            collected_val = self._to_float(collected, "Collected Rent")
            pending_val = self._to_float(pending, "Pending Rent")
            if collected_val < 0 or pending_val < 0:
                raise ValueError("Rent values cannot be negative.")
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))
            return

        self.financial_rows[self.selected_financial_index] = {
            "apartment": apartment,
            "collected": collected_val,
            "pending": pending_val,
            "status": status,
        }
        self.clear_financial()
        self.refresh_financial_view()

    def delete_financial(self):
        if self.selected_financial_index is None:
            messagebox.showinfo("Select record", "Please select a financial record to delete.")
            return
        del self.financial_rows[self.selected_financial_index]
        self.clear_financial()
        self.refresh_financial_view()

    def clear_financial(self, clear_selection=True):
        for entry in (self.fin_apartment, self.fin_collected, self.fin_pending, self.fin_status):
            entry.delete(0, tk.END)
        if clear_selection:
            self.selected_financial_index = None

    def refresh_financial_view(self):
        for item in self.fin_tree.get_children():
            self.fin_tree.delete(item)

        total_collected = 0.0
        total_pending = 0.0

        for i, row in enumerate(self.financial_rows):
            self.fin_tree.insert(
                "",
                "end",
                iid=str(i),
                values=(row["apartment"], f"${row['collected']:.2f}", f"${row['pending']:.2f}", row["status"]),
            )
            total_collected += row["collected"]
            total_pending += row["pending"]

        total_due = total_collected + total_pending
        ratio = (total_collected / total_due * 100) if total_due else 0
        self.fin_collected_label.config(text=f"Collected Total: ${total_collected:.2f}")
        self.fin_pending_label.config(text=f"Pending Total: ${total_pending:.2f}")
        self.fin_ratio_label.config(text=f"Collection Ratio: {ratio:.2f}%")

    def on_financial_select(self, _event):
        selected = self.fin_tree.selection()
        if not selected:
            return
        index = int(selected[0])
        row = self.financial_rows[index]
        self.selected_financial_index = index
        self.clear_financial(clear_selection=False)
        self.fin_apartment.insert(0, row["apartment"])
        self.fin_collected.insert(0, str(row["collected"]))
        self.fin_pending.insert(0, str(row["pending"]))
        self.fin_status.insert(0, row["status"])

    def add_maintenance(self):
        apartment = self.maint_apartment.get().strip()
        category = self.maint_category.get().strip()
        cost = self.maint_cost.get().strip()
        details = self.maint_details.get().strip()
        if not (apartment and category and cost and details):
            messagebox.showwarning("Missing data", "Please fill all Maintenance fields.")
            return

        try:
            cost_val = self._to_float(cost, "Cost")
            if cost_val < 0:
                raise ValueError("Cost cannot be negative.")
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))
            return

        self.maintenance_rows.append(
            {"apartment": apartment, "category": category, "cost": cost_val, "details": details}
        )
        self.clear_maintenance(clear_selection=False)
        self.refresh_maintenance_view()

    def update_maintenance(self):
        if self.selected_maintenance_index is None:
            messagebox.showinfo("Select record", "Please select a maintenance record to update.")
            return

        apartment = self.maint_apartment.get().strip()
        category = self.maint_category.get().strip()
        cost = self.maint_cost.get().strip()
        details = self.maint_details.get().strip()
        if not (apartment and category and cost and details):
            messagebox.showwarning("Missing data", "Please fill all Maintenance fields.")
            return

        try:
            cost_val = self._to_float(cost, "Cost")
            if cost_val < 0:
                raise ValueError("Cost cannot be negative.")
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))
            return

        self.maintenance_rows[self.selected_maintenance_index] = {
            "apartment": apartment,
            "category": category,
            "cost": cost_val,
            "details": details,
        }
        self.clear_maintenance()
        self.refresh_maintenance_view()

    def delete_maintenance(self):
        if self.selected_maintenance_index is None:
            messagebox.showinfo("Select record", "Please select a maintenance record to delete.")
            return
        del self.maintenance_rows[self.selected_maintenance_index]
        self.clear_maintenance()
        self.refresh_maintenance_view()

    def clear_maintenance(self, clear_selection=True):
        for entry in (self.maint_apartment, self.maint_category, self.maint_cost, self.maint_details):
            entry.delete(0, tk.END)
        if clear_selection:
            self.selected_maintenance_index = None

    def refresh_maintenance_view(self):
        for item in self.maint_tree.get_children():
            self.maint_tree.delete(item)

        total_cost = 0.0
        for i, row in enumerate(self.maintenance_rows):
            self.maint_tree.insert(
                "",
                "end",
                iid=str(i),
                values=(row["apartment"], row["category"], f"${row['cost']:.2f}", row["details"]),
            )
            total_cost += row["cost"]

        self.maint_total_label.config(text=f"Maintenance Total: ${total_cost:.2f}")
        self.maint_count_label.config(text=f"Entries: {len(self.maintenance_rows)}")

    def on_maintenance_select(self, _event):
        selected = self.maint_tree.selection()
        if not selected:
            return
        index = int(selected[0])
        row = self.maintenance_rows[index]
        self.selected_maintenance_index = index
        self.clear_maintenance(clear_selection=False)
        self.maint_apartment.insert(0, row["apartment"])
        self.maint_category.insert(0, row["category"])
        self.maint_cost.insert(0, str(row["cost"]))
        self.maint_details.insert(0, row["details"])


def main():
    root = tk.Tk()
    ReportPage(root)
    root.mainloop()


if __name__ == "__main__":
    main()
