from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3


class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory-Category Management")
        self.root.config(bg="white")
        self.root.resizable(False, False)  # Disable window resizing
        self.root.attributes('-toolwindow', False)  # Remove minimize & maximize buttons
        self.root.focus_force()

        # --------------- variables------------------------
        self.var_cat_id = StringVar()
        self.var_name = StringVar()

        # --------------------title-------------------------
        lbl_title = Label(self.root, text="Manage Product Category", font=("goudy old style", 30), bg="#184a45", fg="white", bd=3, relief=RIDGE).pack(side=TOP, fill=X, padx=10, pady=20)

        lbl_name = Label(self.root, text="Enter Category Name", font=("goudy old style", 30), bg="white").place(x=50, y=100)

        def validate_name_input(char, current_text):
            """Allow only letters and limit to 25 characters."""
            if len(current_text) >= 25:  # Limit to 25 characters
                return False
            if not char.isalpha() and char != " ":  # Allow only letters and spaces
                return False
            return True

        vcmd = (self.root.register(validate_name_input), "%S", "%P")

        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 18),
                         bg="lightyellow", validate="key", validatecommand=vcmd)
        txt_name.place(x=50, y=170, width=300)

        btn_add = Button(self.root, text="ADD", command=self.add, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=360, y=170, width=150, height=30)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15), bg="red", fg="white", cursor="hand2").place(x=520, y=170, width=150, height=30)

        # ------------category details------------------
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=700, y=100, width=380, height=400)

        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

        self.category_table = ttk.Treeview(cat_frame, columns=("cid", "name"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.category_table.xview)
        scrolly.config(command=self.category_table.yview)

        self.category_table.heading("cid", text="Category ID")
        self.category_table.heading("name", text="Name")
        self.category_table["show"] = "headings"
        self.category_table.column("cid", width=90)
        self.category_table.column("name", width=100)
        self.category_table.pack(fill=BOTH, expand=1)
        self.category_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # -------------------Functions----------------------

    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category Name MUST be entered", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row:
                    messagebox.showerror("Error", "Category already exists", parent=self.root)
                else:
                    cur.execute("INSERT INTO category (name) VALUES(?)", (self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Category added Successfully", parent=self.root)
                    self.show()
                    self.clear()  # Clear input after adding
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()  # Ensure DB connection closes

    def show(self):
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()

            cur.execute("SELECT * FROM category")
            rows = cur.fetchall()

            self.category_table.delete(*self.category_table.get_children())  # Clear table before inserting new data

            if rows:
                for row in rows:
                    self.category_table.insert('', END, values=row)
            else:
                messagebox.showinfo("Info", "No categories found", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            con.close()  # Ensure database connection closes properly

    def get_data(self, ev):
        try:
            f = self.category_table.focus()  # Get selected row
            if not f:
                messagebox.showerror("Error", "No record selected", parent=self.root)
                return

            content = self.category_table.item(f)
            row = content.get('values', [])

            if len(row) < 2:  # Prevent IndexError
                messagebox.showerror("Error", "Selected record is empty", parent=self.root)
                return

            self.var_cat_id.set(row[0])
            self.var_name.set(row[1])

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Please select a category from the list", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE cid=?", (self.var_cat_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid category selection", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Category Deleted Successfully", parent=self.root)
                        self.show()
                        self.clear()  # Clear inputs after deletion
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()  # Ensure DB connection closes

    def clear(self):
        """Clears input fields."""
        self.var_cat_id.set("")
        self.var_name.set("")


if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()
