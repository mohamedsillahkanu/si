import streamlit as st
import pandas as pd
import numpy as np
from jellyfish import jaro_winkler_similarity
from io import BytesIO

def calculate_match(column1, column2, threshold):
    """Calculate matching scores between two columns using Jaro-Winkler similarity."""
    results = []
    
    for value1 in column1:
        if value1 in column2.values:
            results.append({
                'Col1': value1,
                'Col2': value1,
                'Match_Score': 100,
                'Match_Status': 'Match'
            })
        else:
            best_score = 0
            best_match = None
            for value2 in column2:
                similarity = jaro_winkler_similarity(str(value1), str(value2)) * 100
                if similarity > best_score:
                    best_score = similarity
                    best_match = value2
            results.append({
                'Col1': value1,
                'Col2': best_match,
                'Match_Score': round(best_score, 2),
                'Match_Status': 'Unmatch' if best_score < threshold else 'Match'
            })
    
    for value2 in column2:
        if value2 not in [r['Col2'] for r in results]:
            results.append({
                'Col1': None,
                'Col2': value2,
                'Match_Score': 0,
                'Match_Status': 'Unmatch'
            })
    
    return pd.DataFrame(results)

def main():
    st.title("Health Facility Name Matching")

    # File upload
    st.sidebar.header("Upload Files")
    mfl_file = st.sidebar.file_uploader("Upload Master HF List (CSV, Excel):", type=['csv', 'xlsx', 'xls'])
    dhis2_file = st.sidebar.file_uploader("Upload DHIS2 HF List (CSV, Excel):", type=['csv', 'xlsx', 'xls'])

    if mfl_file and dhis2_file:
        # Read files
        try:
            if mfl_file.name.endswith('.csv'):
                master_hf_list = pd.read_csv(mfl_file)
            else:
                master_hf_list = pd.read_excel(mfl_file)

            if dhis2_file.name.endswith('.csv'):
                health_facilities_dhis2_list = pd.read_csv(dhis2_file)
            else:
                health_facilities_dhis2_list = pd.read_excel(dhis2_file)

            # Display the DataFrames
            st.write("### Master HF List")
            st.dataframe(master_hf_list)

            st.write("### DHIS2 HF List")
            st.dataframe(health_facilities_dhis2_list)

            # User selects columns for matching
            st.sidebar.header("Column Selection")
            mfl_col = st.sidebar.selectbox("Select HF Name column in Master HF List:", master_hf_list.columns)
            dhis2_col = st.sidebar.selectbox("Select HF Name column in DHIS2 HF List:", health_facilities_dhis2_list.columns)

            # Set matching threshold
            st.sidebar.header("Settings")
            threshold = st.sidebar.slider("Set Match Threshold (0-100):", min_value=0, max_value=100, value=70)

            # Process data
            master_hf_list[mfl_col] = master_hf_list[mfl_col].astype(str).drop_duplicates()
            health_facilities_dhis2_list[dhis2_col] = health_facilities_dhis2_list[dhis2_col].astype(str)

            st.write("### Counts of Health Facilities")
            st.write(f"Count of HFs in DHIS2 list: {len(health_facilities_dhis2_list)}")
            st.write(f"Count of HFs in MFL list: {len(master_hf_list)}")

            # Perform matching
            hf_name_match_results = calculate_match(
                master_hf_list[mfl_col],
                health_facilities_dhis2_list[dhis2_col],
                threshold
            )

            # Rename columns and add new column for replacements
            hf_name_match_results = hf_name_match_results.rename(
                columns={'Col1': 'HF_Name_in_MFL', 'Col2': 'HF_Name_in_DHIS2'}
            )
            hf_name_match_results['New_HF_Name_in_MFL'] = np.where(
                hf_name_match_results['Match_Score'] >= threshold,
                hf_name_match_results['HF_Name_in_DHIS2'],
                hf_name_match_results['HF_Name_in_MFL']
            )

            # Display results
            st.write("### Matching Results")
            st.dataframe(hf_name_match_results)

            # Download results
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                hf_name_match_results.to_excel(writer, index=False)
            output.seek(0)

            st.download_button(
                label="Download Matching Results as Excel",
                data=output,
                file_name="hf_name_matching_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"An error occurred while processing the files: {e}")

if __name__ == "__main__":
    main()
