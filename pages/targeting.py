import streamlit as st
import pandas as pd
import numpy as np
import base64
from io import BytesIO

st.set_page_config(page_title="Multi-Dataset Merger", layout="wide")

def read_file(file):
    """Read uploaded file into a dataframe."""
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith(('.xlsx', '.xls')):
        return pd.read_excel(file)
    else:
        st.error(f"Unsupported file format: {file.name}")
        return None

def apply_condition(df, condition):
    """Apply a single condition and return a boolean Series"""
    col = condition["source_column"]
    op = condition["operator"]
    val = condition["value"]
    
    # Try to convert value to numeric if column is numeric
    if pd.api.types.is_numeric_dtype(df[col]) and val.replace('.', '', 1).isdigit():
        val = float(val)
    
    # Apply condition based on operator
    if op == "equals":
        return df[col] == val
    elif op == "not equals":
        return df[col] != val
    elif op == "greater than":
        return df[col] > val
    elif op == "less than":
        return df[col] < val
    elif op == "contains":
        return df[col].astype(str).str.contains(str(val), na=False)
    elif op == "does not contain":
        return ~df[col].astype(str).str.contains(str(val), na=False)
    elif op == "is null":
        return df[col].isna()
    elif op == "is not null":
        return ~df[col].isna()
    
    return pd.Series([False] * len(df))

# Initialize session state
if 'datasets' not in st.session_state:
    st.session_state.datasets = {}
if 'merged_df' not in st.session_state:
    st.session_state.merged_df = None
if 'condition_groups' not in st.session_state:
    st.session_state.condition_groups = []
if 'temp_conditions' not in st.session_state:
    st.session_state.temp_conditions = []

# App header
st.title("Multi-Dataset Merger with Complex Conditions")

# Sidebar for uploading files
with st.sidebar:
    st.header("Upload Datasets")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload dataset (CSV or Excel)", type=['csv', 'xlsx', 'xls'], key="file_upload")
    
    if uploaded_file is not None:
        dataset_name = st.text_input("Enter a name for this dataset:", 
                                     value=uploaded_file.name.split('.')[0])
        
        if st.button("Add Dataset"):
            df = read_file(uploaded_file)
            if df is not None:
                st.session_state.datasets[dataset_name] = df
                st.success(f"Added dataset: {dataset_name}")
    
    # Show currently loaded datasets
    if st.session_state.datasets:
        st.subheader("Loaded Datasets")
        for name in st.session_state.datasets.keys():
            st.write(f"- {name} ({len(st.session_state.datasets[name])} rows)")
        
        if st.button("Clear All Datasets"):
            st.session_state.datasets = {}
            st.session_state.merged_df = None
            st.session_state.condition_groups = []
            st.session_state.temp_conditions = []
            st.experimental_rerun()

# Main workspace
tab1, tab2, tab3 = st.tabs(["Merge Datasets", "Apply Conditions", "Download Results"])

