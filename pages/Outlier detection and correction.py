# Main App
st.title("Outlier Detection and Correction")

if data_management_option == "Outlier Detection and Correction":
    st.header("Select Columns for Outlier Detection")

    if st.session_state.df is None:
        st.warning("No dataset available. Please upload your dataset.")
        uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
        if uploaded_file:
            if uploaded_file.name.endswith(".csv"):
                st.session_state.df = pd.read_csv(uploaded_file)
            else:
                st.session_state.df = pd.read_excel(uploaded_file)
            st.session_state.df['year_mon'] = pd.to_datetime(st.session_state.df['Year'].astype(str) + '-' + st.session_state.df['Month'].astype(str), format='%Y-%m')
            st.success("Dataset uploaded successfully!")
            st.dataframe(st.session_state.df)

    if st.session_state.df is not None:
        # User selects adm1, adm3, Year, Month, hf
        adm1 = st.selectbox("Select adm1:", st.session_state.df['adm1'].unique())
        adm3_options = st.session_state.df[st.session_state.df['adm1'] == adm1]['adm3'].unique()
        adm3 = st.selectbox("Select adm3:", adm3_options)
        Year_options = st.session_state.df[(st.session_state.df['adm1'] == adm1) & (st.session_state.df['adm3'] == adm3)]['Year'].unique()
        Year = st.selectbox("Select Year:", Year_options)
        Month_options = st.session_state.df[(st.session_state.df['adm1'] == adm1) & (st.session_state.df['adm3'] == adm3) & (st.session_state.df['Year'] == Year)]['Month'].unique()
        Month = st.selectbox("Select Month:", Month_options)
        hf_options = st.session_state.df[(st.session_state.df['adm1'] == adm1) & (st.session_state.df['adm3'] == adm3) & (st.session_state.df['Year'] == Year) & (st.session_state.df['Month'] == Month)]['hf'].unique()
        hf = st.multiselect("Select hf:", hf_options)

        # Filter data based on selected values
        filtered_df = st.session_state.df[(st.session_state.df['adm1'] == adm1) &
                                          (st.session_state.df['adm3'] == adm3) &
                                          (st.session_state.df['Year'] == Year) &
                                          (st.session_state.df['Month'] == Month) &
                                          (st.session_state.df['hf'].isin(hf))]

        # User selects the numeric column for outlier detection and correction
        numeric_column = st.selectbox("Select a Numeric Column for Outlier Detection:", filtered_df.select_dtypes(include='number').columns)

        if numeric_column:
            st.write("Outliers will be detected and visualized for the selected categorical values.")

            if st.button("Generate Outlier Report"):
                word_buffer = BytesIO()  # Create a buffer for the Word file
                excel_buffer = BytesIO()  # Create a buffer for the Excel file
                document = Document()

                outlier_data = pd.ExcelWriter(excel_buffer, engine='xlsxwriter')

                # Prepare the zip archive for the output files
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w') as zf:
                    # Create a subplot for detection and correction for each unique hf
                    unique_hfs = hf
                    for unique_hf in unique_hfs:
                        hf_filtered_df = filtered_df[filtered_df['hf'] == unique_hf]
                        fig = create_subplot_for_outlier_detection_and_correction(hf_filtered_df, numeric_column, adm1, adm3, Year, unique_hf)

                        # Display the figure in Streamlit
                        st.pyplot(fig)

                        # Save plot as image to add to Word document
                        img_buffer = BytesIO()
                        fig.savefig(img_buffer, format='png')
                        img_buffer.seek(0)

                        # Add a paragraph before the image
                        document.add_paragraph(f'Outlier Detection and Correction for adm1 = {adm1}, adm3 = {adm3}, Year = {Year}, Month = {Month}, hf = {unique_hf}')
                        document.add_picture(img_buffer, width=Inches(5))
                        plt.close(fig)  # Close the plot to avoid memory issues

                    # Save the Word document
                    document.save(word_buffer)

                    # Close the Excel writer (finalize the file)
                    outlier_data.close()

                    # Write Word and Excel to zip
                    zf.writestr('outliers_report.docx', word_buffer.getvalue())
                    zf.writestr('outliers_data.xlsx', excel_buffer.getvalue())

                st.success("Outliers processed successfully!")
                # Offer the zip file for download
                st.download_button(
                    label="Download ZIP file with Word Report and Outliers",
                    data=zip_buffer.getvalue(),
                    file_name='outliers_results.zip',
                    mime='application/zip'
                )
