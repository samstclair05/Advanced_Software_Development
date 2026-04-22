import tkinter as tk
from tkinter import ttk
# Import your services
from services.report_services import service_get_summary_report, service_get_maintenance_cost_report

#Colour and Font Constants
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

class ReportPage(tk.Frame):
    
    #A page for generating and displaying operational reports for apartment management.
    def __init__(self, parent, current_user=None):
        super().__init__(parent, bg=LIGHT_BG)
        # Store current user state for access control
        self.current_user = current_user or {"role": "Administrator"} # Defaulting for testing
        self.create_widgets()

        # You can automatically load data on startup
        self.refresh_maintenance()
        self.refresh_financials()

    def create_widgets(self):
        
        #Page Header
        title = tk.Label(
            self,
            text="Reports & Analytics",
            bg=LIGHT_BG,
            fg=TEXT,
            font=("Arial", 24, "bold")
        )
        title.pack(anchor="nw", padx=25, pady=(20, 5))

        subtitle = tk.Label(
            self,
            text="Generate and view key operational insights.",
            bg=LIGHT_BG,
            fg=SUBTEXT,
            font=("Arial", 12)
        )
        subtitle.pack(anchor="nw", padx=25, pady=(0, 20))

        #Main container for the three report sections
        main_frame = tk.Frame(self, bg=LIGHT_BG)
        main_frame.pack(fill="both", expand=True, padx=25)

        main_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        main_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        main_frame.grid_columnconfigure(2, weight=1, uniform="group1")

        #1. Occupancy Reports Section
        self.create_occupancy_section(main_frame)

        #2. Financial Summary Section
        self.create_financial_section(main_frame)

        #3. Maintenance Costs Section
        self.create_maintenance_section(main_frame)

    def create_section_frame(self, parent, title_text):
        
        #Helper to create a styled section frame with a title
        frame = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )
        
        title = tk.Label(
            frame,
            text=title_text,
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 14, "bold")
        )
        title.pack(anchor="nw", padx=15, pady=(15, 10))
        
        return frame

    def create_occupancy_section(self, parent):
        #Creates the UI for generating occupancy reports
        occupancy_frame = self.create_section_frame(parent, "Occupancy Reports")
        occupancy_frame.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")

        #Filter controls
        controls_frame = tk.Frame(occupancy_frame, bg=WHITE)
        controls_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(controls_frame, text="Filter by:", bg=WHITE, fg=TEXT, font=("Arial", 11)).pack(side="left", anchor="w")
        
        self.occupancy_filter_var = tk.StringVar(value="Apartment")
        
        apartment_radio = tk.Radiobutton(controls_frame, text="Apartment", variable=self.occupancy_filter_var, value="Apartment", bg=WHITE, font=("Arial", 10), command=self.update_occupancy_hint)
        apartment_radio.pack(side="left", padx=10)
        
        city_radio = tk.Radiobutton(controls_frame, text="City", variable=self.occupancy_filter_var, value="City", bg=WHITE, font=("Arial", 10), command=self.update_occupancy_hint)
        city_radio.pack(side="left")

        #Input and Generate Button
        input_frame = tk.Frame(occupancy_frame, bg=WHITE)
        input_frame.pack(fill="x", padx=15, pady=10)

        self.occupancy_hint_label = tk.Label(input_frame, text="Enter Apt Name/ID:", bg=WHITE, fg=TEXT, font=("Arial", 10))
        self.occupancy_hint_label.pack(side="left", padx=(0, 5))

        self.occupancy_entry = tk.Entry(input_frame, width=20, bg=WHITE, fg=TEXT, insertbackground=TEXT, relief="solid", bd=1)
        self.occupancy_entry.pack(side="left", fill="x", expand=True)

        generate_btn = tk.Button(
            input_frame, text="Generate", bg=LIGHT_BUTTON, fg=TEXT, relief="flat", bd=0,
            font=("Arial", 10, "bold"), cursor="hand2", activebackground=LIGHT_BUTTON_HOVER,
            command=self.generate_occupancy_report
        )
        generate_btn.pack(side="left", padx=(10, 0))

        #Placeholder for report content
        self.occupancy_report_label = tk.Label(occupancy_frame, text="Select a filter, enter details, and click Generate.", bg=WHITE, fg=SUBTEXT, font=("Arial", 11), justify="left")
        self.occupancy_report_label.pack(pady=20, padx=15, fill="x")

    def create_financial_section(self, parent):
        #Creates the UI for the financial summary
        financial_frame = self.create_section_frame(parent, "Financial Summary")
        financial_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        #Content for financial summary
        summary_content = tk.Frame(financial_frame, bg=WHITE)
        summary_content.pack(fill="both", expand=True, padx=15, pady=10)

        tk.Label(summary_content, text="Collected Rent:", bg=WHITE, fg=TEXT, font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.collected_rent_label = tk.Label(summary_content, text="£---", bg=WHITE, fg="green", font=("Arial", 11))
        self.collected_rent_label.grid(row=0, column=1, sticky="e", padx=10)
        
        tk.Label(summary_content, text="Pending Rent:", bg=WHITE, fg=TEXT, font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        self.pending_rent_label = tk.Label(summary_content, text="£---", bg=WHITE, fg="orange", font=("Arial", 11))
        self.pending_rent_label.grid(row=1, column=1, sticky="e", padx=10)
        
        summary_content.grid_columnconfigure(1, weight=1)

        # Refresh button
        refresh_btn = tk.Button(
            financial_frame, text="Refresh Financials", bg=LIGHT_BUTTON, fg=TEXT, relief="flat", bd=0,
            font=("Arial", 10, "bold"), cursor="hand2", activebackground=LIGHT_BUTTON_HOVER,
            command=self.refresh_financials
        )
        refresh_btn.pack(pady=(0, 10))

        #Placeholder for detailed financial report
        self.fin_report_label = tk.Label(financial_frame, text="Financial details will appear here.", bg=WHITE, fg=SUBTEXT, font=("Arial", 11))
        self.fin_report_label.pack(pady=10, padx=15)

    def create_maintenance_section(self, parent):
        #Creates the UI for tracking maintenance costs
        maintenance_frame = self.create_section_frame(parent, "Maintenance Costs")
        maintenance_frame.grid(row=0, column=2, padx=(10, 0), pady=10, sticky="nsew")

        #Content for maintenance costs
        maintenance_content = tk.Frame(maintenance_frame, bg=WHITE)
        maintenance_content.pack(fill="both", expand=True, padx=15, pady=10)

        tk.Label(maintenance_content, text="Total This Month:", bg=WHITE, fg=TEXT, font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.month_maintenance_label = tk.Label(maintenance_content, text="£---", bg=WHITE, fg="red", font=("Arial", 11))
        self.month_maintenance_label.grid(row=0, column=1, sticky="e", padx=10)
        
        tk.Label(maintenance_content, text="Year-to-Date:", bg=WHITE, fg=TEXT, font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        self.ytd_maintenance_label = tk.Label(maintenance_content, text="£---", bg=WHITE, fg=TEXT, font=("Arial", 11))
        self.ytd_maintenance_label.grid(row=1, column=1, sticky="e", padx=10)
        
        maintenance_content.grid_columnconfigure(1, weight=1)

        # Refresh button
        refresh_btn = tk.Button(
            maintenance_frame, text="Refresh Maintenance", bg=LIGHT_BUTTON, fg=TEXT, relief="flat", bd=0,
            font=("Arial", 10, "bold"), cursor="hand2", activebackground=LIGHT_BUTTON_HOVER,
            command=self.refresh_maintenance
        )
        refresh_btn.pack(pady=(0, 10))

        #Placeholder for maintenance log
        self.maintenance_report_label = tk.Label(maintenance_frame, text="Maintenance log will appear here.", bg=WHITE, fg=SUBTEXT, font=("Arial", 11))
        self.maintenance_report_label.pack(pady=10, padx=15)

    def update_occupancy_hint(self):
        filter_type = self.occupancy_filter_var.get()
        if filter_type == "Apartment":
            self.occupancy_hint_label.config(text="Enter Apt Name/ID:")
        else:
            self.occupancy_hint_label.config(text="Enter City Name:")

    def generate_occupancy_report(self):
        filter_type = self.occupancy_filter_var.get()
        entered_val = self.occupancy_entry.get().strip()
        
        if not entered_val and filter_type != "All": # Just as an example
             # Handle validation
             pass

        # Call the service
        report_response = service_get_summary_report(self.current_user)
        
        if not report_response["success"]:
            self.occupancy_report_label.config(text=f"Error: {report_response.get('error')}", fg="red")
            return
            
        data = report_response["data"]
        self.occupancy_report_label.config(
            text=f"Total Apartments: {data['total_apartments']}\n"
                 f"Occupied: {data['occupied_apartments']}\n"
                 f"Vacant: {data['vacant_apartments']}", 
            fg="green"
        )

    def refresh_maintenance(self):
        self.maintenance_report_label.config(text="Fetching maintenance logs...", fg="blue")
        
        # Call the service
        maint_response = service_get_maintenance_cost_report(self.current_user)
        
        if not maint_response["success"]:
            self.maintenance_report_label.config(text=f"Error: {maint_response.get('error')}", fg="red")
            return
            
        data = maint_response["data"]
        # Update the UI labels
        self.month_maintenance_label.config(text=f"£{data['total_maintenance_cost']}")
        self.ytd_maintenance_label.config(text=f"£{data['total_maintenance_cost']}") # Adjust as per your service logic
        self.maintenance_report_label.config(text="Maintenance data loaded.", fg="green")

    def refresh_financials(self):
        # TODO: Retrieve financial data from the database
        self.fin_report_label.config(text="Fetching financial data...", fg="blue")

if __name__ == '__main__':
    #Main application window for testing
    root = tk.Tk()
    root.title("Report Page Demo")
    root.geometry("1200x700")
    
    report_page = ReportPage(root)
    report_page.pack(fill="both", expand=True)
    
    root.mainloop()