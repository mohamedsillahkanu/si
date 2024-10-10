import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import seaborn as sns
from scipy.stats import shapiro, normaltest, anderson, probplot
import numpy as np
from scipy.stats import probplot, norm, shapiro, normaltest, anderson, skew, kurtosis

# Sidebar for Data Management
st.sidebar.title("Data Management")
data_management_option = st.sidebar.radio(
    "Choose an option:",
    ["Import Dataset", "Sanity Checks", "Merge Datasets", "Data Cleaning", "Quality Control/Checks"]
)

# Initialize session state variables
if 'df' not in st.session_state:
    st.session_state.df = None
if 'saved_df' not in st.session_state:
    st.session_state.saved_df = None
if 'dfs' not in st.session_state:
    st.session_state.dfs = []

if 'history' not in st.session_state:
    st.session_state.history = []
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = None

# Function to save updated data to session state and keep history for undo
def save_data():
    if st.session_state.df is not None:
        if 'history' not in st.session_state:
            st.session_state.history = []

        # Save the current state before making any changes
        st.session_state.history.append(st.session_state.df.copy())

        # Limit the history to the last 5 changes
        if len(st.session_state.history) > 5:
            st.session_state.history.pop(0)

        st.session_state.saved_df = st.session_state.df.copy()
    else:
        st.warning("No data available to save.")

def undo_last_action():
    """Undo the last action by reverting to the previous state."""
    if st.session_state.history:
        st.session_state.df = st.session_state.history.pop()
        st.success("Last action undone.")
    else:
        st.warning("No more actions to undo.")

# Function to check for column consistency
def sanity_check(dfs):
    column_lengths = [len(df.columns) for df in dfs]
    column_names = [set(df.columns) for df in dfs]

    if len(set(column_lengths)) == 1 and len(set(frozenset(names) for names in column_names)) == 1:
        st.success("All datasets have consistent columns. Ready to merge!")
        return True
    else:
        st.error("Inconsistency detected in columns across the datasets.")
        return False

# Function to filter dataframe based on categorical column and unique value
def filter_dataframe(df, categorical_column, unique_value):
    return df[df[categorical_column] == unique_value]

# Function for outlier correction methods
def correct_outliers(df, col, method):
    if method == "Winsorization":
        lower_bound = df[col].quantile(0.05)
        upper_bound = df[col].quantile(0.95)
        df[f'{col}_corrected_winsorization'] = df[col].clip(lower_bound, upper_bound)
        st.write("Original vs Corrected Data:")
        st.dataframe(df[[col, f'{col}_corrected_winsorization']])

    elif method == "Moving Average including outliers in MA calculation":
        window_size = st.slider("Select window size:", min_value=3, max_value=12, value=3)
        df[f'{col}_Moving_Avg'] = df[col].rolling(window=window_size, min_periods=1, center=True).mean()
        st.write("Original vs Moving Average Data:")
        st.dataframe(df[[col, f'{col}_Moving_Avg']])

    elif method == "Moving Average excluding outliers in MA calculation":
        window_size = st.slider("Select window size:", min_value=3, max_value=12, value=3)
        lower_bound = df[col].quantile(0.25)
        upper_bound = df[col].quantile(0.75)
        iqr = upper_bound - lower_bound
        outlier_lower_bound = lower_bound - 1.5 * iqr
        outlier_upper_bound = upper_bound + 1.5 * iqr

        def calculate_moving_avg_excluding_outliers(series, window):
            return series.rolling(window=window, min_periods=1, center=True).apply(
                lambda x: np.mean(x[(x >= outlier_lower_bound) & (x <= outlier_upper_bound)])
            )

        df[f'{col}_Moving_Avg_Excluded_Outliers'] = calculate_moving_avg_excluding_outliers(df[col], window_size)
        st.write("Original vs Moving Average (excluding outliers) Data:")
        st.dataframe(df[[col, f'{col}_Moving_Avg_Excluded_Outliers']])

    elif method == "Replacement with Mean excluding outliers in the mean calculation":
        lower_bound = df[col].quantile(0.25)
        upper_bound = df[col].quantile(0.75)
        iqr = upper_bound - lower_bound
        outlier_lower_bound = lower_bound - 1.5 * iqr
        outlier_upper_bound = upper_bound + 1.5 * iqr
        non_outlier_data = df[(df[col] >= outlier_lower_bound) & (df[col] <= outlier_upper_bound)][col]
        mean_value = non_outlier_data.mean()
        df[f'{col}_corrected_Mean_Excluding_Outliers'] = np.where(
            (df[col] < outlier_lower_bound) | (df[col] > outlier_upper_bound),
            mean_value,
            df[col]
        )
        st.write("Original vs Corrected Data (Mean excluding outliers):")
        st.dataframe(df[[col, f'{col}_corrected_Mean_Excluding_Outliers']])

    elif method == "Replacement with Clipped Values":
        lower_bound = df[col].quantile(0.25)
        upper_bound = df[col].quantile(0.75)
        iqr = upper_bound - lower_bound
        outlier_lower_bound = lower_bound - 1.5 * iqr
        outlier_upper_bound = upper_bound + 1.5 * iqr
        df[f'{col}_corrected_clipped'] = df[col].clip(outlier_lower_bound, outlier_upper_bound)
        st.write("Original vs Corrected Data (Clipped Values):")
        st.dataframe(df[[col, f'{col}_corrected_clipped']])

    return df

