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
        st.session_state.renamed_dhis2_col = None

    if "renamed_mfl_col" not in st.session_state:
        st.session_state.renamed_mfl_col = None

    # Display data
    st.subheader("Preview of Uploaded Files")
    st.write("DHIS2 File:")
    st.dataframe(health_facilities_dhis2_list.head())
    st.write("MFL File:")
    st.dataframe(master_hf_list.head())

    # Column selection and renaming
    st.header("Select and Rename Columns")
    dhis2_col = st.selectbox("Select DHIS2 Name Column", health_facilities_dhis2_list.columns, key="dhis2_col")
    mfl_col = st.selectbox("Select MFL Name Column", master_hf_list.columns, key="mfl_col")

    # Update renamed column names in session state
    new_dhis2_col = st.text_input("Rename DHIS2 Column", value=st.session_state.renamed_dhis2_col or dhis2_col)
    new_mfl_col = st.text_input("Rename MFL Column", value=st.session_state.renamed_mfl_col or mfl_col)

    if st.button("Apply Renaming"):
        # Save renamed column names in session state
        st.session_state.renamed_dhis2_col = new_dhis2_col
        st.session_state.renamed_mfl_col = new_mfl_col

        # Rename columns in the DataFrame
        health_facilities_dhis2_list.rename(columns={dhis2_col: new_dhis2_col}, inplace=True)
        master_hf_list.rename(columns={mfl_col: new_mfl_col}, inplace=True)

        # Save renamed DataFrames back to session state
        st.session_state.health_facilities_dhis2_list = health_facilities_dhis2_list.copy()
        st.session_state.master_hf_list = master_hf_list.copy()

        st.success("Column names updated and saved in both original and renamed DataFrames!")

    # Use renamed columns in operations
    if "health_facilities_dhis2_list" in st.session_state:
        st.write("Renamed DHIS2 File:")
        st.dataframe(st.session_state.health_facilities_dhis2_list.head())
    if "master_hf_list" in st.session_state:
        st.write("Renamed MFL File:")
        st.dataframe(st.session_state.master_hf_list.head())

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
        st.write("Session State Renamed DHIS2 Column:", st.session_state.renamed_dhis2_col)
        st.write("Session State Renamed MFL Column:", st.session_state.renamed_mfl_col)
        st.write("DHIS2 Columns:", st.session_state.health_facilities_dhis2_list.columns)
        st.write("MFL Columns:", st.session_state.master_hf_list.columns)

        # Check if renamed columns exist in the DataFrame
        if (
            st.session_state.renamed_dhis2_col in st.session_state.health_facilities_dhis2_list.columns
            and st.session_state.renamed_mfl_col in st.session_state.master_hf_list.columns
        ):
            hf_name_match_results = calculate_match(
                st.session_state.master_hf_list[st.session_state.renamed_mfl_col],
                st.session_state.health_facilities_dhis2_list[st.session_state.renamed_dhis2_col],
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
            st.error("Renamed columns not found in the DataFrame. Please ensure renaming is applied.")
