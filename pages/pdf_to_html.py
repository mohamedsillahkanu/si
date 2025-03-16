import streamlit as st
import os
import tempfile
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from io import StringIO
import base64

# Set page configuration
st.set_page_config(
    page_title="PDF to HTML Converter",
    page_icon="📄",
    layout="centered"
)

# App title and description
st.title("PDF to HTML Converter")
st.markdown("Upload a PDF file and convert it to HTML format.")

# Function to convert PDF to HTML
def convert_pdf_to_html(pdf_file):
    # Create a StringIO object to hold the HTML content
    output = StringIO()
    
    # Extract text from PDF to HTML format
    extract_text_to_fp(pdf_file, output, laparams=LAParams(), 
                      output_type='html', codec=None)
    
    # Return the HTML content
    return output.getvalue()

# Function to create a download link
def get_download_link(html_content, filename="converted.html"):
    """Generate a download link for the HTML content"""
    b64 = base64.b64encode(html_content.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="{filename}">Download HTML file</a>'
    return href

# File uploader widget
uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])

if uploaded_file is not None:
    # Display success message and file details
    st.success("File successfully uploaded!")
    file_details = {
        "Filename": uploaded_file.name,
        "File size": f"{uploaded_file.size / 1024:.2f} KB",
        "File type": uploaded_file.type
    }
    st.write("File Details:")
    for key, value in file_details.items():
        st.write(f"- {key}: {value}")
    
    # Add a convert button
    if st.button("Convert to HTML"):
        with st.spinner("Converting PDF to HTML..."):
            try:
                # Process the conversion
                html_content = convert_pdf_to_html(uploaded_file)
                
                # Show a preview of the HTML
                st.subheader("HTML Preview")
                with st.expander("Show HTML code"):
                    st.code(html_content[:2000] + ("..." if len(html_content) > 2000 else ""), language="html")
                
                # Display the HTML content
                st.subheader("Rendered HTML Preview")
                st.components.v1.html(html_content, height=400, scrolling=True)
                
                # Create a download link for the HTML file
                st.subheader("Download")
                output_filename = uploaded_file.name.rsplit('.', 1)[0] + ".html"
                st.markdown(get_download_link(html_content, output_filename), unsafe_allow_html=True)
                
                # Display success message
                st.success("Conversion completed successfully!")
                
            except Exception as e:
                st.error(f"Error during conversion: {str(e)}")
                st.info("Try with a different PDF file or check if the file is corrupted.")

else:
    # Display instructions when no file is uploaded
    st.info("Please upload a PDF file to convert it to HTML.")
    
    # Example of what the app does
    st.subheader("How it works")
    st.markdown("""
    1. Upload a PDF file using the file uploader above
    2. Click on the 'Convert to HTML' button
    3. Preview the HTML output
    4. Download the HTML file
    
    This app uses the pdfminer.six library to extract text and formatting from PDF files and convert them to HTML format.
    """)
    
    # Limitations section
    st.subheader("Limitations")
    st.markdown("""
    - Complex PDF layouts might not be perfectly preserved
    - Some formatting may be lost in the conversion process
    - Images in PDFs won't be extracted by default
    - Very large PDF files may take longer to process
    """)

# Add footer
st.markdown("---")
st.caption("PDF to HTML Converter | Built with Streamlit and pdfminer.six")
