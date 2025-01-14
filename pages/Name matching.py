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
            match_status = "Match" if best_score >= threshold else "Unmatch"
            results.append((value1, best_match, best_score, match_status))
    return pd.DataFrame(results, columns=["Col1", "Col2", "Match_Score", "Match_Status"])

# Function to rename or recode columns interactively
def handle_recode_and_rename(df, df_name):
    st.header(f"Recode or Rename Columns for {df_name}")
    recode_option = st.selectbox("Choose an option:", ["Rename a Column", "Recode Values in a Column"], key=f"{df_name}_recode_option")

    if recode_option == "Rename a Column":
        column = st.selectbox("Select column to rename", df.columns, key=f"{df_name}_rename_column")
        new_name = st.text_input("New name for the selected column", key=f"{df_name}_new_column_name")
        if st.button("Rename", key=f"{df_name}_rename_button"):
            if new_name:
                df.rename(columns={column: new_name}, inplace=True)
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
                    st.write(f"Values in column '{column}' have been recoded.")
                    st.dataframe(df)
            else:
                st.error("Number of old values and new values must match.")

# Streamlit app setup
st.title("Health Facility Matching and Column Replacement Tool")

# Upload datasets
st.header("Upload Datasets")
master_file = st.file_uploader("Upload Master HF List (Excel)", type=["xlsx"], key="master")
dhis2_file = st.file_uploader("Upload DHIS2 HF List (Excel)", type=["xlsx"], key="dhis2")

if "master_hf_list" not in st.session_state:
    st.session_state.master_hf_list = None
if "health_facilities_dhis2_list" not in st.session_state:
    st.session_state.health_facilities_dhis2_list = None

if master_file:
    st.session_state.master_hf_list = pd.read_excel(master_file)
    handle_recode_and_rename(st.session_state.master_hf_list, "Master HF List")

if dhis2_file:
    st.session_state.health_facilities_dhis2_list = pd.read_excel(dhis2_file)
    handle_recode_and_rename(st.session_state.health_facilities_dhis2_list, "DHIS2 HF List")

if st.session_state.master_hf_list is not None and st.session_state.health_facilities_dhis2_list is not None:
    # Column selection and threshold
    st.header("Matching Options")
    column1 = st.selectbox("Select Column from Master HF List", st.session_state.master_hf_list.columns, key="master_column")
    column2 = st.selectbox("Select Column from DHIS2 HF List", st.session_state.health_facilities_dhis2_list.columns, key="dhis2_column")
    match_threshold = st.slider("Set Match Threshold (0-100)", min_value=0, max_value=100, value=90)

    if st.button("Perform Matching"):
        # Perform matching
        matching_results = calculate_match(st.session_state.master_hf_list[column1], st.session_state.health_facilities_dhis2_list[column2], match_threshold)

        # Display results
        st.subheader("Matching Results")
        st.dataframe(matching_results)

        # Column replacement logic
        st.subheader("Column Replacement Options")
        replacement_results = matching_results.copy()
        replacement_results["Replacement_Column"] = replacement_results.apply(
            lambda row: row["Col1"] if row["Match_Status"] == "Match" else row["Col2"], axis=1
        )

        # Display replacement results
        st.write("Replacement Results")
        st.dataframe(replacement_results)

        # Option to download results
        st.subheader("Download Results")
        output_file = "matching_and_replacement_results.xlsx"
        replacement_results.to_excel(output_file, index=False)
        with open(output_file, "rb") as file:
            st.download_button(label="Download Excel File", data=file, file_name=output_file, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Classification logic
    if st.button("Classify Health Facilities"):
        all_unique_names = pd.DataFrame({
            "Health_Facility_Name": pd.concat([
                st.session_state.master_hf_list[column1],
                st.session_state.health_facilities_dhis2_list[column2]
            ]).unique()
        })

        classified_results = all_unique_names.copy()
        classified_results["Classification"] = classified_results["Health_Facility_Name"].apply(
            lambda x: "HF in both DHIS2 and MFL" if x in st.session_state.master_hf_list[column1].values and x in st.session_state.health_facilities_dhis2_list[column2].values
            else "HF in MFL and not in DHIS2" if x in st.session_state.master_hf_list[column1].values
            else "HF in DHIS2 and not in MFL" if x in st.session_state.health_facilities_dhis2_list[column2].values
            else "Unclassified"
        )

        # Display classification results
        st.subheader("Health Facility Classification Results")
        st.dataframe(classified_results)

        # Bar chart for classification
        st.subheader("Classification Summary")
        classification_counts = classified_results["Classification"].value_counts()
        fig, ax = plt.subplots()
        classification_counts.plot(kind="bar", ax=ax, color="skyblue")
        ax.set_title("Classification Summary")
        ax.set_xlabel("Classification")
        ax.set_ylabel("Count")
        st.pyplot(fig)

        # Option to download classification results
        output_file_classification = "classification_results.xlsx"
        classified_results.to_excel(output_file_classification, index=False)
        with open(output_file_classification, "rb") as file:
            st.download_button(label="Download Excel File", data=file, file_name=output_file_classification, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
