import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz, process
import openpyxl
import matplotlib.pyplot as plt

# Define matching function
def calculate_match(column1, column2, threshold):
    results = []
    for value1 in column1:
        if value1 in column2.values:
            results.append((value1, value1, 100, "Match"))
        else:
            best_match, best_score = process.extractOne(value1, column2.values, scorer=fuzz.token_set_ratio)
            match_status = "Replace" if best_score >= threshold else "Manual"
            results.append((value1, best_match, best_score, match_status))
    return pd.DataFrame(results, columns=["Col1_MFL", "Col2_DHIS2", "Match_Score", "Match_Status"])

# Streamlit app setup
st.title("Health Facility Matching and Replacement Tool")

# Upload datasets
st.header("Upload Datasets")
master_file = st.file_uploader("Upload Master HF List (Excel)", type=["xlsx"], key="master")
dhis2_file = st.file_uploader("Upload DHIS2 HF List (Excel)", type=["xlsx"], key="dhis2")

if "master_hf_list" not in st.session_state:
    st.session_state.master_hf_list = None
if "health_facilities_dhis2_list" not in st.session_state:
    st.session_state.health_facilities_dhis2_list = None

if master_file:
    if st.session_state.master_hf_list is None:
        st.session_state.master_hf_list = pd.read_excel(master_file)

if dhis2_file:
    if st.session_state.health_facilities_dhis2_list is None:
        st.session_state.health_facilities_dhis2_list = pd.read_excel(dhis2_file)

if st.session_state.master_hf_list is not None and st.session_state.health_facilities_dhis2_list is not None:
    master_hf_list = st.session_state.master_hf_list
    health_facilities_dhis2_list = st.session_state.health_facilities_dhis2_list

    # Column selection and threshold
    st.header("Matching Options")
    column1 = st.selectbox("Select Column from Master HF List", master_hf_list.columns, key="master_column")
    column2 = st.selectbox("Select Column from DHIS2 HF List", health_facilities_dhis2_list.columns, key="dhis2_column")
    match_threshold = st.slider("Set Match Threshold (0-100)", min_value=0, max_value=100, value=85)

    if st.button("Perform Matching"):
        # Perform matching
        matching_results = calculate_match(master_hf_list[column1], health_facilities_dhis2_list[column2], match_threshold)

        # Allow user to confirm replacements
        st.subheader("Matching Results")
        for index, row in matching_results.iterrows():
            if row["Match_Status"] == "Replace":
                master_hf_list.loc[master_hf_list[column1] == row["Col1_MFL"], column1] = row["Col2_DHIS2"]
            else:
                user_input = st.text_input(
                    f"Manual Replacement for {row['Col1_MFL']} (Matched: {row['Match_Score']}%)",
                    value=row["Col2_DHIS2"],
                    key=f"manual_replace_{index}"
                )
                if user_input:
                    master_hf_list.loc[master_hf_list[column1] == row["Col1_MFL"], column1] = user_input

        # Save updated DataFrame
        st.session_state.master_hf_list = master_hf_list

        # Display updated DataFrame
        st.subheader("Updated Master HF List")
        st.dataframe(master_hf_list)

        # Option to download updated DataFrame
        st.subheader("Download Updated Master HF List")
        output_file = "updated_master_hf_list.xlsx"
        master_hf_list.to_excel(output_file, index=False)
        with open(output_file, "rb") as file:
            st.download_button(label="Download Excel File", data=file, file_name=output_file, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
