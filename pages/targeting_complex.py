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
    tab1, tab2, tab3 = st.tabs(["Single Column Conditions", "Multiple Column Conditions", "Advanced Conditions (AND/OR Mix)"])
    
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
    
    with tab3:
        st.subheader("Simple AND/OR Mixer")
        
        st.markdown("""
        Build a condition using a mix of AND and OR logic.
        Just add conditions one by one and choose how each should connect to the previous one.
        """)
        
        # Initialize session state to store conditions if not already present
        if 'conditions' not in st.session_state:
            st.session_state.conditions = []
            st.session_state.connections = []  # "AND" or "OR" between conditions
        
        # Display current condition builder
        if st.session_state.conditions:
            st.markdown("### Your Current Condition")
            
            condition_text = ""
            for i, ((col, op, val), connection) in enumerate(zip(st.session_state.conditions, 
                                                              st.session_state.connections + [""])):
                if i > 0:
                    condition_text += f" **{st.session_state.connections[i-1]}** "
                condition_text += f"({col} {op} {val})"
            
            st.markdown(condition_text)
            
            if st.button("Clear All Conditions", key="clear_conditions"):
                st.session_state.conditions = []
                st.session_state.connections = []
                st.experimental_rerun()
        
        # Add new condition
        st.markdown("### Add a Condition")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            column = st.selectbox("Column:", columns, key="simple_mix_col")
        
        with col2:
            operator = st.selectbox(
                "Operator:",
                ["==", ">", "<", ">=", "<=", "!=", "contains", "startswith", "endswith"],
                key="simple_mix_op"
            )
        
        with col3:
            if pd.api.types.is_numeric_dtype(df[column]):
                value = st.number_input("Value:", value=0, key="simple_mix_val")
            else:
                value = st.text_input("Value:", "", key="simple_mix_val")
        
        # Logic connector (AND/OR)
        if st.session_state.conditions:  # Only show if we already have at least one condition
            connection = st.radio(
                "Connect with previous condition using:",
                ["AND", "OR"],
                horizontal=True,
                key="simple_mix_connection"
            )
        else:
            connection = "AND"  # Default, won't be used for first condition
        
        if st.button("Add This Condition", key="add_condition"):
            st.session_state.conditions.append((column, operator, value))
            if len(st.session_state.conditions) > 1:  # Don't add connection for first condition
                st.session_state.connections.append(connection)
            st.experimental_rerun()
        
        # Result configuration (only show if we have conditions)
        if st.session_state.conditions:
            st.markdown("### Result Configuration")
            result_column = st.text_input("Result column name:", "mixed_condition_result", key="result_mix")
            true_value = st.text_input("Value if condition is True:", "True", key="true_mix")
            false_value = st.text_input("Value if condition is False:", "False", key="false_mix")
            
            if st.button("Apply Mixed Conditions", key="apply_mix"):
                try:
                    # Start with the first condition
                    col, op, val = st.session_state.conditions[0]
                    
                    if op == "==":
                        final_condition = (df[col] == val)
                    elif op == ">":
                        final_condition = (df[col] > val)
                    elif op == "<":
                        final_condition = (df[col] < val)
                    elif op == ">=":
                        final_condition = (df[col] >= val)
                    elif op == "<=":
                        final_condition = (df[col] <= val)
                    elif op == "!=":
                        final_condition = (df[col] != val)
                    elif op == "contains":
                        final_condition = (df[col].astype(str).str.contains(str(val)))
                    elif op == "startswith":
                        final_condition = (df[col].astype(str).str.startswith(str(val)))
                    elif op == "endswith":
                        final_condition = (df[col].astype(str).str.endswith(str(val)))
                    
                    # Add remaining conditions with their connections
                    for i in range(1, len(st.session_state.conditions)):
                        col, op, val = st.session_state.conditions[i]
                        connection = st.session_state.connections[i-1]
                        
                        if op == "==":
                            condition = (df[col] == val)
                        elif op == ">":
                            condition = (df[col] > val)
                        elif op == "<":
                            condition = (df[col] < val)
                        elif op == ">=":
                            condition = (df[col] >= val)
                        elif op == "<=":
                            condition = (df[col] <= val)
                        elif op == "!=":
                            condition = (df[col] != val)
                        elif op == "contains":
                            condition = (df[col].astype(str).str.contains(str(val)))
                        elif op == "startswith":
                            condition = (df[col].astype(str).str.startswith(str(val)))
                        elif op == "endswith":
                            condition = (df[col].astype(str).str.endswith(str(val)))
                        
                        if connection == "AND":
                            final_condition = final_condition & condition
                        else:  # "OR"
                            final_condition = final_condition | condition
                    
                    # Apply the condition
                    df[result_column] = np.where(final_condition, true_value, false_value)
                    
                    st.success(f"Applied mixed conditions and created column '{result_column}'")
                    st.dataframe(df)
                    
                    # Generate Python code
                    code_lines = ["import numpy as np", ""]
                    
                    # First condition
                    col, op, val = st.session_state.conditions[0]
                    if isinstance(val, str):
                        val_str = f"'{val}'"
                    else:
                        val_str = str(val)
                        
                    if op == "==":
                        code_lines.append(f"condition = (df['{col}'] == {val_str})")
                    elif op == ">":
                        code_lines.append(f"condition = (df['{col}'] > {val_str})")
                    elif op == "<":
                        code_lines.append(f"condition = (df['{col}'] < {val_str})")
                    elif op == ">=":
                        code_lines.append(f"condition = (df['{col}'] >= {val_str})")
                    elif op == "<=":
                        code_lines.append(f"condition = (df['{col}'] <= {val_str})")
                    elif op == "!=":
                        code_lines.append(f"condition = (df['{col}'] != {val_str})")
                    elif op == "contains":
                        code_lines.append(f"condition = (df['{col}'].astype(str).str.contains('{val}'))")
                    elif op == "startswith":
                        code_lines.append(f"condition = (df['{col}'].astype(str).str.startswith('{val}'))")
                    elif op == "endswith":
                        code_lines.append(f"condition = (df['{col}'].astype(str).str.endswith('{val}'))")
                    
                    # Remaining conditions
                    for i in range(1, len(st.session_state.conditions)):
                        col, op, val = st.session_state.conditions[i]
                        connection = st.session_state.connections[i-1]
                        
                        if isinstance(val, str):
                            val_str = f"'{val}'"
                        else:
                            val_str = str(val)
                            
                        if op == "==":
                            code_lines.append(f"condition = condition {' & ' if connection == 'AND' else ' | '}(df['{col}'] == {val_str})")
                        elif op == ">":
                            code_lines.append(f"condition = condition {' & ' if connection == 'AND' else ' | '}(df['{col}'] > {val_str})")
                        elif op == "<":
                            code_lines.append(f"condition = condition {' & ' if connection == 'AND' else ' | '}(df['{col}'] < {val_str})")
                        elif op == ">=":
                            code_lines.append(f"condition = condition {' & ' if connection == 'AND' else ' | '}(df['{col}'] >= {val_str})")
                        elif op == "<=":
                            code_lines.append(f"condition = condition {' & ' if connection == 'AND' else ' | '}(df['{col}'] <= {val_str})")
                        elif op == "!=":
                            code_lines.append(f"condition = condition {' & ' if connection == 'AND' else ' | '}(df['{col}'] != {val_str})")
                        elif op == "contains":
                            code_lines.append(f"condition = condition {' & ' if connection == 'AND' else ' | '}(df['{col}'].astype(str).str.contains('{val}'))")
                        elif op == "startswith":
                            code_lines.append(f"condition = condition {' & ' if connection == 'AND' else ' | '}(df['{col}'].astype(str).str.startswith('{val}'))")
                        elif op == "endswith":
                            code_lines.append(f"condition = condition {' & ' if connection == 'AND' else ' | '}(df['{col}'].astype(str).str.endswith('{val}'))")
                    
                    code_lines.append("")
                    code_lines.append("# Apply the condition using np.where()")
                    code_lines.append(f"df['{result_column}'] = np.where(condition, '{true_value}', '{false_value}')")
                    
                    # Display generated code
                    st.subheader("Generated Python Code")
                    st.code("\n".join(code_lines), language="python")
                    
                except Exception as e:
                    st.error(f"Error applying conditions: {e}")
        else:
            st.info("Add at least one condition to apply mixed AND/OR logic.")

    
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
