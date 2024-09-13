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

# Function to save updated data to session state
#def #save_data():
    #if st.#session_state.df is not None:
        #st.session_state.saved_df = st.session_state.df.copy()
    #else:
        #st.warning("No data available to save.")

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

# Function for outlier correction methods

def correct_outliers(df, col, method):
    if method == "Winsorization":
        lower_bound = df[col].quantile(0.05)
        upper_bound = df[col].quantile(0.95)

        iqr = upper_bound - lower_bound

        # Define the bounds for outliers
        outlier_lower_bound = lower_bound - 1.5 * iqr
        outlier_upper_bound = upper_bound + 1.5 * iqr
        df[f'{col}_corrected_winsorization'] = df[col].clip(outlier_lower_bound, outlier_upper_bound)
        st.write("Original vs Corrected Data:")
        st.dataframe(df[[col, f'{col}_corrected_winsorization']])

    elif method == "Moving Average including outliers in MA calculation":
        lower_bound = df[col].quantile(0.25)
        upper_bound = df[col].quantile(0.75)
        iqr = upper_bound - lower_bound
        outlier_lower_bound = lower_bound - 1.5 * iqr
        outlier_upper_bound = upper_bound + 1.5 * iqr

    # Calculate the moving average including outliers
        window_size = st.slider("Select window size:", min_value=3, max_value=12, value=3)
        df[f'{col}_Moving_Avg'] = df[col].rolling(window=window_size, min_periods=1, center=True).mean()

    # Replace outliers with the moving average value
        df[f'{col}_corrected_Moving_Avg_Included_Outliers'] = df[col].where(
            (df[col] >= outlier_lower_bound) & (df[col] <= outlier_upper_bound),
            df[f'{col}_Moving_Avg']

        )

        st.write("Original vs Corrected Data:")
        st.dataframe(df[[col, f'{col}_corrected_Moving_Avg_Included_Outliers']])

    elif method == "Moving Average excluding outliers in MA calculation":
        lower_bound = df[col].quantile(0.25)
        upper_bound = df[col].quantile(0.75)

        iqr = upper_bound - lower_bound

        # Define the bounds for outliers
        outlier_lower_bound = lower_bound - 1.5 * iqr
        outlier_upper_bound = upper_bound + 1.5 * iqr

        window_size = st.slider("Select window size:", min_value=3, max_value=12, value=3)

        def calculate_moving_avg_excluding_outliers(series, window, lower_bound, upper_bound):
            return series.rolling(window=window, min_periods=1, center=True).apply(
                lambda x: np.mean(x[(x >= outlier_lower_bound) & (x <= outlier_upper_bound)])
            )

        df[f'{col}_Moving_Avg_Excluded_Outliers'] = calculate_moving_avg_excluding_outliers(df[col], window_size, lower_bound, upper_bound)
        df[f'{col}_corrected_Moving_Avg_Excluded_Outliers'] = np.where(
            (df[col] < outlier_lower_bound) | (df[col] > outlier_upper_bound),
            df[f'{col}_Moving_Avg_Excluded_Outliers'],
            df[col]
        )

        st.write("Original vs Corrected Data:")
        st.dataframe(df[[col, f'{col}_corrected_Moving_Avg_Excluded_Outliers']])

    elif method == "Replacement with Mean excluding outliers in the mean calculation":
        lower_bound = df[col].quantile(0.25)
        upper_bound = df[col].quantile(0.75)

        iqr = upper_bound - lower_bound

        # Define the bounds for outliers
        outlier_lower_bound = lower_bound - 1.5 * iqr
        outlier_upper_bound = upper_bound + 1.5 * iqr
        non_outlier_data = df[(df[col] >= outlier_lower_bound) & (df[col] <= outlier_upper_bound)][col]
        mean_value = non_outlier_data.mean()
        df[f'{col}_corrected_Mean_Excluding_Outliers'] = np.where(
            (df[col] < outlier_lower_bound) | (df[col] > outlier_upper_bound),
            mean_value,
            df[col]
        )


        st.write("Original vs Corrected Data:")
        st.dataframe(df[[col, f'{col}_corrected_Mean_Excluding_Outliers']])

    elif method == "Replacement with Mean including outliers in the mean calculation":

        lower_bound = df[col].quantile(0.25)
        upper_bound = df[col].quantile(0.75)

        iqr = upper_bound - lower_bound

        # Define the bounds for outliers
        outlier_lower_bound = lower_bound - 1.5 * iqr
        outlier_upper_bound = upper_bound + 1.5 * iqr

        mean_value = df[col].mean(skipna=True)
        df[f'{col}_corrected_Mean_Including_Outliers'] = np.where(
            (df[col] < outlier_lower_bound) | (df[col] > outlier_upper_bound),
            mean_value,
            df[col]
        )
        st.write(f"Mean value used for replacement: {mean_value}")
        st.write("Original vs Corrected Data:")
        st.dataframe(df[[col, f'{col}_corrected_Mean_Including_Outliers']])

    elif method == "Replacement with Median excluding outliers in the median calculation":
        lower_bound = df[col].quantile(0.25)
        upper_bound = df[col].quantile(0.75)

        iqr = upper_bound - lower_bound

        # Define the bounds for outliers
        outlier_lower_bound = lower_bound - 1.5 * iqr
        outlier_upper_bound = upper_bound + 1.5 * iqr

        non_outlier_data = df[(df[col] >= outlier_lower_bound) & (df[col] <= outlier_upper_bound)][col]
        median_value = non_outlier_data.median(skipna=True)
        df[f'{col}_corrected_Median_Excluding_Outliers'] = np.where(
            (df[col] < outlier_lower_bound) | (df[col] > outlier_upper_bound),
            median_value,
            df[col]
        )



    elif method == "Replacement with Median including outliers in the median calculation":
        lower_bound = df[col].quantile(0.25)
        upper_bound = df[col].quantile(0.75)
        iqr = upper_bound - lower_bound

        # Define the bounds for outliers
        outlier_lower_bound = lower_bound - 1.5 * iqr
        outlier_upper_bound = upper_bound + 1.5 * iqr

    # Calculate the median
        median_value = df[col].median()
        df[f'{col}_corrected_Median_Including_Outliers'] = np.where(
            (df[col] < outlier_lower_bound) | (df[col] > outlier_upper_bound),
            median_value,
            df[col]
        )

    elif method == "Replacement with Clipped Values":

        lower_bound = df[col].quantile(0.25)
        upper_bound = df[col].quantile(0.75)

        iqr = upper_bound - lower_bound

        # Define the bounds for outliers
        outlier_lower_bound = lower_bound - 1.5 * iqr
        outlier_upper_bound = upper_bound + 1.5 * iqr

        df[f'{col}_corrected_clipped'] = df[col].clip(outlier_lower_bound, outlier_upper_bound)

    return df

