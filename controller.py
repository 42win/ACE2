from model import create_table, insert_data, get_all_data
from view import display_user_data_form, display_credit_application
import streamlit as st
import pandas as pd
from model import get_user_names, get_user_data_by_name, predict_credit_score, update_credit_score, add_credit_score_column

# Fungsi utama untuk menjalankan aplikasi
def run():
    
    st.title("Aplikasi Pengelolaan Data dan Kredit")

    # Sidebar untuk navigasi
    menu = st.sidebar.selectbox("Pilih Menu", ['Data Pengguna', 'Pengajuan Kredit'])

    if menu == 'Data Pengguna':
        # Membuat tabel jika belum ada
        create_table()

        # Menampilkan form input
        user_input = display_user_data_form()

        if user_input:
            name, age, gender, income, education, marital_status, number_of_children, home_ownership = user_input

            # Menyimpan data ke database
            insert_data(name, age, gender, income, education, marital_status, number_of_children, home_ownership)
            
            # Menampilkan hasil input
            st.write(f"Name: {name}")
            st.write(f"Age: {age}")
            st.write(f"Gender: {gender}")
            st.write(f"Income: {income}")
            st.write(f"Education: {education}")
            st.write(f"Marital Status: {marital_status}")
            st.write(f"Number of Children: {number_of_children}")
            st.write(f"Home Ownership: {home_ownership}")

            # Menampilkan data yang sudah disimpan
            st.write("Data yang telah disimpan:")
            data = get_all_data()
            for row in data:
                st.write(row)

    elif menu == 'Pengajuan Kredit':
        # Menampilkan halaman pengajuan kredit
        display_credit_application()

        # Dropdown untuk memilih nama pengguna
        user_names = get_user_names()
        selected_user = st.selectbox("Pilih Nama Pengguna", user_names)

        # Form input untuk pengajuan kredit
        loan_amount = st.number_input("Jumlah Pinjaman", min_value=0, value=100000)
        loan_term = st.number_input("Lama Pinjaman (dalam bulan)", min_value=1, value=12)
        submit_button = st.button("Ajukan Kredit")
        
        if submit_button:
            # Proses pengajuan kredit
            st.write(f"Pengajuan Kredit: Jumlah {loan_amount} selama {loan_term} bulan telah diajukan.")
            
            # Ambil data pengguna berdasarkan nama
            print(selected_user)
            user_data = get_user_data_by_name(selected_user) 
            if user_data:
                print("tyes2")
                # Siapkan data untuk prediksi 		 
                user_data_df = pd.DataFrame([user_data], columns=["id", "name", "Age", "Gender", "Income", "Education", "Marital Status", "Number of Children", "Home Ownership", "Credit Score"])

                id_data = user_data_df['id']

                # Kolom kategori untuk encoding
                # cat_columns = ["gender", "education", "marital_status", "home_ownership"]
                cat_columns = user_data_df.select_dtypes(include='object').columns.tolist()

                # Prediksi menggunakan model
                user_data_df = user_data_df.drop(['name','id','Credit Score'], axis=1)

                prediction = predict_credit_score(user_data_df, cat_columns)

                # Membuat dictionary untuk mapping angka ke label
                label_map = {0: 'Average', 1: 'High', 2: 'Low'}

                # Mengubah prediksi angka menjadi label string
                predicted_labels = [label_map[p] for p in prediction]
 
                # Update kolom Credit Score di database
                # add_credit_score_column()
                update_credit_score(user_data[0], predicted_labels[0])  # Menggunakan ID pengguna untuk pembaruan

                # Menampilkan hasil prediksi
                st.write(f"Prediksi Credit Score untuk {selected_user}: {predicted_labels[0]}")
            else:
                st.error("Data pengguna tidak ditemukan.")