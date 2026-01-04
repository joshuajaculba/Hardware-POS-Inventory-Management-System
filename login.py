import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

class ImagePOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Image-Based POS System")
        self.cart = []

        self.product_frame = tk.Frame(self.root)
        self.product_frame.pack()

        self.cart_label = tk.Label(self.root, text="Cart: 0 items", font=("Arial", 14))
        self.cart_label.pack(pady=10)

        self.load_products()

    def load_products(self):
        try:
            con = sqlite3.connect("ims.db")
            cur = con.cursor()
            cur.execute("SELECT name, price, image FROM product WHERE status='Active'")
            products = cur.fetchall()

            for name, price, image_data in products:
                try:
                    image = Image.open(image_data)
                    image = image.resize((100, 100))
                    photo = ImageTk.PhotoImage(image)

                    card = tk.Frame(self.product_frame, bd=2, relief="raised", padx=10, pady=10)
                    card.pack(side="left", padx=10, pady=10)

                    img_label = tk.Label(card, image=photo)
                    img_label.image = photo
                    img_label.pack()

                    tk.Label(card, text=name).pack()
                    tk.Label(card, text=f"${price:.2f}").pack()
                    tk.Button(card, text="Add", command=lambda n=name, p=price: self.add_to_cart(n, p)).pack()

                except Exception as e:
                    print(f"Error loading image for {name}: {e}")

        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

        finally:
            con.close()

    def add_to_cart(self, name, price):
        self.cart.append((name, price))
        self.cart_label.config(text=f"Cart: {len(self.cart)} items")

# Launch
if __name__ == "__main__":
    root = tk.Tk()
    app = ImagePOS(root)
    root.mainloop()
