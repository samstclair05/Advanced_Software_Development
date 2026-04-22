import tkinter as tk
from tkinter import ttk
# Import your services
from services.report_services import service_get_summary_report, service_get_maintenance_cost_report, service_get_financial_summary

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

        #Input and Generate Button
        input_frame = tk.Frame(occupancy_frame, bg=WHITE)
        input_frame.pack(fill="x", padx=15, pady=10)

        generate_btn = tk.Button(
            input_frame, text="Generate", bg=LIGHT_BUTTON, fg=TEXT, relief="flat", bd=0,
            font=("Arial", 10, "bold"), cursor="hand2", activebackground=LIGHT_BUTTON_HOVER,
            command=self.generate_occupancy_report
        )
        generate_btn.pack(pady=5)

        #Placeholder for report content
        self.occupancy_report_label = tk.Label(occupancy_frame, text="Click 'Generate' to see the latest occupancy summary.", bg=WHITE, fg=SUBTEXT, font=("Arial", 11), justify="left")
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

    def generate_occupancy_report(self):
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
        self.fin_report_label.config(text="Fetching financial data...", fg="blue")
        
        # Call the service
        fin_response = service_get_financial_summary(self.current_user)
        
        if not fin_response["success"]:
            self.fin_report_label.config(text=f"Error: {fin_response.get('error')}", fg="red")
            return
            
        data = fin_response["data"]
        # Update the UI labels
        self.collected_rent_label.config(text=f"£{data['collected_rent']:.2f}")
        self.pending_rent_label.config(text=f"£{data['pending_rent']:.2f}")
        self.fin_report_label.config(text="Financial data loaded.", fg="green")

if __name__ == '__main__':
    #Main application window for testing
    root = tk.Tk()
    root.title("Report Page Demo")
    root.geometry("1200x700")
    
    report_page = ReportPage(root)
    report_page.pack(fill="both", expand=True)
    
    root.mainloop()