# Function to check for normality
def check_normality(data):
    # Perform Shapiro-Wilk test
    stat, p_value = shapiro(data)

    # Perform D'Agostino's K-squared test
    _, p_value_k2 = normaltest(data)

    # Perform Anderson-Darling test
    result_anderson = anderson(data)

    # Determine skewness
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
                st.write("Variable Info:")
                buffer = io.StringIO()
                st.session_state.df.info(buf=buffer)
                info_str = buffer.getvalue()
                st.text(info_str)
            elif option == "Null Values Chart":
                st.write("Null Values Chart:")
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
                st.write("Recode a Column:")
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
                    save_data()
                else:
                    st.error("Please select all columns to ensure the DataFrame structure is preserved.")



    elif cleaning_option == "Compute or Create New Variable":
        st.header("Compute or Create New Variable")
        if st.session_state.df is not None:
            num_variables = st.number_input("Number of new variables to compute:", min_value=1, value=1)

            for i in range(num_variables):
                st.subheader(f"Compute Variable {i+1}")
                new_col_name = st.text_input(f"New column name for variable {i+1}:", key=f"new_col_name_{i}")
                expression = st.text_input(f"Enter the expression (e.g., (A+B)/(C+D)*100) for variable {i+1}:", key=f"expression_{i}")

                # Show available columns for user to select
                st.write("Available Columns:")
                st.write(st.session_state.df.columns.tolist())

                if st.button(f"Compute Variable {i+1}", key=f"compute_{i}"):
                    try:
                        if not expression:
                            st.error(f"Please enter a valid expression for variable {i+1}.")
                        elif not new_col_name:
                            st.error(f"Please enter a name for the new column {i+1}.")
                        else:
                            # Safely evaluate the expression
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
    quality_control_option = st.selectbox("Choose a quality control option:", ["","Inconsistency Check","Check for Normality", "Outlier Detection", "Outlier Correction"])

    if quality_control_option == "Inconsistency Check":
        if st.session_state.df is not None:
            column1 = st.selectbox("Select first column:", st.session_state.df.columns)
            column2 = st.selectbox("Select second column:", st.session_state.df.columns)

            if column1 and column2:
                st.write("1:1 Scattered Plot:")
                fig, ax = plt.subplots()
                ax.scatter(st.session_state.df[column1], st.session_state.df[column2])
                ax.set_xlabel(column1)
                ax.set_ylabel(column2)
                ax.set_title(f'{column1} vs {column2}')
                st.pyplot(fig)
        else:
            st.warning("No dataset available. Please import and merge datasets first.")


    elif quality_control_option == "Check for Normality":
        st.header("Check for Normality")
        if st.session_state.df is not None:
            column = st.selectbox("Select column to check normality:", st.session_state.df.columns)
            if column:
                data = st.session_state.df[column].dropna()  # Remove NaN values

                # Check for normality
                p_value, p_value_k2, result_anderson, skewness_type = check_normality(data)

                st.write(f"Shapiro-Wilk Test p-value: {p_value:.8f}")
                st.write(f"D'Agostino's K-squared Test p-value: {p_value_k2:.8f}")
                st.write(f"Anderson-Darling Test statistic: {result_anderson.statistic:.8f}")

                if p_value > 0.05 and p_value_k2 > 0.05:
                    st.success("Data is likely normally distributed.")
                else:
                    st.warning(f"Data is not normally distributed. It is {skewness_type}.")

                # Q-Q plot
                st.write("Q-Q Plot:")
                fig, ax = plt.subplots()
                probplot(data, dist="norm", plot=ax)
                ax.set_title(f'Q-Q Plot for {column}')
                st.pyplot(fig)


                st.write("Histogram with Normal Curve:")
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


            column = st.selectbox("Select column for outlier correction:", [""] + list(st.session_state.df.columns))

            if column:
                st.write("Outlier Detection Methods:")
                method = st.selectbox("Choose method:", ["","Z-Score", "IQR", "Boxplot", "Scatterplot with Q1=25th percentile and Q3=75th percentile Lines"])

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
                    st.write("Boxplot for Outlier Detection:")
                    fig, ax = plt.subplots()
                    ax.boxplot(st.session_state.df[column])
                    ax.set_title(f'Boxplot for {column}')
                    st.pyplot(fig)

                elif method == "Scatterplot with Q1=25th percentile and Q3=75th percentile Lines":
                    st.write("Scatterplot with Q1=25th percentile and Q3=75th percentile Lines:")
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

            column = st.selectbox("Select column for outlier correction:", [""] + list(st.session_state.df.columns))


            if column:
                st.write("Outlier Correction Methods:")
                method = st.selectbox("Choose method:", ["","Winsorization", "Moving Average including outliers in MA calculation", "Moving Average excluding outliers in MA calculation", "Replacement with Mean excluding outliers in the mean calculation", "Replacement with Mean including outliers in the mean calculation", "Replacement with Median excluding outliers in the median calculation", "Replacement with Median including outliers in the median calculation", "Replacement with Capped Values"])

                if method:
                    corrected_df = correct_outliers(st.session_state.df, column, method)
                    st.write("Corrected Data:")
                    st.dataframe(corrected_df)
                    save_data()
        else:
            st.warning("No dataset available. Please import and merge datasets first.")


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

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import io
import base64
import dataframe_image as dfi
from io import BytesIO
from collections import OrderedDict


