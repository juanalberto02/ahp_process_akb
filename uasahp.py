import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import plotly.express as px

# Fungsi untuk perhitungan AHP
def ahp_attributes(ahp_df):
    sum_array = np.array(ahp_df.sum(numeric_only=True))
    cell_by_sum = ahp_df.drop(["Kriteria"], axis=1).div(sum_array, axis=1)
    priority_df = pd.DataFrame(cell_by_sum.mean(axis=1),
                               index=ahp_df.index, columns=['priority index'])
    return priority_df

# Fungsi untuk menampilkan aksi berdasarkan kepribadian
def show_action(selected_personality):
    if selected_personality == "Neuroticism":
        st.write("Opsional A: Tindakan yang dapat diambil untuk neuroticism.")
    elif selected_personality == "Openness":
        st.write("Opsional B: Tindakan yang dapat diambil untuk openness.")
    elif selected_personality == "Conscientiousness":
        st.write("Opsional C: Tindakan yang dapat diambil untuk conscientiousness.")
    elif selected_personality == "Extraversion":
        st.write("Opsional D: Tindakan yang dapat diambil untuk extraversion.")
    elif selected_personality == "Agreeableness":
        st.write("Opsional E: Tindakan yang dapat diambil untuk agreeableness.")

# Fungsi untuk menampilkan distribusi bobot relatif
# Fungsi untuk menampilkan detail
def show_detail():
    st.title('Detail')
    st.write("""
        Bobot distribusi yang digunakan dalam prediksi kepribadian:

        | Kriteria          | Openness | Conscientiousness | Extraversion | Agreeableness | Neuroticism |
        |-------------------|----------|-------------------|--------------|---------------|-------------|
        | Budget            | 0.2077   | 0.1676            | 0.2073       | 0.1990        | 0.2182      |
        | Camera            | 0.1846   | 0.2427            | 0.1635       | 0.1713        | 0.2379      |
        | RAM               | 0.2198   | 0.1821            | 0.1771       | 0.2186        | 0.2024      |
        | ROM               | 0.1973   | 0.2288            | 0.1639       | 0.1716        | 0.2384      |
        | Battery           | 0.2099   | 0.1882            | 0.1845       | 0.2214        | 0.1960      |
        | Processor         | 0.2003   | 0.1712            | 0.2039       | 0.2079        | 0.2166      |
    """)

    # Data bobot distribusi
    data = {
        "Kriteria": ["Budget", "Camera", "RAM", "ROM", "Battery", "Processor"],
        "Openness": [0.2077, 0.1846, 0.2198, 0.1973, 0.2099, 0.2003],
        "Conscientiousness": [0.1676, 0.2427, 0.1821, 0.2288, 0.1882, 0.1712],
        "Extraversion": [0.2073, 0.1635, 0.1771, 0.1639, 0.1845, 0.2039],
        "Agreeableness": [0.1990, 0.1713, 0.2186, 0.1716, 0.2214, 0.2079],
        "Neuroticism": [0.2182, 0.2379, 0.2024, 0.2384, 0.1960, 0.2166]
    }

    # Membuat DataFrame
    df = pd.DataFrame(data)

    # Menggabungkan data bobot distribusi untuk plot
    df_melted = df.melt(id_vars=["Kriteria"], var_name="Personality", value_name="Bobot")

    # Membuat bar chart interaktif
    fig = px.bar(df_melted, x="Kriteria", y="Bobot", color="Personality", barmode="group", color_discrete_sequence=['#E63946', '#F1FAEE', '#A8DADC', '#457B9D', '#1D3557'])

    # Menampilkan plot
    st.plotly_chart(fig)
    

