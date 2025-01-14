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
            results.append((value1, value1, 100, "Replace"))
        else:
            best_match, best_score = process.extractOne(value1, column2.values, scorer=fuzz.token_set_ratio)
            match_status = "Match" if best_score >= threshold else "No Match"
            results.append((value1, best_match, best_score, match_status))
    return pd.DataFrame(results, columns=["Col1_MFL", "Col2_DHIS2", "Match_Score", "Match_Status"])

# Function to rename or recode columns interactively
def handle_recode_and_rename(df_name):
    df = st.session_state[df_name]
    st.header(f"Recode or Rename Columns for {df_name}")
    recode_option = st.selectbox("Choose an option:", ["Rename a Column", "Recode Values in a Column"], key=f"{df_name}_recode_option")

    if recode_option == "Rename a Column":
        column = st.selectbox("Select column to rename", df.columns, key=f"{df_name}_rename_column")
        new_name = st.text_input("New name for the selected column", key=f"{df_name}_new_column_name")
        if st.button("Rename", key=f"{df_name}_rename_button"):
            if new_name:
                df.rename(columns={column: new_name}, inplace=True)
                st.session_state[df_name] = df  # Save changes to session state
                st.write(f"Column '{column}' renamed to '{new_name}'.")
                st.dataframe(df)
            else:
                st.error("Please enter a new column name.")

    elif recode_option == "Recode Values in a Column":
        column = st.selectbox("Select column to recode", df.columns, key=f"{df_name}_recode_column")
        old_values = st.text_input(f"Old values for {column} (comma-separated)", key=f"{df_name}_old_values")
        new_values = st.text_input(f"New values for {column} (comma-separated)", key=f"{df_name}_new_values")

        if old_values and new_values:
            old_values_list = old_values.split(",")
            new_values_list = new_values.split(",")

            if len(old_values_list) == len(new_values_list):
                recode_map = dict(zip(old_values_list, new_values_list))

                if st.button("Recode", key=f"{df_name}_recode_button"):
                    df[column] = df[column].replace(recode_map)
                    st.session_state[df_name] = df  # Save changes to session state
                    st.write(f"Values in column '{column}' have been recoded.")
                    st.dataframe(df)
            else:
                st.error("Number of old values and new values must match.")

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
    handle_recode_and_rename("master_hf_list")

if dhis2_file:
    if st.session_state.health_facilities_dhis2_list is None:
        st.session_state.health_facilities_dhis2_list = pd.read_excel(dhis2_file)
    handle_recode_and_rename("health_facilities_dhis2_list")

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

        # Add replacement column
        matching_results["Replacement_Column"] = matching_results.apply(
            lambda row: row["Col2_DHIS2"] if row["Match_Status"] == "Replace" else row["Col1_MFL"], axis=1
        )

        # Update Master HF List
        for index, row in matching_results.iterrows():
            if row["Match_Status"] == "Replace":
                master_hf_list.loc[master_hf_list[column1] == row["Col1_MFL"], column1] = row["Replacement_Column"]

        # Save updated DataFrame
        st.session_state.master_hf_list = master_hf_list

        # Display matching results
        st.subheader("Matching Results with Replacement")
        st.dataframe(matching_results)

        # Display updated Master HF List
        st.subheader("Updated Master HF List")
        st.dataframe(master_hf_list)

        # Option to download updated DataFrame
        st.subheader("Download Updated Master HF List")
        output_file = "updated_master_hf_list.xlsx"
        master_hf_list.to_excel(output_file, index=False)
        with open(output_file, "rb") as file:
            st.download_button(label="Download Excel File", data=file, file_name=output_file, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Classification logic
    if st.button("Classify Health Facilities"):
        all_unique_names = pd.DataFrame({
            "Health_Facility_Name": pd.concat([
                master_hf_list[column1],
                health_facilities_dhis2_list[column2]
            ]).unique()
        })

        classified_results = all_unique_names.copy()
        classified_results["Classification"] = classified_results["Health_Facility_Name"].apply(
            lambda x: "HF in both DHIS2 and MFL" if x in master_hf_list[column1].values and x in health_facilities_dhis2_list[column2].values
            else "HF in MFL and not in DHIS2" if x in master_hf_list[column1].values
            else "HF in DHIS2 and not in MFL" if x in health_facilities_dhis2_list[column2].values
            else "Unclassified"
        )

        # Display classification results
        st.subheader("Health Facility Classification Results (Tabular)")
        st.dataframe(classified_results)

        # Option to download classification results
        st.subheader("Download Classification Results")
        output_file_classification = "classification_results.xlsx"
        classified_results.to_excel(output_file_classification, index=False)
        with open(output_file_classification, "rb") as file:
            st.download_button(label="Download Excel File", data=file, file_name=output_file_classification, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
