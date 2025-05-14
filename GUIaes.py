import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import os

# ======== Fungsi utilitas matriks teks ==========
def char_to_num(c):
    if c == ' ':
        return 27
    return ord(c.upper()) - ord('A') + 1

def num_to_char(n):
    if n == 27:
        return ' '
    return chr(int(n) + ord('A') - 1)

def text_to_numbers(text):
    return [char_to_num(c) for c in text]

def numbers_to_text(numbers):
    return ''.join(num_to_char(n) for n in numbers)

def pair_numbers(numbers, n):
    while len(numbers) % n != 0:
        numbers.append(27)
    return [numbers[i:i+n] for i in range(0, len(numbers), n)]

def is_invertible(matrix):
    try:
        np.linalg.inv(matrix)
        return True
    except np.linalg.LinAlgError:
        return False

def encode_message(message, key_matrix):
    n = key_matrix.shape[0]
    numbers = text_to_numbers(message)
    pairs = pair_numbers(numbers, n)
    encoded = []
    for pair in pairs:
        vector = np.array(pair).reshape(n, 1)
        result = np.dot(key_matrix, vector)
        encoded.extend(result.flatten())
    return encoded

def decode_message(encoded_numbers, key_matrix):
    n = key_matrix.shape[0]
    inverse_matrix = np.linalg.inv(key_matrix)
    pairs = pair_numbers(encoded_numbers, n)
    decoded = []
    for pair in pairs:
        vector = np.array(pair).reshape(n, 1)
        result = np.dot(inverse_matrix, vector)
        decoded.extend(result.flatten())
    decoded = [int(round(num)) for num in decoded]
    return numbers_to_text(decoded)

# ======== Fungsi PDF AES ==========
def encrypt_pdf(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    enc_file = file_path + ".enc"
    with open(enc_file, 'wb') as f:
        f.write(cipher.iv + ct_bytes)
    return enc_file

def decrypt_pdf(file_path, key):
    with open(file_path, 'rb') as f:
        iv = f.read(16)
        ct = f.read()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = unpad(cipher.decrypt(ct), AES.block_size)
    dec_file = file_path.replace('.enc', '_decrypted.pdf')
    with open(dec_file, 'wb') as f:
        f.write(data)
    return dec_file

# ======== GUI ==========
def run_gui():
    root = tk.Tk()
    root.title("Enkripsi Teks & File PDF")

    tab_parent = tk.Frame(root)
    tab_parent.pack(fill='both', expand=True)

    # ===== Teks Frame =====
    teks_frame = tk.LabelFrame(tab_parent, text="Enkripsi Teks Matriks")
    teks_frame.pack(fill='x', padx=10, pady=5)

    tk.Label(teks_frame, text="Pesan:").grid(row=0, column=0)
    pesan_entry = tk.Entry(teks_frame, width=40)
    pesan_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(teks_frame, text="Kunci Matriks (string, n^2 char):").grid(row=1, column=0)
    key_entry = tk.Entry(teks_frame, width=40)
    key_entry.grid(row=1, column=1, padx=5, pady=5)

    def proses_enkripsi_teks():
        msg = pesan_entry.get()
        key_str = key_entry.get().upper()
        n = int(len(key_str) ** 0.5)
        if n * n != len(key_str):
            return messagebox.showerror("Error", "Jumlah karakter kunci harus n^2.")
        key_nums = [char_to_num(c) for c in key_str]
        key_matrix = np.array(key_nums).reshape(n, n)
        if not is_invertible(key_matrix):
            return messagebox.showerror("Error", "Matriks tidak bisa diinverskan.")
        encoded = encode_message(msg, key_matrix)
        result = ','.join(map(str, encoded))
        messagebox.showinfo("Hasil Enkripsi", result)

    def proses_dekripsi_teks():
        msg = pesan_entry.get()
        key_str = key_entry.get().upper()
        try:
            data = list(map(int, msg.strip().split(',')))
        except:
            return messagebox.showerror("Error", "Format pesan harus angka dipisah koma.")
        n = int(len(key_str) ** 0.5)
        if n * n != len(key_str):
            return messagebox.showerror("Error", "Jumlah karakter kunci harus n^2.")
        key_nums = [char_to_num(c) for c in key_str]
        key_matrix = np.array(key_nums).reshape(n, n)
        if not is_invertible(key_matrix):
            return messagebox.showerror("Error", "Matriks tidak bisa diinverskan.")
        decoded = decode_message(data, key_matrix)
        messagebox.showinfo("Hasil Dekripsi", decoded)

    tk.Button(teks_frame, text="Enkripsi", command=proses_enkripsi_teks).grid(row=2, column=0, pady=5)
    tk.Button(teks_frame, text="Dekripsi", command=proses_dekripsi_teks).grid(row=2, column=1, pady=5)

    # ===== PDF Frame =====
    pdf_frame = tk.LabelFrame(tab_parent, text="Enkripsi File PDF dengan AES")
    pdf_frame.pack(fill='x', padx=10, pady=5)

    def pilih_file():
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Encrypted", "*.enc")])
        file_path_var.set(path)

    def proses_enkripsi_pdf():
        key = get_random_bytes(16)
        file_path = file_path_var.get()
        if not file_path.lower().endswith(".pdf"):
            return messagebox.showerror("Error", "Pilih file PDF.")
        out = encrypt_pdf(file_path, key)
        with open(out + ".key", 'wb') as f:
            f.write(key)
        messagebox.showinfo("Sukses", f"File terenkripsi: {out}\nKey disimpan di: {out}.key")

    def proses_dekripsi_pdf():
        file_path = file_path_var.get()
        key_path = filedialog.askopenfilename(filetypes=[("Key file", "*.key")])
        if not (file_path.lower().endswith(".enc") and key_path):
            return messagebox.showerror("Error", "Pilih file .enc dan .key.")
        with open(key_path, 'rb') as f:
            key = f.read()
        out = decrypt_pdf(file_path, key)
        messagebox.showinfo("Sukses", f"File didekripsi: {out}")

    file_path_var = tk.StringVar()
    tk.Button(pdf_frame, text="Pilih File", command=pilih_file).pack(pady=5)
    tk.Label(pdf_frame, textvariable=file_path_var).pack()
    tk.Button(pdf_frame, text="Enkripsi PDF", command=proses_enkripsi_pdf).pack(pady=5)
    tk.Button(pdf_frame, text="Dekripsi PDF", command=proses_dekripsi_pdf).pack(pady=5)

    root.mainloop()

if __name__ == '__main__':
    run_gui()
