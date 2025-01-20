import streamlit as st
import pandas as pd
import numpy as np
from stringdist import levenshtein

# Initialize session state for dataframes
if 'dhis2_df' not in st.session_state:
    st.session_state.dhis2_df = None
if 'mfl_df' not in st.session_state:
    st.session_state.mfl_df = None

# Streamlit app
st.title("Health Facility Name Matching")

# File upload
st.header("Upload Your Files")
uploaded_file_dhis2 = st.file_uploader("Upload DHIS2 File (CSV, XLS, XLSX)", type=["csv", "xls", "xlsx"])
uploaded_file_mfl = st.file_uploader("Upload MFL File (CSV, XLS, XLSX)", type=["csv", "xls", "xlsx"])

if uploaded_file_dhis2 and uploaded_file_mfl:
    # Read the uploaded files
    try:
        if st.session_state.dhis2_df is None:
            if uploaded_file_dhis2.name.endswith(".csv"):
                st.session_state.dhis2_df = pd.read_csv(uploaded_file_dhis2)
            else:
                st.session_state.dhis2_df = pd.read_excel(uploaded_file_dhis2)

        if st.session_state.mfl_df is None:
            if uploaded_file_mfl.name.endswith(".csv"):
                st.session_state.mfl_df = pd.read_csv(uploaded_file_mfl)
            else:
                st.session_state.mfl_df = pd.read_excel(uploaded_file_mfl)

        st.success("Files uploaded successfully!")
    except Exception as e:
        st.error(f"Error reading files: {e}")
        st.stop()

    # Display data
    st.subheader("Preview of Uploaded Files")
    st.write("DHIS2 File:")
    st.dataframe(st.session_state.dhis2_df.head())
    st.write("MFL File:")
    st.dataframe(st.session_state.mfl_df.head())

    # Column renaming section
    st.header("Rename Columns")

    rename_option = st.selectbox("Select dataset to rename columns", ["DHIS2", "MFL"])
    
    if rename_option == "DHIS2":
        st.write("Rename Columns in DHIS2:")
        new_column_names = {}
        for col in st.session_state.dhis2_df.columns:
            new_col_name = st.text_input(f"Rename '{col}' in DHIS2", value=col, key=f"rename_dhis2_{col}")
            new_column_names[col] = new_col_name
            
        if st.button("Apply Renaming to DHIS2"):
            st.session_state.dhis2_df = st.session_state.dhis2_df.rename(columns=new_column_names)
            st.success("Renaming applied to DHIS2 dataset.")
            st.write("Renamed DHIS2 File:")
            st.dataframe(st.session_state.dhis2_df.head())

    elif rename_option == "MFL":
        st.write("Rename Columns in MFL:")
        new_column_names = {}
        for col in st.session_state.mfl_df.columns:
            new_col_name = st.text_input(f"Rename '{col}' in MFL", value=col, key=f"rename_mfl_{col}")
            new_column_names[col] = new_col_name
            
        if st.button("Apply Renaming to MFL"):
            st.session_state.mfl_df = st.session_state.mfl_df.rename(columns=new_column_names)
            st.success("Renaming applied to MFL dataset.")
            st.write("Renamed MFL File:")
            st.dataframe(st.session_state.mfl_df.head())

    # Matching threshold
    st.header("Set Matching Threshold")
    threshold = st.slider("Set Matching Threshold (0 to 100)", min_value=0, max_value=100, value=70, step=1)

    # Matching function
    def calculate_match(column1, column2):
        results = []

        for value1 in column1:
            if pd.isna(value1):
                continue
                
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
                    if pd.isna(value2):
                        continue
                    score = levenshtein(str(value1), str(value2))
                    similarity = (1 - score / max(len(str(value1)), len(str(value2)))) * 100
                    if similarity > best_score:
                        best_score = similarity
                        best_match = value2
                results.append({
                    "Col1": value1,
                    "Col2": best_match,
                    "Match_Score": round(best_score, 2),
                    "Match_Status": "Unmatch" if best_score <= threshold else "Match"
                })

        for value2 in column2:
            if pd.isna(value2):
                continue
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
        if st.session_state.dhis2_df is not None and st.session_state.mfl_df is not None:
            # Allow user to select columns for matching
            st.write("Select columns for matching:")
            mfl_col = st.selectbox("Select MFL column", st.session_state.mfl_df.columns)
            dhis2_col = st.selectbox("Select DHIS2 column", st.session_state.dhis2_df.columns)
            
            hf_name_match_results = calculate_match(
                st.session_state.mfl_df[mfl_col],
                st.session_state.dhis2_df[dhis2_col]
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
        else:
            st.error("Please upload both files first")
