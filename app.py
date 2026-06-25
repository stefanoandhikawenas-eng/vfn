import streamlit as st
import pandas as pd
import os


st.set_page_config(
    page_title="Virtual Field Notebook",
    page_icon="🪨",
    layout="wide"
)

st.title("🪨 Virtual Field Notebook")

st.header("Input Data Singkapan")

nama_pengamat = st.text_input("Nama Pengamat")

nama_lokasi = st.text_input("Nama Lokasi")

kode_stasiun = st.text_input("Kode Stasiun")

x = st.number_input(
    "Koordinat X (Easting)",
    format="%.2f"
)

y = st.number_input(
    "Koordinat Y (Northing)",
    format="%.2f"
)

metode_foto = st.radio(
    "Metode Foto",
    ["📁 Upload File", "📷 Kamera"]
)

if metode_foto == "📷 Kamera":
    foto = st.camera_input("Ambil Foto Singkapan")
else:
    foto = st.file_uploader(
        "Upload Foto Singkapan",
        type=["jpg", "jpeg", "png"]
    )

litologi = st.selectbox(
    "Jenis Batuan (Litologi)",
    [
        "Batuan Sedimen Silisiklastik",
        "Batuan Sedimen Karbonat",
        "Batuan Metamorf",
        "Batuan Piroklastik",
        "Batuan Beku",
        "Lainnya"
    ]
)

if litologi == "Lainnya":
    litologi = st.text_input(
        "Masukkan Jenis Batuan Selain Pilihan Sebelumnya"
    )

deskripsi = st.text_area(
    "Deskripsi Singkapan",
    height=150
)

deskripsi_batuan = st.text_area(
    "Deskripsi Batuan",
    height=150
)

struktur = st.multiselect(
    "Struktur Geologi Dominan",
    [
        "Perlapisan",
        "Kekar",
        "Sesar",
        "Lipatan",
        "Rekahan"
    ]
)

strike = st.text_input("Strike")

dip = st.text_input("Dip")

if st.button("💾 Simpan Data"):

    nama_foto = ""

    if foto is not None:

        nama_foto = foto.name

        os.makedirs("photos", exist_ok=True)

        with open(
            os.path.join("photos", nama_foto),
            "wb"
        ) as f:

            f.write(foto.getbuffer())

    data_baru = pd.DataFrame({
        "Nama_Pengamat":[nama_pengamat],
        "Kode":[kode_stasiun],
        "Nama_Lokasi":[nama_lokasi],
        "Koordinat X (Easting)":[x],
        "Koordinat Y (Northing)":[y],
        "Litologi":[litologi],
        "Deskripsi":[deskripsi],
        "Deskripsi_Batuan":[deskripsi_batuan],
        "Struktur":[struktur],
        "Strike":[strike],
        "Dip":[dip],
        "Foto":[nama_foto]
    })

    df_lama = pd.read_csv("singkapan.csv")

    df = pd.concat(
        [df_lama, data_baru],
        ignore_index=True
    )

    df.to_csv(
        "singkapan.csv",
        index=False
    )

    st.success("Data berhasil disimpan!")

df_dashboard = pd.read_csv(
    "singkapan.csv"
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Jumlah Singkapan",
        len(df_dashboard)
    )

with col2:
    st.metric(
        "Jumlah Litologi",
        df_dashboard["Litologi"].nunique()
    )

st.divider()

st.header("📊 Dashboard Data Singkapan")

df_dashboard = pd.read_csv(
    "singkapan.csv"
)

st.dataframe(
    df_dashboard,
    width="stretch"
)
