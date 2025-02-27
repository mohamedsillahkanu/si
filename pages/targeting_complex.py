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
        st.subheader("Condition Builder with Grouping")
        
        st.markdown("""
        Build complex conditions with proper grouping and nesting.
        You can create expressions like: (A==B) AND [(C==D) OR (E==F)]
        """)
        
        # Condition builder state
        if 'expression_parts' not in st.session_state:
            st.session_state.expression_parts = []  # Will store tuples of (type, value)
            # types: "column", "operator", "value", "and", "or", "open_paren", "close_paren"
        
        # Display current expression
        if st.session_state.expression_parts:
            st.markdown("### Current Expression")
            
            # Format the current expression nicely
            expression_text = ""
            for part_type, part_value in st.session_state.expression_parts:
                if part_type == "column":
                    expression_text += f" **{part_value}** "
                elif part_type == "operator":
                    expression_text += f" {part_value} "
                elif part_type == "value":
                    if isinstance(part_value, str):
                        expression_text += f"'{part_value}'"
                    else:
                        expression_text += f"{part_value}"
                elif part_type == "and":
                    expression_text += f" **AND** "
                elif part_type == "or":
                    expression_text += f" **OR** "
                elif part_type == "open_paren":
                    expression_text += " ( "
                elif part_type == "close_paren":
                    expression_text += " ) "
            
            st.markdown(expression_text)
            
            # Clear button
            if st.button("Clear Expression", key="clear_expression"):
                st.session_state.expression_parts = []
                st.experimental_rerun()
        
        # Expression building tools
        st.markdown("### Build Your Expression")
        
        # Add parentheses
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Add Opening Parenthesis ( ", key="add_open_paren"):
                st.session_state.expression_parts.append(("open_paren", "("))
                st.experimental_rerun()
        
        with col2:
            if st.button("Add Closing Parenthesis ) ", key="add_close_paren"):
                st.session_state.expression_parts.append(("close_paren", ")"))
                st.experimental_rerun()
        
        # Add condition
        st.markdown("#### Add a Condition")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            column = st.selectbox("Column:", columns, key="group_col")
        
        with col2:
            operator = st.selectbox(
                "Operator:",
                ["==", ">", "<", ">=", "<=", "!=", "contains", "startswith", "endswith"],
                key="group_op"
            )
        
        with col3:
            if pd.api.types.is_numeric_dtype(df[column]):
                value = st.number_input("Value:", value=0, key="group_val")
            else:
                value = st.text_input("Value:", "", key="group_val")
        
        if st.button("Add This Condition", key="add_group_condition"):
            st.session_state.expression_parts.append(("column", column))
            st.session_state.expression_parts.append(("operator", operator))
            st.session_state.expression_parts.append(("value", value))
            st.experimental_rerun()
        
        # Add logical operator
        st.markdown("#### Add Logical Operator")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Add AND", key="add_and"):
                st.session_state.expression_parts.append(("and", "AND"))
                st.experimental_rerun()
        
        with col2:
            if st.button("Add OR", key="add_or"):
                st.session_state.expression_parts.append(("or", "OR"))
                st.experimental_rerun()
        
        # Result configuration (only show if we have parts)
        if st.session_state.expression_parts:
            st.markdown("### Result Configuration")
            result_column = st.text_input("Result column name:", "grouped_condition_result", key="result_group")
            true_value = st.text_input("Value if condition is True:", "True", key="true_group")
            false_value = st.text_input("Value if condition is False:", "False", key="false_group")
            
            # Parse expression and create code
            if st.button("Apply Grouped Conditions", key="apply_group"):
                # Convert the visual expression to Python code
                python_expr = ""
                valid_expression = True
                error_message = ""
                
                try:
                    # Validate the expression structure
                    if len(st.session_state.expression_parts) < 3:
                        valid_expression = False
                        error_message = "Expression is too short. Need at least one complete condition."
                    
                    # Check parentheses balance
                    open_count = sum(1 for part_type, _ in st.session_state.expression_parts if part_type == "open_paren")
                    close_count = sum(1 for part_type, _ in st.session_state.expression_parts if part_type == "close_paren")
                    if open_count != close_count:
                        valid_expression = False
                        error_message = f"Unbalanced parentheses: {open_count} opening vs {close_count} closing"
                    
                    # Check for logical operators between conditions
                    i = 0
                    while i < len(st.session_state.expression_parts):
                        part_type, part_value = st.session_state.expression_parts[i]
                        
                        # Skip parentheses
                        if part_type in ["open_paren", "close_paren"]:
                            i += 1
                            continue
                        
                        # Check for complete condition (column, operator, value)
                        if part_type == "column" and i+2 < len(st.session_state.expression_parts):
                            op_type, op_value = st.session_state.expression_parts[i+1]
                            val_type, val_value = st.session_state.expression_parts[i+2]
                            
                            if op_type == "operator" and val_type == "value":
                                # This is a complete condition, now check what follows
                                if i+3 < len(st.session_state.expression_parts):
                                    next_type, next_value = st.session_state.expression_parts[i+3]
                                    if next_type not in ["and", "or", "close_paren"]:
                                        valid_expression = False
                                        error_message = f"Expected AND/OR after condition at position {i+3}"
                                i += 3  # Skip past this condition
                            else:
                                valid_expression = False
                                error_message = f"Incomplete condition at position {i}"
                                break
                        elif part_type in ["and", "or"]:
                            # After AND/OR, must have column or open_paren
                            if i+1 < len(st.session_state.expression_parts):
                                next_type, next_value = st.session_state.expression_parts[i+1]
                                if next_type not in ["column", "open_paren"]:
                                    valid_expression = False
                                    error_message = f"Expected column or '(' after AND/OR at position {i+1}"
                            i += 1
                        else:
                            valid_expression = False
                            error_message = f"Unexpected token at position {i}"
                            break
                    
                    if valid_expression:
                        # Build the Python expression
                        for part_type, part_value in st.session_state.expression_parts:
                            if part_type == "column":
                                python_expr += f"df['{part_value}']"
                            elif part_type == "operator":
                                if part_value == "==":
                                    python_expr += " == "
                                elif part_value == ">":
                                    python_expr += " > "
                                elif part_value == "<":
                                    python_expr += " < "
                                elif part_value == ">=":
                                    python_expr += " >= "
                                elif part_value == "<=":
                                    python_expr += " <= "
                                elif part_value == "!=":
                                    python_expr += " != "
                                elif part_value == "contains":
                                    python_expr = f"({python_expr}.astype(str).str.contains"
                                elif part_value == "startswith":
                                    python_expr = f"({python_expr}.astype(str).str.startswith"
                                elif part_value == "endswith":
                                    python_expr = f"({python_expr}.astype(str).str.endswith"
                            elif part_type == "value":
                                if isinstance(part_value, str):
                                    if python_expr.endswith(("contains", "startswith", "endswith")):
                                        python_expr += f"('{part_value}'))"
                                    else:
                                        python_expr += f"'{part_value}'"
                                else:
                                    if python_expr.endswith(("contains", "startswith", "endswith")):
                                        python_expr += f"('{part_value}'))"
                                    else:
                                        python_expr += f"{part_value}"
                            elif part_type == "and":
                                python_expr += " & "
                            elif part_type == "or":
                                python_expr += " | "
                            elif part_type == "open_paren":
                                python_expr += "("
                            elif part_type == "close_paren":
                                python_expr += ")"
                        
                        # Apply the condition
                        result = eval(python_expr)
                        df[result_column] = np.where(result, true_value, false_value)
                        
                        st.success(f"Applied grouped conditions and created column '{result_column}'")
                        st.dataframe(df)
                        
                        # Generate the Python code
                        code_lines = ["import numpy as np", ""]
                        code_lines.append("# Define the condition")
                        code_lines.append(f"condition = {python_expr}")
                        code_lines.append("")
                        code_lines.append("# Apply the condition using np.where()")
                        code_lines.append(f"df['{result_column}'] = np.where(condition, '{true_value}', '{false_value}')")
                        
                        # Display generated code
                        st.subheader("Generated Python Code")
                        st.code("\n".join(code_lines), language="python")
                    else:
                        st.error(f"Invalid expression: {error_message}")
                
                except Exception as e:
                    st.error(f"Error applying conditions: {e}")
        else:
            st.info("Start building your expression using the tools above.")
        
        # Show expression examples
        with st.expander("Example Expressions"):
            st.markdown("""
            ### Simple Examples:
            - `(column1 == value1) AND (column2 > value2)`
            - `(column1 != value1) OR (column2 <= value2)`
            
            ### Complex Example:
            - `(column1 == value1) AND [(column2 > value2) OR (column3 contains value3)]`
            
            ### How to Build:
            1. Click "Add Opening Parenthesis" if needed
            2. Add a condition using the column, operator, and value selectors
            3. Click "Add Closing Parenthesis" if needed
            4. Add logical operators (AND/OR) between conditions
            5. Use parentheses to group conditions as needed
            """)


    
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
