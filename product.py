from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import filedialog
import io


class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("")
        self.root.config(bg="white")
        self.root.resizable(False, False)  # Disable window resizing
        self.root.attributes('-toolwindow', False)  # Remove minimize & maximize buttons
        self.root.focus_force()
        # ------------------------------------------------------
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_cus = StringVar()
        self.cat_list = []
        self.cus_list = []
        self.fetch_cat_cus()

        self.var_name = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()

        self.var_qty.set("0")

        product_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=450, height=480)

        # -----------------------title---------------------------------
        title = Label(product_Frame, text="Manage Product Details", font=("goudy old style", 18), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

        # ------------------------column----------------------------------------
        lbl_category = Label(product_Frame, text="Category", font=("goudy old style", 18), bg="white").place(x=30, y=60)
        lbl_customer = Label(product_Frame, text="Supplier", font=("goudy old style", 18), bg="white").place(x=30, y=110)
        lbl_product_name = Label(product_Frame, text="Name", font=("goudy old style", 18), bg="white").place(x=30, y=160)
        lbl_price = Label(product_Frame, text="Price", font=("goudy old style", 18), bg="white").place(x=30, y=210)
        lbl_qty = Label(product_Frame, text="Quantity", font=("goudy old style", 18), bg="white").place_forget()
        lbl_status = Label(product_Frame, text="Status", font=("goudy old style", 18), bg="white").place_forget()

        # ----------------------Column 2---------------------------------------
        cmb_cat = ttk.Combobox(product_Frame, textvariable=self.var_cat, values=self.cat_list, state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_cat.place(x=150, y=60, width=200)
        cmb_cat.current(0)

        cmb_cus = ttk.Combobox(product_Frame, textvariable=self.var_cus, values=self.cus_list, state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_cus.place(x=150, y=110, width=200)
        cmb_cus.current(0)

        def validate_name(new_value):
            return (new_value.replace(" ", "").isalpha() and len(new_value) <= 25) or new_value == ""

        validate_cmd = (root.register(validate_name), "%P")

        self.txt_name = Entry(root, textvariable=self.var_name, font=("goudy old style", 15),
                              bg="lightyellow", validate="key", validatecommand=validate_cmd)
        self.txt_name.place(x=160, y=170, width=200)

        def validate_price(new_value):
            return new_value.isdigit() and len(new_value) <= 7 or new_value == ""

        validate_cmd = (root.register(validate_price), "%P")

        self.txt_price = Entry(root, textvariable=self.var_price, font=("goudy old style", 15),
                               bg="lightyellow", validate="key", validatecommand=validate_cmd)
        self.txt_price.place(x=160, y=220, width=200)

        def validate_qty(new_value):
            return new_value.isdigit() and len(new_value) <= 6 or new_value == ""

        validate_cmd = (root.register(validate_qty), "%P")
        self.var_qty.set("0")
        self.txt_qty = Entry(root, textvariable=self.var_qty, font=("goudy old style", 15),
                             bg="lightyellow",  state="readonly",validate="key", validatecommand=validate_cmd)
        self.txt_qty.place_forget()
        cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status, values=("Active", "Inactive"), state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_status.place_forget()
        cmb_status.current(0)

        # ---------------button-----------------------
        btn_add = Button(product_Frame, text="Save", command=self.add, font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=10, y=400, width=100, height=40)
        btn_update = Button(product_Frame, text="Update", command=self.update, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=120, y=400, width=100, height=40)
        btn_delete = Button(product_Frame, text="Delete", command=self.delete, font=("goudy old style", 15), bg="#f44336", fg="white", cursor="hand2").place(x=230, y=400, width=100, height=40)
        btn_clear = Button(product_Frame, text="Clear", command=self.clear, font=("goudy old style", 15), bg="#607d8b", fg="white", cursor="hand2").place(x=340, y=400, width=100, height=40)

        self.img_data = None  # To store image binary data
        self.img_path = None  # To store image path temporarily

        self.lbl_image = Label(product_Frame, text="No Image", bd=2, relief=SOLID, width=20, height=10)
        self.lbl_image.place(x=170, y=240, width=150, height=150)  # Adjust width and height as needed

        btn_browse = Button(product_Frame, text="Browse", command=self.browse_image, font=("goudy old style", 13),
                            bg="#607d8b", fg="white", cursor="hand2")
        btn_browse.place(x=70, y=300, width=80, height=30)
        # -----------------search frame-----------------------
        SearchFrame = LabelFrame(self.root, text="Search Product", font=("goudy odl style", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=480, y=10, width=600, height=80)

        # ------------ combo box options---------------------------
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Select", "Category", "Customer", "Name"), state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        def validate_search(new_value):
            return len(new_value) <= 25

        validate_cmd = (root.register(validate_search), "%P")

        self.txt_search = Entry(root, textvariable=self.var_searchtxt, font=("goudy old style", 15),
                                bg="lightyellow", validate="key", validatecommand=validate_cmd)
        self.txt_search.place(x=680, y=43, width=205)
        btn_search = Button(SearchFrame, text="Search", command=self.search, font=("goudy old style", 15), bg="#4caf50",
                            fg="white", cursor="hand2").place(x=410, y=9, width=150, height=30)

        # ------------Product details------------------
        p_frame = Frame(self.root, bd=3, relief=RIDGE)
        p_frame.place(x=480, y=100, width=600, height=390)

        scrolly = Scrollbar(p_frame, orient=VERTICAL)
        scrollx = Scrollbar(p_frame, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(p_frame, columns=("pid", "Customer", "Category", "name", "price", "qty", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)
        self.product_table.heading("pid", text="P ID")
        self.product_table.heading("Category", text="Category")
        self.product_table.heading("Customer", text="Supplier")

        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="Qty")
        self.product_table.heading("status", text="Status")


        self.product_table["show"] = ["headings"]

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




    # ------------------------------------------------------------------------------------------
    def browse_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image", filetypes=(("Image files", "*.jpg;*.png;*.jpeg"),)
        )
        if file_path:
            self.img_path = file_path
            img = Image.open(file_path)

            # Get the label's width and height to fit the image within it
            label_width = self.lbl_image.winfo_width()
            label_height = self.lbl_image.winfo_height()

            # Resize image to maintain aspect ratio and fit within the label
            img.thumbnail((label_width, label_height), Image.Resampling.LANCZOS)

            # Convert the image to a format suitable for Tkinter
            img = ImageTk.PhotoImage(img)

            # Update the label's image and adjust the label size
            self.lbl_image.config(image=img)
            self.lbl_image.image = img  # Keep a reference to the image to avoid garbage collection

            # Optionally, update the label's size if needed
            self.lbl_image.config(width=label_width, height=label_height)

            # Save image data (if needed)
            with open(file_path, 'rb') as file:
                self.img_data = file.read()

    def fetch_cat_cus(self):
        self.cat_list.append("Empty")
        self.cus_list.append("Empty")
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("Select name from category")
            cat = cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("Select name from customer")
            cus = cur.fetchall()
            if len(cus) > 0:
                del self.cus_list[:]
                self.cus_list.append("Select")
                for i in cus:
                    self.cus_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_cat.get() == "Select" or self.var_cat.get() == "Empty" or self.var_cus.get() == "Select" or self.var_name.get() == "":
                messagebox.showerror("Error", "All Fields Are Required MUST be keyed", parent=self.root)
            else:
                cur.execute("Select * from product where name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Product already present, try different", parent=self.root)
                else:
                    cur.execute("""
                        INSERT INTO product 
                        (Category, Customer, name, price, qty, status, image) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        self.var_cat.get(),
                        self.var_cus.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                        self.img_data
                    ))

                    # ✅ Reset quantity after insertion
                    self.var_qty.set("0")

                    con.commit()
                    messagebox.showinfo("Success", "Product added Successfully", parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

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

    def get_data(self, ev):
        f = self.product_table.focus()
        content = self.product_table.item(f)
        row = content['values']
        if row:
            self.var_pid.set(row[0])
            self.var_cus.set(row[1])
            self.var_cat.set(row[2])
            self.var_name.set(row[3])
            self.var_price.set(row[4])
            self.var_qty.set(row[5])
            self.var_status.set(row[6])

            # Fetch image from database
            con = sqlite3.connect(database="ims.db")
            cur = con.cursor()
            cur.execute("SELECT image FROM product WHERE pid=?", (self.var_pid.get(),))
            img_row = cur.fetchone()
            if img_row and img_row[0]:
                image_data = img_row[0]
                img = Image.open(io.BytesIO(image_data))

                # Get the size of the label
                label_width = self.lbl_image.winfo_width()
                label_height = self.lbl_image.winfo_height()

                # Resize image to fit within the label while maintaining aspect ratio
                img.thumbnail((label_width, label_height), Image.Resampling.LANCZOS)

                # Convert the image to a format Tkinter can display
                img_tk = ImageTk.PhotoImage(img)

                # Set the resized image to the label
                self.lbl_image.config(image=img_tk)
                self.lbl_image.image = img_tk  # Keep a reference to avoid garbage collection

    def resize_image_to_label_size(self, img, size):
        """
        Resize the image to the given size, maintaining the aspect ratio.
        """
        img_resized = img.resize(size, Image.Resampling.LANCZOS)  # Resize the image exactly to the label size
        return img_resized

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please select product from list", parent=self.root)
            else:
                # Check if the product exists in the database
                cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Product ID", parent=self.root)
                else:
                    # Ensure img_data is assigned properly before running the update
                    if self.img_data is None:  # Handle case where no new image is provided
                        cur.execute(
                            "UPDATE product SET Category=?, Customer=?, name=?, price=?, qty=?, status=? WHERE pid=?", (
                                self.var_cat.get(),
                                self.var_cus.get(),
                                self.var_name.get(),
                                self.var_price.get(),
                                self.var_qty.get(),
                                self.var_status.get(),
                                self.var_pid.get()
                            ))
                    else:
                        # If img_data exists, include it in the update
                        cur.execute(
                            "UPDATE product SET Category=?, Customer=?, name=?, price=?, qty=?, status=?, image=? WHERE pid=?",
                            (
                                self.var_cat.get(),
                                self.var_cus.get(),
                                self.var_name.get(),
                                self.var_price.get(),
                                self.var_qty.get(),
                                self.var_status.get(),
                                self.img_data,  # Image data
                                self.var_pid.get()  # Product ID
                            ))

                    con.commit()
                    messagebox.showinfo("Success", "Product updated Successfully", parent=self.root)
                    self.show()  # Call your show method to refresh the displayed data
                    self.clear()  # Call clear method to reset the fields

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Select Product from the list ", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from product where pid=?", (self.var_pid.get(),))
                    con.commit()
                    messagebox.showinfo("Delete", "Product Deleted Successfully", parent=self.root)
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear(self):
        # Reset all form fields to their default values
        self.var_cat.set("Select")
        self.var_cus.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")

        # Reset the image label to its default state ("No Image" text and no image)
        self.lbl_image.config(image='', text="No Image")

        # Re-display or update the content (optional)
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            search_by = self.var_searchby.get().strip()
            search_txt = self.var_searchtxt.get().strip()

            # Validate input
            if search_by == "Select":
                messagebox.showerror("Error", "Select a valid Search By option.", parent=self.root)
                return

            # If search text is empty, show all products
            if not search_txt:
                query = "SELECT pid, customer, category, name, price, qty, status FROM product"
                cur.execute(query)
            else:
                query = f"SELECT pid, customer, category, name, price, qty, status FROM product WHERE {search_by} LIKE ?"
                cur.execute(query, ('%' + search_txt + '%',))

            rows = cur.fetchall()

            # If no results, show error and return
            if not rows:
                messagebox.showerror("Error", "No record was found.", parent=self.root)
                return

            # Clear previous data
            self.product_table.delete(*self.product_table.get_children())

            # Apply row colors BEFORE inserting data
            self.product_table.tag_configure("Inactive", background="red", foreground="white")
            self.product_table.tag_configure("Active", background="green", foreground="white")

            # Insert rows with tags (including "status" column)
            for row in rows:
                status_tag = "Inactive" if row[6] == "Inactive" else "Active"
                self.product_table.insert("", "end", values=row, tags=(status_tag,))  # Keep "status" column

        except sqlite3.Error as db_err:
            messagebox.showerror("Database Error", f"Database error: {str(db_err)}", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Unexpected error: {str(ex)}", parent=self.root)
        finally:
            con.close()  # Always close connection


if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()
