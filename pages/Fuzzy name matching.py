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

        # Store data in session state
        if 'df' not in st.session_state:
            st.session_state.df = dhis2_df

        # Display initial previews
        st.subheader("Preview of Uploaded Data")
        st.write("### DHIS2 Data:")
        st.dataframe(dhis2_df)

        st.write("### MFL Data:")
        st.dataframe(mfl_df)

        # Cleaning Options
        st.subheader("Data Cleaning Options")
        cleaning_option = st.selectbox("Choose a cleaning option:", ["None", "Recode Variables", "Delete Column", "Sort Columns"])

        if cleaning_option == "Recode Variables":
            if st.session_state.df is not None:
                recode_option = st.selectbox("Choose recoding option:", ["Recode a Column", "Recode Values in a Column"])

                if recode_option == "Recode a Column":
                    st.write("Recode a Column:")
                    column = st.selectbox("Select column to recode", st.session_state.df.columns)
                    new_name = st.text_input("New name for the selected column")
                    if st.button("Recode"):
                        if new_name:
                            st.session_state.df.rename(columns={column: new_name}, inplace=True)
                            st.write("Column name updated:")
                            st.dataframe(st.session_state.df)
                        else:
                            st.error("Please enter a new column name.")

                elif recode_option == "Recode Values in a Column":
                    st.write("Recode Values in a Column:")
                    column = st.selectbox("Select column to recode", st.session_state.df.columns)
                    old_values = st.text_input(f"Old values for {column} (comma-separated)", "")
                    new_values = st.text_input(f"New values for {column} (comma-separated)", "")

                    if old_values and new_values:
                        old_values_list = old_values.split(",")
                        new_values_list = new_values.split(",")
                        recode_map = dict(zip(old_values_list, new_values_list))

                        if st.button("Recode"):
                            st.session_state.df[column] = st.session_state.df[column].replace(recode_map)
                            st.write("Recoded Data:")
                            st.dataframe(st.session_state.df)
                        else:
                            st.error("Ensure you provide both old and new values.")

        elif cleaning_option == "Delete Column":
            st.header("Delete Column")
            if st.session_state.df is not None:
                columns_to_delete = st.multiselect("Select columns to delete:", st.session_state.df.columns)

                if st.button("Delete"):
                    if columns_to_delete:
                        st.session_state.df.drop(columns=columns_to_delete, inplace=True)
                        st.success(f"Deleted columns: {', '.join(columns_to_delete)}")
                        st.dataframe(st.session_state.df)
                    else:
                        st.error("Please select at least one column to delete.")

        elif cleaning_option == "Sort Columns":
            st.header("Sort Columns")
            if st.session_state.df is not None:
                st.write("Current Column Order:")
                st.dataframe(st.session_state.df.head())

                new_order = st.multiselect("Rearrange columns by selecting them in the desired order:",
                                           st.session_state.df.columns,
                                           default=list(st.session_state.df.columns))

                if st.button("Rearrange Columns"):
                    if len(new_order) == len(st.session_state.df.columns):
                        st.session_state.df = st.session_state.df[new_order]
                        st.success("Columns rearranged successfully.")
                        st.dataframe(st.session_state.df)
                    else:
                        st.error("Please select all columns to ensure the DataFrame structure is preserved.")

if __name__ == "__main__":
    main()