st.title("Data Analysis Section")


def generate_download_link(file_name, file_type='image'):
    with open(file_name, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    if file_type == 'image':
        return f'<a href="data:file/image;base64,{b64}" download="{file_name}">Download {file_name}</a>'
    elif file_type == 'excel':
        return f'<a href="data:file/excel;base64,{b64}" download="{file_name}">Download {file_name}</a>'

def process_data(df0):
    # Processing steps as in the original code
    cols = ['test', 'conf', 'maltreat']
    df0.insert(len(df0.columns), 'key_variables', df0[cols].sum(axis=1, skipna=True, min_count=1))
    df0['key_variables'] = df0['key_variables'].fillna(0)
    df0.insert(len(df0.columns), 'reported', np.where(df0.key_variables == 0, 0, 1))

    d = {}
    for hf in sorted(df0.hf_uid.unique()):
        t = df0[df0.hf_uid == hf]
        d[hf] = t[t.reported == 1].YM.min()

    df0.insert(len(df0.columns), 'first_month_reported', df0.hf_uid.map(d))

    # Create first month reported Excel file
    cols = ['adm1', 'adm2', 'adm3', 'hf', 'hf_uid', 'first_month_reported']
    df = df0[cols].drop_duplicates(subset='hf_uid')
    output = BytesIO()
    df.to_excel(output, index=False)
    excel_data = output.getvalue()
    excel_file_name = 'First_month_reported.xlsx'

    # Additional detailed columns
    df0.insert(len(df0.columns), 'reported_detail', df0.apply(lambda x: 0.5 if ((x.reported == 0) & (x.YM > d[x.hf_uid])) else x.reported, axis=1))
    df0.insert(len(df0.columns), 'hf_active', np.where(df0.reported_detail == 0, False, True))
    df0.insert(len(df0.columns), 'hf_wards', df0.hf.apply(lambda x: 'Inpatient' if x.split()[-1] == 'Hospital' else 'Outpatient'))

    reporting_monthly = {}
    for i in ['Inpatient', 'Outpatient']:
        t = df0[df0.hf_wards == i] if i == 'Inpatient' else df0.copy()
        t = (t[['YM', 'hf_uid', 'hf_active']]
             .groupby('YM')['hf_active'].sum()
             .to_frame()
             .reset_index()
             .rename(columns={'hf_active': 'denominator'}))
        reporting_monthly[i] = t

    return df0, reporting_monthly, excel_data, excel_file_name

def plot_heatmap(df, title):
    cmap = ListedColormap(['lightcoral', 'gold', 'limegreen'])
    fig, ax = plt.subplots(figsize=(30, 20))
    sns.heatmap(ax=ax, data=df, cmap=cmap, cbar=None)
    ax.set_xlabel('')
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='right')

    yticklabels = [l.get_text()[0:-7] for l in ax.get_yticklabels()]
    t = pd.DataFrame(yticklabels).reset_index()
    t1 = t.groupby(0)['index'].mean().astype(int).reset_index()
    t.insert(0, 'pos', t[0].map(dict(zip(t1[0], t1['index']))))
    t = t[[0, 'pos', 'index']]
    t[0] = np.where(t.pos == t['index'], t[0], '')
    test = t[0].to_list()

    ax.set_yticks(ax.get_yticks())
    ax.set_yticklabels(test, size=15)
    ax.set_ylabel('HEALTH FACILITY')
    ylabel_mapping = OrderedDict()
    for adm1, hf_uid in df.index:
        ylabel_mapping.setdefault(adm1, [])
        ylabel_mapping[adm1].append(hf_uid)
    hline = []
    new_ylabels = []
    for adm1, hf_list in ylabel_mapping.items():
        hf_list[0] = "{} - {}".format(adm1, hf_list[0])
        new_ylabels.extend(hf_list)
        if hline:
            hline.append(len(hf_list) + hline[-1])
        else:
            hline.append(len(hf_list))
    plt.hlines(hline, xmin=-10, xmax=0, color="grey", linewidth=2, clip_on=False)
    fig.tight_layout()

    # Save to BytesIO and return
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_data = buf.getvalue()
    return img_data


