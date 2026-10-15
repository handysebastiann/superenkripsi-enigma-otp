import secrets
import math

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# =====================================================================
# 1. MATERI PERTAMA: SUPERENKRIPSI (Caesar Cipher + Myszkowski)
# =====================================================================
def caesar_encrypt(text, shift):
    result = ""
    for char in text.upper():
        if char in ALPHABET:
            idx = (ALPHABET.index(char) + shift) % 26
            result += ALPHABET[idx]
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def get_myszkowski_ranks(key):
    """
    Memberikan nomor urut (mulai dari 1) berdasarkan abjad.
    Huruf yang sama akan mendapatkan nomor yang sama.
    Contoh: 'TOMATO' -> [4, 3, 2, 1, 4, 3]
    """
    key = key.upper()
    unique_sorted_chars = sorted(list(set(key)))
    return [unique_sorted_chars.index(char) + 1 for char in key]

def myszkowski_encrypt(text, key):
    ranks = get_myszkowski_ranks(key)
    num_cols = len(key)
    
    # Memasukkan teks ke dalam baris-baris tabel (tanpa wajib padding penuh)
    grid = []
    for i in range(0, len(text), num_cols):
        grid.append(list(text[i:i + num_cols]))
        
    ciphertext = ""
    max_rank = max(ranks)
    
    # Membaca berdasarkan urutan nomor ( dari 1 sampai nomor terbesar )
    for r in range(1, max_rank + 1):
        # Cari kolom mana saja yang punya nomor urut 'r'
        cols = [col_idx for col_idx, val in enumerate(ranks) if val == r]
        
        if len(cols) == 1:
            # Jika nomor unik (hanya 1 kolom): Baca vertikal dari atas ke bawah
            c = cols[0]
            for row in range(len(grid)):
                if c < len(grid[row]):
                    ciphertext += grid[row][c]
        else:
            # Jika nomor kembar (>1 kolom): Baca menyamping (kiri ke kanan) tiap baris
            for row in range(len(grid)):
                for c in cols:
                    if c < len(grid[row]):
                        ciphertext += grid[row][c]
                        
    return ciphertext

def myszkowski_decrypt(ciphertext, key):
    ranks = get_myszkowski_ranks(key)
    num_cols = len(key)
    num_rows = math.ceil(len(ciphertext) / num_cols)
    
    # Membuat tabel kosong sesuai ukuran teks asli
    grid = []
    rem = len(ciphertext)
    for _ in range(num_rows):
        row_len = min(num_cols, rem)
        grid.append([''] * row_len)
        rem -= row_len
        
    # Mengisi kembali tabel sesuai aturan pembacaan Myszkowski
    idx = 0
    max_rank = max(ranks)
    for r in range(1, max_rank + 1):
        cols = [col_idx for col_idx, val in enumerate(ranks) if val == r]
        
        if len(cols) == 1:
            # Isi secara vertikal (atas ke bawah)
            c = cols[0]
            for row in range(num_rows):
                if c < len(grid[row]):
                    grid[row][c] = ciphertext[idx]
                    idx += 1
        else:
            # Isi secara menyamping (kiri ke kanan per baris)
            for row in range(num_rows):
                for c in cols:
                    if c < len(grid[row]):
                        grid[row][c] = ciphertext[idx]
                        idx += 1
                        
    # Membaca tabel secara normal dari kiri ke kanan untuk mendapat teks semula
    plaintext = "".join("".join(row) for row in grid)
    return plaintext

