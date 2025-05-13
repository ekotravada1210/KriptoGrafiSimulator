import numpy as np

# Pemetaan karakter ke angka (A=1, B=2, ..., Z=26, spasi=27)
def char_to_num(c):
    if c == ' ':
        return 27
    return ord(c.upper()) - ord('A') + 1

# Pemetaan angka ke karakter
def num_to_char(n):
    if n == 27:
        return ' '
    return chr(int(n) + ord('A') - 1)

# Fungsi untuk mengubah teks menjadi list angka
def text_to_numbers(text):
    return [char_to_num(c) for c in text]

# Fungsi untuk mengubah list angka menjadi teks
def numbers_to_text(numbers):
    return ''.join(num_to_char(n) for n in numbers)

# Fungsi untuk membagi list angka menjadi pasangan
def pair_numbers(numbers):
    if len(numbers) % 2 != 0:
        numbers.append(27)  # Tambahkan spasi jika jumlah angka ganjil
    return [numbers[i:i+2] for i in range(0, len(numbers), 2)]

# Fungsi encoding
def encode_message(message, encoding_matrix):
    det = np.linalg.det(encoding_matrix)
    if det == 0:
        raise ValueError("Matriks kunci tidak bisa diinverskan (singular). Gunakan matriks lain.")
    
    numbers = text_to_numbers(message)
    pairs = pair_numbers(numbers)
    encoded = []
    for pair in pairs:
        vector = np.array(pair).reshape(2, 1)
        result = np.dot(encoding_matrix, vector)
        encoded.extend(result.flatten())
    return encoded

# Fungsi decoding
def decode_message(encoded_numbers, encoding_matrix):
    
    det = np.linalg.det(encoding_matrix)
    if det == 0:
        raise ValueError("Matriks kunci tidak bisa diinverskan (singular). Gunakan matriks lain.")
        
    
    inverse_matrix = np.linalg.inv(encoding_matrix)
    pairs = pair_numbers(encoded_numbers)
    decoded = []
    for pair in pairs:
        vector = np.array(pair).reshape(2, 1)
        result = np.dot(inverse_matrix, vector)
        decoded.extend(result.flatten())
    # Pembulatan ke angka terdekat dan konversi ke integer
    decoded = [int(round(num)) for num in decoded]
    return numbers_to_text(decoded)

try:
# Contoh penggunaan
    if __name__ == "__main__":
        message=str(input(" Pesan Anda :"))
    #message = "PULANG KE BANDUNG"
    # Inisialisasi matriks 2x2
    #key = [[0, 0], [0, 0]]

# Mengisi matriks dengan input dari pengguna
    #for i in range(2):
    #    for j in range(2):
    #        key[i][j] = int(input(f"Masukkan Key X{i+1}{j+1}: "))
    key = [[0]*2 for _ in range(2)]

    for i in range(2):
        baris = input(f"Masukkan baris {i+1} (pisahkan dengan spasi): ").split()
        for j in range(2):
            key[i][j] = int(baris[j])

    print("Matriks Key:")
    for row in key:
        print(row)     
    
    encoding_matrix = np.array(key)
    #encoding_matrix = np.array([[2, 2],
    #                            [9, 7]])

    print("Pesan asli:", message)
 
    # Encoding

    encoded = encode_message(message, encoding_matrix)
    print("Hasil encoding:", encoded)

    # Decoding
    #for i in range(2):
    #    for j in range(2):
    #        key[i][j] = int(input(f"Masukkan Key {i+1}{j+1}: "))

    #key = [[0]*2 for _ in range(2)]

    for i in range(2):
        baris = input(f"Masukkan baris {i+1} (pisahkan dengan spasi): ").split()
        for j in range(2):
            key[i][j] = int(baris[j])
    
    print("Matriks Key:")
    for row in key:
        print(row)     
    
    decoding_matrix = np.array(key)
    decoded = decode_message(encoded, decoding_matrix)
    print("Hasil decoding:", decoded)
except ValueError as e:
    print("Key encode atau decode tidak tepat pesan tidak bisa diencrypt/decrypt :")
    print(e)