def create_adm3_uid(df0):
    # Create a unique identifier based on adm1, adm2, and adm3
    df0['adm3_uid'] = df0.groupby(['adm1', 'adm2', 'adm3']).ngroup()
    return df0


def process_data(df0):
    # Processing steps as in the original code
    cols = ['susp','test', 'conf', 'maltreat']
    df0.insert(len(df0.columns), 'key_variables', df0[cols].sum(axis=1, skipna=True, min_count=1))
    df0['key_variables'] = df0['key_variables'].fillna(0)
    df0.insert(len(df0.columns), 'reported', np.where(df0.key_variables == 0, 0, 1))

    d = {}
    for hf in sorted(df0.hf_uid.unique()):
        t = df0[df0.hf_uid == hf]
        d[hf] = t[t.reported == 1].YM.min()

    df0.insert(len(df0.columns), 'first_month_reported', df0.hf_uid.map(d))

    # Create first month reported Excel file
    cols = ['adm1', 'adm2', 'adm3', 'hf', 'hf_uid', 'first_month_reported']
    df = df0[cols].drop_duplicates(subset='hf_uid')
    output = BytesIO()
    df.to_excel(output, index=False)
    excel_data = output.getvalue()
    excel_file_name = 'First_month_reported.xlsx'

    # Additional detailed columns
    df0.insert(len(df0.columns), 'reported_detail', df0.apply(lambda x: 0.5 if ((x.reported == 0) & (x.YM > d[x.hf_uid])) else x.reported, axis=1))
    df0.insert(len(df0.columns), 'hf_active', np.where(df0.reported_detail == 0, False, True))
    df0.insert(len(df0.columns), 'hf_wards', df0.hf.apply(lambda x: 'Inpatient' if x.split()[-1] == 'Hospital' else 'Outpatient'))

    reporting_monthly = {}
    for i in ['Inpatient', 'Outpatient']:
        t = df0[df0.hf_wards == i] if i == 'Inpatient' else df0.copy()
        t = (t[['YM', 'hf_uid', 'hf_active']]
             .groupby('YM')['hf_active'].sum()
             .to_frame()
             .reset_index()
             .rename(columns={'hf_active': 'denominator'}))
        reporting_monthly[i] = t

    return df0, reporting_monthly, excel_data, excel_file_name



