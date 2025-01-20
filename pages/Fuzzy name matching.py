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
    if "df_dhis2" not in st.session_state:
        st.session_state.df_dhis2 = health_facilities_dhis2_list

    if "df_mfl" not in st.session_state:
        st.session_state.df_mfl = master_hf_list

    # Display data
    st.subheader("Preview of Uploaded Files")
    st.write("DHIS2 File:")
    st.dataframe(st.session_state.df_dhis2.head())
    st.write("MFL File:")
    st.dataframe(st.session_state.df_mfl.head())

    # Column renaming section
    st.header("Rename Columns")

    rename_option = st.selectbox("Select dataset to rename columns", ["DHIS2", "MFL"])
    if rename_option == "DHIS2":
        st.write("Rename Columns in DHIS2:")
        new_columns = {}
        for col in st.session_state.df_dhis2.columns:
            new_col_name = st.text_input(f"Rename '{col}' in DHIS2", value=col, key=f"rename_dhis2_{col}")
            new_columns[col] = new_col_name
        if st.button("Apply Renaming to DHIS2"):
            st.session_state.df_dhis2.rename(columns=new_columns, inplace=True)
            st.success("Renaming applied to DHIS2 dataset.")
            st.write("Renamed DHIS2 File:")
            st.dataframe(st.session_state.df_dhis2.head())

    elif rename_option == "MFL":
        st.write("Rename Columns in MFL:")
        new_columns = {}
        for col in st.session_state.df_mfl.columns:
            new_col_name = st.text_input(f"Rename '{col}' in MFL", value=col, key=f"rename_mfl_{col}")
            new_columns[col] = new_col_name
        if st.button("Apply Renaming to MFL"):
            st.session_state.df_mfl.rename(columns=new_columns, inplace=True)
            st.success("Renaming applied to MFL dataset.")
            st.write("Renamed MFL File:")
            st.dataframe(st.session_state.df_mfl.head())

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
        st.write("Renamed DHIS2 Columns:", st.session_state.df_dhis2.columns)
        st.write("Renamed MFL Columns:", st.session_state.df_mfl.columns)

        hf_name_match_results = calculate_match(
            st.session_state.df_mfl.iloc[:, 0],  # Assuming first column contains names
            st.session_state.df_dhis2.iloc[:, 0]  # Assuming first column contains names
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
