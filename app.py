# import streamlit as st 
# import pandas as pd 

# name = st.text_input("Enter Your Name : ")
# f_name = st.text_input("Enter Your Father Name : ")
# adr = st.text_area("Enter Your Address ")
# userClass = st.selectbox("Enter Your Class :",(1,2,3,4,5,6))

import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        color: white;
        font-family: 'Arial', sans-serif;
    }
    .stApp {
        background: transparent;
    }
    .title-text {
        font-size: 3rem;
        text-align: center;
        color: #00ADB5;
        margin-bottom: 2rem;
    }
    .description-text {
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }
    .stFileUploader {
        border: 2px solid #00ADB5;
        border-radius: 15px;
    }
    .stButton>button {
        background-color: #00ADB5;
        color: white;
        border-radius: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #393E46;
    }
    .card {
        padding: 1.5rem;
        border-radius: 15px;
        background: rgba(0, 0, 0, 0.7);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    .section-title {
        color: #00ADB5;
        font-size: 1.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.markdown("<div class='title-text'>Datasweeper Streamlit Integrator By Muhammad Talha</div>", unsafe_allow_html=True)
st.markdown("<div class='description-text'>Transform your files between CSV and Excel formats with built-in data cleaning.</div>", unsafe_allow_html=True)

# File uploader
upload_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read the uploaded file
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine='openpyxl')
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # File details
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Preview the Data</div>", unsafe_allow_html=True)
        st.dataframe(df.head())
        st.markdown("</div>", unsafe_allow_html=True)

        # Data cleaning options
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Data Cleaning Options</div>", unsafe_allow_html=True)

        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values filled!")
        st.markdown("</div>", unsafe_allow_html=True)

        # Select columns to keep
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Select Columns to Keep</div>", unsafe_allow_html=True)

        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]
        st.markdown("</div>", unsafe_allow_html=True)

        # Data visualization
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Data Visualization</div>", unsafe_allow_html=True)

        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        st.markdown("</div>", unsafe_allow_html=True)

        # Conversion options
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Conversion Options</div>", unsafe_allow_html=True)

        conversion_type = st.radio(f"Convert {file.name} to", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"📥 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

        st.markdown("</div>", unsafe_allow_html=True)

st.success("🎉 All files processed successfully!")
