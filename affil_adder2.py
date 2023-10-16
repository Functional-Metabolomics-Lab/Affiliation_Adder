# Import necessary libraries
import streamlit as st
import pandas as pd
from io import StringIO
import base64

# Superscript mapping for numbers
SUPERSCRIPT_MAP = {
    '0': '⁰',
    '1': '¹',
    '2': '²',
    '3': '³',
    '4': '⁴',
    '5': '⁵',
    '6': '⁶',
    '7': '⁷',
    '8': '⁸',
    '9': '⁹',
    ',': '⁺'
}

def to_superscript(number_or_comma):
    """Convert a number or comma to its superscript representation."""
    return ''.join([SUPERSCRIPT_MAP[digit] for digit in str(number_or_comma)])

# Function to download the results as a txt file
def download_link(content, filename, text):
    buffer = StringIO()
    buffer.write(content)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read().encode()).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{text}</a>'

def superscript_comma(content):
    """Convert normal commas to pseudo-superscript using CSS."""
    return content.replace('+', '<span style="position: relative; top: -0.5em;">,</span>')

def main():
    st.title("AffilAdder: Author Affiliation Linker")

    uploaded_file = st.file_uploader("Upload your Excel file", type=['xlsx'])

    if uploaded_file is not None:
        # Read the Excel file
        df = pd.read_excel(uploaded_file)

        # Collect unique affiliations in order
        affiliations = []
        for _, row in df.iterrows():
            for column in ["Affiliation1", "Affiliation2", "Affiliation3"]:
                if pd.notna(row[column]) and row[column] not in affiliations:
                    affiliations.append(row[column])
                    
        # Associate authors with affiliation indices
        author_strings = []
        for _, row in df.iterrows():
            affil_indices = [affiliations.index(row[column]) + 1 for column in ["Affiliation1", "Affiliation2", "Affiliation3"] if pd.notna(row[column])]
            affiliation_string = to_superscript(','.join([str(i) for i in affil_indices]))
            author_string = f"{row['Author']}{affiliation_string}"
            author_strings.append(author_string)
            
        # Combine author strings with commas
        authors_text = ', '.join(author_strings)
        
        # List affiliations at the end
        affiliation_strings = [f"{i+1}. {affiliation}" for i, affiliation in enumerate(affiliations)]
        
        # Compile the entire content
        combined_text = authors_text + '\n\n' + '\n'.join(affiliation_strings)
        
        # Display and provide download link
        combined_html = superscript_comma(combined_text)
        st.markdown(combined_html, unsafe_allow_html=True)
        st.markdown(download_link(combined_text.replace('+', ','), 'author_affiliations.txt', 'Click here to download the text file'), unsafe_allow_html=True)

if __name__ == "__main__":
    main()