import sqlite3
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
from tkcalendar import DateEntry
from tkinter import Toplevel, Label, Button, messagebox
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from tkcalendar import DateEntry
import os
import calendar
from reportlab.lib.pagesizes import letter


class SalesReport:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Report")
        self.root.geometry("1100x500+220+130")
        self.root.config(bg="white")

        title = Label(self.root, text="Sales Report", font=("Arial", 20, "bold"), bg="#009688", fg="white", pady=10)
        title.pack(fill=X)

        # ======= Search Frame =======
        search_frame = Frame(self.root, bg="white")
        search_frame.pack(pady=10)

        Label(search_frame, text="Search by Product/Cashier:", font=("Arial", 12), bg="white").pack(side=LEFT, padx=5)
        self.search_var = StringVar()
        Entry(search_frame, textvariable=self.search_var, font=("Arial", 12), width=30).pack(side=LEFT, padx=5)
        Button(search_frame, text="Search", command=self.search_data, font=("Arial", 12), bg="#4CAF50", fg="white").pack(side=LEFT, padx=5)
        Button(search_frame, text="Show All", command=self.fetch_sales_data, font=("Arial", 12), bg="#607D8B", fg="white").pack(side=LEFT, padx=5)
        Button(search_frame, text="Print", command=self.print_report, font=("Arial", 12), bg="#2196F3", fg="white").pack(side=LEFT, padx=5)

        # ======= Sales Table with Scrollbar =======
        table_frame = Frame(self.root)
        table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Vertical scrollbar
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        # Horizontal scrollbar
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        # Create the Treeview
        self.sales_table = ttk.Treeview(table_frame,
                                        columns=("invoice", "product", "qty", "net", "amount", "change", "cashier", "date"),
                                        show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        # Configure vertical scrollbar
        scroll_y.config(command=self.sales_table.yview)

        # Configure horizontal scrollbar
        scroll_x.config(command=self.sales_table.xview)

        # Set the column headings
        headings = ["Invoice No.", "Product", "Quantity", "Net Total", "Amount Paid", "Change", "Cashier", "Date"]
        for i, col in enumerate(self.sales_table["columns"]):
            self.sales_table.heading(col, text=headings[i])
            self.sales_table.column(col, anchor=CENTER, width=150)

        # Pack the Treeview inside the frame
        self.sales_table.pack(fill=BOTH, expand=True)

        # Ensure both scrollbars are working with the Treeview
        scroll_y.config(command=self.sales_table.yview)
        scroll_x.config(command=self.sales_table.xview)

        # ======= Total Label =======
        self.lbl_summary = Label(self.root, text="Total Sales: ₱0.00", font=("Arial", 14), bg="white", fg="#333")
        self.lbl_summary.pack(pady=5)

        self.fetch_sales_data()

    def fetch_sales_data(self):
        try:
            con = sqlite3.connect(database="ims.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM sales ORDER BY date DESC")
            rows = cur.fetchall()
            self.populate_table(rows)
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to fetch sales data:\n{str(ex)}", parent=self.root)

    def search_data(self):
        search_text = self.search_var.get().strip()
        if not search_text:
            messagebox.showwarning("Input Needed", "Please enter search text.", parent=self.root)
            return
        try:
            con = sqlite3.connect(database="ims.db")
            cur = con.cursor()
            query = f"""SELECT * FROM sales 
                        WHERE product LIKE ? OR cashier LIKE ? 
                        ORDER BY date DESC"""
            search_param = f"%{search_text}%"
            cur.execute(query, (search_param, search_param))
            rows = cur.fetchall()
            self.populate_table(rows)
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to search data:\n{str(ex)}", parent=self.root)

    def populate_table(self, rows):
        from collections import defaultdict

        self.sales_table.delete(*self.sales_table.get_children())
        total_amount = 0

        # Group all data by invoice number
        grouped_data = defaultdict(list)
        invoice_summary = {}

        for row in rows:
            invoice, product, qty, amount, date, cashier, net = row

            # Group products by invoice
            grouped_data[invoice].append((product, qty))

            # Store invoice-level data only once
            if invoice not in invoice_summary:
                invoice_summary[invoice] = {
                    "amount": float(amount),
                    "net": float(net),
                    "date": date,
                    "cashier": cashier
                }
                total_amount += float(amount)  # Add amount only once per invoice

        # Populate the table with grouped data
        for invoice, items in grouped_data.items():
            amount = f"{invoice_summary[invoice]['net']:.2f}"
            net = f"{invoice_summary[invoice]['net']:.2f}"
            amount_paid =  f"{invoice_summary[invoice]['amount']:.2f}"  # Calculate the amount paid
            change = f"{float(amount_paid) - float(net):.2f}"  # Calculate the change (amount - net)
            date = invoice_summary[invoice]["cashier"]
            cashier = invoice_summary[invoice]["date"]

            for i, (product, qty) in enumerate(items):
                # Show invoice number, amount, change, cashier, and date only on the first row
                self.sales_table.insert("", END, values=(invoice if i == 0 else "",  # Show invoice only on first row
                    f"{product} ({qty})",
                    qty,
                    amount if i == 0 else "",  # Show amount only on first row
                    amount_paid if i == 0 else "",  # Show amount paid only on first row
                    change if i == 0 else "",  # Show change only on first row
                    date if i == 0 else "",  # Show date only on first row
                    cashier if i == 0 else "",  # Show cashier only on first row
                    net if i == 0 else ""  # Show net only on first row
                ))

        # Update the total sales label
        self.lbl_summary.config(text=f"Total Sales: ₱{total_amount:,.2f}")

    def print_report(self):
        def show_date_selector():
            popup = Toplevel(self.root)
            popup.title("Select Date Range")
            popup.geometry("300x200")
            popup.resizable(False, False)
            popup.grab_set()

            # Center the popup
            screen_width = popup.winfo_screenwidth()
            screen_height = popup.winfo_screenheight()
            window_width = 300
            window_height = 200
            position_top = int(screen_height / 2 - window_height / 2)
            position_right = int(screen_width / 2 - window_width / 2)
            popup.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

            Label(popup, text="From:").pack(pady=(20, 5))
            from_cal = DateEntry(popup, width=18, background='darkblue', foreground='white',
                                 date_pattern="short", maxdate=datetime.today())
            from_cal.pack()

            Label(popup, text="To:").pack(pady=(10, 5))
            to_cal = DateEntry(popup, width=18, background='darkblue', foreground='white',
                               date_pattern="short", maxdate=datetime.today())
            to_cal.pack()

            def on_ok():
                from_date = from_cal.get_date()
                to_date = to_cal.get_date()

                # Validate date range
                if from_date > to_date:
                    messagebox.showerror("Invalid Date Range", "From date cannot be later than To date.", parent=popup)
                    return

                popup.destroy()
                self.generate_report(from_date, to_date)

            Button(popup, text="Generate Report", command=on_ok, width=20, height=2).pack(pady=10)

        show_date_selector()

    def print_report(self):
        """Prompt user for date range, then generate filtered PDF report."""

        def show_date_selector():
            # Create popup
            popup = Toplevel(self.root)
            popup.title("Select Date Range")
            popup.geometry("300x200")
            popup.resizable(False, False)
            popup.grab_set()  # Make popup modal

            # Center the window on the screen
            screen_width = popup.winfo_screenwidth()
            screen_height = popup.winfo_screenheight()
            window_width = 300
            window_height = 200
            position_top = int(screen_height / 2 - window_height / 2)
            position_right = int(screen_width / 2 - window_width / 2)
            popup.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

            Label(popup, text="From:").pack(pady=(20, 5))

            # Date entry with a valid format like 'short' or 'medium'
            from_cal = DateEntry(popup, width=18, background='darkblue',
                                 foreground='white', date_pattern="short",  # Use 'short' pattern
                                 maxdate=datetime.today())  # Prevent future dates
            from_cal.pack()

            # Label for To date
            Label(popup, text="To:").pack(pady=(10, 5))

            # Date entry with a valid format like 'short' or 'medium'
            to_cal = DateEntry(popup, width=18, background='darkblue',
                               foreground='white', date_pattern="short",  # Use 'short' pattern
                               maxdate=datetime.today())  # Prevent future dates
            to_cal.pack()

            # Function to handle the confirmation and selected dates
            def on_confirm():
                # Get the date string and parse it correctly
                from_date_str = from_cal.get()
                to_date_str = to_cal.get()

                try:
                    if not from_date_str or not to_date_str:
                        messagebox.showerror("Invalid Date", "Both dates must be selected.", parent=self.root)
                        return

                    # Adjust strptime format based on the 'short' date pattern
                    from_date = datetime.strptime(from_date_str, "%m/%d/%y")  # Short date format is like '04/06/25'
                    to_date = datetime.strptime(to_date_str, "%m/%d/%y")  # Short date format is like '04/06/25'

                    # Store the display dates (the ones shown to the user)
                    from_date_display = from_date
                    to_date_display = to_date

                    # Get the last day of the month for the 'to_date'
                    _, last_day_of_month = calendar.monthrange(to_date.year, to_date.month)

                    # If 'to_date' is the last day of the month, ensure it's the end of that day
                    if to_date.day == last_day_of_month:
                        to_date = to_date.replace(hour=23, minute=59, second=59)
                    else:
                        to_date = to_date.replace(hour=23, minute=59,
                                                  second=59)  # Set the selected date to the end of the day

                    # Close the popup
                    popup.destroy()

                    # Generate the report with the selected date range
                    self.generate_report(from_date, to_date, from_date_display,
                                         to_date_display)  # Correct method call with all four arguments

                except ValueError as e:
                    messagebox.showerror("Invalid Date", "Please select valid dates.", parent=self.root)
                    print(e)

            Button(popup, text="OK", command=on_confirm).pack(pady=20)

        # ✅ Ask for confirmation before generating
        if messagebox.askyesno("Print Report", "Are you sure you want to print a report?", parent=self.root):
            show_date_selector()

    def generate_report(self, from_date, to_date, from_date_display, to_date_display):
        # Timestamp with safe characters for filenames
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = fr"C:\Users\ADMIN\OneDrive\Documents\KLBN_sales_report_{timestamp}.pdf"

        # Initialize PDF document with proper margins
        doc = SimpleDocTemplate(file_path, pagesize=letter,
                                leftMargin=40, rightMargin=40,
                                topMargin=30, bottomMargin=30)
        elements = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        title_style.alignment = 1

        center_style = ParagraphStyle(name="Center", parent=styles["Normal"], alignment=1)
        header_style = styles['Heading2']
        header_style.alignment = 1

        # Company logo
        logo_path = "remove.png"
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=100, height=50)
            logo.hAlign = 'CENTER'
            elements.append(logo)

        # Company info
        elements.append(Spacer(1, 10))
        elements.append(Paragraph("KLBN Corporation", title_style))
        elements.append(Paragraph("Sta. Ana Drive, Brgy. Sun Valley", center_style))
        elements.append(Paragraph("Parañaque City, Metro Manila, Philippines", center_style))
        elements.append(Spacer(1, 15))

        # Report title
        elements.append(Paragraph("Sales Report", header_style))
        elements.append(Spacer(1, 15))

        # Date range
        date_range_text = f"Selected Date Range: {from_date_display.strftime('%B %d, %Y')} to {to_date_display.strftime('%B %d, %Y')}"
        elements.append(Paragraph(date_range_text, styles['Normal']))
        elements.append(Spacer(1, 15))

        # Table data
        data = [["Invoice No.", "Product", "Quantity", "Net Total", "Amount Paid", "Change", "Cashier", "Date"]]
        skipped_rows = 0

        for item in self.sales_table.get_children():
            row = self.sales_table.item(item, "values")

            # Debugging: print the row data
            print(f"Row data: {row}")  # This will show the entire row to help identify the issue

            # Handle row with extra columns by trimming to 8 columns
            if len(row) > 8:
                row = row[:8]  # Trim the extra column

            # Check if the row has the expected number of columns (8)
            if len(row) == 8:
                try:
                    row_date = datetime.strptime(row[7], "%B %d, %Y (%I:%M %p)")
                    if from_date <= row_date <= to_date:
                        data.append(row)
                except Exception as e:
                    skipped_rows += 1
                    print(f"Skipping row with invalid date: {row[7]} - {e}")
            else:
                skipped_rows += 1
                print(f"Skipping row with unexpected number of columns: {len(row)}")

        if len(data) == 1:
            messagebox.showinfo("No Data", "No records found for selected dates.", parent=self.root)
            return

        # Table styling with added space on the sides
        table = Table(data, colWidths=[90, 60, 40, 60, 60, 60, 90], rowHeights=25)  # Adjusted column widths
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 6.5),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))

        elements.append(table)

        # Build PDF
        doc.build(elements)
        messagebox.showinfo("Success", f"Report saved as {file_path}", parent=self.root)

        # Optional: Open the file automatically
        try:
            os.startfile(file_path)
        except Exception as e:
            print(f"Could not open the file automatically: {e}")

        if skipped_rows:
            print(f"{skipped_rows} rows skipped due to invalid or unparsable dates.")


# Run the app
if __name__ == "__main__":
    root = Tk()
    SalesReport(root)
    root.mainloop()
