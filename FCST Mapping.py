import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="📊 FCST Replacer (With FDATE)", layout="centered")
st.title("🔁 Replace FCST Based on LOC + ITEM + CHANNEL + FDATE")

st.markdown("""
This tool replaces only the `FCST` in the **first file**, based on exact match of:

**`LOC + ITEM + CHANNEL + FDATE`** from the **second file**

🛡 All formats (like leading zeros) will be preserved.  
📋 Only `FCST` will be replaced. Everything else stays untouched.
""")

# File uploaders
file1 = st.file_uploader("📂 Upload File 1 (Base)", type=["csv", "txt"])
file2 = st.file_uploader("📂 Upload File 2 (Source)", type=["csv", "txt"])

if file1 and file2:
    try:
        # Read raw string lines from file1 (pipe-delimited single column)
        file1_lines = file1.read().decode("utf-8").splitlines()
        header = file1_lines[0].strip()
        col_names = header.split("|")

        # Convert File 1 to structured DataFrame
        data1 = [line.split("|") for line in file1_lines[1:]]
        df1 = pd.DataFrame(data1, columns=col_names)

        # Read File 2 normally
        df2 = pd.read_csv(file2, delimiter='|', dtype=str, keep_default_na=False)

        # Create match key: LOC + ITEM + CHANNEL + FDATE
        df1['KEY'] = df1['LOC'].str.strip() + df1['ITEM'].str.strip() + df1['CHANNEL'].str.strip() + df1['FDATE'].str.strip()
        df2['KEY'] = df2['LOC'].str.strip() + df2['ITEM'].str.strip() + df2['CHANNEL'].str.strip() + df2['FDATE'].str.strip()

        # FCST map from File 2
        fcst_map = df2.set_index('KEY')['FCST'].to_dict()

        # Replace FCST in df1 based on key match
        df1['FCST'] = df1.apply(lambda row: fcst_map.get(row['KEY'], row['FCST']), axis=1)

        # Drop helper column
        df1.drop(columns=['KEY'], inplace=True)

        # Reconstruct pipe-delimited lines
        output_lines = ['|'.join(col_names)]
        for _, row in df1.iterrows():
            output_lines.append('|'.join(row.astype(str)))

        result_data = '\n'.join(output_lines)

        # Download and preview
        st.success("✅ FCST values updated.")
        st.download_button("📥 Download Updated CSV", result_data, file_name="fcst_updated.csv", mime="text/csv")

        st.text("🔍 Preview:")
        st.code('\n'.join(output_lines[:5]), language='text')

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("⬆️ Upload both files to proceed.")
