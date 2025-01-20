import streamlit as st
import pandas as pd
import numpy as np
from Levenshtein import distance as levenshtein_distance

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

    # Column selection for matching
    st.header("Select Columns for Matching")
    if st.session_state.mfl_df is not None and st.session_state.dhis2_df is not None:
        mfl_col = st.selectbox("Select MFL column", st.session_state.mfl_df.columns)
        dhis2_col = st.selectbox("Select DHIS2 column", st.session_state.dhis2_df.columns)
    
    # Matching threshold
    st.header("Set Matching Threshold")
    threshold = st.slider("Set Matching Threshold (0 to 100)", min_value=0, max_value=100, value=70, step=1)

    # Matching function
    def calculate_match(column1, column2):
        results = []
        
        # Convert series to lists and handle NaN values
        col1_values = [str(x) for x in column1.fillna('').tolist()]
        col2_values = [str(x) for x in column2.fillna('').tolist()]

        for value1 in col1_values:
            if value1 == '':
                continue
                
            if value1 in col2_values:
                results.append({
                    "Col1": value1,
                    "Col2": value1,
                    "Match_Score": 100,
                    "Match_Status": "Match"
                })
            else:
                best_score = 0
                best_match = None
                
                for value2 in col2_values:
                    if value2 == '':
                        continue
                        
                    max_len = max(len(value1), len(value2))
                    if max_len == 0:
                        similarity = 0
                    else:
                        # Calculate similarity score
                        distance = levenshtein_distance(value1, value2)
                        similarity = (1 - distance / max_len) * 100
                        
                    if similarity > best_score:
                        best_score = similarity
                        best_match = value2
                
                match_status = "Match" if best_score > threshold else "Unmatch"
                results.append({
                    "Col1": value1,
                    "Col2": best_match,
                    "Match_Score": round(best_score, 2),
                    "Match_Status": match_status
                })

        # Add remaining unmatched values from column2
        matched_col2_values = {r["Col2"] for r in results if r["Col2"] is not None}
        unmatched_col2 = set(col2_values) - matched_col2_values
        
        for value2 in unmatched_col2:
            if value2 and value2 != '':
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
        try:
            with st.spinner('Performing matching...'):
                hf_name_match_results = calculate_match(
                    st.session_state.mfl_df[mfl_col],
                    st.session_state.dhis2_df[dhis2_col]
                )

                hf_name_match_results["New_HF_Name_in_MFL"] = np.where(
                    hf_name_match_results["Match_Score"] > threshold,
                    hf_name_match_results["Col2"],
                    hf_name_match_results["Col1"]
                )

                st.write("Matching Results:")
                st.dataframe(hf_name_match_results)

                # Download results
                st.download_button(
                    label="Download Matching Results",
                    data=hf_name_match_results.to_csv(index=False),
                    file_name="matching_results.csv",
                    mime="text/csv"
                )
        except Exception as e:
            st.error(f"An error occurred during matching: {str(e)}")
