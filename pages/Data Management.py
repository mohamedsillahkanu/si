import streamlit as st
import pandas as pd
import numpy as np
from stringdist import levenshtein

# Streamlit app
st.title("Health Facility Name Matching")

# File upload
st.header("Upload Your Files")
uploaded_file_dhis2 = st.file_uploader("Upload DHIS2 File (CSV, XLS, XLSX)", type=["csv", "xls", "xlsx"])
uploaded_file_mfl = st.file_uploader("Upload MFL File (CSV, XLS, XLSX)", type=["csv", "xls", "xlsx"])

if uploaded_file_dhis2 and uploaded_file_mfl:
    # Read the uploaded files
    try:
        if uploaded_file_dhis2.name.endswith(".csv"):
            health_facilities_dhis2_list = pd.read_csv(uploaded_file_dhis2)
        else:
            health_facilities_dhis2_list = pd.read_excel(uploaded_file_dhis2)

        if uploaded_file_mfl.name.endswith(".csv"):
            master_hf_list = pd.read_csv(uploaded_file_mfl)
        else:
            master_hf_list = pd.read_excel(uploaded_file_mfl)

        st.success("Files uploaded successfully!")
    except Exception as e:
        st.error(f"Error reading files: {e}")
        st.stop()

    # Initialize session state for renamed columns
    if "renamed_dhis2_col" not in st.session_state:
        st.session_state.renamed_dhis2_col = health_facilities_dhis2_list.columns.tolist()

    if "renamed_mfl_col" not in st.session_state:
        st.session_state.renamed_mfl_col = master_hf_list.columns.tolist()

    # Display data
    st.subheader("Preview of Uploaded Files")
    st.write("DHIS2 File:")
    st.dataframe(health_facilities_dhis2_list.head())
    st.write("MFL File:")
    st.dataframe(master_hf_list.head())

    # Column renaming section
    st.header("Rename Columns")

    rename_option = st.selectbox("Select dataset to rename columns", ["DHIS2", "MFL"])
    if rename_option == "DHIS2":
        st.write("Rename Columns in DHIS2:")
        for col in health_facilities_dhis2_list.columns:
            new_col_name = st.text_input(f"Rename '{col}' in DHIS2", value=col, key=f"rename_dhis2_{col}")
            if new_col_name != col:
                st.session_state.renamed_dhis2_col = [
                    new_col_name if c == col else c for c in st.session_state.renamed_dhis2_col
                ]
        if st.button("Apply Renaming to DHIS2"):
            health_facilities_dhis2_list.columns = st.session_state.renamed_dhis2_col
            st.success("Renaming applied to DHIS2 dataset.")
            st.write("Renamed DHIS2 File:")
            st.dataframe(health_facilities_dhis2_list.head())

    elif rename_option == "MFL":
        st.write("Rename Columns in MFL:")
        for col in master_hf_list.columns:
            new_col_name = st.text_input(f"Rename '{col}' in MFL", value=col, key=f"rename_mfl_{col}")
            if new_col_name != col:
                st.session_state.renamed_mfl_col = [
                    new_col_name if c == col else c for c in st.session_state.renamed_mfl_col
                ]
        if st.button("Apply Renaming to MFL"):
            master_hf_list.columns = st.session_state.renamed_mfl_col
            st.success("Renaming applied to MFL dataset.")
            st.write("Renamed MFL File:")
            st.dataframe(master_hf_list.head())

    # Matching threshold
    st.header("Set Matching Threshold")
    threshold = st.slider("Set Matching Threshold (0 to 100)", min_value=0, max_value=100, value=70, step=1)

    # Matching function
    def calculate_match(column1, column2):
        results = []

        for value1 in column1:
            if value1 in column2.values:
                results.append({
                    "Col1": value1,
                    "Col2": value1,
                    "Match_Score": 100,
                    "Match_Status": "Match"
                })
            else:
                best_score = 0
                best_match = None
                for value2 in column2:
                    score = levenshtein(value1, value2)
                    similarity = (1 - score / max(len(value1), len(value2))) * 100
                    if similarity > best_score:
                        best_score = similarity
                        best_match = value2
                results.append({
                    "Col1": value1,
                    "Col2": best_match,
                    "Match_Score": round(best_score, 2),
                    "Match_Status": "Unmatch"
                })

        for value2 in column2:
            if value2 not in [result["Col2"] for result in results if result["Col2"] is not None]:
                results.append({
                    "Col1": None,
                    "Col2": value2,
                    "Match_Score": 0,
                    "Match_Status": "Unmatch"
                })

        return pd.DataFrame(results)

    # Perform matching
    st.header("Matching Results")

    if st.button("Run Matching"):
        # Debugging: Display session state and column names
        st.write("Renamed DHIS2 Columns:", health_facilities_dhis2_list.columns)
        st.write("Renamed MFL Columns:", master_hf_list.columns)

        hf_name_match_results = calculate_match(
            master_hf_list.iloc[:, 0],  # Assuming first column contains names
            health_facilities_dhis2_list.iloc[:, 0]  # Assuming first column contains names
        )

        hf_name_match_results["New_HF_Name_in_MFL"] = np.where(
            hf_name_match_results["Match_Score"] > threshold,
            hf_name_match_results["Col2"],
            hf_name_match_results["Col1"],
        )

        st.write("Matching Results:")
        st.dataframe(hf_name_match_results)

        # Download results
        st.download_button(
            label="Download Matching Results",
            data=hf_name_match_results.to_csv(index=False),
            file_name="matching_results.csv",
            mime="text/csv",
        )
