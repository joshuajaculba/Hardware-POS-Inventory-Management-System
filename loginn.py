from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk, ImageSequence
from tkinter import messagebox, ttk
import sqlite3
import os
import email_pass
import smtplib
import time


class Login_system():
    def __init__(self, root):

        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Set desired window size
        window_width = min(2000, screen_width)  # Prevents overflow
        window_height = min(1000, screen_height)

        # Calculate x and y for centering
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set window size and center position
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.state("zoomed")
        self.root.title("Login System")
        self.otp =''

        # Load GIF
        self.gif = Image.open("image/log.gif")
        self.frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(self.gif)]
        self.index = 0

        # Create Label for GIF
        self.label = Label(self.root)
        self.label.pack()

        # Start animation
        self.update_gif()

        # Left image
        # self.left = ImageTk.PhotoImage(file="pic.png")
        # left = Label(self.root, image=self.left).place(x=70, y=90, width=600, height=540)
        # # ----------------login frame---------------------
        self.employee_id = StringVar()
        self.password = StringVar()

        # Load background image (make sure it's in the same folder)
         # Set image to fill the window
        # Make the entire window transparent
        self.root.attributes("-alpha", 0.80)  # 0.0 = fully transparent, 1.0 = fully opaque

        # Remove window decorations (optional, makes it frameless)

        # Labels with no background (transparent effect)
        # title = Label(self.root, text="Login System", font=("Elephant", 20, "bold"), bg="white")
        # title.place(x=588, y=180)

        # lbl_user = Label(self.root, text="Employee ID", font=("Andalus", 15), bg="white")
        # lbl_user.place(x=500, y=450)

        # # Button to close the window
        # close_btn = Button(self.root, text="Close", command=self.root.destroy)
        # close_btn.place(x=900, y=20)
        self.left = ImageTk.PhotoImage(file="image/profile (1).png")
        left = Label(self.root, image=self.left).place(x=530, y=470, width=40, height=40)

        self.right = ImageTk.PhotoImage(file="image/locked (1).png")
        right = Label(self.root, image=self.right).place(x=530, y=520, width=40, height=40)

        def character_limit(P):
            if P == "" or P == self.placeholder_text:  # Allow empty field or placeholder
                return True
            return P.isdigit() and len(P) <= 6  # Only numbers, max 6 characters

            # Register validation

        vcmd = (self.root.register(character_limit), '%P')

        # Create Entry widget with validation
        self.txt_employee_id = Entry(
            self.root,
            textvariable=self.employee_id,
            font=("Times New Roman", 15),
            bg="#ECECEC",
            fg="gray",  # Initial placeholder color
            validate="key",
            validatecommand=vcmd
        )
        self.txt_employee_id.place(x=580, y=480, width=260)

        # Add placeholder
        self.placeholder_text = "Enter Employee ID"
        self.txt_employee_id.insert(0, self.placeholder_text)

        # Bind focus events
        self.txt_employee_id.bind("<FocusIn>", self.clear_placeholder)
        self.txt_employee_id.bind("<FocusOut>", self.add_placeholder)

        # Function to clear placeholder on focus

        def clear_placeholder(self, event):
          if self.txt_employee_id.get() == self.placeholder_text:
            self.txt_employee_id.delete(0, "end")
            self.txt_employee_id.config(fg="black")  # Change text color when typing

        # Function to restore placeholder if empty on focus out

        def add_placeholder(self, event):
          if not self.txt_employee_id.get():
            self.txt_employee_id.insert(0, self.placeholder_text)
            self.txt_employee_id.config(fg="gray")  # Set placeholder color back

        # Create validation function
        def character_limit(P):
            return len(P) <= 20  # Limits input to 20 characters

        # Register validation
        vcmd = (self.root.register(character_limit), '%P')

        # Placeholder text
        self.placeholders_text = "Enter Password"

        # Create password Entry widget
        self.txt_pass = Entry(
            self.root,
            textvariable=self.password,
            font=("Times New Roman", 15),
            bg="#ECECEC",
            fg="gray",  # Placeholder color
            validate='key',
            validatecommand=vcmd
        )
        self.txt_pass.place(x=580, y=525, width=260)

        # Insert placeholder
        self.txt_pass.insert(0, self.placeholders_text)

        # Bind events for focus
        self.txt_pass.bind("<FocusIn>", self.clear_placeholders)
        self.txt_pass.bind("<FocusOut>", self.add_placeholders)

       # shw_pass =  Combobox(login_frame, font=("Ariel Rounded MT Bold", 15), bg="#00B0F0", activebackground="#00B0F0", fg="white", activeforeground="white", cursor="hand3").place(x=560, y=200, width=250, height=35)
        btn_login = Button(self.root, command=self.login, text="Log In", font=("Ariel Rounded MT Bold", 15), bg="#00B0F0", activebackground="#00B0F0", fg="white", activeforeground="white", cursor="hand2").place(x=560, y=580, width=250, height=35)

        # hr = Label(self.root, bg="lightgray").place(x=50, y=370, width=250, height=2)
        # or_ = Label(self.root, text="OR", bg="white", fg="lightgray", font=("times new roman", 15, "bold")).place(x=150, y=355)

        btn_forget = Button(self.root, text="Forget Password?",command=self.forget_window, font=("times new roman", 13), bg=root.cget("bg"), fg="#00759E",activebackground="white", activeforeground="#00759E", bd=0, ).place(x=620, y=620)
        self.toggle_btn = Checkbutton(self.root, text="Show Password", command=self.toggle_password, bg=root.cget("bg") , fg="grey")
        self.toggle_btn.place(x=730, y=553)  # Adjusted y to align with entry box

        credits_btn = Button(root, text="Credits", command=self.show_credits, font=("Arial", 8),  bg=root.cget("bg"), fg="grey")
        credits_btn.pack(pady=5)
        credits_btn.place(x=800 , y=650 )
        # -----------------------frame 2 --------------------------------
        # register_frame = Frame(self.root, bd=2, relief=RIDGE, bg="#aaa9ad")
        # register_frame.place(x=650, y=550, width=350, height=80)

        # lbl_reg = Label(register_frame, text="", font=("times new roman", 13), bg="#aaa9ad").place(x=0, y=20, relwidth=1)