def plot_heatmap(df, title):
    cmap = ListedColormap(['lightcoral', 'gold', 'limegreen'])
    fig, ax = plt.subplots(figsize=(30, 20))
    sns.heatmap(ax=ax, data=df, cmap=cmap, cbar=None)
    ax.set_xlabel('')
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='right')

    yticklabels = [l.get_text()[0:-7] for l in ax.get_yticklabels()]
    t = pd.DataFrame(yticklabels).reset_index()
    t1 = t.groupby(0)['index'].mean().astype(int).reset_index()
    t.insert(0, 'pos', t[0].map(dict(zip(t1[0], t1['index']))))
    t = t[[0, 'pos', 'index']]
    t[0] = np.where(t.pos == t['index'], t[0], '')
    test = t[0].to_list()

    ax.set_yticks(ax.get_yticks())
    ax.set_yticklabels(test, size=15)
    ax.set_ylabel('HEALTH FACILITY')
    ylabel_mapping = OrderedDict()
    for adm1, hf_uid in df.index:
        ylabel_mapping.setdefault(adm1, [])
        ylabel_mapping[adm1].append(hf_uid)
    hline = []
    new_ylabels = []
    for adm1, hf_list in ylabel_mapping.items():
        hf_list[0] = "{} - {}".format(adm1, hf_list[0])
        new_ylabels.extend(hf_list)
        if hline:
            hline.append(len(hf_list) + hline[-1])
        else:
            hline.append(len(hf_list))
    plt.hlines(hline, xmin=-10, xmax=0, color="grey", linewidth=2, clip_on=False)
    fig.tight_layout()

    # Save to BytesIO and return
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_data = buf.getvalue()
    return img_data



###################################################
def plot_heatmap(df1, title):
    cmap = ListedColormap(['lightcoral', 'gold', 'limegreen'])
    fig, ax = plt.subplots(figsize=(30, 20))
    sns.heatmap(ax=ax, data=df1, cmap=cmap, cbar=None)
    ax.set_xlabel('')
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='right')

    yticklabels = [l.get_text()[0:-7] for l in ax.get_yticklabels()]
    t = pd.DataFrame(yticklabels).reset_index()
    t1 = t.groupby(0)['index'].mean().astype(int).reset_index()
    t.insert(0, 'pos', t[0].map(dict(zip(t1[0], t1['index']))))
    t = t[[0, 'pos', 'index']]
    t[0] = np.where(t.pos == t['index'], t[0], '')
    test = t[0].to_list()

    ax.set_yticks(ax.get_yticks())
    ax.set_yticklabels(test, size=15)
    ax.set_ylabel('HEALTH FACILITY')
    ylabel_mapping = OrderedDict()
    for adm1, hf_uid in df.index:
        ylabel_mapping.setdefault(adm1, [])
        ylabel_mapping[adm1].append(hf_uid)
    hline = []
    new_ylabels = []
    for adm1, hf_list in ylabel_mapping.items():
        hf_list[0] = "{} - {}".format(adm1, hf_list[0])
        new_ylabels.extend(hf_list)
        if hline:
            hline.append(len(hf_list) + hline[-1])
        else:
            hline.append(len(hf_list))
    plt.hlines(hline, xmin=-10, xmax=0, color="grey", linewidth=2, clip_on=False)
    fig.tight_layout()

    # Save to BytesIO and return
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_data = buf.getvalue()
    return img_data



