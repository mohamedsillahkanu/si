import streamlit as st
import pandas as pd

def read_file(file):
    file_type = file.name.split('.')[-1].lower()
    try:
        if file_type == 'csv':
            return pd.read_csv(file)
        elif file_type in ['xlsx', 'xls']:
            return pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_type}")
            return None
    except Exception as e:
        st.error(f"Error reading file {file.name}: {str(e)}")
        return None

def validate_and_combine_files(files):
    if not files:
        return None

    dfs = []
    reference_df = read_file(files[0])
    
    if reference_df is None:
        return None
        
    reference_columns = list(reference_df.columns)
    dfs.append(reference_df)
    
    for file in files[1:]:
        df = read_file(file)
        if df is None:
            continue
            
        if list(df.columns) != reference_columns:
            st.error(f"Column mismatch in {file.name}")
            st.write("Expected columns:", reference_columns)
            st.write("Found columns:", list(df.columns))
            st.write("Missing columns:", set(reference_columns) - set(df.columns))
            st.write("Extra columns:", set(df.columns) - set(reference_columns))
            return None
            
        dfs.append(df)
    
    return pd.concat(dfs, ignore_index=True)

if 'combined_df' not in st.session_state:
    st.session_state.combined_df = None

st.title("File Combiner")
uploaded_files = st.file_uploader("Upload files", type=['xlsx', 'xls', 'csv'], accept_multiple_files=True)

if uploaded_files:
    combined_df = validate_and_combine_files(uploaded_files)
    
    if combined_df is not None:
        st.session_state.combined_df = combined_df.copy()
        st.success("Files successfully combined!")
        st.write("Preview of combined data:")
        st.dataframe(st.session_state.combined_df.head())
        
        csv = st.session_state.combined_df.to_csv(index=False)
        st.download_button(
            label="Download Combined Data",
            data=csv,
            file_name="combined_data.csv",
            mime="text/csv"
        )
