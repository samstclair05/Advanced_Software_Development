#Lonique Mayoua 24027974

import tkinter as tk
from tkinter import ttk
from services.report_services import (
    service_get_summary_report,
    service_get_maintenance_cost_report,
    service_get_financial_summary,
)

# Colour and Font Constants
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

VALID_LOCATIONS = ["Bristol", "Cardiff", "London", "Manchester"]


class ReportPage(tk.Frame):

    def __init__(self, parent, current_user):
        super().__init__(parent, bg=LIGHT_BG)
        self.current_user = current_user
        self.create_widgets()

    def _is_admin(self):
        return self.current_user.get("role", "").lower() == "administrator"

    def _get_requested_location(self):
        """Return chosen location for admins, None for everyone else."""
        if self._is_admin() and hasattr(self, "admin_location_var"):
            return self.admin_location_var.get()
        return None

    def create_widgets(self):

        # Page Header
        tk.Label(self, text="Reports & Analytics", bg=LIGHT_BG, fg=TEXT,
                 font=("Arial", 24, "bold")).pack(anchor="nw", padx=25, pady=(20, 5))

        tk.Label(self, text="Generate and view key operational insights.",
                 bg=LIGHT_BG, fg=SUBTEXT, font=("Arial", 12)).pack(anchor="nw", padx=25, pady=(0, 10))

        # Admin location picker
        if self._is_admin():
            loc_frame = tk.Frame(self, bg=LIGHT_BG)
            loc_frame.pack(anchor="nw", padx=25, pady=(0, 15))

            tk.Label(loc_frame, text="Reporting Location:", bg=LIGHT_BG, fg=TEXT,
                     font=("Arial", 11, "bold")).pack(side="left", padx=(0, 10))

            self.admin_location_var = tk.StringVar(
                value=self.current_user.get("location") or VALID_LOCATIONS[0]
            )
            ttk.Combobox(
                loc_frame,
                textvariable=self.admin_location_var,
                values=VALID_LOCATIONS,
                state="readonly",
                width=15,
                font=("Arial", 11)
            ).pack(side="left")

        # Three report columns
        main_frame = tk.Frame(self, bg=LIGHT_BG)
        main_frame.pack(fill="both", expand=True, padx=25)
        main_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        main_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        main_frame.grid_columnconfigure(2, weight=1, uniform="group1")

        self.create_occupancy_section(main_frame)
        self.create_financial_section(main_frame)
        self.create_maintenance_section(main_frame)

  
    def create_section_frame(self, parent, title_text):
        frame = tk.Frame(parent, bg=WHITE, highlightbackground=BORDER_COLOR, highlightthickness=1)
        tk.Label(frame, text=title_text, bg=WHITE, fg=TEXT,
                 font=("Arial", 14, "bold")).pack(anchor="nw", padx=15, pady=(15, 10))
        return frame

 
    def create_occupancy_section(self, parent):
        frame = self.create_section_frame(parent, "Occupancy Reports")
        frame.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")

        tk.Button(
            frame, text="Generate", bg=LIGHT_BUTTON, fg=TEXT,
            relief="flat", font=("Arial", 10, "bold"), cursor="hand2",
            activebackground=LIGHT_BUTTON_HOVER,
            command=self.generate_occupancy_report
        ).pack(pady=(0, 10))

        self.occupancy_result = tk.Label(
            frame, text="Click 'Generate' to see the latest occupancy summary.",
            bg=WHITE, fg=SUBTEXT, font=("Arial", 11), wraplength=260, justify="left"
        )
        self.occupancy_result.pack(pady=10, padx=15)

    def generate_occupancy_report(self):
        result = service_get_summary_report(self.current_user, self._get_requested_location())
        if result["success"]:
            d = result["data"]
            self.occupancy_result.config(fg=TEXT, text=(
                f"Location: {result['location']}\n\n"
                f"Total Apartments:  {d['total_apartments']}\n"
                f"Occupied:          {d['occupied_apartments']}\n"
                f"Vacant:            {d['vacant_apartments']}\n"
                f"Active Tenants:    {d['total_tenants']}"
            ))
        else:
            self.occupancy_result.config(fg="red", text=f"Error: {result['error']}")

   

    def create_financial_section(self, parent):
        frame = self.create_section_frame(parent, "Financial Summary")
        frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        content = tk.Frame(frame, bg=WHITE)
        content.pack(fill="x", padx=15, pady=10)
        content.grid_columnconfigure(1, weight=1)

        tk.Label(content, text="Collected Rent:", bg=WHITE, fg=TEXT,
                 font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.collected_rent_label = tk.Label(content, text="£---", bg=WHITE, fg="green", font=("Arial", 11))
        self.collected_rent_label.grid(row=0, column=1, sticky="e", padx=10)

        tk.Label(content, text="Pending Rent:", bg=WHITE, fg=TEXT,
                 font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        self.pending_rent_label = tk.Label(content, text="£---", bg=WHITE, fg="orange", font=("Arial", 11))
        self.pending_rent_label.grid(row=1, column=1, sticky="e", padx=10)

        tk.Button(
            frame, text="Refresh Financials", bg=LIGHT_BUTTON, fg=TEXT,
            relief="flat", font=("Arial", 10, "bold"), cursor="hand2",
            activebackground=LIGHT_BUTTON_HOVER,
            command=self.generate_financial_report
        ).pack(pady=10)

        self.financial_error = tk.Label(frame, text="", bg=WHITE, fg="red",
                                        font=("Arial", 10), wraplength=260)
        self.financial_error.pack(padx=15, pady=(0, 10))

    def generate_financial_report(self):
        result = service_get_financial_summary(self.current_user, self._get_requested_location())
        if result["success"]:
            d = result["data"]
            self.collected_rent_label.config(text=f"£{d['collected_rent']:,.2f}")
            self.pending_rent_label.config(text=f"£{d['pending_rent']:,.2f}")
            self.financial_error.config(text="")
        else:
            self.financial_error.config(text=result["error"])

 

    def create_maintenance_section(self, parent):
        frame = self.create_section_frame(parent, "Maintenance Costs")
        frame.grid(row=0, column=2, padx=(10, 0), pady=10, sticky="nsew")

        content = tk.Frame(frame, bg=WHITE)
        content.pack(fill="x", padx=15, pady=10)
        content.grid_columnconfigure(1, weight=1)

        tk.Label(content, text="Total Cost:", bg=WHITE, fg=TEXT,
                 font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.maintenance_cost_label = tk.Label(content, text="£---", bg=WHITE, fg="red", font=("Arial", 11))
        self.maintenance_cost_label.grid(row=0, column=1, sticky="e", padx=10)

        tk.Button(
            frame, text="Refresh Maintenance", bg=LIGHT_BUTTON, fg=TEXT,
            relief="flat", font=("Arial", 10, "bold"), cursor="hand2",
            activebackground=LIGHT_BUTTON_HOVER,
            command=self.generate_maintenance_report
        ).pack(pady=10)

        self.maintenance_error = tk.Label(frame, text="", bg=WHITE, fg="red",
                                          font=("Arial", 10), wraplength=260)
        self.maintenance_error.pack(padx=15, pady=(0, 10))

    def generate_maintenance_report(self):
        result = service_get_maintenance_cost_report(self.current_user, self._get_requested_location())
        if result["success"]:
            d = result["data"]
            self.maintenance_cost_label.config(text=f"£{d['total_maintenance_cost']:,.2f}")
            self.maintenance_error.config(text="")
        else:
            self.maintenance_error.config(text=result["error"])