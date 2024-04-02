import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO

# Fungsi untuk perhitungan AHP
def ahp_attributes(ahp_df):
    sum_array = np.array(ahp_df.sum(numeric_only=True))
    cell_by_sum = ahp_df.drop(["Kriteria"], axis=1).div(sum_array, axis=1)
    priority_df = pd.DataFrame(cell_by_sum.mean(axis=1),
                               index=ahp_df.index, columns=['priority index'])
    return priority_df

# Fungsi utama untuk aplikasi Streamlit
def main():
    # Menambahkan judul dan deskripsi
    st.title('Aplikasi AHP menggunakan Streamlit')
    st.write("""
    Aplikasi ini menggunakan metode Analytic Hierarchy Process (AHP) untuk membantu pengguna mengambil keputusan dengan membandingkan berbagai kriteria.
    """)

    # Teks dari DataFrame
    data_text = """
             Budget  Camera     RAM     ROM  Battery  Processor
    Openness           0.2077  0.1846  0.2198  0.1973   0.2099     0.2003
    Conscientiousness  0.1676  0.2427  0.1821  0.2288   0.1882     0.1712
    Extraversion       0.2073  0.1635  0.1771  0.1639   0.1845     0.2039
    Agreeableness      0.1990  0.1713  0.2186  0.1716   0.2214     0.2079
    Neuroticism        0.2182  0.2379  0.2024  0.2384   0.1960     0.2166
    """

    # Membaca DataFrame dari teks
    df = pd.read_csv(StringIO(data_text), delim_whitespace=True, index_col=0)

   

    # Placeholder untuk input bobot relatif
    placeholders = {
        "budvscam": st.empty(),
        "budvsram": st.empty(),
        "budvsrom": st.empty(),
        "budvsbat": st.empty(),
        "budvsprc": st.empty(),
        "camvsram": st.empty(),
        "camvsrom": st.empty(),
        "camvsbat": st.empty(),
        "camvsprc": st.empty(),
        "ramvsrom": st.empty(),
        "ramvsbat": st.empty(),
        "ramvsprc": st.empty(),
        "romvsbat": st.empty(),
        "romvsprc": st.empty(),
        "batvsprc": st.empty()
    }

    # Proses input bobot relatif
    budvscam = placeholders["budvscam"].number_input("Seberapa penting harga dibandingkan kamera?", value=1)
    budvsram = placeholders["budvsram"].number_input("Seberapa penting harga dibandingkan RAM?", value=1)
    budvsrom = placeholders["budvsrom"].number_input("Seberapa penting harga dibandingkan ROM?", value=1)
    budvsbat = placeholders["budvsbat"].number_input("Seberapa penting harga dibandingkan baterai?", value=1)
    budvsprc = placeholders["budvsprc"].number_input("Seberapa penting harga dibandingkan processor?", value=1)
    camvsram = placeholders["camvsram"].number_input("Seberapa penting kamera dibandingkan RAM?", value=1)
    camvsrom = placeholders["camvsrom"].number_input("Seberapa penting kamera dibandingkan ROM?", value=1)
    camvsbat = placeholders["camvsbat"].number_input("Seberapa penting kamera dibandingkan batera?", value=1)
    camvsprc = placeholders["camvsprc"].number_input("Seberapa penting kamera dibandingkan processor?", value=1)
    ramvsrom = placeholders["ramvsrom"].number_input("Seberapa penting RAM dibandingkan ROM?", value=1)
    ramvsbat = placeholders["ramvsbat"].number_input("Seberapa penting RAM dibandingkan baterai?", value=1)
    ramvsprc = placeholders["ramvsprc"].number_input("Seberapa penting RAM dibandingkan processor?", value=1)
    romvsbat = placeholders["romvsbat"].number_input("Seberapa penting ROM dibandingkan baterai?", value=1)
    romvsprc = placeholders["romvsprc"].number_input("Seberapa penting ROM dibandingkan processor?", value=1)
    batvsprc = placeholders["batvsprc"].number_input("Seberapa penting baterai dibandingkan processor?", value=1)

    # Proses AHP saat tombol ditekan
    if st.button('Proses AHP'):
        data1 = {
            "Kriteria": ["Budget", "Camera", "RAM", "ROM", "Battery", "Processor"],
            "Budget": [1, 1/budvscam, 1/budvsram, 1/budvsrom, 1/budvsbat, 1/budvsprc],
            "Camera": [budvscam, 1, 1/camvsram, 1/camvsrom, 1/camvsbat, 1/camvsprc],
            "RAM": [budvsram, camvsram, 1, 1/ramvsrom, 1/ramvsbat, 1/ramvsprc],
            "ROM": [budvsrom, camvsrom, ramvsrom, 1, 1/romvsbat, 1/romvsprc],
            "Battery": [budvsbat, camvsbat, ramvsbat, romvsbat, 1, 1/batvsprc],
            "Processor": [budvsprc, camvsprc, ramvsprc, romvsprc, batvsprc, 1]
        }
        df1 = pd.DataFrame(data1)
        ahp_att = ahp_attributes(df1)

        # Membuat DataFrame hasil
        ahp_att1 = ahp_att.rename(columns={0: "Budget", 1: "Camera", 2: "RAM", 3: "ROM", 4: "Battery", 5: "Processor"})
        hasil = np.dot(df.values, ahp_att1.values)
        dfhasil = pd.DataFrame({
            "Personality": df.index,
            "Hasil": hasil.flatten()
        })
        max_personality = dfhasil[dfhasil["Hasil"] == dfhasil["Hasil"].max()]

        # Menampilkan DataFrame hasil
        st.header('Hasil Akhir AHP')
        st.write("Personality yang terpilih:", max_personality)

    # Menambahkan halaman sidebar untuk menjelaskan definisi dari masing-masing personality
    if st.sidebar.button('Definisi Personality'):
        st.header('Definisi Personality')
        st.write("""
        - **Openness**: Ciri-ciri kepribadian yang menunjukkan minat pada seni, kepemimpinan, atau emosi.
        - **Conscientiousness**: Ciri-ciri kepribadian yang menunjukkan kepatuhan, kedisiplinan, dan keseriusan dalam suatu tindakan.
        - **Extraversion**: Ciri-ciri kepribadian yang menunjukkan sifat sosial, percaya diri, dan antusiasme.
        - **Agreeableness**: Ciri-ciri kepribadian yang menunjukkan kerjasama, empati, dan toleransi terhadap orang lain.
        - **Neuroticism**: Ciri-ciri kepribadian yang menunjukkan tingkat kecemasan, ketegangan, dan sensitivitas emosional.
        """)
# Memanggil fungsi utama
if __name__ == '__main__':
    main()
