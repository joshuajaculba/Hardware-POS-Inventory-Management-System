from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
from reportlab.lib.styles import ParagraphStyle
from datetime import datetime
from tkinter import Toplevel, Label, Button
from tkcalendar import DateEntry
from datetime import datetime
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import Toplevel
from datetime import datetime
from tkinter import Toplevel, Label, Button, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import os
from tkinter import Toplevel, Label, Button, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, Spacer, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
import calendar


import sqlite3

class InventoryLog:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Log")
        self.root.config(bg="white")
        self.root.resizable(False, False)  # Disable window resizing
        self.root.attributes('-toolwindow', False)  # Keep default title bar with buttons
        self.root.focus_force()  # Optional: ensures it starts focused

        # ================== VARIABLES ==================
        self.var_pid = StringVar()
        self.var_cus = StringVar()
        self.var_cat = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()
        self.current = StringVar()
        self.new = StringVar()
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.current_datetime = datetime.now().strftime("%m %d %Y")
        product_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=450, height=270)

        # -----------------------title---------------------------------
        title = Label(product_Frame, text="Manage Inventory", font=("goudy old style", 18), bg="#ffb6c1",
                      fg="black").pack(side=TOP, fill=X)

        # ================== DATABASE INIT ==================
       # Ensure table exists

        # ================== UI COMPONENTS ==================
        # Label(self.root, text="Inventory Log", font=("goudy old style", 20, "bold"), bg="white").pack(pady=10)
        lbl_product_name = Label(product_Frame, text="Name", font=("goudy old style", 18), bg="white").place(x=30, y=80)
        lbl_price = Label(product_Frame, text="Price", font=("goudy old style", 18), bg="white").place(x=30, y=130)
        lbl_qty = Label(product_Frame, text="Quantity", font=("goudy old style", 18), bg="white").place(x=30, y=180)


        self.var_date = StringVar()
        self.var_date.set(datetime.now().strftime("%m %d %Y"))  # Format the date
        # Create an Entry widget (readonly) to display the date
        self.manager = StringVar()
        self.manager.set("Admin")  # Set default value
        txt_manager= Entry(product_Frame,textvariable=self.manager, font=("goudy old style", 15),
                         bg="lightyellow", state="readonly")
        txt_manager.place_forget()
        # Create an Entry widget (readonly) to display the date
        txt_date = Entry(product_Frame, textvariable=self.var_date, font=("goudy old style", 15),
                         bg="lightyellow", state="readonly")
        txt_date.place_forget()

        txt_manager = Entry(product_Frame, textvariable=self.current, font=("goudy old style", 15),
                            bg="lightyellow", state="readonly")
        txt_manager.place_forget()

        txt_manager = Entry(product_Frame, textvariable=self.new, font=("goudy old style", 15),
                            bg="lightyellow", state="readonly")
        txt_manager.place_forget()


        def validate_name(new_value):
            return (new_value.replace(" ", "").isalpha() and len(new_value) <= 25) or new_value == ""

        validate_cmd = (root.register(validate_name), "%P")

        self.txt_name = Entry(root, textvariable=self.var_name, font=("goudy old style", 15),
                              bg="lightyellow", state="readonly", validate="key", validatecommand=validate_cmd)
        self.txt_name.place(x=160, y=90, width=200)

        def validate_price(new_value):
            return new_value.isdigit() and len(new_value) <= 7 or new_value == ""

        validate_cmd = (root.register(validate_price), "%P")

        self.txt_price = Entry(root, textvariable=self.var_price, font=("goudy old style", 15),
                               bg="lightyellow", state="readonly", validate="key", validatecommand=validate_cmd)
        self.txt_price.place(x=160, y=140, width=200)

        def validate_qty(new_value):
            return new_value.isdigit() and len(new_value) <= 6 or new_value == ""

        validate_cmd = (root.register(validate_qty), "%P")

        self.txt_qty = Entry(root, textvariable=self.var_qty, font=("goudy old style", 15),
                             bg="lightyellow", validate="key", validatecommand=validate_cmd)
        self.txt_qty.place(x=160, y=190, width=200)

        cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status, values=("Active", "Inactive"),
                                  state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_status.place_forget()
        cmb_status.current(0)

        btn_update = Button(product_Frame, text="Update", command=self.update, font=("goudy old style", 15),
                            bg="#4b0680", fg="white", cursor="hand2").place(x=150, y=220, width=90, height=40)

        btn_clear = Button(product_Frame, text="Print", command=self.print, font=("goudy old style", 15), bg="#607d8b",
                           fg="white", cursor="hand2").place(x=250, y=220, width=100, height=40)

        def validate_search(new_value):
            return len(new_value) <= 25

        validate_cmd = (root.register(validate_search), "%P")

        self.txt_search = Entry(root, textvariable=self.var_searchtxt, font=("goudy old style", 15),
                                bg="lightyellow", validate="key", validatecommand=validate_cmd)
        self.txt_search.place(x=30, y=300, width=300)
        btn_search = Button(root, text="Search", command=self.search, font=("goudy old style", 15), bg="#068029",
                            fg="white", cursor="hand2").place(x=350, y=300, width=100, height=27)
        # ========== INVENTORY LOG TABLE ==========
        # Create a Frame to hold the Table and Scrollbars
        table_frame = Frame(self.root)
        table_frame.place(x=10, y=350, width=1080, height=140)  # Adjust position and size

        # Add Scrollbars (Vertical and Horizontal)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        # Create Treeview (Table)
        self.log_table = ttk.Treeview(table_frame, columns=("product", "current", "stock", "new", "date", "action"),
                                      show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        # Configure Scrollbars
        scroll_y.config(command=self.log_table.yview)
        scroll_x.config(command=self.log_table.xview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)

        # Define Table Headings
        self.log_table.heading("product", text="Product Name", command=lambda: self.sort_table("product", False))
        self.log_table.heading("current", text="Current Stocks", command=lambda: self.sort_table("current", True))
        self.log_table.heading("stock", text="Updated Stocks", command=lambda: self.sort_table("stock", True))
        self.log_table.heading("new", text="New Stocks", command=lambda: self.sort_table("new", True))
        self.log_table.heading("date", text="Date", command=lambda: self.sort_table("date", False))
        self.log_table.heading("action", text="Manager", command=lambda: self.sort_table("action", False))

        # Define Column Widths
        self.log_table.column("product", width=150)
        self.log_table.column("current", width=100, anchor=CENTER)
        self.log_table.column("stock", width=100, anchor=CENTER)
        self.log_table.column("new", width=100, anchor=CENTER)
        self.log_table.column("date", width=180)
        self.log_table.column("action", width=120, anchor=CENTER)

        # Pack the Treeview inside the Frame
        self.log_table.pack(fill=BOTH, expand=1)

        # Sample Data for Testing
        self.populate_sample_data()

    def populate_sample_data(self):
        """Populates the table with sample data for testing sorting."""
        sample_data = [
            ("Apple", 50, 10, 60, "March 30, 2025 (12:45 PM)", "Manager A"),
            ("Banana", 30, 5, 35, "March 29, 2025 (02:10 AM)", "Manager B"),
            ("Cherry", 20, 15, 35, "March 28, 2025 (06:25 PM)", "Manager C"),
            ("Date", 40, 20, 60, "March 27, 2025 (09:55 AM)", "Manager D"),
        ]
        for row in sample_data:
            self.log_table.insert("", "end", values=row)

        # ========== PRODUCT TABLE ==========
        p_frame = Frame(self.root, bd=3, relief=RIDGE)
        p_frame.place(x=480, y=9, width=600, height=320)

        scrolly = Scrollbar(p_frame, orient=VERTICAL)
        scrollx = Scrollbar(p_frame, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(p_frame,
                                          columns=("pid", "Customer", "Category", "name", "price", "qty", "status"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="Product ID")
        self.product_table.heading("Category", text="Category")
        self.product_table.heading("Customer", text="Supplier")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="Qty")
        self.product_table.heading("status", text="Status")

        self.product_table["show"] = "headings"  # Corrected syntax

        self.product_table.column("pid", width=90)
        self.product_table.column("Category", width=100)
        self.product_table.column("Customer", width=100)
        self.product_table.column("name", width=100)
        self.product_table.column("price", width=100)
        self.product_table.column("qty", width=100)
        self.product_table.column("status", width=100)
        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()
        self.load_logs()

    # ================== DATABASE HELPER FUNCTION ==================
    def execute_query(self, query, params=()):
        """Helper function to execute queries safely."""
        with sqlite3.connect("inventory.db") as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    # ================== DATABASE OPERATIONS ==================
    def sort_table(self, column, reverse):
        """Sorts the table by the selected column when the user clicks on a header."""
        data = [(self.log_table.set(item, column), item) for item in self.log_table.get_children()]

        # Try to sort numerically, otherwise sort as string
        try:
            data.sort(key=lambda x: int(x[0]) if x[0].isdigit() else x[0], reverse=reverse)
        except ValueError:
            data.sort(key=lambda x: x[0], reverse=reverse)

        for index, (val, item) in enumerate(data):
            self.log_table.move(item, "", index)

        # Toggle sorting order for next click
        self.log_table.heading(column, command=lambda: self.sort_table(column, not reverse))

    def load_logs(self):
        """Fetch inventory logs from the database and display them in the log_table in real-time."""
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT product, current, stock, new, date, action FROM inventory")  # Fetch all records from the log table
            rows = cur.fetchall()

            # Clear existing data in the table
            self.log_table.delete(*self.log_table.get_children())

            # Insert fetched data into the Treeview
            for row in rows:
                self.log_table.insert("", END, values=row)

        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)
        finally:
            con.close()  # Close the connection

        # Schedule next update (every 2 seconds)
        self.root.after(2000, self.load_logs)  # 2000ms = 2 seconds

    def update_new_value(self):
        try:
            # Convert current and var_qty to integers (ensure they are not empty)
            current_stock = int(self.current.get()) if self.current.get().strip() else 0
            added_stock = int(self.var_qty.get()) if self.var_qty.get().strip() else 0

            # Perform addition
            self.new.set(current_stock + added_stock)  # Update the variable linked to the readonly textbox

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numbers only.", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()

            # Clear existing data
            self.product_table.delete(*self.product_table.get_children())

            for row in rows:
                try:
                    qty = int(row[5])
                except (ValueError, TypeError):
                    qty = 0

                # Default to existing status
                status = row[6]

                # If quantity is zero, set status to "Inactive" visually
                if qty == 0:
                    status = "Inactive"  # <-- this line changes status text
                    row = row[:6] + (status,) + row[7:]  # replace status in the row tuple

                # Determine tag for coloring
                if qty == 0 and status == "Inactive":
                    status_tag = "ZeroQtyInactive"
                elif qty == 0:
                    status_tag = "ZeroQty"
                elif status == "Inactive":
                    status_tag = "Inactive"
                else:
                    status_tag = "Active"

                self.product_table.insert("", "end", values=row, tags=(status_tag,))

            # Configure row colors
            self.product_table.tag_configure("ZeroQtyInactive", background="darkred", foreground="white")
            self.product_table.tag_configure("ZeroQty", background="red", foreground="white")
            self.product_table.tag_configure("Inactive", background="orange", foreground="white")
            self.product_table.tag_configure("Active", background="green", foreground="white")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_cus.set("Select"),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_qty.set(""),
        self.var_status.set("Active"),
        self.var_pid.set(""),
        self.var_searchtxt.set(""),
        self.var_searchby.set("Select")
        self.show()

    def print(self):
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

                    # Get the last day of the month for the 'to_date'
                    _, last_day_of_month = calendar.monthrange(to_date.year, to_date.month)

                    # If 'to_date' is the last day of the month, ensure it's the end of that day
                    if to_date.day == last_day_of_month:
                        to_date = to_date.replace(hour=23, minute=59, second=59)
                    else:
                        # If 'to_date' is not the last day of the month, we do not change it.
                        # If the 'to_date' is earlier in the month, just leave it as the selected date
                        to_date = to_date.replace(hour=23, minute=59,
                                                  second=59)  # Set the selected date to the end of the day

                    # Close the popup
                    popup.destroy()

                    # Generate the report with the selected date range
                    generate_report(from_date, to_date, from_date, to_date)
                except ValueError as e:
                    messagebox.showerror("Invalid Date", "Please select valid dates.", parent=self.root)
                    print(e)
            Button(popup, text="OK", command=on_confirm).pack(pady=20)

        # ✅ 2. Report generation with filtering
        def generate_report(from_date, to_date, from_date_display, to_date_display):
            # Timestamp with safe characters for filenames
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = fr"C:\Users\ADMIN\OneDrive\Documents\KLBN_inventory_report_{timestamp}.pdf"

            # Initialize PDF document
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
            elements.append(Paragraph("Inventory Report", header_style))
            elements.append(Spacer(1, 15))

            # Date range
            date_range_text = f"Selected Date Range: {from_date_display.strftime('%B %d, %Y')} to {to_date_display.strftime('%B %d, %Y')}"
            elements.append(Paragraph(date_range_text, styles['Normal']))
            elements.append(Spacer(1, 15))

            # Table data
            data = [["Product Name", "Current Stocks", "Updated Stocks", "New Stocks", "Date", "Manager"]]
            skipped_rows = 0

            for item in self.log_table.get_children():
                row = self.log_table.item(item, "values")
                try:
                    row_date = datetime.strptime(row[4], "%B %d, %Y (%I:%M %p)")
                    if from_date <= row_date <= to_date:
                        data.append(row)
                except Exception as e:
                    skipped_rows += 1
                    print(f"Skipping row with invalid date: {row[4]} - {e}")

            if len(data) == 1:
                messagebox.showinfo("No Data", "No records found for selected dates.", parent=self.root)
                return

            # Table styling
            table = Table(data, colWidths=[120, 70, 80, 70, 130, 100])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.black),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
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

        # ✅ Ask for confirmation before generating
        if messagebox.askyesno("Print Report", "Are you sure you want to print a report?", parent=self.root):
            show_date_selector()

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if not self.var_pid.get().strip():
                messagebox.showerror("Error", "Please select a product from the list", parent=self.root)
                return

            cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
            row = cur.fetchone()
            if row is None:
                messagebox.showerror("Error", "Invalid Product ID", parent=self.root)
                return

            # Convert values safely
            try:
                new_stock = int(self.var_qty.get()) if self.var_qty.get().strip() else 0
                current_stock = int(self.current.get()) if self.current.get().strip() else 0
                total_stock = current_stock + new_stock  # Calculate new stock
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity. Please enter numbers only.", parent=self.root)
                return

            # Determine status: "Inactive" if 0, "Active" otherwise
            status = "Inactive" if total_stock == 0 else "Active"

            # Update Product Stock and Status in `product` table
            cur.execute("""
                UPDATE product SET qty=?, status=? WHERE pid=?
            """, (total_stock, status, self.var_pid.get()))

            # Get current date and time in the required format
            formatted_date = datetime.now().strftime("%B %d, %Y (%I:%M %p)")

            # Insert transaction into `inventory` log
            cur.execute("""
                INSERT INTO inventory (product, new, date, action, stock, current) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                self.var_name.get(),
                total_stock,  # Updated stock
                formatted_date,  # Insert formatted date
                self.manager.get(),  # Action type
                new_stock,  # Stock added
                current_stock  # Previous stock

            ))

            # Commit changes
            con.commit()
            messagebox.showinfo("Success", "Product updated successfully", parent=self.root)
            self.show()# Refresh UI
            self.clear()

        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)
        finally:
            con.close()  # Ensure database connection is closed

    def get_data(self, ev):
        """Fetch selected row data and store in variables."""
        try:
            f = self.product_table.focus()
            content = self.product_table.item(f)
            row = content.get('values', [])

            if row:
                self.var_pid.set(row[0])
                self.var_cus.set(row[1])
                self.var_cat.set(row[2])
                self.var_name.set(row[3])
                self.var_price.set(row[4])
                self.current.set(row[5])
                self.var_status.set(row[6])
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to fetch row data: {ex}", parent=self.root)

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            search_txt = self.var_searchtxt.get().strip()

            # Base query
            query = "SELECT product, new, date, action, stock, current FROM inventory"

            if search_txt:
                # Search dynamically across all columns
                query += """
                    WHERE product LIKE ? OR 
                          new LIKE ? OR 
                          date LIKE ? OR 
                          action LIKE ? OR 
                          stock LIKE ? OR 
                          current LIKE ?
                """
                cur.execute(query, ('%' + search_txt + '%',) * 6)
            else:
                cur.execute(query)

            rows = cur.fetchall()

            # Clear and insert new data
            self.log_table.delete(*self.log_table.get_children())
            if rows:
                for row in rows:
                    self.log_table.insert("", END, values=row)
            else:
                messagebox.showerror("Error", "No record was found.", parent=self.root)

        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)
        finally:
            con.close()  # Close DB connection

    # def searchs(self):
    #     con = sqlite3.connect(database=r'ims.db')
    #     cur = con.cursor()
    #     try:
    #         search_by = self.var_searchby.get().strip()
    #         search_txt = self.var_searchtxt.get().strip()
    #
    #         # Validate input
    #         if search_by == "Select":
    #             messagebox.showerror("Error", "Select a valid Search By option.", parent=self.root)
    #             return
    #
    #         # If search text is empty, show all products
    #         if not search_txt:
    #             query = "SELECT pid, customer, category, name, price, qty, status FROM product"
    #             cur.execute(query)
    #         else:
    #             query = f"SELECT pid, customer, category, name, price, qty, status FROM product WHERE {search_by} LIKE ?"
    #             cur.execute(query, ('%' + search_txt + '%',))
    #
    #         rows = cur.fetchall()
    #
    #         # If no results, show error and return
    #         if not rows:
    #             messagebox.showerror("Error", "No record was found.", parent=self.root)
    #             return
    #
    #         # Clear previous data
    #         self.product_table.delete(*self.product_table.get_children())
    #
    #         # Apply row colors BEFORE inserting data
    #         self.product_table.tag_configure("Inactive", background="red", foreground="white")
    #         self.product_table.tag_configure("Active", background="green", foreground="white")
    #
    #         # Insert rows with tags (including "status" column)
    #         for row in rows:
    #             status_tag = "Inactive" if row[6] == "Inactive" else "Active"
    #             self.product_table.insert("", "end", values=row, tags=(status_tag,))  # Keep "status" column
    #
    #     except sqlite3.Error as db_err:
    #         messagebox.showerror("Database Error", f"Database error: {str(db_err)}", parent=self.root)
    #     except Exception as ex:
    #         messagebox.showerror("Error", f"Unexpected error: {str(ex)}", parent=self.root)
    #     finally:
    #         con.close()  # Always close connection
    #
    #

# ================== RUN APPLICATION ==================
if __name__ == "__main__":
    root = Tk()
    app = InventoryLog(root)
    root.mainloop()