#######################################################


st.sidebar.title("Analysis Options")
analysis_option = st.sidebar.radio("Select Analysis Option", ["None","Reporting Status by HF and Key variables"])

if analysis_option == "Reporting Status by HF and Key variables":
    uploaded_file = st.file_uploader("Please upload your clean data management file", type=["csv", "xlsx"])
    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df0 = pd.read_csv(uploaded_file)
        else:
            df0 = pd.read_excel(uploaded_file)

        # Update DataFrame with adm3_uid
        df0 = create_adm3_uid(df0)

        # Save DataFrame to session state
        st.session_state.df0 = df0

        # Process data
        df0, reporting_monthly, excel_data, excel_file_name = process_data(df0)

        # Generate and display heatmap

        # Step 1: Filter out HFs that have never reported
        df_filtered = df0.groupby(['adm1', 'hf_uid']).filter(lambda x: x['reported_detail'].sum() > 0)

        df1=df0.groupby(['adm1', 'hf_uid']).filter(lambda x: x['reported_detail'].sum() >= 0)

        # Step 2: Generate the heatmap
        df = (df_filtered.pivot(index=['adm1', 'hf_uid', 'first_month_reported'], columns='YM', values='reported_detail')
                      .sort_values(by=['adm1', 'first_month_reported']))

        df1 = (df1.pivot(index=['adm1', 'hf_uid', 'first_month_reported'], columns='YM', values='reported_detail')
                      .sort_values(by=['adm1', 'first_month_reported']))


        df = df.reset_index().drop(['first_month_reported'], axis=1).set_index(['adm1', 'hf_uid'])

        df1 = df1.reset_index().drop(['first_month_reported'], axis=1).set_index(['adm1', 'hf_uid'])

        # Step 3: Plot and display the heatmap
        img_data1 = plot_heatmap(df1, 'Reports Traffic Light Heatmap Sorted ADM1')
        st.image(img_data1, caption='Reports Traffic Light Heatmap Sorted ADM1 including all HFs')

