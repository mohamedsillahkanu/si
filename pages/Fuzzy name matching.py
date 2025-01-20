import streamlit as st
import pandas as pd
from rapidfuzz import fuzz, process

# Streamlit UI
def main():
    st.title("Interactive Data Processing and Matching Tool")

    # File upload
    st.subheader("Upload Files")
    dhis2_file = st.file_uploader("Upload the DHIS2 file (Excel or CSV):", type=["xlsx", "xls", "csv"])
    mfl_file = st.file_uploader("Upload the MFL file (Excel or CSV):", type=["xlsx", "xls", "csv"])

    if dhis2_file and mfl_file:
        # Load data
        if dhis2_file.name.endswith(('xlsx', 'xls')):
            dhis2_df = pd.read_excel(dhis2_file)
        else:
            dhis2_df = pd.read_csv(dhis2_file)

        if mfl_file.name.endswith(('xlsx', 'xls')):
            mfl_df = pd.read_excel(mfl_file)
        else:
            mfl_df = pd.read_csv(mfl_file)

        # Display initial previews
        st.subheader("Preview of Uploaded Data")
        st.write("### DHIS2 Data:")
        st.dataframe(dhis2_df)

        st.write("### MFL Data:")
        st.dataframe(mfl_df)

        # Allow renaming columns
        st.subheader("Column Management")
        st.write("#### Rename Columns")
        dhis2_rename_cols = {
            col: st.text_input(f"Rename column '{col}' in DHIS2:", value=col) for col in dhis2_df.columns
        }
        mfl_rename_cols = {
            col: st.text_input(f"Rename column '{col}' in MFL:", value=col) for col in mfl_df.columns
        }

        dhis2_df.rename(columns=dhis2_rename_cols, inplace=True)
        mfl_df.rename(columns=mfl_rename_cols, inplace=True)

        # Allow column reordering
        st.write("#### Reorder Columns")
        dhis2_order_cols = st.multiselect("Reorder DHIS2 Columns:", options=dhis2_df.columns, default=dhis2_df.columns)
        mfl_order_cols = st.multiselect("Reorder MFL Columns:", options=mfl_df.columns, default=mfl_df.columns)

        dhis2_df = dhis2_df[dhis2_order_cols]
        mfl_df = mfl_df[mfl_order_cols]

        # Allow column deletion
        st.write("#### Delete Columns")
        dhis2_delete_cols = st.multiselect("Delete Columns from DHIS2:", options=dhis2_df.columns)
        mfl_delete_cols = st.multiselect("Delete Columns from MFL:", options=mfl_df.columns)

        dhis2_df.drop(columns=dhis2_delete_cols, inplace=True)
        mfl_df.drop(columns=mfl_delete_cols, inplace=True)

        # Display processed data
        st.write("### Processed DHIS2 Data:")
        st.dataframe(dhis2_df)
        st.write("### Processed MFL Data:")
        st.dataframe(mfl_df)

        # Column selection for merging
        st.subheader("Matching Settings")
        dhis2_col = st.selectbox("Select the column for DHIS2 health facility names:", dhis2_df.columns)
        mfl_col = st.selectbox("Select the column for MFL health facility names:", mfl_df.columns)

        if st.button("Perform Matching"):
            # Matching function
            def calculate_match(column1, column2):
                results = []

                for value1 in column1:
                    if value1 in column2:
                        results.append({
                            'Col1': value1,
                            'Col2': value1,
                            'Match_Score': 100,
                            'Match_Status': 'Match'
                        })
                    else:
                        matches = process.extract(value1, column2, scorer=fuzz.ratio, limit=1)
                        if matches:
                            best_match, best_score = matches[0]
                            results.append({
                                'Col1': value1,
                                'Col2': best_match,
                                'Match_Score': best_score,
                                'Match_Status': 'Unmatch'
                            })

                for value2 in column2:
                    if value2 not in [result['Col2'] for result in results]:
                        results.append({
                            'Col1': None,
                            'Col2': value2,
                            'Match_Score': 0,
                            'Match_Status': 'Unmatch'
                        })

                return pd.DataFrame(results)

            # Perform matching
            hf_name_match_results = calculate_match(mfl_df[mfl_col], dhis2_df[dhis2_col])

            # Add replacements
            unique_hf_name_results = hf_name_match_results.copy()
            unique_hf_name_results.rename(columns={"Col1": "HF_Name_in_MFL", "Col2": "HF_Name_in_DHIS2"}, inplace=True)
            threshold = st.slider("Set Match Score Threshold:", 0, 100, 70)

            unique_hf_name_results['New_HF_Name_in_MFL'] = unique_hf_name_results.apply(
                lambda row: row['HF_Name_in_DHIS2'] if row['Match_Score'] > threshold else row['HF_Name_in_MFL'], axis=1
            )

            # Display results
            st.write("### Matching Results")
            st.dataframe(unique_hf_name_results)

            # Save results
            output_file = st.text_input("Enter the filename for the results (e.g., results.xlsx):", "unique_hf_name_results_with_replacements.xlsx")

            if st.button("Save Results"):
                unique_hf_name_results.to_excel(output_file, index=False)
                st.success(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
