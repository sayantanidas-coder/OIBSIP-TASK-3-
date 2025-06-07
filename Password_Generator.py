import tkinter as tk
from tkinter import messagebox, filedialog
import string
import secrets
import pyperclip
import qrcode
from PIL import ImageTk, Image

# === MAIN WINDOW ===
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("500x800")
root.resizable(False, False)

# === DARK THEME CONFIGURATION ===
theme = {
    "bg": "#1e1e1e",
    "fg": "#ffffff",
    "entry_bg": "#2e2e2e",
    "entry_fg": "#00ff59",
    "btn_bg": "#ff6600",
    "btn_fg": "#ffffff",
    "selectcolor": "#333333"
}

def apply_theme():
    root.configure(bg=theme["bg"])
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Label, tk.Checkbutton, tk.Scale)):
            widget.configure(bg=theme["bg"], fg=theme["fg"])
        elif isinstance(widget, tk.Entry):
            widget.configure(bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["fg"])
        elif isinstance(widget, tk.Button):
            widget.configure(bg=theme["btn_bg"], fg=theme["btn_fg"], activebackground="#cc5200")

# === PASSWORD GENERATION ===
def generate_password():
    charset = ''
    if var_lower.get(): charset += string.ascii_lowercase
    if var_upper.get(): charset += string.ascii_uppercase
    if var_digits.get(): charset += string.digits
    if var_symbols.get(): charset += string.punctuation

    length = length_var.get()
    if not charset:
        messagebox.showerror("Error", "Select at least one character type.")
        return

    password = ''.join(secrets.choice(charset) for _ in range(length))
    password_var.set(password)
    update_strength(password)

# === PASSWORD STRENGTH ===
def update_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if len(password) >= 11: score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1

    if score <= 2:
        strength_label.config(text="Strength: Weak", fg="#ff4d4d")
    elif 3 <= score <= 11:
        strength_label.config(text="Strength: Moderate", fg="#ffaa00")
    else:
        strength_label.config(text="Strength: Strong", fg="#00e673")

# === COPY PASSWORD ===
def copy_password():
    pwd = password_var.get()
    if pwd:
        pyperclip.copy(pwd)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

# === SAVE TO FILE ===
def save_to_file():
    pwd = password_var.get()
    if pwd:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "a") as f:
                f.write(pwd + "\n")
            messagebox.showinfo("Saved", f"Password saved to {file_path}")

# === TOGGLE PASSWORD VISIBILITY ===
def toggle_password():
    entry.config(show="" if show_var.get() else "•")

# === GENERATE QR CODE ===
def generate_qr():
    pwd = password_var.get()
    if not pwd:
        messagebox.showerror("Error", "No password to encode.")
        return
    qr_img = qrcode.make(pwd)
    qr_img = qr_img.resize((150, 150), Image.LANCZOS)
    qr_photo = ImageTk.PhotoImage(qr_img)
    qr_label.config(image=qr_photo)
    qr_label.image = qr_photo  # prevent garbage collection

# === GUI SETUP ===
font_main = ("Segoe UI", 12)
btn_font = ("Segoe UI", 12, "bold")

tk.Label(root, text="Password Generator", font=("Segoe UI", 16, "bold")).pack(pady=15)

length_var = tk.IntVar(value=12)
tk.Label(root, text="Password Length", font=font_main).pack()
tk.Scale(root, from_=1, to=64, orient='horizontal', variable=length_var,
         troughcolor="#444", highlightthickness=0, bg=theme["bg"],
         fg=theme["fg"]).pack()

# === CHECKBOXES ===
var_lower = tk.BooleanVar(value=True)
var_upper = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=False)

def themed_checkbox(text, var):
    return tk.Checkbutton(root, text=text, variable=var,
                          font=font_main, anchor="w", selectcolor=theme["selectcolor"],
                          activebackground=theme["bg"], activeforeground=theme["fg"],
                          bg=theme["bg"], fg=theme["fg"], padx=30)

themed_checkbox("Include Lowercase (a-z)", var_lower).pack(fill='x')
themed_checkbox("Include Uppercase (A-Z)", var_upper).pack(fill='x')
themed_checkbox("Include Digits (0-9)", var_digits).pack(fill='x')
themed_checkbox("Include Symbols (!@#$)", var_symbols).pack(fill='x')

# === GENERATE BUTTON ===
tk.Button(root, text="Generate Password", command=generate_password,
          font=btn_font).pack(pady=15)

# === PASSWORD ENTRY ===
password_var = tk.StringVar()
entry = tk.Entry(root, textvariable=password_var, font=("Courier", 14), width=30,
                 justify='center', show="•", relief="sunken")
entry.pack()

# === SHOW PASSWORD ===
show_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Show Password", variable=show_var,
               command=toggle_password, font=("Segoe UI", 10),
               selectcolor=theme["selectcolor"], bg=theme["bg"],
               fg=theme["fg"], activebackground=theme["bg"]).pack()

# === STRENGTH LABEL ===
strength_label = tk.Label(root, text="Strength: ", font=("Segoe UI", 10, "bold"))
strength_label.pack(pady=5)

# === COPY / SAVE / QR ===
tk.Button(root, text="Copy to Clipboard", command=copy_password,
          font=btn_font).pack(pady=5)

tk.Button(root, text="Save to File", command=save_to_file,
          font=btn_font).pack(pady=5)

tk.Button(root, text="Generate QR Code", command=generate_qr,
          font=btn_font).pack(pady=5)

# === QR IMAGE HOLDER ===
qr_label = tk.Label(root, bg=theme["bg"])
qr_label.pack(pady=20)

# === APPLY THEME & RUN ===
apply_theme()
root.mainloop()
