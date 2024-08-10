import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os
import io
import sqlite3


def generate_key(paraphrase, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # AES-256 requires a key of 32 bytes
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = kdf.derive(paraphrase.encode())
    return key


def encrypt_image(image_data, paraphrase):
    salt = os.urandom(16)
    iv = os.urandom(16)
    key = generate_key(paraphrase, salt)
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_image = encryptor.update(image_data) + encryptor.finalize()
    return encrypted_image, salt, iv


def decrypt_image(encrypted_image, paraphrase, salt, iv):
    key = generate_key(paraphrase, salt)
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_image = decryptor.update(encrypted_image) + decryptor.finalize()
    return decrypted_image


# Database setup
def create_database():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS images
                 (id INTEGER PRIMARY KEY, image_blob BLOB, salt BLOB, iv BLOB)"""
    )
    conn.commit()
    conn.close()


create_database()


# Login screen class
class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x150")  # Fixed size window

        self.style = ttk.Style()
        self.style.theme_use("clam")  # Modern look

        self.label = ttk.Label(root, text="Enter Paraphrase:")
        self.label.pack(pady=10)

        self.paraphrase_entry = ttk.Entry(root, show="*")
        self.paraphrase_entry.pack(pady=5)

        self.login_button = ttk.Button(
            root, text="Login", command=self.verify_paraphrase
        )
        self.login_button.pack(pady=20)

    def verify_paraphrase(self):
        entered_paraphrase = self.paraphrase_entry.get()
        if entered_paraphrase:
            self.root.destroy()
            main_app = tk.Tk()
            HomePage(main_app, entered_paraphrase)
        else:
            messagebox.showerror("Error", "Paraphrase cannot be empty!")


# Home page class
class HomePage:
    def __init__(self, root, paraphrase):
        self.root = root
        self.paraphrase = paraphrase
        self.root.title("Home Page")

        self.style = ttk.Style()
        self.style.theme_use("clam")  # Modern look

        # Initialize image list and current index
        self.image_list = []
        self.current_index = 0

        # Set the window to maximized (not fullscreen)
        self.root.state('zoomed')  # Maximize the window

        # Create navigation buttons and image display
        self.image_label = ttk.Label(root)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        self.prev_button = ttk.Button(
            root, text="Previous", command=self.show_previous_image
        )
        self.prev_button.pack(side="left", padx=10, pady=10)

        self.next_button = ttk.Button(root, text="Next", command=self.show_next_image)
        self.next_button.pack(side="right", padx=10, pady=10)

        self.upload_button = ttk.Button(
            root, text="Upload Images", command=self.bulk_upload_images
        )
        self.upload_button.pack(pady=10)

        # Ensure the window has fully initialized
        self.root.update_idletasks()  # Process all pending events to complete window setup

        # Load images from the database
        self.load_images_from_db()

        # Display the first image if available
        if self.image_list:
            self.show_image()

    def bulk_upload_images(self):
        filepaths = filedialog.askopenfilenames(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]
        )
        for filepath in filepaths:
            image = Image.open(filepath)
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format="PNG")
            encrypted_image, salt, iv = encrypt_image(
                img_byte_arr.getvalue(), self.paraphrase
            )
            self.store_image_in_db(encrypted_image, salt, iv)
        self.load_images_from_db()
        self.show_image()

    def store_image_in_db(self, encrypted_image, salt, iv):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO images (image_blob, salt, iv) VALUES (?, ?, ?)",
            (encrypted_image, salt, iv),
        )
        conn.commit()
        conn.close()

    def load_images_from_db(self):
        self.image_list = []  # Reset image list
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT image_blob, salt, iv FROM images")
        rows = c.fetchall()
        for row in rows:
            try:
                decrypted_image = decrypt_image(row[0], self.paraphrase, row[1], row[2])
                self.image_list.append(decrypted_image)
            except Exception as e:
                print(f"Error decrypting image: {e}")
                continue
        conn.close()

    def show_image(self):
        if self.image_list:
            image_data = self.image_list[self.current_index]
            image = Image.open(io.BytesIO(image_data))

            # Resize image to fit the available space while maintaining aspect ratio
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            image_width, image_height = image.size
            scaling_factor = min(window_width / image_width, window_height / image_height)
            new_size = (int(image_width * scaling_factor), int(image_height * scaling_factor))
            resized_image = image.resize(new_size, Image.Resampling.LANCZOS)

            # Create a PhotoImage object
            photo = ImageTk.PhotoImage(resized_image)

            # Center the image
            self.image_label.config(image=photo)
            self.image_label.image = photo
            self.image_label.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.image_label.config(image="")
            messagebox.showinfo("Info", "No images available.")

    def show_next_image(self):
        if self.image_list:
            self.current_index = (self.current_index + 1) % len(self.image_list)
            self.show_image()

    def show_previous_image(self):
        if self.image_list:
            self.current_index = (self.current_index - 1) % len(self.image_list)
            self.show_image()

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Nikhi's GUI")

    app = LoginScreen(root)
    root.mainloop()