def demo_superenkripsi():
    print("\n" + "="*65)
    print(" DEMO 1: SUPERENKRIPSI (Substitusi Caesar + Transposisi Myszkowski)")
    print("="*65)
    
    plaintext = "SERANGMARKAS"
    kunci_geser = 3
    kunci_myszkowski = "TOMATO" # Punya huruf kembar 'T' dan 'O'
    ranks = get_myszkowski_ranks(kunci_myszkowski)
    
    print(f"[*] Plaintext Asli            : {plaintext}")
    print(f"[*] Kunci 1 (Geser Caesar)    : {kunci_geser}")
    print(f"[*] Kunci 2 (Kata Myszkowski) : {kunci_myszkowski}")
    print("-" * 65)
    
    # Tahap 1: Substitusi Caesar
    tahap_1 = caesar_encrypt(plaintext, kunci_geser)
    print(f"[1] Hasil Substitusi Caesar   : {tahap_1}")
    
    # Visualisasi Tabel Myszkowski untuk Audiens
    print(f"\n[2] Visualisasi Tabel Myszkowski:")
    header_huruf = " | ".join(list(kunci_myszkowski))
    header_angka = " | ".join(str(r) for r in ranks)
    print(f"    Huruf Kunci : | {header_huruf} |")
    print(f"    Nomor Urut  : | {header_angka} |")
    print("    " + "-" * (len(kunci_myszkowski) * 4 + 1))
    
    num_cols = len(kunci_myszkowski)
    for i in range(0, len(tahap_1), num_cols):
        baris = " | ".join(list(tahap_1[i:i+num_cols]))
        print(f"                  | {baris} |")
        
    # Tahap 2: Enkripsi Myszkowski
    ciphertext = myszkowski_encrypt(tahap_1, kunci_myszkowski)
    print(f"\n[3] Ciphertext Akhir          : {ciphertext}")
    print("    (Catatan: Nomor tunggal dibaca menurun, nomor kembar dibaca menyamping)")
    print("-" * 65)
    
    # Proses Dekripsi (Dibalik: Dekripsi Myszkowski dulu, baru Dekripsi Caesar)
    dekripsi_tahap_1 = myszkowski_decrypt(ciphertext, kunci_myszkowski)
    dekripsi_akhir = caesar_decrypt(dekripsi_tahap_1, kunci_geser)
    print(f"[4] Dekripsi Myszkowski       : {dekripsi_tahap_1}")
    print(f"[5] Dekripsi Caesar (Asli)    : {dekripsi_akhir}")


# =====================================================================
# 2. MATERI KEDUA: SIMULASI MESIN ENIGMA (3 Rotor + Reflector + Plugboard)
# =====================================================================
class SimpleEnigma:
    def __init__(self, rotor_positions, plugboard_pairs):
        self.rotors = [
            "EKMFLGDQVZNTOWYHXUSPAIBRCJ", # Rotor 1 (Kanan - Cepat)
            "AJDKSIRUXBLHWTMCQGZNPYFVOE", # Rotor 2 (Tengah - Sedang)
            "BDFHJLCPRTXVZNYEIWGAKMUSQO"  # Rotor 3 (Kiri - Lambat)
        ]
        self.reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
        self.positions = [ALPHABET.index(p.upper()) for p in rotor_positions]
        
        self.plugboard = {}
        for pair in plugboard_pairs:
            a, b = pair[0].upper(), pair[1].upper()
            self.plugboard[a] = b
            self.plugboard[b] = a

    def _step_rotors(self):
        self.positions[0] = (self.positions[0] + 1) % 26
        if self.positions[0] == 0:
            self.positions[1] = (self.positions[1] + 1) % 26
            if self.positions[1] == 0:
                self.positions[2] = (self.positions[2] + 1) % 26

    def _pass_plugboard(self, char):
        return self.plugboard.get(char, char)

    def process_char(self, char):
        if char not in ALPHABET:
            return char
            
        self._step_rotors()
        c = self._pass_plugboard(char)
        
        # Arus Maju (Rotor 1 -> 2 -> 3)
        idx = ALPHABET.index(c)
        for i in range(3):
            shifted_idx = (idx + self.positions[i]) % 26
            mapped_char = self.rotors[i][shifted_idx]
            idx = (ALPHABET.index(mapped_char) - self.positions[i]) % 26
            
        # Pantulan Reflector
        reflected_char = self.reflector[idx]
        idx = ALPHABET.index(reflected_char)
        
        # Arus Balik (Rotor 3 -> 2 -> 1)
        for i in reversed(range(3)):
            shifted_idx = (idx + self.positions[i]) % 26
            target_char = ALPHABET[shifted_idx]
            rotor_idx = self.rotors[i].index(target_char)
            idx = (rotor_idx - self.positions[i]) % 26
            
        out_char = ALPHABET[idx]
        return self._pass_plugboard(out_char)

    def process_text(self, text, tampilkan_detail=False):
        result = ""
        for char in text.upper():
            out = self.process_char(char)
            result += out
            if tampilkan_detail and char in ALPHABET:
                pos_str = "-".join(ALPHABET[p] for p in self.positions)
                print(f"    Ketik '{char}' | Posisi Rotor [{pos_str}] -> Lampu Menyala: '{out}'")
        return result

