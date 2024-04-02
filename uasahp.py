import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import plotly.express as px

st.markdown(
    """
    <style>
        body {
            background-color: #1E1E1E;
            color: white;
        }
        .sidebar .sidebar-content {
            background-color: #333333;
            color: white;
        }
        .Widget>label {
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)
# Fungsi untuk perhitungan AHP
def ahp_attributes(ahp_df):
    sum_array = np.array(ahp_df.sum(numeric_only=True))
    cell_by_sum = ahp_df.drop(["Kriteria"], axis=1).div(sum_array, axis=1)
    priority_df = pd.DataFrame(cell_by_sum.mean(axis=1),
                               index=ahp_df.index, columns=['priority index'])
    return priority_df



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
    
def consistency_ratio(priority_index, ahp_df):
    priority_index = priority_index.transpose()
    random_matrix = {
        1: 0, 2: 0, 3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24, 7: 1.32,
        8: 1.14, 9: 1.45, 10: 1.49, 11: 1.51, 12: 1.48, 13: 1.56,
        14: 1.57, 15: 1.59, 16: 1.605, 17: 1.61, 18: 1.615, 19: 1.62, 20: 1.625
    }
    # Check for consistency
    consistency_df = ahp_df.drop(df1.columns[[0]], axis=1).multiply(np.array(priority_index.loc['priority index']), axis=1)
    consistency_df['sum_of_col'] = consistency_df.sum(axis=1)
    # To find lambda max
    lambda_max_df = consistency_df['sum_of_col'].div(np.array(priority_index.transpose()['priority index']), axis=0)
    lambda_max = lambda_max_df.mean()
    # To find the consistency index
    consistency_index = round((lambda_max - len(ahp_df.index)) / (len(ahp_df.index) - 1), 3)
    print(f'The Consistency Index is: {consistency_index}')
    # To find the consistency ratio
    consistency_ratio = round(consistency_index / random_matrix[len(ahp_df.index)], 3)
    print(f'The Consistency Ratio is: {consistency_ratio}')
    if consistency_ratio < 0.1:
        print('The model is consistent')
    else:
        print('The model is not consistent')

# Fungsi utama untuk aplikasi Streamlit
def main():
    st.sidebar.title('Menu')
    page = st.sidebar.selectbox("Choose a page", ["Beranda", "Prediction", "Definition", "Detail"])
    if page == "Beranda":
        st.markdown(
        """
        <style>
            @keyframes moveInFromTop {
                from {
                    transform: translateY(-100%);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }

            @keyframes moveInFromBottom {
                from {
                    transform: translateY(100%);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }

            h1 {
                animation: moveInFromTop 1s ease-out;
            }

            .subtitle {
                animation: moveInFromBottom 1s ease-out;
                
            }
        </style>
        """
        , unsafe_allow_html=True
        )

        st.markdown("<br><br><br><br><br><br><br><br><br><h1 style='text-align: center;'>Welcome to Personality Trait Prediction !</h1><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
        
        st.markdown("<p class='subtitle' style='text-align: center; font-size: 20px;'>By Kelompok 14</p>", unsafe_allow_html=True)


    elif page == "Prediction":
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

            max_personality_name = dfhasil.loc[dfhasil["Hasil"].idxmax(), "Personality"]
            # Piechart hasil
            st.header('Pie Chart Hasil')
            fig = px.pie(dfhasil, values='Hasil', names='Personality', color_discrete_sequence=['#E63946', '#F1FAEE', '#A8DADC', '#457B9D', '#1D3557'])
            st.plotly_chart(fig)

            # Menampilkan hasil
            st.markdown("""
                <style>
                    /* Animasi gradien merah */
                    @keyframes colorchange {
                        0% {color: #FF0000;}
                        25% {color: #FF3333;}
                        50% {color: #FF6666;}
                        75% {color: #FF9999;}
                        100% {color: #FFCCCC;}
                    }

                    /* Menerapkan animasi ke teks */
                    .animated-text {
                        animation: colorchange 5s infinite;
                    }
                </style>
            """, unsafe_allow_html=True)

            # Menampilkan hasil selected personality dengan animasi gradien merah
            selected_personality = max_personality_name  # Ganti dengan hasil selected personality Anda
            st.markdown(f"<h1 style='text-align: center;'>Personality yang terpilih: <span class='animated-text'>{selected_personality}</span></h1>", unsafe_allow_html=True)

    # Page Definition
    elif page == "Definition":
        st.markdown(
            f"<h1 style='text-align: center;'>Personality Trait</h1>",
            unsafe_allow_html=True
        )

        # Daftar kepribadian
        personalities = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
        
        # Pilihan drop-down untuk memilih kepribadian
        selected_personality = st.selectbox("Pilih Personality", personalities)

        # Data definisi dan strategi pemasaran
        definition_strategies = {
        "Openness": {
            "Deskripsi": "Openness adalah kecenderungan individu untuk berpikir dan bertindak secara kreatif, terbuka terhadap pengalaman baru, dan memiliki minat yang luas dalam seni, kepemimpinan, atau emosi.",
            "Strategi Pemasaran": "Menggunakan desain yang inovatif dan menarik untuk produk yang dapat meningkatkan kreativitas pelanggan."
        },
        "Conscientiousness": {
            "Deskripsi": "Conscientiousness adalah kecenderungan individu untuk bertindak secara hati-hati, teratur, dan bertanggung jawab dalam segala tindakan.",
            "Strategi Pemasaran": "Menyoroti keandalan dan kualitas produk serta menawarkan jaminan kepuasan pelanggan."
        },
        "Extraversion": {
            "Deskripsi": "Extraversion adalah kecenderungan individu untuk menjadi sosial, percaya diri, dan antusias dalam interaksi sosial.",
            "Strategi Pemasaran": "Mengadakan acara promosi dan aktivitas sosial untuk menarik perhatian pelanggan dan meningkatkan keterlibatan."
        },
        "Agreeableness": {
            "Deskripsi": "Agreeableness adalah kecenderungan individu untuk bersikap ramah, empatik, dan toleran terhadap orang lain.",
            "Strategi Pemasaran": "Menekankan pada layanan pelanggan yang ramah dan menawarkan produk yang mendukung kebutuhan dan nilai-nilai pelanggan."
        },
        "Neuroticism": {
            "Deskripsi": "Neuroticism adalah kecenderungan individu untuk mengalami tingkat kecemasan, ketegangan, dan sensitivitas emosional yang tinggi.",
            "Strategi Pemasaran": "Menyediakan produk atau layanan yang menawarkan rasa aman dan kenyamanan bagi pelanggan."
        }
    }

        # Menampilkan definisi dan strategi pemasaran dalam bentuk tabel
        st.table(definition_strategies[selected_personality])

    elif page == "Detail":
        show_detail()

# Memanggil fungsi utama
if __name__ == '__main__':
    main()