########################################################################################################
        img_data = plot_heatmap(df, 'Reports Traffic Light Heatmap Sorted ADM1')
        st.image(img_data, caption='Reports Traffic Light Heatmap Sorted ADM1 including active HFs')




        # Monthly reporting rate by variable heatmaps
        d = {'Outpatient': ['allout', 'test', 'conf', 'pres', 'maltreat'],
             'Inpatient': ['maladm', 'maldth']}

        for i, variables in d.items():
            t = df0[df0.hf_wards == i] if i == 'Inpatient' else df0.copy()
            for c in variables:
                t[f'{c}_reported'] = np.where(t[c].isnull(), False, True)

            cols = [f'{c}_reported' for c in variables]
            t = t.groupby('YM')[cols].sum().reset_index()
            t = t.merge(reporting_monthly[i], on='YM', how='outer', validate='1:1')
            for c in cols:
                t[f'{c[0:-9]}_RR'] = 100 * t[c].div(t['denominator'])

            cols = [f'{c[0:-9]}_RR' for c in cols]
            t = t[['YM'] + cols].set_index('YM').T

            h = 4 if i == 'Inpatient' else 4
            fig, ax = plt.subplots(figsize=(8, h))
            sns.heatmap(ax=ax, data=t, cmap='Spectral', vmin=0, vmax=100, cbar_kws={'label': '%'})
            ax.set_xlabel('')
            ax.set_xticks(ax.get_xticks())
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='right')
            ax.set_yticks(ax.get_yticks())
            ax.set_yticklabels([l.get_text()[0:-3] for l in ax.get_yticklabels()], rotation=0, ha='right')
            ax.set_title(f'{i} Variables')

            fig.tight_layout()
            buf = BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            img_data = buf.getvalue()
            st.image(img_data, caption=f'Monthly Reporting Rate by Variable Heatmap ({i})')

     

        # Calculating confirmed variable
        reporting_monthly_adm3 = {}
        for chiefdom in df0.adm3_uid.unique():
            t = df0[df0.adm3_uid == chiefdom]
            t = (t[['YM', 'hf_uid', 'hf_active']]
                 .groupby(['YM'])['hf_active'].sum()
                 .to_frame()
                 .reset_index()
                 .rename(columns={'hf_active': 'denominator'}))
            reporting_monthly_adm3[chiefdom] = t

        t = df0[['adm3_uid', 'hf_uid']].drop_duplicates()
        t = t.groupby(['adm3_uid'])['hf_uid'].count().reset_index()
        d_chiefdoms = dict(zip(t.adm3_uid, t.hf_uid))

        for denominator in ['ActiveHFsDenominator']:
            df = df0.copy()
            df['conf_reported'] = np.where(df['conf'].isnull(), False, True)

            df = df.groupby(['adm1', 'adm2', 'adm3', 'adm3_uid', 'YM'])['conf_reported'].sum().reset_index()
            if denominator == 'AllHFsDenominator':
                df.insert(0, 'denominator', df.adm3_uid.map(d_chiefdoms))
            else:
                def temp(x):
                    t = reporting_monthly_adm3[x.adm3_uid]
                    return t[t.YM == x.YM].denominator.values[0]

                df.insert(0, 'denominator', df.apply(lambda x: temp(x), axis=1))

            df['conf_RR'] = 100 * df['conf_reported'].div(df['denominator'])

            df['TPR']= 100 * df['conf'].div(df['test'])

            df = (df.pivot(index=['adm1', 'adm2', 'adm3', 'adm3_uid'], columns='YM', values='conf_RR')
                  .sort_values(by=['adm1', 'adm3_uid']))

            df = df.reset_index().drop(['adm2', 'adm3'], axis=1).set_index(['adm1', 'adm3_uid'])

            fig, ax = plt.subplots(figsize=(30, 15))
            sns.heatmap(ax=ax,
                        data=df,
                        cmap='Spectral',
                        vmin=0,
                        vmax=100,
                        cbar_kws={'label': '%'})
            ax.set_xlabel('')
            ax.set_xticks(ax.get_xticks())
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='right')

            yticklabels = [l.get_text()[0:-12] for l in ax.get_yticklabels()]

            t = pd.DataFrame(yticklabels).reset_index()
            t1 = t.groupby(0)['index'].mean().astype(int).reset_index()
            t.insert(0, 'pos', t[0].map(dict(zip(t1[0], t1['index']))))
            t = t[[0, 'pos', 'index']]
            t[0] = np.where(t.pos == t['index'], t[0], '')
            test = t[0].to_list()



            ax.set_yticklabels(ax.get_yticklabels(), rotation=0, ha='right')
            ax.set_yticklabels(test, size=20)
            ax.set_ylabel('CHIEFDOMS')


            ylabel_mapping = OrderedDict()
            for adm1, adm3_uid in df.index:
                ylabel_mapping.setdefault(adm1, [])
                ylabel_mapping[adm1].append(adm3_uid)

            hline = []
            new_ylabels = []

            for adm1, adm3_list in ylabel_mapping.items():
                hf_list = []
                hf_list.append(f"{adm1} - {adm3_list[0]}")
                new_ylabels.extend(adm3_list)

                if hline:
                    hline.append(len(adm3_list) + hline[-1])
                else:
                    hline.append(len(adm3_list))

            plt.hlines(hline, xmin=-10, xmax=0, color="black", linewidth=4, clip_on=False)

            # Display the plot in Streamlit
            st.pyplot(fig)



##########################################################################
import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import tempfile
import numpy as np

# Sidebar: Analysis Options
analysis_option = st.sidebar.radio(
    "Choose an Analysis Option",
    ("None", "Geospatial Analysis")
)

