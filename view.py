import streamlit as st

# Fungsi untuk menampilkan form input
def display_user_data_form():
    # Form untuk input data
    with st.form(key='user_input_form'):
        # Input untuk 'Name' - String input
        name = st.text_input("Name")

        # Input untuk 'Age' - Number input
        age = st.number_input("Age", min_value=18, max_value=100, value=25)

        # Input untuk 'Gender' - Dropdown
        gender = st.selectbox("Gender", ['Female', 'Male'])

        # Input untuk 'Income' - Number input
        income = st.number_input("Income", min_value=0, value=50000)

        # Input untuk 'Education' - Dropdown
        education = st.selectbox("Education", ['Bachelor\'s Degree', 'Master\'s Degree', 'Doctorate',
                                               'High School Diploma', 'Associate\'s Degree'])

        # Input untuk 'Marital Status' - Dropdown
        marital_status = st.selectbox("Marital Status", ['Single', 'Married'])

        # Input untuk 'Number of Children' - Number input
        number_of_children = st.number_input("Number of Children", min_value=0, value=0)

        # Input untuk 'Home Ownership' - Dropdown
        home_ownership = st.selectbox("Home Ownership", ['Rented', 'Owned'])

        # Button untuk submit form
        submit_button = st.form_submit_button(label='Submit')

        # Jika button diklik, tampilkan hasil input dan simpan ke database
        if submit_button:
            return name, age, gender, income, education, marital_status, number_of_children, home_ownership
        else:
            return None

# Fungsi untuk menampilkan halaman pengajuan kredit
def display_credit_application():
    st.title("Halaman Pengajuan Kredit")
    st.write("""
        Di halaman ini, Anda dapat mengajukan permohonan kredit dengan mengisi beberapa informasi terkait penghasilan, 
        pekerjaan, dan kebutuhan pinjaman. Kami akan memproses pengajuan Anda dan memberikan rekomendasi.
    """)