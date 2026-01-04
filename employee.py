from calendar import Calendar
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox
from tkinter import END
from datetime import datetime
from tkcalendar import Calendar
import os
class employeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory-Employee Management")
        self.root.config(bg="white")
        self.root.resizable(False, False)  # Disable window resizing
        self.root.attributes('-toolwindow',False)  # Remove minimize & maximize buttons
        self.root.focus_force()

        # ----------------------------------------------------
        # ALL Variables -----------

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_address = StringVar()
        self.var_salary = StringVar()

        self.counter_file = "counter.txt"
        # self.var_emp_id = None  # Assuming it's linked to an Entry widget

        # Ensure the file exists with an initial value of 100000
        if not os.path.exists(self.counter_file):
            with open(self.counter_file, "w") as f:
                f.write("100000")  # Start from 100000

        # Generate and set the auto number
        self.var_emp_id.set(self.generate_auto_number())

        # Button to open the calendar
        self.dob_button = Button(self.root, text="📅 Select Date", command=self.pick_dob, font=("Arial", 12), width= 19)
        self.dob_button.place(x=500, y=190)

        self.current_datetime = datetime.now().strftime("%B %d,%Y")

        self.lbl_clock = Label(self.root,
                               text="\t\t Date: DD-YYYY\t\t Time: HH:MM:SS",
                               font=("times new roman", 15, "bold"), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=100, relwidth=1, height=30)

        # -----------------search frame-----------------------
        SearchFrame = LabelFrame(self.root, text="Search Employee", font=("goudy odl style", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=250, y=20, width=600, height=70)

        # ------------ combo box options---------------------------
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Select", "Email", "Name", "Contact"), state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        # Create validation function
        def character_limit(P):
            return len(P) <= 20  # Limits to 20 characters - adjust this number as needed

        # Register validation
        vcmd = (SearchFrame.register(character_limit), '%P')

        # Create search Entry widget - separate creation and placement
        txt_search = Entry(
            SearchFrame,
            textvariable=self.var_searchtxt,
            font=("goudy old style", 15),
            bg="light yellow",
            validate='key',
            validatecommand=vcmd
        )
        txt_search.place(x=200, y=10)
        btn_search = Button(SearchFrame, text= "Search", command=self.search, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=410, y=9, width=150, height=30)

        # -----------------------title---------------------------------
        title = Label(self.root,text="Employee Details", font=("goudy old style", 15), bg="#0f4d7d", fg="white").place(x=50, y=100, width=1000)

        # -------------------content----------------------------
        # ----------------------row1-----------------------------
        lbl_empid = Label(self.root, text="Emp ID", font=("goudy old style", 15), bg="white").place(x=50, y=150)
        lbl_gender = Label(self.root, text="Gender", font=("goudy old style", 15), bg="white").place(x=350, y=150)
        lbl_contact = Label(self.root, text="Contact", font=("goudy old style", 15), bg="white").place(x=750, y=150)

        # Define character limit function inside the class

        def character_limit(P):
            return len(P) <= 6  # Limits input to 6 characters

        # Register validation function
        vcmd = (self.root.register(character_limit), '%P')

        # Create Employee ID Entry widget
        txt_empid = Entry( self.root,textvariable=self.var_emp_id, font=("goudy old style", 15), bg="Lightyellow", validate='key',validatecommand=vcmd
        )
        txt_empid.place(x=150, y=150, width=180)

        txt_gender = Entry(self.root, textvariable=self.var_gender, font=("goudy old style", 15), bg="lightyellow").place(x=500, y=150, width=180)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Other"), state="readonly", justify=CENTER,font=("goudy old style", 15))
        cmb_gender.place(x=500, y=150, width=180)
        cmb_gender.current(0)

        # Create validation function for numbers only with length limit
        def validate_contact(P):
            # Check if input is numeric and within length limit (11 digits)
            return (P.isdigit() or P == "") and len(P) <= 11

        # Register validation
        vcmd = (self.root.register(validate_contact), '%P')

        # Create contact Entry widget - separate creation and placement
        txt_contact = Entry(
            self.root,
            textvariable=self.var_contact,
            font=("goudy old style", 15),
            bg="lightyellow",
            validate='key',
            validatecommand=vcmd
        )
        txt_contact.place(x=850, y=150, width=180)
        # --------------------------row2--------------------------------
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15), bg="white").place(x=50, y=190)
        lbl_dob = Label(self.root, text="D.O.B", font=("goudy old style", 15), bg="white").place(x=350, y=190)
        lbl_doj = Label(self.root, text="D.O.J", font=("goudy old style", 15), bg="white").place(x=750, y=190)

        # Create validation function for letters only with length limit
        def validate_name(P):
            # Check if input contains only letters, spaces and is within length limit
            return all(char.isalpha() or char.isspace() for char in P) and len(P) <= 25

        # Register validation
        vcmd = (self.root.register(validate_name), '%P')

        # Create name Entry widget - separate creation and placement
        txt_name = Entry(
            self.root,
            textvariable=self.var_name,
            font=("goudy old style", 15),
            bg="Lightyellow",
            validate='key',
            validatecommand=vcmd
        )
        txt_name.place(x=150, y=190, width=180)

        # Variable to store Date of Joining (DOJ)
        self.var_doj = StringVar()
        self.var_doj.set(self.current_datetime)  # Set current date and time




        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15),bg="lightyellow").place_forget()

        txt_doj = Entry(self.root, textvariable=self.var_doj, font=("goudy old style", 15),bg="lightyellow", state= "readonly").place(x=850, y=190, width=180)

        # --------------------------row3--------------------------------
        lbl_email = Label(self.root, text="Email", font=("goudy old style", 15), bg="white").place(x=50, y=230)
        lbl_pass = Label(self.root, text="Password", font=("goudy old style", 15), bg="white").place(x=350, y=230)
        lbl_utype = Label(self.root, text="User Type", font=("goudy old style", 15), bg="white").place_forget()

        def validate_email_input(action, current_text, char):
            if action == "1":  # If a character is being inserted
                if len(current_text) >= 30:
                    return False
                if not (char.isalnum() or char == '@', '.'):
                    return False
            return True  # Allow backspace and deletions


        validate_cmd = root.register(lambda action, current_text, char:
                                     validate_email_input(action, current_text, char))

        txt_name = Entry(root, textvariable=self.var_email, font=("goudy old style", 15), bg="Lightyellow",
                            validate="key", validatecommand=(validate_cmd, "%d", "%P", "%S"))
        txt_name.place(x=150, y=230, width=180)

        txt_pass = Entry(self.root, textvariable=self.var_pass, font=("goudy old style", 15), bg="lightyellow", state= 'disabled').place(x=500, y=230, width=180)
        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=("Employee"), state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_utype.place_forget()
        cmb_utype.current(0)
        self.var_pass.set("12345678")
        # --------------------------row4--------------------------------
        lbl_address = Label(self.root, text="Address", font=("goudy old style", 15), bg="white").place(x=50, y=270)
        lbl_salary = Label(self.root, text="Salary", font=("goudy old style", 15), bg="white").place_forget()

        def limit_chars(event):
            if len(self.txt_address.get("1.0", "end-1c")) >= 90 and event.keysym not in ("BackSpace", "Delete"):
                return "break"  # Prevent further input


        self.txt_address = Text(root, font=("Goudy Old Style", 15), bg="Lightyellow")
        self.txt_address.place(x=150, y=270, width=300, height=60)
        self.txt_address.bind("<KeyPress>", limit_chars)

        self.var_salary.set("₱")
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("goudy old style", 15), bg="lightyellow")
        txt_salary.place_forget()
        # ---------------button-----------------------
        btn_add = Button(self.root, text="Save", command=self.add, font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=500, y=305, width=110, height=28)
        btn_update = Button(self.root, text="Update", command=self.update, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=620, y=305, width=110, height=28)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15), bg="#f44336", fg="white", cursor="hand2").place(x=740, y=305, width=110, height=28)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15), bg="#607d8b", fg="white", cursor="hand2").place(x=870, y=305, width=110, height=28)

        # ------------Employee details------------------
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=350, relwidth=1, height=150)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_frame, columns=("eid", "name", "email", "gender", "contact", "dob", "doj", "pass", "utype", "address", "salary"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)
        self.EmployeeTable.heading("eid", text="Emp ID")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="Date of Birth")
        self.EmployeeTable.heading("doj", text="Date of Joining")
        self.EmployeeTable.heading("pass", text="Password")
        self.EmployeeTable.heading("utype", text="User Type")
        self.EmployeeTable.heading("address", text="Address")


        self.EmployeeTable["show"] = ["headings"]

        self.EmployeeTable.column("eid", width=70)
        self.EmployeeTable.column("name", width=150)
        self.EmployeeTable.column("email", width=170)
        self.EmployeeTable.column("gender", width=100)
        self.EmployeeTable.column("contact", width=100)
        self.EmployeeTable.column("dob", width=100)
        self.EmployeeTable.column("doj", width=100)
        self.EmployeeTable.column("pass", width=100)
        self.EmployeeTable.column("utype", width=100)
        self.EmployeeTable.column("address", width=100)
        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

