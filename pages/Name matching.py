import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz, process
import openpyxl
import matplotlib.pyplot as plt

# Define matching function
def calculate_match(column1, column2, threshold):
    results = []
    for value1 in column1:
        best_match, best_score = process.extractOne(value1, column2.values, scorer=fuzz.token_set_ratio)
        match_status = "Match" if best_score >= threshold else "Unmatch"
        new_name = best_match if match_status == "Match" else value1
        results.append((value1, best_match, best_score, match_status, new_name))
    return pd.DataFrame(results, columns=["HF_in_MFL", "HF_in_DHIS2", "Match_Score", "Match_Status", "new_MFL_name"])

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

        # Update Master HF List with new_MFL_name
        master_hf_list["new_MFL_name"] = matching_results["new_MFL_name"]
        st.session_state.master_hf_list = master_hf_list

        # Display matching results
        st.subheader("Matching Results with new_MFL_name")
        st.dataframe(matching_results)

        # Display updated Master HF List
        st.subheader("Updated Master HF List with new_MFL_name")
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
                master_hf_list["new_MFL_name"],
                health_facilities_dhis2_list[column2]
            ]).unique()
        })

        classified_results = all_unique_names.copy()
        classified_results["Classification"] = classified_results["Health_Facility_Name"].apply(
            lambda x: "HF in both DHIS2 and MFL" if x in master_hf_list["new_MFL_name"].values and x in health_facilities_dhis2_list[column2].values
            else "HF in MFL and not in DHIS2" if x in master_hf_list["new_MFL_name"].values
            else "HF in DHIS2 and not in MFL" if x in health_facilities_dhis2_list[column2].values
            else "Unclassified"
        )

        # Display classification results
        st.subheader("Health Facility Classification Results (Tabular)")
        st.dataframe(classified_results)

        # Create summary counts and percentages
        summary = classified_results["Classification"].value_counts().reset_index()
        summary.columns = ["Classification", "Count"]
        summary["Percentage"] = (summary["Count"] / summary["Count"].sum()) * 100

        st.subheader("Summary of Classification")
        st.dataframe(summary)

        # Count bar chart
        st.subheader("Count Bar Chart of Classification Results")
        fig_count, ax_count = plt.subplots()
        summary.plot(kind="bar", x="Classification", y="Count", ax=ax_count)
        plt.title("Count of Classification Results")
        plt.ylabel("Count")
        st.pyplot(fig_count)

        # Percentage bar chart
        st.subheader("Percentage Bar Chart of Classification Results")
        fig_percentage, ax_percentage = plt.subplots()
        summary.plot(kind="bar", x="Classification", y="Percentage", ax=ax_percentage)
        plt.title("Percentage of Classification Results")
        plt.ylabel("Percentage")
        st.pyplot(fig_percentage)

        # Option to download classification results
        st.subheader("Download Classification Results")
        output_file_classification = "classification_results.xlsx"
        classified_results.to_excel(output_file_classification, index=False)
        with open(output_file_classification, "rb") as file:
            st.download_button(label="Download Excel File", data=file, file_name=output_file_classification, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
