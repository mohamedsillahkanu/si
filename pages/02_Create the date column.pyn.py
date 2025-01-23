import streamlit as st
import pandas as pd

def process_dataframe_with_integer_month(df, column_to_split, drop_column):
    try:
        month_map = {
            'January': '01', 'February': '02', 'March': '03', 'April': '04',
            'May': '05', 'June': '06', 'July': '07', 'August': '08',
            'September': '09', 'October': '10', 'November': '11', 'December': '12'
        }

        df = df.copy()
        df[['month', 'year']] = df[column_to_split].str.split(' ', expand=True)
        df['month'] = df['month'].map(month_map)
        df['year'] = pd.to_numeric(df['year'], errors='raise')
        df['Date'] = df['year'].astype(str) + '-' + df['month']
        df.drop(columns=[drop_column], inplace=True)
        return df
    except Exception as e:
        st.error(f"Error processing DataFrame: {e}")
        return None

st.title("Date Processor")

if 'combined_df' in st.session_state and st.session_state.combined_df is not None:
    if st.button("Create Date Column"):
        processed_df = process_dataframe_with_integer_month(
            st.session_state.combined_df, 'periodname', 'orgunitlevel5'
        )
        if processed_df is not None:
            st.session_state.processed_df = processed_df.copy()
            st.success("Date column created successfully!")
            st.write("Preview of processed data:")
            st.dataframe(processed_df.head())
            
            csv = processed_df.to_csv(index=False)
            st.download_button(
                label="Download Processed Data",
                data=csv,
                file_name="processed_data.csv",
                mime="text/csv"
            )
else:
    st.warning("Please combine files first in the File Combiner app.")
