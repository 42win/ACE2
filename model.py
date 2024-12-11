import sqlite3

import joblib
import pandas as pd

# Memuat model dan encoder yang sudah disimpan
loaded_model = joblib.load('./model/logistic_regression_model.pkl')
loaded_le_dict = joblib.load('./model/label_encoder.pkl')

def predict_credit_score(user_data_df, cat_columns):
    """
    Melakukan prediksi berdasarkan data pengguna dan model yang sudah dilatih.
    
    Parameters:
    - user_data_df: DataFrame yang berisi data pengguna
    - cat_columns: List kolom kategori yang perlu di-transformasi
    
    Returns:
    - prediction: Hasil prediksi model
    """
    # Menyaring kolom kategori yang ada pada data baru
    cat = user_data_df.select_dtypes(include='object').columns.tolist()
    cat_in_new_data = [col for col in cat if col in user_data_df.columns] 
    
    # Transformasi data kategori jika diperlukan
    for col in cat_in_new_data:
        le = loaded_le_dict[col]
        user_data_df[col] = le.transform(user_data_df[col])

    # Melakukan prediksi
    prediction = loaded_model.predict(user_data_df)

    return prediction

def get_user_data_by_name(name):
    """Mengambil data pengguna berdasarkan nama dari tabel data_user."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data_user WHERE name = ?", (name,))
    user_data = cursor.fetchone()
    conn.close()

    # Jika data ditemukan, mengubahnya menjadi DataFrame
    if user_data: 
        return user_data
    return None

    # Fungsi untuk memperbarui tabel data_user berdasarkan id dengan nilai Credit Score yang diprediksi
def update_credit_score(user_id, predicted_label):
    conn = create_connection()
    cursor = conn.cursor()
    
    # Update kolom Credit Score di tabel data_user berdasarkan id
    cursor.execute('''UPDATE data_user SET credit_score = ? WHERE id = ?''', 
                   (predicted_label, user_id))  # Menyimpan hasil prediksi ke kolom Credit Score
    
    conn.commit()
    conn.close()

def add_credit_score_column():
    # Membuka koneksi ke database
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()

    # Menambahkan kolom credit_score jika belum ada
    try:
        c.execute('''ALTER TABLE data_user ADD COLUMN credit_score TEXT''')
        print("Kolom credit_score berhasil ditambahkan.")
    except sqlite3.OperationalError as e:
        print("Error saat menambahkan kolom:", e)

    # Menyimpan perubahan dan menutup koneksi
    conn.commit()
    conn.close()

# Panggil fungsi untuk menambahkan kolom
add_credit_score_column()

# Fungsi untuk membuat koneksi ke database SQLite
def create_connection():
    conn = sqlite3.connect('mydatabase.db')
    return conn

# Fungsi untuk membuat tabel data_user jika belum ada
def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data_user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    gender TEXT,
                    income INTEGER,
                    education TEXT,
                    marital_status TEXT,
                    number_of_children INTEGER,
                    home_ownership TEXT)''')
    conn.commit()
    conn.close()

# Fungsi untuk menyimpan data pengguna ke dalam database
def insert_data(name, age, gender, income, education, marital_status, number_of_children, home_ownership):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO data_user (name, age, gender, income, education, marital_status, number_of_children, home_ownership)
                 VALUES (?,?, ?, ?, ?, ?, ?, ?)''', 
                 (name, age, gender, income, education, marital_status, number_of_children, home_ownership))
    conn.commit()
    conn.close()

# Fungsi untuk mengambil semua data dari tabel
def get_all_data():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM data_user")
    data = c.fetchall()
    conn.close()
    return data

# Fungsi untuk mengambil nama-nama dari tabel data_user
def get_user_names():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM data_user")  # Query untuk mengambil nama
    users = cursor.fetchall()
    conn.close()
    return [user[0] for user in users]  # Mengembalikan list nama pengguna