def demo_enigma():
    print("\n" + "="*65)
    print(" DEMO 2: SIMULASI MESIN ENIGMA (Rotor Dinamis & Simetris)")
    print("="*65)
    
    posisi_awal = ['A', 'A', 'A']
    kabel_plugboard = ["AB", "CD"]
    pesan = "AAAAA"
    
    print(f"[*] Posisi Awal Rotor : {posisi_awal}")
    print(f"[*] Plugboard Aktif   : {kabel_plugboard}")
    print(f"[*] Pesan Diketik     : {pesan} (Perhatikan huruf A berubah terus!)")
    print("-" * 65)
    
    enigma_pengirim = SimpleEnigma(posisi_awal, kabel_plugboard)
    print("[+] Proses Enkripsi per Ketikan:")
    ciphertext = enigma_pengirim.process_text(pesan, tampilkan_detail=True)
    print(f"\n[*] Ciphertext Hasil  : {ciphertext}")
    print("-" * 65)
    
    enigma_penerima = SimpleEnigma(posisi_awal, kabel_plugboard)
    print("[+] Proses Dekripsi (Mesin di-reset ke A-A-A, ketik Ciphertext):")
    decrypted = enigma_penerima.process_text(ciphertext, tampilkan_detail=True)
    print(f"\n[*] Hasil Dekripsi    : {decrypted}")


# =====================================================================
# 3. MATERI KETIGA: ONE-TIME PAD (OTP - Klasik Modulo 26 & Modern XOR)
# =====================================================================
def demo_otp():
    print("\n" + "="*65)
    print(" DEMO 3: ONE-TIME PAD (OTP) - Sandi yang Mustahil Dipecahkan")
    print("="*65)
    
    plaintext = "KULIAHKRIPTO"
    kunci_otp = "".join(secrets.choice(ALPHABET) for _ in range(len(plaintext)))
    
    # Enkripsi Modulo 26: C = (P + K) mod 26
    ciphertext = ""
    for p_char, k_char in zip(plaintext, kunci_otp): ##Loop untuk mengambil satu huruf plaintext dan satu huruf kunci secara bersamaan, karena panjangnya sama.
        p_val = ALPHABET.index(p_char) ##Mengubah huruf plaintext menjadi angka index, contoh: A:0, B:1
        k_val = ALPHABET.index(k_char) ##Sama namun untuk kunci otp
        c_val = (p_val + k_val) % 26 ##(plaintext + key) % 26
        ciphertext += ALPHABET[c_val] ##mengubah hasil index kembali menjadi huruf,
                                      ##lalu menambahkannya ke hasil ciphertext
        
    # Dekripsi Modulo 26: P = (C - K) mod 26
    decrypted = ""
    for c_char, k_char in zip(ciphertext, kunci_otp):
        c_val = ALPHABET.index(c_char)
        k_val = ALPHABET.index(k_char)
        p_val = (c_val - k_val) % 26 ##(ciphertext - kunci) % 26
        decrypted += ALPHABET[p_val] ##hasilnya dikembalikan ke huruf plaintext

    print("--- A. OTP Klasik (Operasi Huruf Modulo 26) ---")
    print(f"[*] Plaintext           : {plaintext} (Panjang: {len(plaintext)})")
    print(f"[*] Kunci Acak (Sekali) : {kunci_otp} (Panjang: {len(kunci_otp)})")
    print(f"[*] Ciphertext          : {ciphertext}")
    print(f"[*] Hasil Dekripsi      : {decrypted}")
    
    print("\n--- B. OTP Komputer Modern (Operasi Bitwise XOR) ---")
    pesan_byte = plaintext.encode('utf-8') ##ubah teks plaintext menjadi byte
    kunci_byte = secrets.token_bytes(len(pesan_byte)) ##Ini mirip dengan OTP klasik, tapi bekerja pada level byte, bukan huruf alfabet.
    
    cipher_byte = bytes([p ^ k for p, k in zip(pesan_byte, kunci_byte)])
    dekripsi_byte = bytes([c ^ k for c, k in zip(cipher_byte, kunci_byte)])
    
    print(f"[*] Plaintext (Teks)    : {plaintext}")
    print(f"[*] Kunci Acak (Hex)    : {kunci_byte.hex().upper()}")
    print(f"[*] Ciphertext (Hex)    : {cipher_byte.hex().upper()}")
    print(f"[*] Dekripsi XOR (Teks) : {dekripsi_byte.decode('utf-8')}")
    print("="*65 + "\n")

if __name__ == "__main__":
    demo_superenkripsi()
    demo_enigma()
    demo_otp()