# Tab 1: Merge Datasets
with tab1:
    st.header("Merge Datasets")
    
    if len(st.session_state.datasets) < 2:
        st.info("Please upload at least 2 datasets in the sidebar to perform a merge.")
    else:
        # Select datasets to merge
        st.subheader("Select Datasets to Merge")
        
        dataset_names = list(st.session_state.datasets.keys())
        base_dataset = st.selectbox("Select base dataset:", dataset_names)
        
        merge_list = []
        merge_settings = {}
        
        # Start with base dataset
        if base_dataset:
            base_df = st.session_state.datasets[base_dataset]
            result_df = base_df.copy()
            
            # Setup for merging additional datasets
            for i, name in enumerate([n for n in dataset_names if n != base_dataset]):
                if st.checkbox(f"Merge with {name}", key=f"merge_{i}"):
                    merge_list.append(name)
                    
                    # Find common columns
                    second_df = st.session_state.datasets[name]
                    common_cols = list(set(result_df.columns).intersection(set(second_df.columns)))
                    
                    # Select merge columns
                    merge_cols = st.multiselect(
                        f"Select columns to join on for {name}:",
                        common_cols,
                        default=common_cols[0] if common_cols else None,
                        key=f"cols_{i}"
                    )
                    
                    # Select merge type
                    merge_type = st.selectbox(
                        f"Join type for {name}:",
                        ["Left join", "Inner join", "Right join", "Outer join"],
                        key=f"type_{i}"
                    )
                    
                    # Store merge settings for this dataset
                    merge_settings[name] = {
                        "columns": merge_cols,
                        "type": merge_type
                    }
            
            # Perform merge button
            if merge_list and st.button("Perform Merge"):
                result_df = base_df.copy()
                
                # Sequentially merge datasets
                for name in merge_list:
                    second_df = st.session_state.datasets[name]
                    merge_cols = merge_settings[name]["columns"]
                    merge_how = {
                        "Left join": "left",
                        "Inner join": "inner", 
                        "Right join": "right",
                        "Outer join": "outer"
                    }[merge_settings[name]["type"]]
                    
                    # Perform the merge
                    result_df = pd.merge(
                        result_df, 
                        second_df,
                        on=merge_cols,
                        how=merge_how,
                        suffixes=(f'', f'_{name}')
                    )
                
                st.session_state.merged_df = result_df
                st.success(f"Successfully merged {len(merge_list)+1} datasets! Result has {len(result_df)} rows.")
        
        # Display merged result preview
        if st.session_state.merged_df is not None:
            st.subheader("Merged Dataset Preview")
            st.dataframe(st.session_state.merged_df.head())
            st.info(f"Total columns: {len(st.session_state.merged_df.columns)}")

