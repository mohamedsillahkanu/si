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

# Function to rename columns interactively
def rename_columns_interactively(df, df_name):
    st.header(f"Rename Columns for {df_name}")
    renamed_columns = {}
    for col in df.columns:
        new_name = st.text_input(f"Rename column '{col}'", col, key=f"{df_name}_{col}")
        renamed_columns[col] = new_name
    df.rename(columns=renamed_columns, inplace=True)
    st.write(f"Updated {df_name}:")
    st.dataframe(df)
    return df

# Streamlit app setup
st.title("Health Facility Matching and Column Replacement Tool")

# Upload datasets
st.header("Upload Datasets")
master_file = st.file_uploader("Upload Master HF List (Excel)", type=["xlsx"], key="master")
dhis2_file = st.file_uploader("Upload DHIS2 HF List (Excel)", type=["xlsx"], key="dhis2")

master_hf_list = None
health_facilities_dhis2_list = None

if master_file:
    master_hf_list = pd.read_excel(master_file)
    master_hf_list = rename_columns_interactively(master_hf_list, "Master HF List")

if dhis2_file:
    health_facilities_dhis2_list = pd.read_excel(dhis2_file)
    health_facilities_dhis2_list = rename_columns_interactively(health_facilities_dhis2_list, "DHIS2 HF List")

if master_hf_list is not None and health_facilities_dhis2_list is not None:
    # Column selection and threshold
    st.header("Matching Options")
    column1 = st.selectbox("Select Column from Master HF List", master_hf_list.columns, key="master_column")
    column2 = st.selectbox("Select Column from DHIS2 HF List", health_facilities_dhis2_list.columns, key="dhis2_column")
    match_threshold = st.slider("Set Match Threshold (0-100)", min_value=0, max_value=100, value=90)

    if st.button("Perform Matching"):
        # Perform matching
        matching_results = calculate_match(master_hf_list[column1], health_facilities_dhis2_list[column2], match_threshold)

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
