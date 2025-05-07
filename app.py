import streamlit as st
import pandas as pd
import io

st.title("📊 Materijal - filtriranje po delovima")

uploaded_file = st.file_uploader("📂 Izaberi Excel fajl", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.write("✅ Učitani podaci:")
    st.dataframe(df)

    if "IFC_Tag" in df.columns:
        delovi = df["IFC_Tag"].dropna().unique()
        izabrani = st.multiselect("🔍 Izaberi jedan ili više IFC_Tag delova", options=delovi)

        if izabrani:
            filtrirani_df = df[df["IFC_Tag"].isin(izabrani)]

            st.write("📌 Filtrirani rezultati:")
            st.dataframe(filtrirani_df)

            if "Масса" in filtrirani_df.columns:
                ukupna_masa = filtrirani_df["Масса"].sum()
                st.success(f"🧮 Ukupna masa za izabrane delove: {ukupna_masa:.2f}")

            # Priprema Excel fajla u memoriji
            excel_file = io.BytesIO()
            filtrirani_df.to_excel(excel_file, index=False, engine='openpyxl')
            excel_file.seek(0)

            st.download_button(
                label="📥 Preuzmi filtrirani fajl",
                data=excel_file,
                file_name="filtrirani_izvestaj.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("⬅️ Izaberi bar jedan IFC_Tag za prikaz.")
    else:
        st.error("❌ Fajl ne sadrži kolonu 'IFC_Tag'.")


