import streamlit as st
import pandas as pd

# Function to load data from file
def load_data():
    try:
        data = pd.read_csv('user_data1.csv')
    except FileNotFoundError:
        data = pd.DataFrame(columns=['Gender', 'Occupation Role', 'Grade', 'Years in Civil Service', 'Years in Current Position', 'Highest Degree', 'Age Group', 'Supervise Staff', 'Number Supervised', 'Change Employment', 'Retirement Timeline'])
    return data

# Function to save data to file
def save_data(data):
    data.to_csv('user_data1.csv', index=False)

# Page 1: Data Collection Form
def data_collection_page():
    st.title("Data Collection Form")

    # Load existing data
    data_container = load_data()

    # Using st.form to reset form fields after submission
    with st.form("data_collection_form"):
        gender = st.selectbox("Q1. Gender", ["", "Female", "Male"], key="gender")
        occupation_role = st.selectbox("Q2. Main Occupation Role", [
            "", "Public Health Practitioner",
            "Clinical Practitioner",
            "Nursing Practitioner",
            "Allied Health Practitioner",
            "Professional Administrative Staff"
        ], key="occupation_role")
        grade = st.selectbox("Q3. Select your grade in the civil service", ["", "Grade 9", "Grade 10", "Grade 11", "Grade 12", "Grade 13", "Grade 14"], key="grade")
        years_in_civil_service = st.number_input("Q4. How many years have you been employed at the civil service?", min_value=0, key="years_in_civil_service")
        years_in_current_position = st.number_input("Q5. How many years have you been in your current position at MoH?", min_value=0, key="years_in_current_position")
        highest_degree = st.selectbox("Q6. What is your highest degree earned?", ["", "Professional diploma", "Bachelor", "Masters", "Doctorate"], key="highest_degree")
        age_group = st.selectbox("Q7. Your age group", ["", "Under 29", "30-39", "40-49", "50-59", "Above 59 years"], key="age_group")
        supervise_staff = st.selectbox("Q8. In your current role, do you directly supervise other staff?", ["", "Yes", "No"], key="supervise_staff")
        num_supervised = st.number_input("If yes, how many staff do you directly supervise?", min_value=0, key="num_supervised") if supervise_staff == "Yes" else None
        change_employment = st.selectbox("Q9. Do you expect to change the place of your employment within the next 5 years?", ["", "Not at all", "I am not sure", "Possibly yes", "Certainly yes"], key="change_employment")
        retirement_timeline = st.selectbox("Q10. When do you expect to retire?", ["", "In the next 0-5 years", "In the next 6-10 years", "In more than 15 years"], key="retirement_timeline")

        submit_button = st.form_submit_button("Submit")
       

        if submit_button:
            # Save data and move to the next page
            submitted_data = {
                "Gender": gender,
                "Occupation Role": occupation_role,
                "Grade": grade,
                "Years in Civil Service": years_in_civil_service,
                "Years in Current Position": years_in_current_position,
                "Highest Degree": highest_degree,
                "Age Group": age_group,
                "Supervise Staff": supervise_staff,
                "Number Supervised": num_supervised if supervise_staff == "Yes" else None,
                "Change Employment": change_employment,
                "Retirement Timeline": retirement_timeline,
            }

            # Append the submitted data to the session state
            data_container = load_data()
            data_container = pd.concat([data_container, pd.DataFrame([submitted_data])], ignore_index=True)
            save_data(data_container)

         

# Page 2: Display All Data
def display_all_data_page():
    st.title("All Submitted Data")

    # Display all submitted data
    data_container = load_data()
    st.write(data_container)  # Use st.write instead of st.dataframe

    # Save data to CSV
    if st.button("Download All Data as CSV"):
        save_data(data_container)
        st.success("All data downloaded successfully!")

# Page 3: Data Analysis
def data_analysis_page():
    st.title("Data Analysis")

    # Display individual bar charts for each variable
    if not load_data().empty:
        st.subheader("Interactive Bar Charts")

        # Create a DataFrame with the submitted data
        data_df = load_data()

        # Display individual bar charts for each variable
        for variable in data_df.columns:
            st.subheader(f"{variable} Bar Chart")

            if data_df[variable].dtype == "object":  # Check if the variable is categorical
                value_counts = data_df[variable].value_counts()
                st.bar_chart(value_counts)

                # If you want to display the exact counts, uncomment the following line:
                # st.write(value_counts)

            else:
                st.bar_chart(data_df[variable])

# Streamlit App
def main():
    st.set_page_config(page_title="MoH Data Collection App", layout="wide")

    # Page navigation
    pages = {
        "Data Collection": data_collection_page,
        "Display All Data": display_all_data_page,
        "Data Analysis": data_analysis_page,
    }

    page = st.sidebar.selectbox("Select Page", list(pages.keys()))

    # Execute the selected page
    pages[page]()

if __name__ == "__main__":
    main()
