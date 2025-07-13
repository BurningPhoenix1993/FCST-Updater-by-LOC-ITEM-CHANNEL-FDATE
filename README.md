# 🔁 FCST Value Replacer Based on LOC + ITEM + CHANNEL + FDATE

A powerful and offline-capable Streamlit tool that replaces only the `FCST` values in a pipe-delimited forecast dataset, based on matching keys from another file. It ensures formatting like leading zeros, date strings, and structure are fully preserved.

---

## 📦 Features

- 🔁 **Replaces only FCST values** in File 1, based on File 2
- 🔍 Matching is done on: `LOC + ITEM + CHANNEL + FDATE`
- 🛡 **Preserves format**, including leading zeros, pipe separators, etc.
- 📂 Accepts `.csv` or `.txt` files (pipe-delimited)
- 💡 Works **completely offline** — no external APIs needed
- 📥 Download updated file in original format
- ✅ Easy-to-use Streamlit interface

- 📌 Algorithm (How It Works)
Load File 1 as pipe-delimited text, split into structured DataFrame
Load File 2 using pandas (| delimiter)
Construct unique key: LOC + ITEM + CHANNEL + FDATE
Create dictionary: KEY → FCST from File 2
Loop through File 1, replace FCST where a match is found
Rebuild the original pipe format
Display preview and download updated file