# Function to check for normality
def check_normality(data):
    stat, p_value = shapiro(data)
    _, p_value_k2 = normaltest(data)
    result_anderson = anderson(data)
    skewness = data.skew()
    skewness_type = "Normally Distributed" if abs(skewness) < 0.5 else ("Right Skewed" if skewness > 0 else "Left Skewed")

    return p_value, p_value_k2, result_anderson, skewness_type

# Main App
st.title("Data Processing App")

if data_management_option == "Import Dataset":
    st.header("Import Dataset")
    files = st.file_uploader("Upload files", type=["csv", "xlsx"], accept_multiple_files=True)
    if files:
        st.session_state.dfs = []
        for file in files:
            if file.name.endswith(".csv"):
                st.session_state.dfs.append(pd.read_csv(file))
            else:
                st.session_state.dfs.append(pd.read_excel(file))
        st.success("Datasets uploaded successfully!")

elif data_management_option == "Sanity Checks":
    st.header("Sanity Checks")
    if st.session_state.dfs:
        consistent = sanity_check(st.session_state.dfs)
        if consistent:
            if st.button("Merge Datasets"):
                st.session_state.df = pd.concat(st.session_state.dfs, ignore_index=True)
                st.write("Merged Data:")
                st.dataframe(st.session_state.df)
                save_data()
    else:
        st.warning("Please upload datasets first.")

elif data_management_option == "Merge Datasets":
    st.header("Merge Datasets")
    if st.session_state.df is not None:
        st.write("Merged Data:")
        st.dataframe(st.session_state.df)
    else:
        st.warning("No merged dataset available. Please perform sanity checks and merge the datasets.")

