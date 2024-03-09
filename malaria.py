import streamlit as st
import pandas as pd
from datetime import datetime

# Load or create the initial drug inventory and usage data
inventory_data = {
    'Name of PHU': ['A', 'B', 'C', 'D', 'E'],
    'Month': ['January', 'February', 'March', 'April', 'May'],
    'Name of drug': ['Malaria', 'HIV', 'Malaria', 'TB', 'HIV'],
    'Number of drug supply': [600, 400, 200, 300, 400],
    'Date Supplied': ['21/03/2024'] * 5,
    'Confirmed by': ['Mohamed', 'Musa', 'Mohamed', 'Musa', 'Alie']
}

usage_data = {
    'Name of PHU': [],
    'Name of patient': [],
    'Age': [],
    'Sex': [],
    'Pregnant': [],
    'Months Pregnant': [],
    'Date Submitted': [],
    'Month Submitted': [],
    'Name of drug': [],
    'Quantity Used': []
}

# CSV file paths
inventory_file_path = 'drug_inventory12.csv'
usage_file_path = 'drug_usage_records12.csv'

# Load or create DataFrames from CSV files
try:
    inventory_df = pd.read_csv(inventory_file_path)
    usage_df = pd.read_csv(usage_file_path)
except FileNotFoundError:
    inventory_df = pd.DataFrame(inventory_data)
    usage_df = pd.DataFrame(usage_data)

# Streamlit UI
def main():
    st.title("Drug Inventory and Usage Tracking System")

    menu = ["View Drug Inventory", "Record Drug Usage", "Drug Usage Summary", "View Drug Usage"]
    choice = st.sidebar.selectbox("Select Action", menu)

    global inventory_df, usage_df  # Declare as global variables

    if choice == "View Drug Inventory":
        st.subheader("View Drug Inventory")
        view_inventory()

    elif choice == "Record Drug Usage":
        st.subheader("Record Drug Usage")
        inventory_df, usage_df = record_drug_usage()

    elif choice == "Drug Usage Summary":
        st.subheader("Drug Usage Summary")
        drug_usage_summary()

    elif choice == "View Drug Usage":
        st.subheader("View Drug Usage")
        view_drug_usage()

# Functions for data manipulation
def view_inventory():
    global inventory_df
    st.table(inventory_df.sort_values(by=['Name of PHU', 'Month', 'Name of drug', 'Number of drug supply']))

def record_drug_usage():
    global inventory_df, usage_df

    if inventory_df.empty:
        st.error("Error: The inventory is empty. Please ensure there is data in the inventory.")
        return inventory_df, usage_df  # Return original DataFrames

    phu_name = st.selectbox("Select PHU Name", inventory_df['Name of PHU'].unique())
    month = st.selectbox("Select Month", inventory_df['Month'].unique())
    drug_name = st.selectbox("Select Name of Drug", inventory_df['Name of drug'].unique())
    quantity_used = st.number_input("Enter Quantity Used", min_value=1, step=1)

    # Check if the selected quantity is available in the inventory
    available_quantity = inventory_df.loc[
        (inventory_df['Name of PHU'] == phu_name) &
        (inventory_df['Month'] == month) &
        (inventory_df['Name of drug'] == drug_name), 
        'Number of drug supply'
    ]

    if available_quantity.empty or quantity_used > available_quantity.values[0]:
        st.error("Insufficient quantity in the inventory.")
        return inventory_df, usage_df  # Return original DataFrames

    name_of_patient = st.text_input("Enter Name of Patient")
    age = st.number_input("Enter Age", min_value=0)
    sex = st.radio("Select Sex", ["Male", "Female"])

    pregnant = None
    months_pregnant = None

    if sex == "Female" and age > 13:
        pregnant = st.radio("Are you pregnant?", ["Yes", "No"])
        if pregnant == "Yes":
            months_pregnant = st.number_input("Enter Months Pregnant", min_value=1, step=1)

    if st.button("Submit"):
        date_submitted = datetime.now()
        month_submitted = date_submitted.strftime('%B')  # Extract month separately

        # Update usage DataFrame
        usage_df = pd.concat([usage_df, pd.DataFrame({
            'Name of PHU': [phu_name],
            'Name of patient': [name_of_patient],
            'Age': [age],
            'Sex': [sex],
            'Pregnant': [pregnant],
            'Months Pregnant': [months_pregnant],
            'Date Submitted': [date_submitted],
            'Month Submitted': [month_submitted],
            'Name of drug': [drug_name],
            'Quantity Used': [quantity_used],
            'Month': [month]
        })], ignore_index=True)

        # Update inventory DataFrame
        inventory_df.loc[(inventory_df['Name of PHU'] == phu_name) &
                          (inventory_df['Month'] == month) &
                          (inventory_df['Name of drug'] == drug_name),
                          'Number of drug supply'] == quantity_used

        # Save DataFrames to CSV files
        inventory_df.to_csv(inventory_file_path, index=False)
        usage_df.to_csv(usage_file_path, index=False)

        st.success("Drug usage recorded successfully!")

        # Automatically update the Drug Usage Summary
        drug_usage_summary()

    return inventory_df, usage_df  # Return updated DataFrames

def drug_usage_summary():
    global inventory_df, usage_df
    summary_df = pd.DataFrame(columns=['Name of PHU', 'Month', 'Name of drug', 'Total drugs supplied', 'Quantity Used', 'Drugs remaining'])

    for index, row in inventory_df.iterrows():
        phu_name = row['Name of PHU']
        month = row['Month']
        drug_name = row['Name of drug']
        total_supply = row['Number of drug supply']
        drugs_used = usage_df[(usage_df['Name of PHU'] == phu_name) & (usage_df['Month'] == month) & (usage_df['Name of drug'] == drug_name)]['Quantity Used'].sum()

        # Calculate drugs remaining
        drugs_remaining = total_supply - drugs_used

        summary_df = pd.concat([summary_df, pd.DataFrame({
            'Name of PHU': [phu_name],
            'Month': [month],
            'Name of drug': [drug_name],
            'Total drugs supplied': [total_supply],
            'Quantity Used': [drugs_used],
            'Drugs remaining': [drugs_remaining]
        })], ignore_index=True)

    st.table(summary_df.sort_values(by=['Name of PHU', 'Month', 'Name of drug']))

def view_drug_usage():
    global usage_df
    add_another_record = st.button("Add Another Record")
    if add_another_record:
        # Clear fields for entering a new record
        st.experimental_rerun()

    st.table(usage_df.sort_values(by=['Name of PHU', 'Month Submitted', 'Name of drug']))

if __name__ == "__main__":
    main()
