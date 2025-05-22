import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import chardet
from io import BytesIO
import os 

os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "1024"
st.set_page_config(page_title="CSV UTF-8 Converter", layout="centered")

st.title("📁 CSV to UTF-8 (with BOM) Converter")
st.markdown("Ensure Arabic content displays correctly in Excel by converting CSVs to UTF-8 with BOM.")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    raw_data = uploaded_file.read()
    
    # Detect encoding
    detection = chardet.detect(raw_data)
    encoding = detection.get("encoding")
    confidence = detection.get("confidence", 0)

    if not encoding:
        st.error("Could not detect encoding. Please check the file.")
    else:
        st.success(f"Detected Encoding: `{encoding}` (Confidence: {confidence:.2f})")
        
        try:
            df = pd.read_csv(BytesIO(raw_data), encoding=encoding)

            # Convert to UTF-8 with BOM
            output = BytesIO()
            df.to_csv(output, index=False, encoding="utf-8-sig")  # Excel-friendly
            output.seek(0)

            st.download_button(
                label="⬇️ Download UTF-8 (with BOM) CSV",
                data=output,
                file_name="converted_utf8_bom.csv",
                mime="text/csv"
            )

            st.dataframe(df.head())

        except Exception as e:
            st.error(f"Error reading the file: {e}")