elif data_management_option == "Data Cleaning":
    st.header("Data Cleaning")
    cleaning_option = st.selectbox("Choose a cleaning option:", ["EDA", "Recode Variables", "Change Data Type", "Compute or Create New Variable", "Delete Column", "Sort Columns"])

    if cleaning_option == "EDA":
        if st.session_state.df is not None:
            option = st.radio("Choose analysis type:", ["Summary Statistics", "Variable Info", "Null Values Chart"])
            if option == "Summary Statistics":
                st.write("Summary Statistics:")
                st.write(st.session_state.df.describe())
            elif option == "Variable Info":
                buffer = io.StringIO()
                st.session_state.df.info(buf=buffer)
                info_str = buffer.getvalue()
                st.text(info_str)
            elif option == "Null Values Chart":
                for column in st.session_state.df.columns:
                    null_count = st.session_state.df[column].isnull().sum()
                    non_null_count = st.session_state.df[column].notnull().sum()
                    fig, ax = plt.subplots()
                    ax.bar(['Missing Values', 'Non-missing Values'], [null_count, non_null_count], color=['red', 'green'])
                    ax.set_title(f'Null vs Non-null Values for {column}')
                    ax.set_ylabel('Count')
                    st.pyplot(fig)
        else:
            st.warning("No dataset available. Please import and merge datasets first.")

    elif cleaning_option == "Recode Variables":
        if st.session_state.df is not None:
            recode_option = st.selectbox("Choose recoding option:", ["Recode a Column", "Recode Values in a Column"])
            if recode_option == "Recode a Column":
                column = st.selectbox("Select column to recode", st.session_state.df.columns)
                new_name = st.text_input("New name for the selected column")
                if st.button("Recode"):
                    if new_name:
                        st.session_state.df.rename(columns={column: new_name}, inplace=True)
                        st.write("Column name updated:")
                        st.dataframe(st.session_state.df)
                        save_data()
                    else:
                        st.error("Please enter a new column name.")
            elif recode_option == "Recode Values in a Column":
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
                        save_data()
                    else:
                        st.error("Ensure you provide both old and new values.")

    elif cleaning_option == "Change Data Type":
        st.header("Change Data Type")
        if st.session_state.df is not None:
            col = st.selectbox("Select column to change data type:", st.session_state.df.columns)
            dtype = st.selectbox("Select new data type:", ["int", "float", "str", "bool"])
            if st.button("Change Data Type"):
                try:
                    st.session_state.df[col] = st.session_state.df[col].astype(dtype)
                    st.success(f"Changed data type of {col} to {dtype}.")
                    st.dataframe(st.session_state.df)
                    save_data()
                except ValueError as e:
                    st.error(f"Error: {e}")

        else:
            st.warning("No dataset available. Please import and merge datasets first.")

    elif cleaning_option == "Delete Column":
        st.header("Delete Column")
        if st.session_state.df is not None:
            columns_to_delete = st.multiselect("Select columns to delete:", st.session_state.df.columns)
            if st.button("Delete"):
                if columns_to_delete:
                    st.session_state.df.drop(columns=columns_to_delete, inplace=True)
                    st.success(f"Deleted columns: {', '.join(columns_to_delete)}")
                    st.dataframe(st.session_state.df)
                    save_data()
                else:
                    st.error("Please select at least one column to delete.")

    elif cleaning_option == "Sort Columns":
        st.header("Sort Columns")
        if st.session_state.df is not None:
            new_order = st.multiselect("Rearrange columns by selecting them in the desired order:", st.session_state.df.columns, default=list(st.session_state.df.columns))
            if st.button("Rearrange Columns"):
                if len(new_order) == len(st.session_state.df.columns):
                    st.session_state.df = st.session_state.df[new_order]
                    st.success("Columns rearranged successfully.")
                    st.dataframe(st.session_state.df)
                    save_data()
                else:
                    st.error("Please select all columns to ensure the DataFrame structure is preserved.")

    elif cleaning_option == "Compute or Create New Variable":
        st.header("Compute or Create New Variable")
        if st.session_state.df is not None:
            num_variables = st.number_input("Number of new variables to compute:", min_value=1, value=1)
            for i in range(num_variables):
                new_col_name = st.text_input(f"New column name for variable {i+1}:", key=f"new_col_name_{i}")
                expression = st.text_input(f"Enter the expression (e.g., (A+B)/(C+D)*100) for variable {i+1}:", key=f"expression_{i}")
                if st.button(f"Compute Variable {i+1}", key=f"compute_{i}"):
                    try:
                        if not expression:
                            st.error(f"Please enter a valid expression for variable {i+1}.")
                        elif not new_col_name:
                            st.error(f"Please enter a name for the new column {i+1}.")
                        else:
                            st.session_state.df[new_col_name] = st.session_state.df.eval(expression)
                            st.write(f"Computed variable {i+1}:")
                            st.dataframe(st.session_state.df)
                            save_data()
                    except Exception as e:
                        st.error(f"Error computing new variable {i+1}: {e}")
        else:
            st.warning("No dataset available. Please import and merge datasets first.")

