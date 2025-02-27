import streamlit as st
import pandas as pd
import numpy as np
import io

st.set_page_config(layout="wide", page_title="DataFrame Condition Builder")

st.title("DataFrame Condition Builder")
st.write("Upload a CSV or Excel file and apply conditional operations using np.where()")

# File upload
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    # Load the data based on file type
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension == 'csv':
        df = pd.read_csv(uploaded_file)
    elif file_extension in ['xlsx', 'xls']:
        df = pd.read_excel(uploaded_file)
    
    # Display original dataframe
    st.subheader("Original DataFrame")
    st.dataframe(df)
    
    # Get column names for selection
    columns = df.columns.tolist()
    
    # Create tabs for different operations
    tab1, tab2 = st.tabs(["Single Column Conditions", "Multiple Column Conditions"])
    
    with tab1:
        st.subheader("Apply conditions to a single column")
        
        # Select column to apply conditions
        target_column = st.selectbox("Select column to apply conditions:", columns, key="single_col")
        
        # Display column data type
        col_dtype = df[target_column].dtype
        st.info(f"Column data type: {col_dtype}")
        
        # Add condition type selector
        condition_type = st.selectbox(
            "Select condition type:",
            ["Simple Condition", "Multiple Conditions (AND)", "Multiple Conditions (OR)"],
            key="cond_type_single"
        )
        
        # Create result column name
        result_column = st.text_input("Result column name:", f"{target_column}_result", key="result_single")
        
        if condition_type == "Simple Condition":
            # Simple condition inputs
            operator = st.selectbox(
                "Select operator:",
                ["==", ">", "<", ">=", "<=", "!=", "contains", "startswith", "endswith"],
                key="op_simple"
            )
            
            # Value input based on data type
            if pd.api.types.is_numeric_dtype(df[target_column]):
                value = st.number_input("Value:", value=0, key="val_simple")
            else:
                value = st.text_input("Value:", "", key="val_simple")
            
            # True and False values
            true_value = st.text_input("Value if True:", "True", key="true_simple")
            false_value = st.text_input("Value if False:", "False", key="false_simple")
            
            if st.button("Apply Simple Condition", key="apply_simple"):
                try:
                    if operator == "==":
                        df[result_column] = np.where(df[target_column] == value, true_value, false_value)
                    elif operator == ">":
                        df[result_column] = np.where(df[target_column] > value, true_value, false_value)
                    elif operator == "<":
                        df[result_column] = np.where(df[target_column] < value, true_value, false_value)
                    elif operator == ">=":
                        df[result_column] = np.where(df[target_column] >= value, true_value, false_value)
                    elif operator == "<=":
                        df[result_column] = np.where(df[target_column] <= value, true_value, false_value)
                    elif operator == "!=":
                        df[result_column] = np.where(df[target_column] != value, true_value, false_value)
                    elif operator == "contains":
                        df[result_column] = np.where(df[target_column].astype(str).str.contains(str(value)), true_value, false_value)
                    elif operator == "startswith":
                        df[result_column] = np.where(df[target_column].astype(str).str.startswith(str(value)), true_value, false_value)
                    elif operator == "endswith":
                        df[result_column] = np.where(df[target_column].astype(str).str.endswith(str(value)), true_value, false_value)
                    
                    st.success(f"Applied condition and created column '{result_column}'")
                    st.dataframe(df)
                except Exception as e:
                    st.error(f"Error applying condition: {e}")
        
        elif condition_type == "Multiple Conditions (AND)":
            # Number of conditions
            num_conditions = st.number_input("Number of conditions:", min_value=1, max_value=5, value=2, key="num_and")
            
            conditions = []
            
            for i in range(num_conditions):
                st.markdown(f"**Condition {i+1}**")
                col1, col2 = st.columns(2)
                
                with col1:
                    operator = st.selectbox(
                        f"Operator {i+1}:",
                        ["==", ">", "<", ">=", "<=", "!=", "contains", "startswith", "endswith"],
                        key=f"op_and_{i}"
                    )
                
                with col2:
                    if pd.api.types.is_numeric_dtype(df[target_column]):
                        value = st.number_input(f"Value {i+1}:", value=0, key=f"val_and_{i}")
                    else:
                        value = st.text_input(f"Value {i+1}:", "", key=f"val_and_{i}")
                
                conditions.append((operator, value))
            
            # True and False values
            true_value = st.text_input("Value if ALL conditions are True:", "True", key="true_and")
            false_value = st.text_input("Value if ANY condition is False:", "False", key="false_and")
            
            if st.button("Apply AND Conditions", key="apply_and"):
                try:
                    # Start with all True condition
                    combined_condition = np.ones(len(df), dtype=bool)
                    
                    # AND all conditions together
                    for op, val in conditions:
                        if op == "==":
                            combined_condition = combined_condition & (df[target_column] == val)
                        elif op == ">":
                            combined_condition = combined_condition & (df[target_column] > val)
                        elif op == "<":
                            combined_condition = combined_condition & (df[target_column] < val)
                        elif op == ">=":
                            combined_condition = combined_condition & (df[target_column] >= val)
                        elif op == "<=":
                            combined_condition = combined_condition & (df[target_column] <= val)
                        elif op == "!=":
                            combined_condition = combined_condition & (df[target_column] != val)
                        elif op == "contains":
                            combined_condition = combined_condition & (df[target_column].astype(str).str.contains(str(val)))
                        elif op == "startswith":
                            combined_condition = combined_condition & (df[target_column].astype(str).str.startswith(str(val)))
                        elif op == "endswith":
                            combined_condition = combined_condition & (df[target_column].astype(str).str.endswith(str(val)))
                    
                    df[result_column] = np.where(combined_condition, true_value, false_value)
                    
                    st.success(f"Applied AND conditions and created column '{result_column}'")
                    st.dataframe(df)
                except Exception as e:
                    st.error(f"Error applying conditions: {e}")
        
        elif condition_type == "Multiple Conditions (OR)":
            # Number of conditions
            num_conditions = st.number_input("Number of conditions:", min_value=1, max_value=5, value=2, key="num_or")
            
            conditions = []
            
            for i in range(num_conditions):
                st.markdown(f"**Condition {i+1}**")
                col1, col2 = st.columns(2)
                
                with col1:
                    operator = st.selectbox(
                        f"Operator {i+1}:",
                        ["==", ">", "<", ">=", "<=", "!=", "contains", "startswith", "endswith"],
                        key=f"op_or_{i}"
                    )
                
                with col2:
                    if pd.api.types.is_numeric_dtype(df[target_column]):
                        value = st.number_input(f"Value {i+1}:", value=0, key=f"val_or_{i}")
                    else:
                        value = st.text_input(f"Value {i+1}:", "", key=f"val_or_{i}")
                
                conditions.append((operator, value))
            
            # True and False values
            true_value = st.text_input("Value if ANY condition is True:", "True", key="true_or")
            false_value = st.text_input("Value if ALL conditions are False:", "False", key="false_or")
            
            if st.button("Apply OR Conditions", key="apply_or"):
                try:
                    # Start with all False condition
                    combined_condition = np.zeros(len(df), dtype=bool)
                    
                    # OR all conditions together
                    for op, val in conditions:
                        if op == "==":
                            combined_condition = combined_condition | (df[target_column] == val)
                        elif op == ">":
                            combined_condition = combined_condition | (df[target_column] > val)
                        elif op == "<":
                            combined_condition = combined_condition | (df[target_column] < val)
                        elif op == ">=":
                            combined_condition = combined_condition | (df[target_column] >= val)
                        elif op == "<=":
                            combined_condition = combined_condition | (df[target_column] <= val)
                        elif op == "!=":
                            combined_condition = combined_condition | (df[target_column] != val)
                        elif op == "contains":
                            combined_condition = combined_condition | (df[target_column].astype(str).str.contains(str(val)))
                        elif op == "startswith":
                            combined_condition = combined_condition | (df[target_column].astype(str).str.startswith(str(val)))
                        elif op == "endswith":
                            combined_condition = combined_condition | (df[target_column].astype(str).str.endswith(str(val)))
                    
                    df[result_column] = np.where(combined_condition, true_value, false_value)
                    
                    st.success(f"Applied OR conditions and created column '{result_column}'")
                    st.dataframe(df)
                except Exception as e:
                    st.error(f"Error applying conditions: {e}")
    
    with tab2:
        st.subheader("Apply conditions across multiple columns")
        
        # Number of columns to include in condition
        num_columns = st.number_input("Number of columns to include:", min_value=1, max_value=5, value=2, key="num_multi_col")
        
        # Create column selectors and conditions
        column_conditions = []
        
        for i in range(num_columns):
            st.markdown(f"**Column {i+1} Condition**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                column = st.selectbox(f"Column {i+1}:", columns, key=f"multi_col_{i}")
            
            with col2:
                operator = st.selectbox(
                    f"Operator {i+1}:",
                    ["==", ">", "<", ">=", "<=", "!=", "contains", "startswith", "endswith"],
                    key=f"multi_op_{i}"
                )
            
            with col3:
                if pd.api.types.is_numeric_dtype(df[column]):
                    value = st.number_input(f"Value {i+1}:", value=0, key=f"multi_val_{i}")
                else:
                    value = st.text_input(f"Value {i+1}:", "", key=f"multi_val_{i}")
            
            column_conditions.append((column, operator, value))
        
        # Condition combination method
        combination_method = st.radio(
            "Combine conditions using:",
            ["AND (all conditions must be true)", "OR (any condition can be true)"],
            key="multi_combine"
        )
        
        # Result column name and values
        result_column = st.text_input("Result column name:", "multi_column_result", key="result_multi")
        true_value = st.text_input("Value if condition is True:", "True", key="true_multi")
        false_value = st.text_input("Value if condition is False:", "False", key="false_multi")
        
        if st.button("Apply Multi-Column Conditions", key="apply_multi"):
            try:
                if combination_method.startswith("AND"):
                    # Start with all True
                    combined_condition = np.ones(len(df), dtype=bool)
                    
                    # AND all conditions
                    for col, op, val in column_conditions:
                        if op == "==":
                            combined_condition = combined_condition & (df[col] == val)
                        elif op == ">":
                            combined_condition = combined_condition & (df[col] > val)
                        elif op == "<":
                            combined_condition = combined_condition & (df[col] < val)
                        elif op == ">=":
                            combined_condition = combined_condition & (df[col] >= val)
                        elif op == "<=":
                            combined_condition = combined_condition & (df[col] <= val)
                        elif op == "!=":
                            combined_condition = combined_condition & (df[col] != val)
                        elif op == "contains":
                            combined_condition = combined_condition & (df[col].astype(str).str.contains(str(val)))
                        elif op == "startswith":
                            combined_condition = combined_condition & (df[col].astype(str).str.startswith(str(val)))
                        elif op == "endswith":
                            combined_condition = combined_condition & (df[col].astype(str).str.endswith(str(val)))
                
                else:  # OR
                    # Start with all False
                    combined_condition = np.zeros(len(df), dtype=bool)
                    
                    # OR all conditions
                    for col, op, val in column_conditions:
                        if op == "==":
                            combined_condition = combined_condition | (df[col] == val)
                        elif op == ">":
                            combined_condition = combined_condition | (df[col] > val)
                        elif op == "<":
                            combined_condition = combined_condition | (df[col] < val)
                        elif op == ">=":
                            combined_condition = combined_condition | (df[col] >= val)
                        elif op == "<=":
                            combined_condition = combined_condition | (df[col] <= val)
                        elif op == "!=":
                            combined_condition = combined_condition | (df[col] != val)
                        elif op == "contains":
                            combined_condition = combined_condition | (df[col].astype(str).str.contains(str(val)))
                        elif op == "startswith":
                            combined_condition = combined_condition | (df[col].astype(str).str.startswith(str(val)))
                        elif op == "endswith":
                            combined_condition = combined_condition | (df[col].astype(str).str.endswith(str(val)))
                
                # Apply the combined condition
                df[result_column] = np.where(combined_condition, true_value, false_value)
                
                st.success(f"Applied multi-column conditions and created column '{result_column}'")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error applying conditions: {e}")
    
    # Add download button for modified DataFrame
    st.subheader("Download Modified DataFrame")
    
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name="modified_dataframe.csv",
        mime="text/csv",
    )
    
    # Add custom np.where() code generator
    st.subheader("Generated np.where() Code")
    st.write("Here's the Python code you can use to reproduce this operation:")
    
    code = "import numpy as np\n\n"
    code += "# Apply the condition(s)\n"
    code += f"df['{result_column}'] = np.where(<your_condition_here>, '{true_value}', '{false_value}')"
    
    st.code(code, language="python")
