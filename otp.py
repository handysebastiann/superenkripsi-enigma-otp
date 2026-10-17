import secrets

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# =====================================================================
# FUNGSI OTP KLASIK (MODULO 26)
# =====================================================================
def otp_classic_encrypt(plaintext, key):
    ciphertext = ""
    for p_char, k_char in zip(plaintext, key): ##Loop untuk mengambil satu huruf plaintext dan satu huruf kunci secara bersamaan, karena panjangnya sama.
        p_val = ALPHABET.index(p_char) ##Mengubah huruf plaintext menjadi angka index, contoh: A:0, B:1
        k_val = ALPHABET.index(k_char) ##Sama namun untuk kunci otp
        c_val = (p_val + k_val) % 26 ##(plaintext + key) % 26
        ciphertext += ALPHABET[c_val] ##mengubah hasil index kembali menjadi huruf, lalu menambahkannya ke hasil ciphertext
    return ciphertext

def otp_classic_decrypt(ciphertext, key):
    decrypted = ""
    for c_char, k_char in zip(ciphertext, key):
        c_val = ALPHABET.index(c_char)
        k_val = ALPHABET.index(k_char)
        p_val = (c_val - k_val) % 26 ##(ciphertext - kunci) % 26
        decrypted += ALPHABET[p_val] ##hasilnya dikembalikan ke huruf plaintext
    return decrypted


# =====================================================================
# FUNGSI OTP MODERN (BITWISE XOR)
# =====================================================================
def otp_xor_process(data_bytes, key_bytes):
    """Fungsi XOR bersifat simetris (dipakai untuk Enkripsi sekaligus Dekripsi)"""
    return bytes([b ^ k for b, k in zip(data_bytes, key_bytes)])


# =====================================================================
# EKSEKUSI UTAMA
# =====================================================================
if __name__ == "__main__":
    # --- PLAINTEXT HARDCODE ---
    plaintext = "KULIAHKRIPTO"
    
    print("\n" + "="*68)
    print(" DEMO ONE-TIME PAD (OTP): MODULO 26 KLASIK & BITWISE XOR MODERN")
    print("="*68)
    
    # 1. Demo OTP Klasik (Huruf A-Z)
    # Membuat kunci acak murni yang panjangnya SAMA PERSIS dengan plaintext
    kunci_huruf = "".join(secrets.choice(ALPHABET) for _ in range(len(plaintext)))
    cipher_huruf = otp_classic_encrypt(plaintext, kunci_huruf)
    dekripsi_huruf = otp_classic_decrypt(cipher_huruf, kunci_huruf)
    
    print("--- A. OTP Klasik (Penjumlahan Huruf Modulo 26) ---")
    print(f"[*] Plaintext Asli      : {plaintext} (Panjang: {len(plaintext)} huruf)")
    print(f"[*] Kunci Acak (Sekali) : {kunci_huruf} (Panjang: {len(kunci_huruf)} huruf)")
    print(f"[*] Ciphertext Hasil    : {cipher_huruf}")
    print(f"[*] Hasil Dekripsi      : {dekripsi_huruf}")
    print("-" * 68)
    
    # 2. Demo OTP Komputer Modern (Operasi Bitwise XOR)
    pesan_byte = plaintext.encode('utf-8')
    kunci_byte = secrets.token_bytes(len(pesan_byte)) # Byte acak sepanjang pesan
    
    cipher_byte = otp_xor_process(pesan_byte, kunci_byte)
    dekripsi_byte = otp_xor_process(cipher_byte, kunci_byte)
    
    print("--- B. OTP Komputer Modern (Operasi Bitwise XOR '^') ---")
    print(f"[*] Plaintext (Teks)    : {plaintext}")
    print(f"[*] Plaintext (Hex)     : {pesan_byte.hex().upper()}")
    print(f"[*] Kunci Acak (Hex)    : {kunci_byte.hex().upper()}")
    print(f"[*] Ciphertext (Hex)    : {cipher_byte.hex().upper()}")
    print(f"[*] Dekripsi XOR (Teks) : {dekripsi_byte.decode('utf-8')}")
    print("="*68 + "\n")