elif data_management_option == "Quality Control/Checks":
    st.header("Quality Control/Checks")
    quality_control_option = st.selectbox("Choose a quality control option:", ["", "Inconsistency Check", "Check for Normality", "Outlier Detection", "Outlier Correction"])

    if quality_control_option == "Inconsistency Check":
        if st.session_state.df is not None:
            column1 = st.selectbox("Select first column:", st.session_state.df.columns)
            column2 = st.selectbox("Select second column:", st.session_state.df.columns)
            if column1 and column2:
                fig, ax = plt.subplots()
                ax.scatter(st.session_state.df[column1], st.session_state.df[column2])
                ax.set_xlabel(column1)
                ax.set_ylabel(column2)
                ax.set_title(f'{column1} vs {column2}')
                st.pyplot(fig)
        else:
            st.warning("No dataset available. Please import and merge datasets first.")

    elif quality_control_option == "Check for Normality":
        if st.session_state.df is not None:
            column = st.selectbox("Select column to check normality:", st.session_state.df.columns)
            if column:
                data = st.session_state.df[column].dropna()
                p_value, p_value_k2, result_anderson, skewness_type = check_normality(data)
                st.write(f"Shapiro-Wilk Test p-value: {p_value:.8f}")
                st.write(f"D'Agostino's K-squared Test p-value: {p_value_k2:.8f}")
                st.write(f"Anderson-Darling Test statistic: {result_anderson.statistic:.8f}")
                st.write(f"Data Skewness: {skewness_type}")
                fig, ax = plt.subplots()
                probplot(data, dist="norm", plot=ax)
                ax.set_title(f'Q-Q Plot for {column}')
                st.pyplot(fig)
                fig, ax = plt.subplots()
                mean = np.mean(data)
                median = np.median(data)
                sns.histplot(data, kde=False, color='blue', stat='density', bins=30, ax=ax)
                xmin, xmax = ax.get_xlim()
                x = np.linspace(xmin, xmax, 100)
                p = norm.pdf(x, mean, np.std(data))
                ax.plot(x, p, 'k', linewidth=2)
                ax.axvline(mean, color='r', linestyle='--', label=f'Mean: {mean:.2f}')
                ax.axvline(median, color='g', linestyle='--', label=f'Median: {median:.2f}')
                ax.set_title(f'Histogram with Normal Curve for {column}')
                ax.set_xlabel(column)
                ax.set_ylabel('Density')
                ax.legend()
                st.pyplot(fig)

    elif quality_control_option == "Outlier Detection":
        if st.session_state.df is not None:
            column = st.selectbox("Select column for outlier detection:", st.session_state.df.columns)
            if column:
                method = st.selectbox("Choose detection method:", ["", "Z-Score", "IQR", "Boxplot", "Scatterplot with Q1=25th percentile and Q3=75th percentile Lines"])
                def detect_outliers_z_score(df, col):
                    return df[(df[col] - df[col].mean()) / df[col].std() > 3]
                def detect_outliers_iqr(df, col):
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    return df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))]
                if method == "Z-Score":
                    outliers = detect_outliers_z_score(st.session_state.df, column)
                    st.write("Outliers detected by Z-Score:")
                    st.dataframe(outliers)
                elif method == "IQR":
                    outliers = detect_outliers_iqr(st.session_state.df, column)
                    st.write("Outliers detected by IQR:")
                    st.dataframe(outliers)
                elif method == "Boxplot":
                    fig, ax = plt.subplots()
                    ax.boxplot(st.session_state.df[column])
                    ax.set_title(f'Boxplot for {column}')
                    st.pyplot(fig)
                elif method == "Scatterplot with Q1=25th percentile and Q3=75th percentile Lines":
                    Q1 = st.session_state.df[column].quantile(0.25)
                    Q3 = st.session_state.df[column].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers = st.session_state.df[(st.session_state.df[column] < lower_bound) | (st.session_state.df[column] > upper_bound)]
                    fig, ax = plt.subplots()
                    ax.scatter(st.session_state.df.index, st.session_state.df[column])
                    ax.axhline(lower_bound, color='green', linestyle='--', label='lower_bound')
                    ax.axhline(upper_bound, color='red', linestyle='--', label='upper_bound')
                    ax.scatter(outliers.index, outliers[column], color='red', label='Outliers', zorder=5)
                    ax.set_title(f'Scatterplot with lower and upper bound Lines for {column}')
                    ax.set_xlabel('Index')
                    ax.set_ylabel(column)
                    ax.legend()
                    st.pyplot(fig)
        else:
            st.warning("No dataset available. Please import and merge datasets first.")

    elif quality_control_option == "Outlier Correction":
        if st.session_state.df is not None:
            st.write("Step 1: Filter Data")
            categorical_column = st.selectbox("Select Categorical Column:", st.session_state.df.select_dtypes(include='object').columns)
            unique_values = st.session_state.df[categorical_column].unique()
            selected_value = st.selectbox(f"Select a value from '{categorical_column}':", unique_values)
            numeric_column = st.selectbox("Select Numeric Column for Outlier Correction:", st.session_state.df.select_dtypes(include='number').columns)
            if st.button("Apply Filter"):
                st.session_state.filtered_df = filter_dataframe(st.session_state.df, categorical_column, selected_value)
                st.write(f"Filtered Data (based on {categorical_column} = {selected_value}):")
                st.dataframe(st.session_state.filtered_df)
            if st.session_state.filtered_df is not None:
                method = st.selectbox("Choose Outlier Correction Method:", ["", "Winsorization", "Moving Average including outliers in MA calculation", "Moving Average excluding outliers in MA calculation", "Replacement with Mean excluding outliers in the mean calculation", "Replacement with Clipped Values"])
                if method:
                    corrected_df = correct_outliers(st.session_state.filtered_df, numeric_column, method)
                    st.write(f"Corrected Data (based on {method}):")
                    st.dataframe(corrected_df)
                    if st.button("Save Filtered and Corrected Data"):
                        st.session_state.df.update(corrected_df)
                        st.success("Filtered and corrected data saved.")
                        st.dataframe(st.session_state.df)

# Add Undo Button
if st.session_state.df is not None:
    if st.button("Undo Last Action"):
        undo_last_action()
        st.dataframe(st.session_state.df)

# Always show Save and Download buttons
if st.session_state.df is not None:
    st.write("Save and Download Updated Data:")
    if st.button("Save"):
        save_data()
        st.success("Data saved successfully.")
    if st.session_state.saved_df is not None:
        st.download_button(
            label="Download Updated Data",
            data=st.session_state.saved_df.to_csv(index=False),
            file_name="updated_data.csv",
            mime="text/csv"
        )