# If Geospatial Analysis is selected
if analysis_option == "Geospatial Analysis":

    # Step 1: Upload Clean Excel File
    uploaded_file = st.file_uploader("Upload Clean Excel File", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.write("Uploaded Data:", df.head())

        # Step 2: Group by adm3 and Year, Create DataFrame for Each Year
        grouped_df = df.groupby(['adm1', 'adm2', 'adm3', 'Year']).sum().reset_index()

        # Step 3: Upload Chiefdom Data Excel
        uploaded_chiefdom_file = st.file_uploader("Upload Chiefdom Data (Chiefdom_data.xlsx)", type=["xlsx"])
        if uploaded_chiefdom_file:
            chiefdom_df = pd.read_excel(uploaded_chiefdom_file)
            st.write("Chiefdom Data:", chiefdom_df.head())

            # Step 4: Merge Each Yearly DataFrame with Chiefdom Data
            unique_years = grouped_df['Year'].unique()
            yearly_dfs = {}

            for year in unique_years:
                year_df = grouped_df[grouped_df['Year'] == year]
                merged_df = pd.merge(year_df, chiefdom_df, how='left', on='adm3')
                yearly_dfs[year] = merged_df
                st.write(f"Merged Data for Year {year}:", merged_df.tail())

            # Step 5: Upload Shapefile Components (.shp, .shx, .dbf, etc.)
            uploaded_shapefile = st.file_uploader("Upload Shapefile Components", type=["shp", "shx", "dbf", "prj"], accept_multiple_files=True)

            if uploaded_shapefile:
                # Dictionary to store file paths
                shapefile_dict = {}

                for file in uploaded_shapefile:
                    file_name = file.name
                    if file_name.endswith('.shp'):
                        shapefile_dict['shp'] = file
                    elif file_name.endswith('.shx'):
                        shapefile_dict['shx'] = file
                    elif file_name.endswith('.dbf'):
                        shapefile_dict['dbf'] = file
                    elif file_name.endswith('.prj'):
                        shapefile_dict['prj'] = file

                # Ensure that the mandatory shapefile components are uploaded
                if all(key in shapefile_dict for key in ['shp', 'shx', 'dbf']):
                    # Create a temporary directory to save uploaded files
                    with tempfile.TemporaryDirectory() as tmp_dir:
                        for key, file in shapefile_dict.items():
                            file_path = os.path.join(tmp_dir, file.name)
                            with open(file_path, "wb") as f:
                                f.write(file.getbuffer())

                        # Load the shapefile using geopandas
                        shp_path = os.path.join(tmp_dir, shapefile_dict['shp'].name)
                        gdf = gpd.read_file(shp_path)
                        st.write("Geospatial Data:", gdf.tail())

                        # Step 6: Merge with Geospatial Data
                        for year, merged_df in yearly_dfs.items():
                            # Merge with geospatial data on ['FIRST_DNAM', 'FIRST_CHIE']
                            merged_gdf = pd.merge(gdf, merged_df, how='left', on=['FIRST_DNAM', 'FIRST_CHIE'], validate="1:1")
                            st.write(f"Merged Geospatial Data for Year {year}:", merged_gdf.head())

                            # Step 7: Create Map for Each Year for Variables like 'allout', 'susp', 'test', 'maltreat', 'pres'
                            for var in ['allout', 'susp', 'test', 'maltreat', 'pres']:
                                fig, ax = plt.subplots(figsize=(10, 10))
                                merged_gdf.plot(column=var, cmap='Set3', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
                                # Plot the FIRST_DNAM boundaries in white
                                merged_gdf.boundary.plot(ax=ax, color='black', linewidth=1)
                                merged_gdf.dissolve(by='FIRST_DNAM').boundary.plot(ax=ax, color='white', linewidth=3)



                                ax.set_title(f"Map for '{var}' in Year {year}")
                                ax.set_axis_off()
                                st.pyplot(fig)

                            # Get unique FIRST_DNAMs
                            unique_dnam = merged_gdf['FIRST_DNAM'].unique()

                            for dnam in unique_dnam:
                                # Filter data for the current FIRST_DNAM
                                dnam_gdf = merged_gdf[merged_gdf['FIRST_DNAM'] == dnam]

                                fig, ax = plt.subplots(figsize=(10, 10))
                                dnam_gdf.plot(column=var, cmap='Set3', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

                                # Plot boundaries of each 'FIRST_CHIE'
                                dnam_gdf.boundary.plot(ax=ax, color='black', linewidth=1)

                                # Plot boundaries of each 'FIRST_CHIE' with a distinct color
                                dnam_gdf.dissolve(by='FIRST_CHIE').boundary.plot(ax=ax, color='white', linewidth=3)

                                # Add labels for each 'FIRST_CHIE' within the 'FIRST_DNAM'
                                for idx, row in dnam_gdf.iterrows():
                                    x, y = row.geometry.centroid.x, row.geometry.centroid.y
                                    label = row['FIRST_CHIE']
                                    ax.text(x, y, label, fontsize=8, ha='center', color='black',
                                            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

                                ax.set_title(f"Map of {dnam} for '{var}' in Year {year}")
                                ax.set_axis_off()
                                st.pyplot(fig)
