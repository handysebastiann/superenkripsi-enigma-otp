import math

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# =====================================================================
# BAGIAN 1: FUNGSI SUBSTITUSI (HILL CIPHER 2x2)
# Penjelasan: Hill Cipher mengganti huruf berdasarkan perkalian
# matriks dengan pasangan angka dari plaintext.
# Rumus: C = K × P mod 26
# =====================================================================
def mod_inverse(a, m=26):
    """Mencari invers perkalian modulo 26: (a * x) % 26 == 1"""
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def get_hill_inverse_matrix(key_matrix):
    """Menghitung Matriks Invers 2x2 Modulo 26 untuk Dekripsi"""
    a, b = key_matrix[0][0], key_matrix[0][1]
    c, d = key_matrix[1][0], key_matrix[1][1]
    
    det = (a * d - b * c) % 26
    det_inv = mod_inverse(det, 26)
    
    if det_inv is None:
        raise ValueError("Matriks kunci tidak valid (tidak memiliki invers mod 26).")
        
    inv_matrix = [
        [(d * det_inv) % 26, (-b * det_inv) % 26],
        [(-c * det_inv) % 26, (a * det_inv) % 26]
    ]
    return inv_matrix

def hill_encrypt(text, key_matrix):
    text = "".join(c for c in text.upper() if c in ALPHABET)
    # Tambah padding 'X' jika jumlah huruf ganjil
    if len(text) % 2 != 0:
        text += 'X'
        
    result = ""
    for i in range(0, len(text), 2):
        p1 = ALPHABET.index(text[i])
        p2 = ALPHABET.index(text[i+1])
        
        c1 = (key_matrix[0][0] * p1 + key_matrix[0][1] * p2) % 26
        c2 = (key_matrix[1][0] * p1 + key_matrix[1][1] * p2) % 26
        
        result += ALPHABET[c1] + ALPHABET[c2]
    return result

def hill_decrypt(ciphertext, key_matrix):
    inv_matrix = get_hill_inverse_matrix(key_matrix)
    return hill_encrypt(ciphertext, inv_matrix)


# =====================================================================
# BAGIAN 2: FUNGSI TRANSPOSISI (MYSZKOWSKI)
# Penjelasan: Myszkowski mengubah posisi huruf berdasarkan peringkat
# alfabet dari kata kunci. Huruf kembar mendapat peringkat yang sama.
# =====================================================================
def get_myszkowski_ranks(key):
    """Memberi nomor urut berdasarkan abjad (huruf kembar mendapat nomor sama)"""
    key = key.upper()
    unique_sorted = sorted(list(set(key)))
    return [unique_sorted.index(c) + 1 for c in key]

def myszkowski_encrypt(text, key):
    ranks = get_myszkowski_ranks(key)
    num_cols = len(key)
    grid = [list(text[i:i + num_cols]) for i in range(0, len(text), num_cols)]
    
    ciphertext = ""
    for r in range(1, max(ranks) + 1):
        cols = [col_idx for col_idx, val in enumerate(ranks) if val == r]
        if len(cols) == 1:
            # Nomor unik: baca vertikal dari atas ke bawah
            c = cols[0]
            for row in range(len(grid)):
                if c < len(grid[row]):
                    ciphertext += grid[row][c]
        else:
            # Nomor kembar: baca menyamping (kiri ke kanan) tiap baris
            for row in range(len(grid)):
                for c in cols:
                    if c < len(grid[row]):
                        ciphertext += grid[row][c]
    return ciphertext

def myszkowski_decrypt(ciphertext, key):
    ranks = get_myszkowski_ranks(key)
    num_cols = len(key)
    num_rows = math.ceil(len(ciphertext) / num_cols)
    
    grid = []
    rem = len(ciphertext)
    for _ in range(num_rows):
        row_len = min(num_cols, rem)
        grid.append([''] * row_len)
        rem -= row_len
        
    idx = 0
    for r in range(1, max(ranks) + 1):
        cols = [col_idx for col_idx, val in enumerate(ranks) if val == r]
        if len(cols) == 1:
            c = cols[0]
            for row in range(num_rows):
                if c < len(grid[row]):
                    grid[row][c] = ciphertext[idx]
                    idx += 1
        else:
            for row in range(num_rows):
                for c in cols:
                    if c < len(grid[row]):
                        grid[row][c] = ciphertext[idx]
                        idx += 1
    return "".join("".join(row) for row in grid)


