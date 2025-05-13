import numpy as np

# Pemetaan karakter ke angka (A=1, ..., Z=26, spasi=27)
def char_to_num(c):
    return 27 if c == ' ' else ord(c.upper()) - ord('A') + 1

def num_to_char(n):
    return ' ' if n == 27 else chr(int(n) + ord('A') - 1)

def text_to_numbers(text):
    return [char_to_num(c) for c in text]

def numbers_to_text(numbers):
    return ''.join(num_to_char(n) for n in numbers)

# Membagi angka menjadi blok dengan panjang n dan menambahkan padding jika perlu
def split_blocks(numbers, n):
    while len(numbers) % n != 0:
        numbers.append(27)  # Tambah spasi sebagai padding
    return [numbers[i:i + n] for i in range(0, len(numbers), n)]

# Fungsi encoding
def encode_message(message, matrix):
    n = matrix.shape[0]
    if np.linalg.det(matrix) == 0:
        raise ValueError("Matriks kunci tidak bisa diinverskan (singular). Gunakan matriks lain.")

    numbers = text_to_numbers(message)
    blocks = split_blocks(numbers, n)
    encoded = []
    for block in blocks:
        vector = np.array(block).reshape(n, 1)
        result = np.dot(matrix, vector)
        encoded.extend(result.flatten())
    return encoded

# Fungsi decoding
def decode_message(encoded_numbers, matrix):
    n = matrix.shape[0]
    if np.linalg.det(matrix) == 0:
        raise ValueError("Matriks kunci tidak bisa diinverskan (singular). Gunakan matriks lain.")

    inverse_matrix = np.linalg.inv(matrix)
    blocks = split_blocks(encoded_numbers, n)
    decoded = []
    for block in blocks:
        vector = np.array(block).reshape(n, 1)
        result = np.dot(inverse_matrix, vector)
        decoded.extend(result.flatten())
    decoded = [int(round(num)) for num in decoded]
    return numbers_to_text(decoded)

# Input matriks dari pengguna
def input_matrix(dimension, label="Key"):
    print(f"Masukkan Matriks {label} berukuran {dimension}x{dimension}:")
    matrix = []
    for i in range(dimension):
        row = input(f"Baris {i+1} (pisahkan dengan spasi): ").split()
        if len(row) != dimension:
            raise ValueError(f"Jumlah elemen pada baris {i+1} harus {dimension}.")
        matrix.append([int(x) for x in row])
    return np.array(matrix)

# Program utama
def main():
    try:
        message = input("Pesan Anda: ")
        dimension = int(input("Ukuran matriks kunci (misal: 2, 3, 4): "))
        
        encoding_matrix = input_matrix(dimension, label="Encoding")
        print("Matriks Encoding:")
        print(encoding_matrix)

        encoded = encode_message(message, encoding_matrix)
        print("Hasil Encoding:", encoded)

        decoding_matrix = input_matrix(dimension, label="Decoding")
        print("Matriks Decoding:")
        print(decoding_matrix)

        decoded = decode_message(encoded, decoding_matrix)
        print("Hasil Decoding:", decoded)

    except ValueError as e:
        print("Terjadi kesalahan:", e)

if __name__ == "__main__":
    main()
