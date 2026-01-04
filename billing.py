from tkinter import *
from tkinter import ttk, messagebox
import os
import sys
import time
import sqlite3
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk
from io import BytesIO


class BillClass:
    def __init__(self, root, employee_id="Unknown"):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("")
        self.root.config(bg="white")
        self.root.state("zoomed")
        self.cart_list = []
        self.chk_print = 0

        # ---------------title----------------

        self.icon_title = PhotoImage(file="")
        title = Label(self.root, text="", image=self.icon_title, compound=LEFT, font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=100)

        # --------btn logout -------------
        # ---------clock--------------------
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System\t\t Date: DD-YYYY\t\t Time: HH:MM:SS", font=("times new roman", 15, "bold"), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=11, relwidth=1, height=30)

        # ------------product frame------------------------
        self.var_search = StringVar()
        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProductFrame1.place(x=6, y=50, width=944, height=500)

        pTitle = Label(ProductFrame1, text="All Products", font=("goudy old style", 20, "bold"), bg="#262626", fg="white").pack(side=TOP, fill=X)

        # --------------Product Search Frame------------------
        self.var_search = StringVar()
        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg="white")
        ProductFrame2.place(x=270, y=42, width=398, height=90)

        lbl_search = Label(ProductFrame2, text="Search Product | By Name", font=("times new roman", 15, "bold"), bg="white", fg="green").place(x=2, y=5)

        lbl_search = Label(ProductFrame2, text="Product Name", font=("times new roman", 15, "bold"), bg="white").place(x=2, y=45)
        txt_search = Entry(ProductFrame2, textvariable=self.var_search, font=("times new roman", 15), bg="lightyellow").place(x=128, y=47, width=150, height=22)
        btn_search = Button(ProductFrame2, text="Search", command=self.search, font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=285, y=45, width=100, height=25)
        btn_show_all = Button(ProductFrame2, text="Show All", command=self.show, font=("goudy old style", 15), bg="#083531", fg="white", cursor="hand2").place_forget()

        # --- Product Frame ---
        ProductFrame1 = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        ProductFrame1.place(x=12, y=190, width=930, height=350)

        # --- New Scrollable Product Display Area ---
        canvas_frame = Frame(ProductFrame1)
        canvas_frame.place(x=6, y=5, width=915, height=290)

        self.canvas = Canvas(canvas_frame, bg="white")
        self.product_display = Frame(self.canvas, bg="white")

        scrollbar = Scrollbar(canvas_frame, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas.create_window((0, 0), window=self.product_display, anchor="nw")

        # Enable scrolling when content overflows
        self.product_display.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Category Buttons Frame
        self.ProductFrame1 = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        self.ProductFrame1.place(x=12, y=190, width=920, height=350)

        self.create_scrollable_product_area()
        self.create_category_buttons()
        self.show("Home")

        # --- Label for stock info ---
        self.lbl_inStock = Label(ProductFrame1, text="In Stock: 0", font=("goudy old style", 12), bg="white",
                                 fg="green")
        self.lbl_inStock.place(x=10, y=520)

        # --- Show products on startup ---
        self.show()
        # lbl_note = Label(ProductFrame1, text="Note: 'Enter 0 Quantity to remove product from the Cart", font=("goudy old style", 11),anchor="w", bg="white", fg="red").pack(side=BOTTOM, fill=X)

        # ---------------------Customer Frame--------------------
        self.var_cname = StringVar()
        self.cashiname = StringVar()
        self.IdCashi = StringVar()
        self.var_contact = StringVar()
        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        CustomerFrame.place_forget()

        cTitle = Label(CustomerFrame, text="Customer Details", font=("goudy old style", 15,), bg="lightgray").pack(side=TOP, fill=X)
        lbl_name = Label(CustomerFrame, text=" Name", font=("times new roman", 15,), bg="white").place(x=5, y=35)
        txt_name = Entry(CustomerFrame, textvariable=self.var_cname, font=("times new roman", 13), bg="lightyellow").place(x=80, y=35, width=180)
        cname = Entry(CustomerFrame, textvariable=self.cashiname, font=("times new roman", 13),bg="lightyellow").place_forget()
        id = Entry(CustomerFrame, textvariable=self.IdCashi, font=("times new roman", 13), bg="lightyellow").place_forget()
        self.IdCashi.set(employee_id)
        # self.IdCashi.set(f"python loginn.py {self.employee_id}")
        lbl_contact = Label(CustomerFrame, text=" Contact No.", font=("times new roman", 15,), bg="white").place(x=270, y=35)
        txt_contact = Entry(CustomerFrame, textvariable=self.var_contact, font=("times new roman", 13), bg="lightyellow").place(x=380, y=35, width=140)

        # --------------Cal Cart Frame------------------
        Cal_Cart_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Cal_Cart_Frame.place_forget()

        # --------------Cart Frame------------------
        Cart_Frame = Frame(Cal_Cart_Frame, bd=3, relief=RIDGE)
        Cart_Frame.place_forget()
        self.cartTitle = Label(Cart_Frame, text="Cart \t Total Products: [0]", font=("goudy old style", 15,), bg="lightgray")
        self.cartTitle.pack(side=TOP, fill=X)

        scrolly = Scrollbar(Cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(Cart_Frame, orient=HORIZONTAL)

        self.Cart_Table = ttk.Treeview(Cart_Frame, columns=("pid", "name", "price", "qty"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack_forget()
        scrolly.pack_forget()
        scrollx.config(command=self.Cart_Table.xview)
        scrolly.config(command=self.Cart_Table.yview)

        self.Cart_Table.heading("pid", text="PID")
        self.Cart_Table.heading("name", text="Name")
        self.Cart_Table.heading("price", text="Price")
        self.Cart_Table.heading("qty", text="QTY")
        self.Cart_Table["show"] = "headings"
        self.Cart_Table.column("pid", width=40)
        self.Cart_Table.column("name", width=90)
        self.Cart_Table.column("price", width=90)
        self.Cart_Table.column("qty", width=40)
        self.Cart_Table.pack(fill=BOTH, expand=1)
        self.Cart_Table.bind("<ButtonRelease-1>", self.get_data_cart)

        # --------------Add cart Widget Frame------------------
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()


        Add_CartWidgetsFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Add_CartWidgetsFrame.place(x=240, y=550, width=530, height=110)

        lbl_p_name = Label(Add_CartWidgetsFrame, text="Product Name", font=("times new roman", 15), bg="white").place(x=5, y=5)
        txt_p_name = Entry(Add_CartWidgetsFrame, textvariable=self.var_pname, font=("times new roman", 15), bg="lightyellow", state='readonly').place(x=5, y=35, width=190, height=22)

        lbl_p_price = Label(Add_CartWidgetsFrame, text="Price per Qty", font=("times new roman", 15), bg="white").place(x=230, y=5)
        txt_p_price = Entry(Add_CartWidgetsFrame, textvariable=self.var_price, font=("times new roman", 15), bg="lightyellow", state='readonly').place(x=230, y=35, width=150, height=22)

        lbl_p_qty = Label(Add_CartWidgetsFrame, text="Quantity", font=("times new roman", 15), bg="white").place(x=390, y=5)
        txt_p_qty = Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, font=("times new roman", 15), bg="lightyellow").place(x=390, y=35, width=120, height=22)

        self.lbl_inStock = Label(Add_CartWidgetsFrame, text="In Stock", font=("times new roman", 15), bg="white")
        self.lbl_inStock.place(x=5, y=70)

        btn_clear_cart = Button(Add_CartWidgetsFrame, text="Clear", font=("times new roman", 15, "bold"),command=self.clear_cart, bg="lightgrey", cursor="hand2").place(x=180, y=70, width=150, height=30)
        btn_add_cart = Button(Add_CartWidgetsFrame, text="Del. | Update Cart", command=self.add_update_cart, font=("times new roman0", 15, "bold"), bg="orange", cursor="hand2").place(x=340, y=70, width=180, height=30)

        # -------------billing area------------------------
        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billFrame.place(x=953, y=50, width=410, height=470)

        BTitle = Label(billFrame, text="Sales Cart", font=("goudy old style", 20, "bold"),
                       bg="#f44336", fg="white").pack(side=TOP, fill=X)

        # ✅ Scrollbars
        scrollx = Scrollbar(billFrame, orient=HORIZONTAL)
        scrollx.pack_forget()

        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        # ✅ Treeview with Scrollbar support
        self.Cart_Table = ttk.Treeview(
            billFrame,
            columns=("pid", "name", "price", "qty"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set
        )
        self.Cart_Table.pack(fill=BOTH, expand=1)

        scrollx.config(command=self.Cart_Table.xview)
        scrolly.config(command=self.Cart_Table.yview)

        # ✅ Table Headers
        self.Cart_Table.heading("pid", text="ID")
        self.Cart_Table.heading("name", text="Product Name")
        self.Cart_Table.heading("price", text="Price")
        self.Cart_Table.heading("qty", text="Quantity")
        self.Cart_Table["show"] = "headings"

        # ✅ Column Widths
        self.Cart_Table.column("pid", width=60)
        self.Cart_Table.column("name", width=150)
        self.Cart_Table.column("price", width=100)
        self.Cart_Table.column("qty", width=60)

        # ✅ Event Binding
        self.Cart_Table.bind("<ButtonRelease-1>", self.get_data_cart)

        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack_forget()
        scrolly.config(command=self.txt_bill_area.yview)


        # --------------------billing buttons-------------------------------
        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billMenuFrame.place(x=953, y=520, width=410, height=140)

        self.lbl_amnt=Label(billMenuFrame, text="Bill Amount\n[0]", font=("goudy old style", 15, "bold"), bg="#3f51b5", fg="white")
        self.lbl_amnt.place(x=2, y=5, width=120, height=70)

        self.lbl_discount = Label(billMenuFrame, text="Discount\n[5]", font=("goudy old style", 15, "bold"), bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=124, y=5, width=120, height=70)

        self.lbl_net_pay = Label(billMenuFrame, text="Net Pay\n[0]", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white")
        self.lbl_net_pay.place(x=246, y=5, width=160, height=70)

        btn_print = Button(billMenuFrame, text="Print", command=self.print_bill,cursor="hand2", font=("goudy old style", 15, "bold"), bg="lightgreen", fg="white")
        btn_print.place_forget()

        btn_clear_all = Button(billMenuFrame, text="Clear All",command=self.clear_all, cursor="hand2", font=("goudy old style", 15, "bold"), bg="gray", fg="white")
        btn_clear_all.place(x=124, y=80, width=120, height=50)

        btn_generate = Button(billMenuFrame, text="Bill", command=self.payment_confirmation, cursor="hand2", font=("goudy old style", 15, "bold"), bg="#009688", fg="white")
        btn_generate.place(x=2, y=80, width=120, height=50)

        btn_logout = Button(self.root, text="Logout", command=self.logout, font=("times new roman", 15, "bold"),
                            bg="yellow", cursor="hand2").place(x=1200, y=603, width=160, height=50)

        self.cart_list = []

        # -----------------footer----------------------------------------
        footer=Label(self.root, text="IMS- Inventory Management System", font=("times new roman", 11), bg="#4d636d", fg="white").pack(side=BOTTOM, fill=X)

        self.show()
        # self.bill_top()
        self.update_date_time()

        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()

            # ✅ Fetch the name where `eid` matches `self.IdCashi`
            cur.execute("SELECT name FROM employee WHERE eid = ?", (self.IdCashi.get(),))
            row = cur.fetchone()  # Fetch a single result

            if row:
                self.cashiname.set(row[0])  # Store the employee name in `self.cashiname`
            else:
                messagebox.showinfo("Info", "No employee found with this ID.", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            con.close()

            # -----------------------All function----------------------------------

    from PIL import Image, ImageTk
    import os

    from io import BytesIO
    def create_scrollable_product_area(self):
        canvas_frame = Frame(self.ProductFrame1)
        canvas_frame.place(x=6, y=5, width=915, height=340)

        self.canvas = Canvas(canvas_frame, bg="white")
        self.product_display = Frame(self.canvas, bg="white")

        scrollbar = Scrollbar(canvas_frame, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas.create_window((0, 0), window=self.product_display, anchor="nw")

        self.product_display.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

    def create_category_buttons(self):
        category_frame = Frame(self.ProductFrame1, bg="white")
        category_frame.place(x=150, y=288, width=600, height=40)

        # Fetch categories dynamically from DB
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT DISTINCT category FROM product WHERE status='Active'")
            categories = [row[0] for row in cur.fetchall()]
        except Exception as ex:
            messagebox.showerror("Error", f"Error loading categories: {str(ex)}", parent=self.root)
            categories = []
        finally:
            con.close()

        # Add "Home" button first
        categories.insert(0, "Home")

        # Create a container frame to center buttons
        center_frame = Frame(category_frame, bg="white")
        center_frame.pack(expand=True)

        for cat in categories:
            btn = Button(
                center_frame,
                text=cat,
                font=("goudy old style", 14, "bold"),
                bg="#e0e0e0",
                fg="black",
                cursor="hand2",
                padx=12,
                pady=5,
                bd=0,
                relief=SOLID,
                command=lambda c=cat: self.show(c)
            )
            btn.pack(side=LEFT, padx=10)

    def show(self, category="Home"):
        for widget in self.product_display.winfo_children():
            widget.destroy()

        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if category == "Home":
                cur.execute("SELECT pid, name, price, image FROM product WHERE status='Active' AND qty > 0")
            else:
                cur.execute("SELECT pid, name, price, image FROM product WHERE category=? AND status='Active' AND qty > 0", (category,))
            rows = cur.fetchall()

            self.product_images = []
            max_columns = 4
            row_num = 0
            col_num = 0

            for row in rows:
                pid, name, price, img_data = row

                photo = self.load_product_image_from_db(img_data)
                self.product_images.append(photo)

                item_frame = Frame(self.product_display, bd=1, relief=SOLID, bg="white")
                item_frame.grid(row=row_num, column=col_num, padx=10, pady=10)

                btn = Button(
                    item_frame,
                    text=f"{name}\n₱{float(price):.2f}",
                    compound=TOP,
                    font=("times new roman", 12),
                    wraplength=100,
                    bg="white",
                    image=photo,
                    cursor="hand2",
                    command=lambda r=row: self.select_product(r)
                )
                btn.pack()

                col_num += 1
                if col_num >= max_columns:
                    col_num = 0
                    row_num += 1

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def filter_by_category(self, category):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if category == "Home":
                cur.execute("SELECT pid, name, price, image FROM product WHERE status='Active' AND qty > 0")
            else:
                cur.execute(
                    "SELECT pid, name, price, image FROM product WHERE category=? AND status='Active' AND qty > 0",
                    (category,))

            rows = cur.fetchall()

            # Clear current product display
            for widget in self.product_display.winfo_children():
                widget.destroy()

            self.product_images = []
            row_num = 0
            col_num = 0
            max_columns = 4

            for row in rows:
                pid, name, price, img_data = row
                photo = self.load_product_image_from_db(img_data)
                self.product_images.append(photo)

                item_frame = Frame(self.product_display, bd=1, relief=SOLID, bg="white")
                item_frame.grid(row=row_num, column=col_num, padx=10, pady=10)

                btn = Button(
                    item_frame,
                    text=f"{name}\n₱{float(price):.2f}",
                    compound=TOP,
                    font=("times new roman", 12),
                    wraplength=100,
                    bg="white",
                    image=photo,
                    cursor="hand2",
                    command=lambda r=row: self.select_product(r)
                )
                btn.pack()

                col_num += 1
                if col_num >= max_columns:
                    col_num = 0
                    row_num += 1

        except Exception as ex:
            messagebox.showerror("Error", f"Error while filtering: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def load_product_image_from_db(self, img_data):
        try:
            if img_data:
                img = Image.open(BytesIO(img_data))
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                return photo
            else:
                print("No image data found in database, using default image.")
                img = Image.new('RGB', (100, 100), color='gray')
                photo = ImageTk.PhotoImage(img)
                return photo
        except Exception as e:
            print(f"Failed to load image from database: {e}")
            img = Image.new('RGB', (100, 100), color='gray')
            photo = ImageTk.PhotoImage(img)
            return photo

    def select_product(self, row):
        try:
            pid, name, price, img = row
            self.var_pid.set(pid)
            self.var_pname.set(name)
            self.var_price.set(price)

            # Connect to the database and retrieve the stock for the selected product
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            cur.execute("SELECT qty FROM product WHERE pid=?", (pid,))
            result = cur.fetchone()

            if result:  # If the product is found in the database
                stock = result[0]
                self.var_stock.set(stock)
                self.var_qty.set("1")  # Default quantity is 1
                self.lbl_inStock.config(text=f"In Stock: {stock}")

                # Now, add the product to the cart list (if not already in the cart)
                self.add_to_cart(pid, name, price, stock)

                self.bill_updates()

            else:
                messagebox.showerror("Error", "Product not found in the database.", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

        finally:
            con.close()

    def add_to_cart(self, pid, pname, price, stock):
        # Check if the product is already in the cart
        for item in self.cart_list:
            if item[0] == pid:  # Check if product already in cart
                messagebox.showinfo("Info", "Product is already in the cart.", parent=self.root)
                return  # Exit if already in the cart

        # Add new product to the cart list (with quantity set to 1 initially)
        cart_item = [pid, pname, price, "1", stock]  # cart item format: [pid, pname, price, qty, stock]
        self.cart_list.append(cart_item)

        # Update the cart display (Treeview) with the new product
        self.update_cart_table()

    def update_cart_table(self):
        # Clear the existing rows in the Treeview to avoid duplicates
        for row in self.Cart_Table.get_children():
            self.Cart_Table.delete(row)

        # Insert all items from cart_list into the Treeview
        for item in self.cart_list:
            self.Cart_Table.insert('', 'end', values=item)

    def search(self):
        # Clear previous product display
        for widget in self.product_display.winfo_children():
            widget.destroy()

        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            search_term = self.var_search.get().strip()
            if search_term == "":
                self.show()
                return

            cur.execute("SELECT pid, name, price, image FROM product WHERE name LIKE ? AND status='Active'",
                        ('%' + search_term + '%',))
            rows = cur.fetchall()

            if rows:
                self.product_images = []
                max_columns = 4
                row_num = col_num = 0

                for row in rows:
                    pid, name, price, img_data = row
                    photo = self.load_product_image_from_db(img_data)
                    self.product_images.append(photo)

                    item_frame = Frame(self.product_display, bd=1, relief=SOLID, bg="white")
                    item_frame.grid(row=row_num, column=col_num, padx=10, pady=10)

                    btn = Button(
                        item_frame,
                        text=f"{name}\n₱{float(price):.2f}",
                        compound=TOP,
                        font=("times new roman", 12),
                        wraplength=100,
                        bg="white",
                        image=photo,
                        cursor="hand2",
                        command=lambda r=row: self.select_product(r)
                    )
                    btn.pack()

                    col_num += 1
                    if col_num >= max_columns:
                        col_num = 0
                        row_num += 1
            else:
                messagebox.showinfo("Info", "No record was found", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, product):
        """Receives product data from button click and updates fields."""
        print("Clicked product:", product)

        pid, pname, price, stock = product

        self.var_pid.set(pid)
        self.var_pname.set(pname)
        self.var_price.set(price)
        self.lbl_inStock.config(text=f"In Stock[{stock}]")
        self.var_stock.set(stock)
        self.var_qty.set("1")  # Default quantity

        print("Calling add_update_cart...")
        self.add_update_cart()

    def get_data_cart(self, ev):
        # Get the selected row

        selected_item = self.Cart_Table.focus()
        content = self.Cart_Table.item(selected_item)
        row = content.get('values', [])  # Get row values, avoid errors

        if row:  # Check if row is not empty
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.var_qty.set(row[3])
            self.lbl_inStock.config(text=f"In Stock[{str(row[4])}]")
            self.var_stock.set(row[4])



    def add_update_cart(self):
        if self.var_pid.get() == '':
            messagebox.showerror('Error', "Please select product from the list", parent=self.root)
        elif self.var_qty.get() == '':
            messagebox.showerror('Error', "Input Quantity", parent=self.root)
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror('Error', "Invalid Quantity", parent=self.root)

        else:
            # price_cal = int(self.var_qty.get())*float(self.var_price.get())
            # price_cal = float(price_cal)
            price_cal = self.var_price.get()
            # pid, name, price, qty, stock
            cart_data = [self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get()]
            # ----------update cart--------------------
            present = 'no'
            index_ = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = 'yes'
                    break
                index_+= 1
            if present == 'yes':
                op = messagebox.askyesno('confirm', "Product already present\nDo you want to Update| Remove from the Cart List", parent=self.root)
                if op == True:
                    if self.var_qty.get() == "0":
                        self.cart_list.pop(index_)
                    else:
                        # pid, name, price, qty, status
                        # self.cart_list[index_][2] = price_cal #price
                        self.cart_list[index_][3] = self.var_qty.get() #quantity
            else:
                self.cart_list.append(cart_data)

            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amnt = 0
        self.net_pay = 0
        self.discount = 0

        for row in self.cart_list:
            # pid, name, price, qty, stock
            self.bill_amnt += float(row[2]) * int(row[3])

        # Check if customer is a loyal customer (Modify this condition as needed)
        if self.var_cname.get() and self.var_contact.get():  # If customer details exist
            is_loyal_customer = messagebox.askyesno(
                "Loyalty Discount", "Is this customer a loyal customer?\nApply 5% discount?", parent=self.root
            )
            if is_loyal_customer:
                self.discount = (self.bill_amnt * 5) / 100

        # Calculate final net pay
        self.net_pay = self.bill_amnt - self.discount

        # Update labels with proper formatting
        self.lbl_amnt.config(text=f'Bill Amount (₱)\n{self.bill_amnt:.2f}')
        self.lbl_net_pay.config(text=f'Net Pay (₱)\n{self.net_pay:.2f}')
        self.cartTitle.config(text=f"Cart \t Total Products: [{len(self.cart_list)}]")

    def show_cart(self):
        try:
            self.Cart_Table.delete(*self.Cart_Table.get_children())
            for row in self.cart_list:
                self.Cart_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def payment_confirmation(self):
        """ Open a confirmation window before generating the bill """

        if self.net_pay == 0:
            messagebox.showerror("Error", "No items in the cart!", parent=self.root)
            return

        self.payment_win = Toplevel(self.root)
        self.payment_win.title("Payment Confirmation")
        self.payment_win.geometry("400x250+500+200")
        self.payment_win.focus_force()

        Label(self.payment_win, text="Confirm Payment", font=('goudy old style', 15, 'bold'), bg="#3f51b5",
              fg="white").pack(side=TOP, fill=X)

        # Display Net Pay
        Label(self.payment_win, text=f"Net Pay (₱): {self.net_pay:.2f}", font=('times new roman', 12, 'bold')).place(
            x=20, y=60)

        # Customer Payment Amount Entry
        Label(self.payment_win, text="Customer Payment (₱):", font=('times new roman', 12)).place(x=20, y=100)

        self.var_payment_amount = StringVar()

        # Validation function (only digits, max 7 characters)
        def validate_payment(new_value):
            if new_value == "":  # Allow empty input
                return True
            return new_value.isdigit() and len(new_value) <= 7

        validate_cmd = (self.payment_win.register(validate_payment), "%P")

        self.txt_payment = Entry(self.payment_win, textvariable=self.var_payment_amount, font=("times new roman", 12),
                                 bg="lightyellow", validate="key", validatecommand=validate_cmd)
        self.txt_payment.place(x=20, y=130, width=250, height=30)

        # Proceed Button
        Button(self.payment_win, text="Proceed", command=self.validate_payment, font=("times new roman", 12),
               bg="lightblue").place(x=280, y=130, width=100, height=30)

    def validate_payment(self):
        """ Validate payment amount before generating bill """
        try:
            entered_amount = int(self.var_payment_amount.get())

            if entered_amount < self.net_pay:
                messagebox.showerror("Error", "Insufficient amount!", parent=self.payment_win)
            else:
                change = entered_amount - self.net_pay
                self.change = change  # Store change as a class attribute

                if change > 0:
                    messagebox.showinfo("Change", f"Payment Confirmed!\nChange: ₱{change:.2f}", parent=self.payment_win)
                else:
                    messagebox.showinfo("Success", "Payment Confirmed!", parent=self.payment_win)

                self.payment_win.destroy()  # Close the payment window
                self.generate_bill()  # Proceed to generate the bill
                self.clear_cart()  # Clear cart after successful payment
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered!", parent=self.payment_win)

            # Load the logo image

    def generate_bill(self):

        # Check if the cart is empty
        if len(self.cart_list) == 0:
            messagebox.showerror("Error", f"Please Add Product to the Cart", parent=self.root)
            return

        # --------------------Bill Top--------------------------
        self.bill_top()

        # --------------------Bill Middle--------------------------
        self.bill_middle()

        # --------------------Bill Bottom--------------------------
        self.bill_bottom()

        # Prepare data to insert into the database
        # Validate payment amount before looping
        try:
            payment_amount = float(self.var_payment_amount.get())
            if payment_amount <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Error", "Invalid amount value. Please enter a valid number.", parent=self.root)
            return

        data_to_insert = []

        for row in self.Cart_Table.get_children():
            product = self.Cart_Table.item(row, "values")[1]  # Correct index for product
            qty = self.Cart_Table.item(row, "values")[3]  # Correct index for quantity

            # Ensure qty is an integer
            try:
                qty = int(qty)
            except ValueError:
                messagebox.showerror("Error", f"Invalid quantity value for product {product}.", parent=self.root)
                return

            if not product or qty <= 0:
                messagebox.showerror("Error", "Product or quantity is missing.", parent=self.root)
                return

            formatted_date = datetime.now().strftime("%B %d, %Y (%I:%M %p)")
            data_to_insert.append((self.invoice, product, qty, payment_amount, formatted_date,
                                   self.cashiname.get(), self.net_pay))

        # Now insert into DB
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()

            cur.executemany('''
                   INSERT INTO sales (invoice, product, quantity, amount, date, cashier, net)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
               ''', data_to_insert)

            con.commit()
            # messagebox.showinfo("Success", "Data inserted successfully!", parent=self.root)
            print("Data inserted successfully")

        except sqlite3.Error as ex:
            messagebox.showerror("Database Error", f"Failed to insert data: {str(ex)}", parent=self.root)
            print(f"Database error: {str(ex)}")

        finally:
            con.close()

        # Save the bill
        try:
            with open(f'bill/{str(self.invoice)}.txt', 'w') as fp:
                fp.write(self.txt_bill_area.get('1.0', 'end'))
        #     messagebox.showinfo('Saved', "Bill has been Saved", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the bill: {str(e)}", parent=self.root)

        self.chk_print = 1
        self.root.after(1000, self.auto_print_after_generate)

    def auto_print_after_generate(self):
        if self.chk_print == 1:
            response = messagebox.askyesno("Print Preview", "Do you want to preview the bill before printing?")
            if response:
                self.print_bill()
                self.root.after(1000, self.clear_all())
            else:
                self.auto_print_only()
                self.root.after(1000, self.clear_all())  # Wait 1 sec then clear
            self.chk_print = 0

    def bill_top(self):
        """ Create the top section of the bill including cashier name, bill number, and date/time. """
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f'''

    Cashier Name: {self.cashiname.get()}
    Bill Number: {str(self.invoice)}
    Date: {str(time.strftime("%m/%d/%Y"))}   Time: {str(time.strftime("%I:%M:%S %p"))}

    Product Name       QTY       Price
    '''

        self.txt_bill_area.delete('1.0', END)  # Clear any previous text in the bill area
        self.txt_bill_area.insert('1.0', bill_top_temp)  # Insert the bill header

    def bill_bottom(self):
        """ Create the bottom section of the bill including total amounts, discount, payment, and change. """

        # Create the formatted string for the bottom section without bold
        bill_bottom_temp = f'''
        Bill Amount:   PHP{self.bill_amnt:.2f}
       

        Net Pay:       PHP{self.net_pay:.2f}  
        Payment:       PHP{self.var_payment_amount.get()}  
        Change:        PHP{self.change:.2f}  
        '''

        # Insert the formatted bill content into the Text widget
        self.txt_bill_area.insert(END, bill_bottom_temp)

        # Apply bold formatting to the parts of the bill (Net Pay, Payment, Change)
        # We assume these values appear at the end, adjust ranges as necessary
        # Apply bold formatting to 'Net Pay', 'Payment', and 'Change' lines

        # Example of making the last three lines bold
        start_idx = self.txt_bill_area.index("end-6c")  # Adjust this if necessary
        end_idx = self.txt_bill_area.index("end-2c")  # Adjust this if necessary

        # Apply bold formatting to these lines
        self.txt_bill_area.tag_add("bold", start_idx, end_idx)
        self.txt_bill_area.tag_configure("bold", font=("Courier", 10, "bold"))

    def bill_middle(self):
        """ Insert the middle section of the bill, which includes product names, quantities, and prices. """
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Loop through items in the cart and format them for display in the bill
            for row in self.cart_list:
                # pid, name, price, qty, stock
                pid = row[0]
                name = row[1]
                qty = int(row[4]) - int(row[3])  # Remaining quantity
                status = 'Inactive' if int(row[3]) == int(row[4]) else 'Active'
                price = float(row[2]) * int(row[3])  # Total price per item
                price = f"PHP {price:.2f}"  # Format price with currency symbol

                # Format the product line: aligned for product name, quantity, and price
                self.txt_bill_area.insert(END, f"\n{name:<20} {row[3]:<5} {price:<10}")

                # Update product quantity and status in the database
                cur.execute('UPDATE product SET qty=?, status=? WHERE pid=?', (
                    qty,
                    status,
                    pid
                ))
                con.commit()

            con.close()
            self.show()  # Refresh any UI updates (if needed)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')


    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0', END)
        self.cartTitle.config(text=f"Cart \t Total Products: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()
        self.chk_print = 0

    def update_date_time(self):
        time_ = time.strftime("%I:%M:%S")
        date_ = time.strftime("%m-%d-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200, self.update_date_time)

    def print_bill(self):
        """ Generate and preview the bill as a clean, well-formatted PDF receipt with a logo. """
        bill_content = self.txt_bill_area.get('1.0', 'end').strip()  # Get full text

        if not bill_content:
            messagebox.showerror('Print', "Bill is empty. Generate the bill first.", parent=self.root)
            return

        messagebox.showinfo('Print', "Generating PDF, please wait...", parent=self.root)

        try:
            import tempfile
            from reportlab.pdfgen import canvas
            from reportlab.lib.utils import ImageReader  # ✅ Allows image handling
            import os
            import webbrowser

            # ✅ Path to your logo image (Ensure it's a valid path)
            logo_path = "remove.png"  # Change this to your actual image path

            # ✅ Create a temporary PDF file
            temp_pdf = tempfile.mktemp('.pdf')

            # ✅ Base receipt width
            receipt_width = 250  # Fixed width for a compact receipt
            line_height = 14  # Space between lines
            padding = 50  # Extra spacing for headers and footers

            # ✅ Calculate exact height based on bill content
            num_lines = len(bill_content.split('\n'))
            receipt_height = padding + (num_lines * line_height) + 50  # Adjust height dynamically

            pdf = canvas.Canvas(temp_pdf, pagesize=(receipt_width, receipt_height))
            pdf.setFont("Courier-Bold", 10)  # ✅ Larger, bolder font

            # ✅ Draw Image (Logo)
            try:
                pdf.drawImage(ImageReader(logo_path), 70, receipt_height - 50, width=100, height=40, mask='auto')
            except Exception:
                print("⚠️ Logo not found or cannot be loaded. Skipping image.")

            # ✅ Centered Title
            pdf.drawCentredString(receipt_width / 2, receipt_height - 70, "KLBN Corporation")
            pdf.setFont("Courier", 9)
            pdf.drawCentredString(receipt_width / 2, receipt_height - 85, "Sta. Ana Drive, Brgy. Sun Valley")
            pdf.drawCentredString(receipt_width / 2, receipt_height - 100, "Parañaque City, Metro Manila, Philippines")

            y_position = receipt_height - 120  # Start below the title

            # ✅ Draw horizontal separator line
            def draw_separator():
                nonlocal y_position
                y_position -= line_height

            draw_separator()  # Top separator

            # ✅ Add bill details dynamically, center product name, qty, price
            lines = bill_content.split('\n')
            for line in lines:
                if line.strip():  # Skip empty lines
                    parts = line.strip().split('|')  # Assuming data is separated by "|"
                    if len(parts) == 3:
                        product_name, qty, price = parts
                        # Center product, qty, and price
                        # Calculate positions dynamically based on string lengths
                        product_name_x = (receipt_width - len(product_name) * 7) / 2
                        qty_x = (receipt_width - len(qty) * 7) / 2
                        price_x = (receipt_width - len(price) * 7) / 2

                        pdf.drawString(product_name_x, y_position, product_name)
                        pdf.drawString(qty_x, y_position - 10, qty)
                        pdf.drawString(price_x, y_position - 20, price)
                    else:
                        pdf.drawString(10, y_position, line.strip())  # Left-aligned text if format is unexpected
                    y_position -= line_height  # Move down for the next line

            draw_separator()  # Bottom separator



            pdf.save()  # ✅ Save the PDF file

            # ✅ Open the PDF for preview
            if os.name == 'nt':  # Windows
                os.startfile(temp_pdf)
            else:  # macOS / Linux
                webbrowser.open(temp_pdf)

        except Exception as ex:
            messagebox.showerror("Print Error", f"Error while generating receipt: {str(ex)}", parent=self.root)

    def auto_print_only(self):
        """ Generate and print the bill as a clean PDF receipt without preview. """
        bill_content = self.txt_bill_area.get('1.0', 'end').strip()

        if not bill_content:
            messagebox.showerror('Print', "Bill is empty. Generate the bill first.", parent=self.root)
            return

        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.utils import ImageReader
            import os
            import subprocess
            import platform

            logo_path = "remove.png"
            filename = f"bill/{str(self.invoice)}.pdf"  # Save permanently

            receipt_width = 250
            line_height = 14
            padding = 50
            num_lines = len(bill_content.split('\n'))
            receipt_height = padding + (num_lines * line_height) + 50

            pdf = canvas.Canvas(filename, pagesize=(receipt_width, receipt_height))
            pdf.setFont("Courier-Bold", 10)

            try:
                pdf.drawImage(ImageReader(logo_path), 70, receipt_height - 50, width=100, height=40, mask='auto')
            except Exception:
                print("⚠️ Logo not found or cannot be loaded. Skipping image.")

            pdf.drawCentredString(receipt_width / 2, receipt_height - 70, "KLBN Corporation")
            pdf.setFont("Courier", 9)
            pdf.drawCentredString(receipt_width / 2, receipt_height - 85, "Sta. Ana Drive, Brgy. Sun Valley")
            pdf.drawCentredString(receipt_width / 2, receipt_height - 100, "Parañaque City, Metro Manila, Philippines")

            y_position = receipt_height - 120

            def draw_separator():
                nonlocal y_position
                y_position -= line_height

            draw_separator()

            lines = bill_content.split('\n')
            for line in lines:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        product_name, qty, price = parts
                        product_name_x = (receipt_width - len(product_name) * 7) / 2
                        qty_x = (receipt_width - len(qty) * 7) / 2
                        price_x = (receipt_width - len(price) * 7) / 2

                        pdf.drawString(product_name_x, y_position, product_name)
                        pdf.drawString(qty_x, y_position - 10, qty)
                        pdf.drawString(price_x, y_position - 20, price)
                    else:
                        pdf.drawString(10, y_position, line.strip())
                    y_position -= line_height

            draw_separator()
            pdf.save()
            print("✅ Bill saved without preview.")

            # ✅ Auto send to printer after saving
            system_platform = platform.system()
            if system_platform == "Windows":
                os.startfile(os.path.abspath(filename), "print")
            elif system_platform == "Darwin":  # macOS
                subprocess.run(["lp", filename])
            elif system_platform == "Linux":
                subprocess.run(["lp", filename])
            else:
                print("❌ Printing not supported on this OS.")

        except Exception as ex:
            messagebox.showerror("Print Error", f"Error while generating receipt: {str(ex)}", parent=self.root)

    def logout(self):
        self.root.destroy()
        # self.root.destroy()
        os.system("python loginn.py")

if __name__ == "__main__":
    employee_id = sys.argv[1] if len(sys.argv) > 1 else "Unknown"

    root = Tk()
    obj = BillClass(root,employee_id)
    root.mainloop()