# =====================================================================
# EKSEKUSI UTAMA (HARDCODED)
# Penjelasan: Bagian ini menjalankan seluruh proses, mulai dari
# enkripsi Hill, enkripsi Myszkowski, hingga kedua tahap dekripsi.
# Urutan enkripsi: Hill -> Myszkowski.
# Urutan dekripsi: Myszkowski -> Hill.
# =====================================================================
if __name__ == "__main__":
    # --- DATA HARDCODE ---
    plaintext = "SERANGMARKAS"
    kunci_matriks = [[3, 3], [2, 5]]  # Matriks 2x2
    kunci_myszkowski = "TOMATO"       # Kata kunci transposisi
    
    ranks = get_myszkowski_ranks(kunci_myszkowski)
    inv_matriks = get_hill_inverse_matrix(kunci_matriks)
    
    print("\n" + "="*68)
    print(" DEMO SUPERENKRIPSI: HILL CIPHER (2x2) + TRANSPOSISI MYSZKOWSKI")
    print("="*68)
    print(f"[*] Plaintext Asli              : {plaintext}")
    print(f"[*] Kunci 1 (Matriks Hill 2x2)  : {kunci_matriks[0]} , {kunci_matriks[1]}")
    print(f"[*] Matriks Invers Dekripsi     : {inv_matriks[0]} , {inv_matriks[1]}")
    print(f"[*] Kunci 2 (Kata Myszkowski)   : {kunci_myszkowski}")
    print("-" * 68)
    
    # 1. Enkripsi Tahap 1: Substitusi Hill Cipher
    tahap_1 = hill_encrypt(plaintext, kunci_matriks)
    pasangan_asli = " ".join(plaintext[i:i+2] for i in range(0, len(plaintext), 2))
    pasangan_hill = " ".join(tahap_1[i:i+2] for i in range(0, len(tahap_1), 2))
    print(f"[1] Pembagian Blok 2 Huruf      : {pasangan_asli}")
    print(f"    Hasil Substitusi Hill       : {tahap_1} (Blok: {pasangan_hill})")
    
    # 2. Visualisasi Tabel Myszkowski
    print(f"\n[2] Visualisasi Tabel Myszkowski:")
    print(f"    Huruf Kunci : | {' | '.join(list(kunci_myszkowski))} |")
    print(f"    Nomor Urut  : | {' | '.join(str(r) for r in ranks)} |")
    print("    " + "-" * (len(kunci_myszkowski) * 4 + 1))
    
    num_cols = len(kunci_myszkowski)
    for i in range(0, len(tahap_1), num_cols):
        baris = " | ".join(list(tahap_1[i:i+num_cols]))
        print(f"                  | {baris} |")
        
    # 3. Enkripsi Tahap 2: Transposisi Myszkowski
    ciphertext = myszkowski_encrypt(tahap_1, kunci_myszkowski)
    print(f"\n[3] Ciphertext Akhir            : {ciphertext}")
    print("-" * 68)
    
    # 4. Dekripsi (Urutan dibalik: Myszkowski dulu, baru Hill Cipher)
    dekripsi_tahap_1 = myszkowski_decrypt(ciphertext, kunci_myszkowski)
    dekripsi_akhir = hill_decrypt(dekripsi_tahap_1, kunci_matriks)
    print(f"[4] Dekripsi Myszkowski         : {dekripsi_tahap_1}")
    print(f"[5] Dekripsi Hill Cipher (Asli) : {dekripsi_akhir}")
    print("="*68 + "\n")