# def limit_chars(self, *args):
    #     value = self.employee_id.get()
    #     value = self.password.get()
    #     if len(value) > 6:
    #         self.employee_id.set(value[:6])
    #     if len(value) > 20:
    #         self.password.set(value[:20])
    #

    def show_credits(self):
        credits_window = Toplevel()
        credits_window.title("The Minds Behind the Code")
        credits_window.configure(bg="black")
        credits_window.attributes('-alpha', 0.85)  # Transparency effect
        credits_window.resizable(False, False)  # Disable resizing
        credits_window.overrideredirect(True)  # Remove minimize, maximize, and close buttons

        # **Center the window dynamically**
        window_width = 300
        window_height = 350
        screen_width = credits_window.winfo_screenwidth()
        screen_height = credits_window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        credits_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # **Title Label**
        Label(credits_window, text="The Minds Behind the Code", font=("Arial", 14, "bold"), fg="white",
              bg="black").pack(pady=10)

        # **Frame for animation**
        frame = Frame(credits_window, bg="black")
        frame.pack(expand=True, fill="both")

        # **Names list**
        names = [
            "Andrei Atilano",
            "Zyra Canapi",
            "Joshua N. Jaculba",
            "Bryan Manlapaz",
            "Franz Ian Maico",
            "Francis Ventura"
        ]

        labels = []
        for name in names:
            lbl = Label(frame, text=name, font=("Times New Roman", 12), fg="white", bg="black")
            lbl.place(x=90, y=-50)  # Place off-screen initially
            labels.append(lbl)

        # **Fly-in Animation Function**
        def animate_labels(index=0):
            if index < len(labels):
                labels[index].place(x=90, y=30 + (index * 30))  # Move into visible area
                credits_window.after(550, animate_labels, index + 1)  # Delay between each name appearing

        # Start animation
        credits_window.after(1000, animate_labels)  # Small delay before starting animation

        # **Close Button**
        Button(credits_window, text="OK", font=("Arial", 12), bg="#333333", fg="white",
               command=credits_window.destroy).pack(pady=10)

    def clear_placeholders(self, event):
        """Removes placeholder and enables password masking"""
        if self.txt_pass.get() == self.placeholders_text:
            self.txt_pass.delete(0, END)
            self.txt_pass.config(fg="black", show="*")  # Show password as asterisks

    def add_placeholders(self, event):
        """Restores placeholder if entry is empty"""
        if self.txt_pass.get() == "":
            self.txt_pass.insert(0, self.placeholders_text)
            self.txt_pass.config(fg="gray", show="")  # Show placeholder text

    def clear_placeholder(self, event):
        """Remove placeholder when clicking inside"""
        if self.txt_employee_id.get() == self.placeholder_text:
            self.txt_employee_id.delete(0, END)
            self.txt_employee_id.config(fg="black")  # Change text color

    def add_placeholder(self, event):
        """Restore placeholder if empty"""
        if self.txt_employee_id.get() == "":
            self.txt_employee_id.insert(0, self.placeholder_text)
            self.txt_employee_id.config(fg="gray")  # Reset placeholder color

        # lbl_pass = Label(self.root, text="Password", font=("Andalus", 15), bg="#CD853F").place(x=50, y=200)
    def update_gif(self):
        """ Update the GIF frame-by-frame """
        self.label.configure(image=self.frames[self.index])  # Update label image
        self.index = (self.index + 1) % len(self.frames)  # Loop animation
        self.root.after(100, self.update_gif)  # Repeat every 100ms

    def toggle_password(self):
        """Toggle password visibility"""
        if self.txt_pass.cget('show') == '*':
            self.txt_pass.config(show='')  # Show plain text
        else:
            self.txt_pass.config(show='*')  # Mask password with asterisks

    def login(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "" or self.password.get() == "":
                messagebox.showerror('Error', "All Fields are Required", parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? AND pass=?", (self.employee_id.get(), self.password.get()))
                user = cur.fetchone()
                if user == None:

                    self.employee_id.set('')
                    self.password.set('')
                    messagebox.showerror('Error', "Invalid Username/Password", parent=self.root)
                else:
                    # print(user)
                    print(f"User Type: {user[0]}")  # Check what user[0] contains

                    if user[0] == "Admin":
                        self.root.destroy()
                        os.system("python main.py")

                    else:
                        self.root.destroy()
                        os.system(f"python billing.py {self.employee_id.get()}")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def forget_window(self):
        """Opens the password reset window and hides the main login window."""

        self.root = root
        self.employee_id = StringVar()
        self.var_otp = StringVar()
        self.var_new_pass = StringVar()
        self.var_conf_pass = StringVar()
        self.forget_win = None
        self.otp = None

        self.forget_win = Toplevel(self.root)
        self.forget_win.title('Reset Password')
        self.forget_win.geometry('400x250+500+100')
        self.forget_win.focus_force()
        self.forget_win.resizable(False, False)  # Disable maximize/minimize
        self.forget_win.attributes('-topmost', True)  # Keeps the window always on top
        self.forget_win.transient(self.root)  # Makes it modal (linked to main window)
        self.forget_win.grab_set()  # Lock interaction with main window

        # Handle closing behavior
        self.forget_win.protocol("WM_DELETE_WINDOW", self.on_close)
        # Hide main window


        Label(self.forget_win, text="Reset Password", font=('goudy old style', 15, 'bold'),
              bg="#3f51b5", fg="white").pack(side=TOP, fill=X)

        def limit_inputs(var, max_length=6):
            """Limit the input length to `max_length` characters and allow only digits."""
            value = var.get()

            # Remove non-digit characters
            value = ''.join(filter(str.isdigit, value))

            # Trim to max_length
            if len(value) > max_length:
                value = value[:max_length]

            var.set(value)  # Update the variable with valid input

        # Employee ID Field
        Label(self.forget_win, text="Employee ID:", font=('times new roman', 12)).place(x=20, y=60)
        self.employee_id = StringVar()
        self.employee_id.trace_add("write", lambda *args: limit_inputs(self.employee_id))  # Limit to 6 characters
        Entry(self.forget_win, textvariable=self.employee_id, font=('times new roman', 12),
              bg="lightyellow").place(x=20, y=90, width=250, height=30)
        # Set placeholder



        self.countdown_label = Label(self.forget_win, font=('times new roman', 12))
        self.countdown_label.place(x=20, y=130)

        # Verification Code Field
        Label(self.forget_win, text="Verification Code:", font=('times new roman', 12)).place(x=20, y=160)
        self.var_otp = StringVar()
        self.var_otp.trace_add("write", lambda *args: limit_inputs(self.var_otp))  # Limit to 6 characters
        self.code_entry = Entry(self.forget_win, textvariable=self.var_otp, font=('times new roman', 12),
                                bg="lightyellow", state='disabled')
        self.code_entry.place(x=20, y=190, width=250, height=30)

        # Buttons
        self.verify_btn = Button(self.forget_win, text="Verify", command=self.verify_otp,
                                 font=("times new roman", 12), bg="lightblue", state='disabled')
        self.verify_btn.place(x=280, y=190, width=100, height=30)

        self.send_btn = Button(self.forget_win, text="Send Code", command=self.start_reset_process,
                               font=("times new roman", 12), bg="lightblue")
        self.send_btn.place(x=280, y=90, width=100, height=30)

        self.resend_btn = Button(self.forget_win, text="Resend OTP", command=self.resend_otp,
                                 font=("times new roman", 12), bg="lightgray", state='disabled')
        self.resend_btn.place_forget()

        self.clearbtn = Button(self.forget_win, text="Clear", command=self.clear,
                             font=("times new roman", 12), bg="lightgray", state='disabled')
        self.clearbtn.place_forget()



    def on_close(self):
        if self.forget_win:
            self.forget_win.grab_release()
            self.forget_win.destroy()
            self.forget_win = None  # Prevent further use

        if self.root.winfo_exists():  # Ensure root is still running
            self.root.deiconify()  #

    def start_reset_process(self):

        if not self.employee_id.get():
            messagebox.showerror('Error', "Employee ID required", parent=self.forget_win)
            return

        email = self.get_email()
        if not email:
            self.employee_id.set('')
            messagebox.showerror('Error', "Invalid Employee ID", parent=self.forget_win)
            return

        if self.send_email(email[0]) == 'f':
            self.employee_id.set('')
            messagebox.showerror("Error", "No internet connection", parent=self.forget_win)
            return

        # Hide "Send Code" button and show "Resend OTP" in the same position
        self.send_btn.place_forget()  # Hide the button
        self.resend_btn.place(x=280, y=90, width=100, height=30)  # Show the resend button
        self.clearbtn.place(x=280, y=130, width=100, height=30)

        self.resend_btn.config(state='disabled', bg="lightgray")
        self.clearbtn.config(state='disabled', bg="lightgray")# Initially disable Resend OTP
        self.countdown(60)  # Start countdown for 10 seconds
        self.code_entry.config(state='normal')
        self.verify_btn.config(state='normal')

    def clear(self):
        self.employee_id.set("")
        self.send_btn.place(x=280, y=90, width=100, height=30)  # Show Send Code button
        self.code_entry.config(state='disabled')
        self.verify_btn.config(state='disabled')

    def countdown(self, remaining):
        if remaining <= 0:
            self.countdown_label.config(text="")
            self.resend_btn.config(state='normal', bg="lightblue")
            self.clearbtn.config(state='normal', bg="green") # Enable Resend OTP button
            return

        self.countdown_label.config(text=f"Resend in {remaining}s")
        self.forget_win.after(1000, self.countdown, remaining - 1)

    def resend_otp(self):
        """Resend OTP and restart countdown"""
        email = self.get_email()
        if not email:
            messagebox.showerror('Error', "Invalid Employee ID", parent=self.forget_win)
            return

        if self.send_email(email[0]) == 'f':
            messagebox.showerror("Error", "No internet connection", parent=self.forget_win)
            return

        self.resend_btn.config(state='disabled', bg="lightgray")  # Disable Resend OTP button
        self.countdown(10)  # Restart 10-second countdown

    def enable_verification(self):
        self.code_entry.config(state='normal')
        self.verify_btn.config(state='normal')
    def verify_otp(self):
        if self.var_otp.get() == str(self.otp):
            self.show_new_password_window()
        else:
            self.var_otp.set('')
            messagebox.showerror("Error", "Invalid code", parent=self.forget_win)

    def show_new_password_window(self):
        def update_emoticon(var, label):
            """Update the displayed emoticon based on character length."""
            length = len(var.get())

            if length == 0 or length <= 3:
                label.config(image=self.emoticon1)
            elif length <= 7:
                label.config(image=self.emoticon2)
            elif length <= 11:
                label.config(image=self.emoticon3)
            elif length <= 16:
                label.config(image=self.emoticon4)
            else:  # 17-20 characters
                label.config(image=self.emoticon5)

        def limit_input(var):
            """Limit the input to 20 characters."""
            if len(var.get()) > 20:
                var.set(var.get()[:20])  # Trim to 20 characters

        def toggle_password(entry, var):
            """Toggle password visibility for a specific entry."""
            if var.get():
                entry.config(show="")  # Show plain text
            else:
                entry.config(show="*")  # Mask password

        # Destroy previous widgets
        for widget in self.forget_win.winfo_children():
            widget.destroy()

        self.forget_win.geometry('400x350+500+100')

        Label(self.forget_win, text="Reset Password", font=('goudy old style', 15, 'bold'),
              bg="#3f51b5", fg="white").pack(side=TOP, fill=X)

        Label(self.forget_win, text="New Password", font=('times new roman', 12)).place(x=60, y=100)

        Label(self.forget_win, text="Do not share your new password!", font=('times new roman', 12, 'bold'),
              fg="red").place(x=60, y=60)
        # Load emoticons
        self.emoticon1 = ImageTk.PhotoImage(file="sorry.png")
        self.emoticon2 = ImageTk.PhotoImage(file="worried.png")
        self.emoticon3 = ImageTk.PhotoImage(file="thumbs-up.png")
        self.emoticon4 = ImageTk.PhotoImage(file="excited.png")
        self.emoticon5 = ImageTk.PhotoImage(file="image_2025-02-27_170335728.png")

        # Emoticon for new password
        emoticon_label1 = Label(self.forget_win, image=self.emoticon1)
        emoticon_label1.place(x=20, y=130, width=30, height=30)

        # New Password Entry
        self.var_new_pass = StringVar()
        entry1 = Entry(self.forget_win, textvariable=self.var_new_pass, show="*",
                       font=('times new roman', 12), bg="lightyellow")
        entry1.place(x=60, y=130, width=310, height=30)

        # Update emoticon dynamically
        self.var_new_pass.trace_add("write", lambda *args: [limit_input(self.var_new_pass),
                                                            update_emoticon(self.var_new_pass, emoticon_label1)])

        # Show Password Checkbox for New Password
        self.show_pass_var1 = IntVar()
        Checkbutton(self.forget_win, text="Show Password", variable=self.show_pass_var1,
                    command=lambda: toggle_password(entry1, self.show_pass_var1), bg="grey").place(x=60, y=165)

        Label(self.forget_win, text="Confirm Password", font=('times new roman', 12)).place(x=60, y=200)

        # Emoticon for confirm password
        emoticon_label2 = Label(self.forget_win, image=self.emoticon1)
        emoticon_label2.place(x=20, y=230, width=30, height=30)

        # Confirm Password Entry
        self.var_conf_pass = StringVar()
        entry2 = Entry(self.forget_win, textvariable=self.var_conf_pass, show="*",
                       font=('times new roman', 12), bg="lightyellow")
        entry2.place(x=60, y=230, width=310, height=30)

        # Update emoticon dynamically
        self.var_conf_pass.trace_add("write", lambda *args: [limit_input(self.var_conf_pass),
                                                             update_emoticon(self.var_conf_pass, emoticon_label2)])

        # Show Password Checkbox for Confirm Password
        self.show_pass_var2 = IntVar()
        Checkbutton(self.forget_win, text="Show Password", variable=self.show_pass_var2,
                    command=lambda: toggle_password(entry2, self.show_pass_var2), bg="grey").place(x=60, y=265)

        # Reset Password Button
        Button(self.forget_win, text="Reset Password", command=self.update_password,
               font=("times new roman", 12), bg="lightblue").place(x=140, y=300, width=120, height=30)

    def get_email(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT email FROM employee WHERE eid=?", (self.employee_id.get(),))
            email = cur.fetchone()
            return email
        except Exception as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.forget_win)
        finally:
            con.close()

    def update_password(self):
        new_pass = self.var_new_pass.get().strip()
        conf_pass = self.var_conf_pass.get().strip()

        # Validate password length
        if len(new_pass) < 8 or len(new_pass) > 20:
            messagebox.showerror("Error", "Make your password 8-20 characters!", parent=self.forget_win)
            self.var_new_pass.set('')
            self.var_conf_pass.set('')
            return

        # Check if fields are empty
        if "" in (new_pass, conf_pass):
            messagebox.showerror("Error", "All fields are required", parent=self.forget_win)
            self.var_new_pass.set('')
            self.var_conf_pass.set('')
            return

        # Check if passwords match
        if new_pass != conf_pass:
            messagebox.showerror("Error", "Passwords don't match", parent=self.forget_win)
            self.var_new_pass.set('')
            self.var_conf_pass.set('')
            return

        # Update database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("UPDATE employee SET pass=? WHERE eid=?", (new_pass, self.employee_id.get()))
            con.commit()
            messagebox.showinfo("Success", "Please do not share your new password!", parent=self.forget_win)
            self.forget_win.destroy()
        except Exception as ex:
            con.rollback()
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.forget_win)
        finally:
            con.close()

    def send_email(self, to_):
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()

            email_ = "joshuanombradojaculba@gmail.com"
            pass_ = "hula miwi pgpv dvky"

            s.login(email_, pass_)

            self.otp = int(time.strftime("%H%S%M")) + int(time.strftime("%S"))

            msg = f"Subject: IMS - Password Reset Code\n\nYour FPCC is {self.otp}."
            s.sendmail(email_, to_, msg)
            s.quit()
            return 's'
        except Exception as e:
            print(f"Email error: {str(e)}")
            return 'f'

root = Tk()
obj = Login_system(root)
root.mainloop()