# Fungsi utama untuk aplikasi Streamlit
def main():
    st.sidebar.title('Menu')
    page = st.sidebar.selectbox("Choose a page", ["Prediction", "Definition", "Detail"])

    if page == "Prediction":
        st.markdown(
            f"<h1 style='text-align: center;'>Personality Trait Prediction</h1>"
            "<h4 style='text-align: center;'>By Kelompok 14</h4>", 
            unsafe_allow_html=True
        )

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
        budvscam = placeholders["budvscam"].slider("Seberapa penting harga dibandingkan kamera?", min_value=0, max_value=9, value=5, format="%.0f", key="budvscam", help="0: Tidak Penting, 9: Sangat Penting")
        budvsram = placeholders["budvsram"].slider("Seberapa penting harga dibandingkan RAM?", min_value=0, max_value=9, value=5, format="%.0f", key="budvsram")
        budvsrom = placeholders["budvsrom"].slider("Seberapa penting harga dibandingkan ROM?", min_value=0, max_value=9, value=5, format="%.0f", key="budvsrom")
        budvsbat = placeholders["budvsbat"].slider("Seberapa penting harga dibandingkan baterai?", min_value=0, max_value=9, value=5, format="%.0f", key="budvsbat")
        budvsprc = placeholders["budvsprc"].slider("Seberapa penting harga dibandingkan processor?", min_value=0, max_value=9, value=5, format="%.0f", key="budvsprc")
        camvsram = placeholders["camvsram"].slider("Seberapa penting kamera dibandingkan RAM?", min_value=0, max_value=9, value=5, format="%.0f", key="camvsram")
        camvsrom = placeholders["camvsrom"].slider("Seberapa penting kamera dibandingkan ROM?", min_value=0, max_value=9, value=5, format="%.0f", key="camvsrom")
        camvsbat = placeholders["camvsbat"].slider("Seberapa penting kamera dibandingkan batera?", min_value=0, max_value=9, value=5, format="%.0f", key="camvsbat")
        camvsprc = placeholders["camvsprc"].slider("Seberapa penting kamera dibandingkan processor?", min_value=0, max_value=9, value=5, format="%.0f", key="camvsprc")
        ramvsrom = placeholders["ramvsrom"].slider("Seberapa penting RAM dibandingkan ROM?", min_value=0, max_value=9, value=5, format="%.0f", key="ramvsrom")
        ramvsbat = placeholders["ramvsbat"].slider("Seberapa penting RAM dibandingkan baterai?", min_value=0, max_value=9, value=5, format="%.0f", key="ramvsbat")
        ramvsprc = placeholders["ramvsprc"].slider("Seberapa penting RAM dibandingkan processor?", min_value=0, max_value=9, value=5, format="%.0f", key="ramvsprc")
        romvsbat = placeholders["romvsbat"].slider("Seberapa penting ROM dibandingkan baterai?", min_value=0, max_value=9, value=5, format="%.0f", key="romvsbat")
        romvsprc = placeholders["romvsprc"].slider("Seberapa penting ROM dibandingkan processor?", min_value=0, max_value=9, value=5, format="%.0f", key="romvsprc")
        batvsprc = placeholders["batvsprc"].slider("Seberapa penting baterai dibandingkan processor?", min_value=0, max_value=9, value=5, format="%.0f", key="batvsprc")

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

            # Piechart hasil
            st.header('Pie Chart Hasil')
            fig = px.pie(dfhasil, values='Hasil', names='Personality', color_discrete_sequence=['#E63946', '#F1FAEE', '#A8DADC', '#457B9D', '#1D3557'])
            st.plotly_chart(fig)

            # Menampilkan DataFrame hasil
            st.write("Personality yang terpilih:", max_personality)

            # Aksi yang dapat diambil
            if st.button('Lihat Aksi yang Dapat Diambil'):
                # Atur parameter URL untuk mengarahkan ke halaman lain
                st.experimental_set_query_params(page='Action')

    elif page == "Definition":
        st.title('Definisi Personality Traits')

        # Daftar kepribadian
        personalities = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
        
        # Pilihan drop-down untuk memilih kepribadian
        selected_personality = st.selectbox("Pilih Personality", personalities)

        # Menampilkan definisi berdasarkan pilihan pengguna
        if selected_personality == "Openness":
            st.write("**Openness**: Ciri-ciri kepribadian yang menunjukkan minat pada seni, kepemimpinan, atau emosi.")
        elif selected_personality == "Conscientiousness":
            st.write("**Conscientiousness**: Ciri-ciri kepribadian yang menunjukkan kepatuhan, kedisiplinan, dan keseriusan dalam suatu tindakan.")
        elif selected_personality == "Extraversion":
            st.write("**Extraversion**: Ciri-ciri kepribadian yang menunjukkan sifat sosial, percaya diri, dan antusiasme.")
        elif selected_personality == "Agreeableness":
            st.write("**Agreeableness**: Ciri-ciri kepribadian yang menunjukkan kerjasama, empati, dan toleransi terhadap orang lain.")
        elif selected_personality == "Neuroticism":
            st.write("**Neuroticism**: Ciri-ciri kepribadian yang menunjukkan tingkat kecemasan, ketegangan, dan sensitivitas emosional.")

    elif page == "Detail":
        show_detail()

# Memanggil fungsi utama
if __name__ == '__main__':
    main()