# ------------------------------------------------------------------------------------------

    def generate_auto_number(self, increment=True):
        """Read current auto-number from a file. Return next number as a zero-padded string."""
        try:
            # Open for reading and writing, create if doesn't exist
            with open(self.counter_file, "a+") as f:
                f.seek(0)
                content = f.read().strip()

                # Default to 100000 if file is empty or invalid
                num = int(content) if content.isdigit() else 100000

                if increment:
                    num += 1
                    f.seek(0)
                    f.truncate()
                    f.write(str(num).zfill(6))  # Save updated number

            return str(num).zfill(6)

        except Exception as e:
            print(f"Error reading or writing counter file: {e}")
            return "000000"

    def pick_dob(self):
        """ Function to open the calendar and select DOB """
        # Create a new top-level window
        top = Toplevel(self.root)
        top.title("📅 Date of Birth")

        # Get screen width and height
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()

        # Set window dimensions
        window_width = 350
        window_height = 300  # Adjusted height to fit calendar + button

        # Calculate x and y coordinates for centering
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)

        # Set window position
        top.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Get today's date
        today = datetime.today()

        # Calendar widget (Prevents future date selection)
        cal = Calendar(top, selectmode="day", date_pattern="MM-dd-yyyy", maxdate=today)
        cal.pack(fill="both", expand=True, pady=10, padx=10)

        # Function to get the selected date
        def get_date():
            selected_date = cal.get_date()  # Get the selected date
            self.dob_button.config(text=f"📅 {selected_date}")  # Update button text
            self.var_dob.set(selected_date)  # Set it in the Entry field
            top.destroy()  # Close the popup

        # OK Button to confirm date selection
        Button(top, text="OK", command=get_date, width=10).pack(pady=10,padx= 10)

    # Running the Tkinter application



    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID MUST be keyed", parent=self.root)
                self.clear()
            elif (self.var_name.get() == "" or
                  self.var_email.get() == "" or
                  self.var_gender.get() == "" or
                  self.var_contact.get() == "" or
                  self.var_dob.get() == "" or
                  self.var_doj.get() == "" or
                  self.var_pass.get() == "" or
                  self.var_utype.get() == "" or
                  self.txt_address.get("1.0", "end-1c").strip() == ""):
                messagebox.showerror("Error", "Please fill all the information", parent=self.root)
                self.clear()
            elif "@" not in self.var_email.get():
                messagebox.showerror("Error", "Please input a valid email address", parent=self.root)
                self.clear()
            else:
                cur.execute("Select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error", "This Employee ID already assigned, try different", parent=self.root)

                else:
                    cur.execute("Insert into employee (eid, name, email, gender, contact, dob, doj, pass,utype,address, salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                                              self.var_emp_id.get(),
                                              self.var_name.get(),
                                              self.var_email.get(),
                                              self.var_gender.get(),
                                              self.var_contact.get(),
                                              self.var_dob.get(),
                                              self.var_doj.get(),

                                              self.var_pass.get(),
                                              self.var_utype.get(),
                                              self.txt_address.get('1.0', END),
                                              self.var_salary.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee added Successfully", parent=self.root)
                    self.send_welcome_email()

                    self.clear()
                    self.show()
                    self.var_emp_id.set(self.generate_auto_number(increment=False))

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def send_welcome_email(self):
        # Email configuration
        sender_email = "joshuanombradojaculba@gmail.com"  # Replace with your email
        sender_password = "hula miwi pgpv dvky"  # Replace with your email password or app password
        recipient_email = self.var_email.get()  # Employee's email

        # Determine salutation based on gender
        if self.var_gender.get() == "Male":
            salutation = "Mr."
        elif self.var_gender.get() == "Female":
            salutation = "Ms."
        else:
            salutation = "Mr./Ms."

        # Email subject and body
        subject = "Employee details"
        body = f"""
        Dear {salutation} {self.var_name.get()},

        Welcome to KLBN Corporation! We are excited to have you on board.
        DO NOT SHARE YOUR EMPLOYEE ID AND PASSWORD!
        
        Employee ID:  {self.var_emp_id.get()}
        Password:     {self.var_pass.get()}

        Let's keep your account secure!
        🔹 Step 1: Go to the forgot password  
        🔹 Step 2: Enter your employee ID  
        🔹 Step 3: Enter the FPCC (Forgot Password Confirmation Code)  
        🔹 Step 4: Create a new password  

        A secure account starts with a strong password. Update yours today!
        
        
        Best regards,
        KLBN Corporation
        """

        # Set up the MIME
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject

        # Attach the body to the email
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as session:  # Use Gmail's SMTP server
                session.starttls()  # Enable security
                session.login(sender_email, sender_password)  # Login with your email and password
                session.sendmail(sender_email, recipient_email, message.as_string())
            print(f"Welcome email sent to {recipient_email} successfully!")
        except Exception as e:
            print(f"Failed to send email. Error: {e}")

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Select only the necessary columns, excluding salary
            cur.execute("SELECT eid, name, email, gender, contact, dob, doj, pass, utype, address FROM employee")
            rows = cur.fetchall()

            self.EmployeeTable.delete(*self.EmployeeTable.get_children())  # Clear existing data

            for row in rows:
                self.EmployeeTable.insert('', END, values=row)  # Insert row without salary

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()  # Ensure the database connection is closed

    def get_data(self, ev):
        f = self.EmployeeTable.focus()
        content = self.EmployeeTable.item(f)
        row = content['values']

        if not row:  # Prevents errors if no row is selected
            return

        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])

        self.txt_address.delete('1.0', END)
        self.txt_address.insert(END, row[9])  # Adjusted index since salary is removed

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID MUST be keyed ", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                else:
                    cur.execute("Update employee set name=?, email=?, gender=?, contact=?, dob=?, doj=?, pass=?, utype=?,address=?, salary=? where eid=?",(
                                                 self.var_name.get(),
                                                 self.var_email.get(),
                                                 self.var_gender.get(),
                                                 self.var_contact.get(),
                                                 self.var_dob.get(),
                                                 self.var_doj.get(),

                                                 self.var_pass.get(),
                                                 self.var_utype.get(),
                                                 self.txt_address.get('1.0', END),
                                                 self.var_salary.get(),
                                                 self.var_emp_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee updated Successfully", parent=self.root)
                    self.show()
                    self.var_emp_id.set(self.generate_auto_number(increment=False))
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID MUST be keyed ", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Employee Deleted Successfully", parent=self.root)
                        self.clear()
                        self.var_emp_id.set(self.generate_auto_number(increment=False))
                    else:
                        # You can add any action here if deletion was canceled or not confirmed
                        messagebox.showinfo("Cancelled", "Employee deletion cancelled", parent=self.root)



        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear(self):
        self.var_emp_id.set(self.generate_auto_number(increment=False))
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.dob_button.config(text=f"📅 Select Date")  # Update button text
        self.var_doj.set(self.current_datetime)  # Set current date and time
        self.var_pass.set("12345678")
        self.var_utype.set("Employee")
        self.txt_address.delete('1.0', END)
        self.var_salary.set("₱")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                 messagebox.showerror("Error", "Select Search By Option", parent=self.root)

            elif self.var_searchtxt.get() == "":
                # Select only the necessary columns, excluding salary
                cur.execute("SELECT eid, name, email, gender, contact, dob, doj, pass, utype, address FROM employee")
                rows = cur.fetchall()

                self.EmployeeTable.delete(*self.EmployeeTable.get_children())  # Clear existing data

                for row in rows:
                    self.EmployeeTable.insert('', END, values=row)  # Insert row without salary

            else:
                cur.execute("select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows = cur.fetchall()
            if len(rows) != 0:
                self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                for row in rows:
                    self.EmployeeTable.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No record was found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()
