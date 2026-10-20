import math

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# =====================================================================
# BAGIAN 1: FUNGSI SUBSTITUSI (HILL CIPHER NxN)
# Penjelasan: Hill Cipher mengganti huruf berdasarkan perkalian
# matriks dengan blok angka dari plaintext.
# Rumus: C = K × P mod 26
# =====================================================================
def mod_inverse(a, m=26):
    """Mencari invers perkalian modulo 26: (a * x) % 26 == 1"""
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def get_matrix_minor(m, i, j):
    """Mengambil minor matriks dengan menghapus baris i dan kolom j"""
    return [row[:j] + row[j+1:] for row in (m[:i] + m[i+1:])]

def get_matrix_determinant(m):
    """Menghitung determinan matriks nxn secara rekursif"""
    n = len(m)
    if n == 1:
        return m[0][0]
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    det = 0
    for c in range(n):
        det += ((-1) ** c) * m[0][c] * get_matrix_determinant(get_matrix_minor(m, 0, c))
    return det

def get_hill_inverse_matrix(key_matrix):
    """Menghitung Matriks Invers nxn Modulo 26 untuk Dekripsi"""
    n = len(key_matrix)
    det = get_matrix_determinant(key_matrix) % 26
    det_inv = mod_inverse(det, 26)
    
    if det_inv is None:
        raise ValueError(f"Matriks kunci tidak valid (determinan {det} tidak memiliki invers mod 26).")
        
    if n == 1:
        return [[det_inv % 26]]
        
    # Adjugate matrix adalah transpose dari matriks kofaktor
    inv_matrix = []
    for i in range(n):
        inv_row = []
        for j in range(n):
            minor = get_matrix_minor(key_matrix, j, i)
            cofactor = ((-1) ** (i + j)) * get_matrix_determinant(minor)
            inv_row.append((cofactor * det_inv) % 26)
        inv_matrix.append(inv_row)
    return inv_matrix

def hill_encrypt(text, key_matrix):
    n = len(key_matrix)
    text = "".join(c for c in text.upper() if c in ALPHABET)
    # Tambah padding 'X' jika panjang teks bukan kelipatan n
    while len(text) % n != 0:
        text += 'X'
        
    result = ""
    for i in range(0, len(text), n):
        block = [ALPHABET.index(c) for c in text[i:i+n]]
        for row in range(n):
            c_val = sum(key_matrix[row][col] * block[col] for col in range(n)) % 26
            result += ALPHABET[c_val]
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
# EKSEKUSI UTAMA (INPUT DINAMIS)
# Penjelasan: Bagian ini menjalankan seluruh proses, mulai dari
# enkripsi Hill, enkripsi Myszkowski, hingga kedua tahap dekripsi.
# Urutan enkripsi: Hill -> Myszkowski.
# Urutan dekripsi: Myszkowski -> Hill.
# =====================================================================
if __name__ == "__main__":
    print("\n" + "="*68)
    print(" INPUT DATA SUPERENKRIPSI (HILL CIPHER + TRANSPOSISI MYSZKOWSKI)")
    print("="*68)
    
    plaintext = input("Masukkan Plaintext: ").strip()
    
    n = int(input("Masukkan ordo matriks Hill (misal 2 untuk 2x2, 3 untuk 3x3): "))
    print(f"Masukkan elemen matriks baris demi baris ({n} angka dipisah spasi):")
    kunci_matriks = []
    for i in range(n):
        baris = [int(x) for x in input(f"Baris ke-{i+1}: ").replace(',', ' ').split()]
        kunci_matriks.append(baris)
        
    kunci_myszkowski = input("Masukkan Kunci Transposisi Myszkowski: ").strip()
    
    ranks = get_myszkowski_ranks(kunci_myszkowski)
    inv_matriks = get_hill_inverse_matrix(kunci_matriks)
    
    print("\n" + "="*68)
    print(f" DEMO SUPERENKRIPSI: HILL CIPHER ({n}x{n}) + TRANSPOSISI MYSZKOWSKI")
    print("="*68)
    print(f"[*] Plaintext Asli              : {plaintext}")
    print(f"[*] Kunci 1 (Matriks Hill {n}x{n})  : {' , '.join(str(row) for row in kunci_matriks)}")
    print(f"[*] Matriks Invers Dekripsi     : {' , '.join(str(row) for row in inv_matriks)}")
    print(f"[*] Kunci 2 (Kata Myszkowski)   : {kunci_myszkowski}")
    print("-" * 68)
    
    # 1. Enkripsi Tahap 1: Substitusi Hill Cipher
    tahap_1 = hill_encrypt(plaintext, kunci_matriks)
    clean_pt = "".join(c for c in plaintext.upper() if c in ALPHABET)
    while len(clean_pt) % n != 0:
        clean_pt += 'X'
    pasangan_asli = " ".join(clean_pt[i:i+n] for i in range(0, len(clean_pt), n))
    pasangan_hill = " ".join(tahap_1[i:i+n] for i in range(0, len(tahap_1), n))
    print(f"[1] Pembagian Blok {n} Huruf      : {pasangan_asli}")
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