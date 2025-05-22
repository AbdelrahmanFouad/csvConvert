import streamlit as st
import chardet
from io import BytesIO

st.set_page_config(page_title="CSV UTF-8 Converter", layout="wide")
st.title("📁 CSV to UTF-8 (with BOM) Converter")
st.markdown("Convert CSV files to UTF-8 with BOM for Excel compatibility.")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    raw_data = uploaded_file.read()

    # Detect encoding from first 10 KB only for speed
    sample_bytes = raw_data[:10_000]
    detection = chardet.detect(sample_bytes)
    encoding = detection.get("encoding")
    confidence = detection.get("confidence", 0)

    if not encoding:
        st.error("Could not detect encoding. Please check the file.")
    else:
        st.success(f"Detected Encoding: `{encoding}` (Confidence: {confidence:.2f})")

        try:
            # Decode raw bytes with detected encoding
            text = raw_data.decode(encoding)

            # Re-encode text as UTF-8 with BOM bytes
            output_bytes = b'\xef\xbb\xbf' + text.encode('utf-8')

            output = BytesIO(output_bytes)

            st.download_button(
                label="⬇️ Download UTF-8 (with BOM) CSV",
                data=output,
                file_name="converted_utf8_bom.csv",
                mime="text/csv"
            )

            # Optional preview (slow, pandas needed)
            if st.checkbox("Show preview of first 5 rows (slow for big files)"):
                import pandas as pd
                df = pd.read_csv(BytesIO(raw_data), encoding=encoding, nrows=5)
                st.dataframe(df)

        except Exception as e:
            st.error(f"Error processing the file: {e}")
