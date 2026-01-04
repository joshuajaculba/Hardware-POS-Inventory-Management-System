from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os


class customerClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory-Supplier Management")
        self.root.config(bg="white")
        self.root.resizable(False, False)  # Disable window resizing
        self.root.attributes('-toolwindow', False)  # Remove minimize & maximize buttons
        self.root.focus_force()

        # ----------------------------------------------------
        # ALL Variables -----------

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_cus_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        self.counter_file = "counter.txt"
        # self.var_emp_id = None  # Assuming it's linked to an Entry widget

        # Ensure the file exists with an initial value of 100000
        if not os.path.exists(self.counter_file):
            with open(self.counter_file, "w") as f:
                f.write("100000")  # Start from 100000

        # Generate and set the auto number
        self.var_cus_invoice.set(self.generate_auto_number())

        # -----------------search frame-----------------------

        # ------------ combo box options---------------------------
        lbl_search = Label(self.root, text="Supplier Id", bg="white", font=("goudy old style", 15))
        lbl_search.place(x=700, y=80)

        txt_search = Entry(self.root, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="light yellow").place(x=800, y=80, width=160)
        btn_search = Button(self.root, text="Search", command=self.search, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=980, y=79, width=100, height=28)

        # -----------------------title---------------------------------
        title = Label(self.root, text="Supplier Details", font=("goudy old style", 20), bg="#0f4d7d", fg="white").place(x=50, y=10, width=1000, height=40)

        # -------------------content----------------------------
        # ----------------------row1-----------------------------
        lbl_customer_invoice = Label(self.root, text="Supplier Id", font=("goudy old style", 15), bg="white").place(x=50, y=80)

        # Validation function
        def validate_input(new_value):
            return new_value.isdigit() and len(new_value) <= 6 or new_value == ""

        validate_cmd = (root.register(validate_input), "%P")

        self.txt_customer_invoice = Entry(
            self.root, textvariable=self.var_cus_invoice, font=("goudy old style", 15),
            bg="Lightyellow", validate="key", validatecommand=validate_cmd
        )
        self.txt_customer_invoice.place(x=180, y=80, width=180)
        # --------------------------row2--------------------------------
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15), bg="white").place(x=50, y=120)

        def validate_name(new_value):
            return (new_value.replace(" ", "").isalpha() and len(new_value) <= 25) or new_value == ""

        validate_cmd = (root.register(validate_name), "%P")

        self.txt_name = Entry(
            self.root, textvariable=self.var_name, font=("goudy old style", 15),
            bg="Lightyellow", validate="key", validatecommand=validate_cmd
        )
        self.txt_name.place(x=180, y=120, width=180)
        # --------------------------row3--------------------------------
        lbl_contact = Label(self.root, text="Contact", font=("goudy old style", 15), bg="white").place(x=50, y=160)

        def validate_contact(new_value):
            return new_value.isdigit() and len(new_value) <= 11 or new_value == ""

        validate_cmd = (root.register(validate_contact), "%P")

        self.txt_contact = Entry(
            self.root, textvariable=self.var_contact, font=("goudy old style", 15),
            bg="Lightyellow", validate="key", validatecommand=validate_cmd
        )
        self.txt_contact.place(x=180, y=160, width=180)
        # --------------------------row4--------------------------------
        lbl_desc = Label(self.root, text="Description", font=("goudy old style", 15), bg="white").place(x=50, y=200)
        self.txt_desc = Text(self.root, font=("goudy old style", 15), bg="Lightyellow")
        self.txt_desc.place(x=180, y=200, width=470, height=120)

        # ---------------button-----------------------
        btn_add = Button(self.root, text="Save", command=self.add, font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=180, y=370, width=110, height=35)
        btn_update = Button(self.root, text="Update", command=self.update, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=300, y=370, width=110, height=35)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15), bg="#f44336", fg="white", cursor="hand2").place(x=420, y=370, width=110, height=35)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15), bg="#607d8b", fg="white", cursor="hand2").place(x=540, y=370, width=110, height=35)

        # ------------Customer details------------------
        cus_frame = Frame(self.root, bd=3, relief=RIDGE)
        cus_frame.place(x=700, y=120, width=380, height=350)

        scrolly = Scrollbar(cus_frame, orient=VERTICAL)
        scrollx = Scrollbar(cus_frame, orient=HORIZONTAL)

        self.customerTable = ttk.Treeview(cus_frame, columns=("invoice", "name", "contact", "desc"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.customerTable.xview)
        scrolly.config(command=self.customerTable.yview)

        self.customerTable.heading("invoice", text="Supplier Id")
        self.customerTable.heading("name", text="Name")
        self.customerTable.heading("contact", text="Contact")
        self.customerTable.heading("desc", text="Description")
        self.customerTable["show"] = "headings"
        self.customerTable.column("invoice", width=90)
        self.customerTable.column("name", width=100)
        self.customerTable.column("contact", width=100)
        self.customerTable.column("desc", width=100)
        self.customerTable.pack(fill=BOTH, expand=1)
        self.customerTable.bind("<ButtonRelease-1>", self.get_data)

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
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_cus_invoice.get() == "":
                messagebox.showerror("Error", "Invoice MUST be keyed ", parent=self.root)
            else:
                cur.execute("Select * from customer where invoice=?", (self.var_cus_invoice.get(),))
                row = cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error", "Invoice No already assigned, try different", parent=self.root)

                else:
                    cur.execute("Insert into customer (invoice, name, contact, desc) values(?,?,?,?)",(
                                              self.var_cus_invoice.get(),
                                              self.var_name.get(),
                                              self.var_contact.get(),
                                              self.txt_desc.get('1.0', END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Customer added Successfully", parent=self.root)
                    self.show()
                    self.clear()
                    self.var_cus_invoice.set(self.generate_auto_number(increment=False))
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show(self):
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            try:
                cur.execute("select * from customer")
                rows = cur.fetchall()
                self.customerTable.delete(*self.customerTable.get_children())
                for row in rows:
                    self.customerTable.insert('', END, values=row)
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.customerTable.focus()
        content = (self.customerTable.item(f))
        row = content['values']
        print(row)
        self.var_cus_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0', END),
        self.txt_desc.insert(END, row[3]),

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        try:
            if self.var_cus_invoice.get() == "":
                messagebox.showerror("Error", "INVOICE No. MUST be keyed ", parent=self.root)
            else:
                cur.execute("Select * from customer where invoice=?", (self.var_cus_invoice.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Invalid Invoice NO.", parent=self.root)
                else:
                    cur.execute("Update customer set name=?, contact=?, desc=? where invoice=?",(
                                                 self.var_name.get(),
                                                 self.var_contact.get(),
                                                 self.txt_desc.get('1.0', END),
                                                 self.var_cus_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Customer updated Successfully", parent=self.root)
                    self.show()
                    self.clear()
                    self.var_cus_invoice.set(self.generate_auto_number(increment=False))
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def delete(self):

            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            try:
                invoice_no = self.var_cus_invoice.get().strip()  # Ensure no leading/trailing spaces

                if not invoice_no:
                    messagebox.showerror("Error", "INVOICE No. MUST be keyed", parent=self.root)
                    return

                cur.execute("SELECT * FROM customer WHERE invoice=?", (invoice_no,))
                row = cur.fetchone()

                if row is None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Employee Deleted Successfully", parent=self.root)
                        self.clear()  # Ensure self.clear() exists
                        self.var_cus_invoice.set(self.generate_auto_number(increment=False))

                    else:
                        # You can add any action here if deletion was canceled or not confirmed
                        messagebox.showinfo("Cancelled", "Employee deletion cancelled", parent=self.root)


            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            finally:
                con.close()  # Close the database connection safely

    def clear(self):

        self.var_cus_invoice.set(self.generate_auto_number(increment=False))

        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0', END)
        self.var_searchtxt.get()
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                self.show()
            else:
                cur.execute("select * from customer where invoice=?", (self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row!=None:
                    self.customerTable.delete(*self.customerTable.get_children())
                    self.customerTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record was found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = customerClass(root)
    root.mainloop()