# Tab 2: Apply Conditions
with tab2:
    st.header("Apply Complex Conditional Logic")
    
    if st.session_state.merged_df is None:
        st.info("Please merge datasets in the 'Merge Datasets' tab first.")
    else:
        st.subheader("Create Condition Groups")
        
        # Display all columns available for conditions
        all_columns = st.session_state.merged_df.columns.tolist()
        
        # Section to create a new condition group
        with st.expander("Create New Condition Group", expanded=True):
            st.write("A condition group combines multiple conditions with AND/OR logic into a single result column.")
            
            # Group name and result values
            group_name = st.text_input("Name for result column:", value="condition_result")
            group_logic = st.selectbox("Combine conditions with:", ["AND", "OR"])
            true_value = st.text_input("Value when conditions are TRUE:", value="Yes")
            false_value = st.text_input("Value when conditions are FALSE:", value="No")
            
            # Temporary conditions for this group
            st.write("### Add conditions to this group")
            
            # Add a new condition to the group
            with st.form("add_condition"):
                st.write("Add a new condition:")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    source_col = st.selectbox("Select column:", all_columns)
                    
                    # Show sample values
                    if source_col:
                        unique_vals = st.session_state.merged_df[source_col].dropna().unique()
                        if len(unique_vals) > 5:
                            st.write(f"Sample values: {', '.join(map(str, unique_vals[:5]))}, ...")
                        else:
                            st.write(f"Unique values: {', '.join(map(str, unique_vals))}")
                    
                    operator = st.selectbox("Condition type:", [
                        "equals", "not equals", "greater than", "less than", 
                        "contains", "does not contain", "is null", "is not null"
                    ])
                
                with col2:
                    # Only show value input if operator requires it
                    if operator not in ["is null", "is not null"]:
                        condition_value = st.text_input("Condition value:")
                    else:
                        condition_value = ""
                
                add_condition = st.form_submit_button("Add to Group")
                
                if add_condition:
                    new_condition = {
                        "source_column": source_col,
                        "operator": operator,
                        "value": condition_value
                    }
                    
                    st.session_state.temp_conditions.append(new_condition)
            
            # Display current conditions in this group
            if st.session_state.temp_conditions:
                st.write("### Current conditions in this group:")
                
                for i, condition in enumerate(st.session_state.temp_conditions):
                    col_name = condition["source_column"]
                    op = condition["operator"]
                    val = condition["value"]
                    
                    if op in ["is null", "is not null"]:
                        st.write(f"{i+1}. {col_name} {op}")
                    else:
                        st.write(f"{i+1}. {col_name} {op} '{val}'")
                    
                    if st.button(f"Remove", key=f"remove_temp_{i}"):
                        st.session_state.temp_conditions.pop(i)
                        st.experimental_rerun()
            
            # Save the condition group
            if st.button("Save Condition Group"):
                if not st.session_state.temp_conditions:
                    st.error("Please add at least one condition to the group.")
                elif not group_name:
                    st.error("Please provide a name for the result column.")
                else:
                    new_group = {
                        "name": group_name,
                        "logic": group_logic,
                        "true_value": true_value,
                        "false_value": false_value,
                        "conditions": st.session_state.temp_conditions.copy()
                    }
                    
                    st.session_state.condition_groups.append(new_group)
                    st.session_state.temp_conditions = []
                    st.success(f"Saved condition group: {group_name}")
                    st.experimental_rerun()
        
        # Display existing condition groups
        if st.session_state.condition_groups:
            st.subheader("Saved Condition Groups")
            
            for i, group in enumerate(st.session_state.condition_groups):
                with st.expander(f"Group: {group['name']} ({len(group['conditions'])} conditions)"):
                    st.write(f"Logic: {group['logic']}")
                    st.write(f"Values: {group['true_value']} when TRUE, {group['false_value']} when FALSE")
                    
                    st.write("Conditions:")
                    for j, condition in enumerate(group['conditions']):
                        col_name = condition["source_column"]
                        op = condition["operator"]
                        val = condition["value"]
                        
                        if op in ["is null", "is not null"]:
                            st.write(f"{j+1}. {col_name} {op}")
                        else:
                            st.write(f"{j+1}. {col_name} {op} '{val}'")
                    
                    if st.button(f"Remove Group", key=f"remove_group_{i}"):
                        st.session_state.condition_groups.pop(i)
                        st.experimental_rerun()
            
            # Apply all condition groups
            if st.button("Apply All Condition Groups"):
                result_df = st.session_state.merged_df.copy()
                
                for group in st.session_state.condition_groups:
                    # Initialize result arrays for each condition
                    condition_results = []
                    
                    # Apply each condition in the group
                    for condition in group["conditions"]:
                        condition_result = apply_condition(result_df, condition)
                        condition_results.append(condition_result)
                    
                    # Combine conditions based on group logic
                    if group["logic"] == "AND":
                        final_result = pd.Series([True] * len(result_df))
                        for result in condition_results:
                            final_result = final_result & result
                    else:  # OR
                        final_result = pd.Series([False] * len(result_df))
                        for result in condition_results:
                            final_result = final_result | result
                    
                    # Set the values in the new column
                    result_df[group["name"]] = np.where(
                        final_result, 
                        group["true_value"], 
                        group["false_value"]
                    )
                
                st.session_state.merged_df = result_df
                st.success("Successfully applied all condition groups!")
                
                # Display preview of result
                st.subheader("Result Preview")
                st.dataframe(st.session_state.merged_df.head())

# Tab 3: Download Results
with tab3:
    st.header("Download Results")
    
    if st.session_state.merged_df is None:
        st.info("Please merge datasets and apply conditions before downloading.")
    else:
        st.subheader("Preview Final Dataset")
        st.dataframe(st.session_state.merged_df.head())
        
        st.subheader("Download Options")
        filename = st.text_input("Enter filename for download (without extension):", value="merged_result")
        
        file_format = st.radio("Select file format:", ["CSV", "Excel"])
        
        if st.button("Generate Download Link"):
            try:
                if file_format == "CSV":
                    csv = st.session_state.merged_df.to_csv(index=False)
                    b64 = base64.b64encode(csv.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Click here to download {filename}.csv</a>'
                else:
                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        st.session_state.merged_df.to_excel(writer, index=False, sheet_name='Results')
                    b64 = base64.b64encode(buffer.getvalue()).decode()
                    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}.xlsx">Click here to download {filename}.xlsx</a>'
                
                st.markdown(href, unsafe_allow_html=True)
                st.success(f"Download link generated for {filename}!")
            except Exception as e:
                st.error(f"Error generating download: {e}")
