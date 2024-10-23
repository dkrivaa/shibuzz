import streamlit as st
import pandas as pd
from io import BytesIO

try:
    results = st.session_state['match_result']

    df = pd.DataFrame(results[0], columns=['file1', 'file2'])

    st.subheader('Your Results:')
    st.dataframe(df, hide_index=True)

    st.write('---')

    st.subheader('Summary:')
    st.write(f'File 1: :blue[{results[1][0]}] out of :blue[{results[1][1]}] got one of preferred options')
    st.write(f'File 2: :blue[{results[2][0]}] out of :blue[{results[2][1]}] got one of preferred options')

    st.write('---')

    # Function to convert DataFrame to Excel and return as a downloadable file
    def convert_df_to_excel(df):
        output = BytesIO()
        # Use ExcelWriter to save DataFrame to Excel in memory
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)  # Set pointer to the beginning of the file
        return output

    # Create data for Excel file
    excel_data = convert_df_to_excel(df)

    # Provide download button for the Excel file
    st.download_button(
        label="Download results as Excel",
        type='primary',
        data=excel_data,
        file_name='results.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode("utf-8")

    csv = convert_df(df)

    st.download_button(
        label="Download results as CSV",
        type='primary',
        data=csv,
        file_name="results.csv",
        mime="text/csv",
    )

except:
    st.subheader('Please start by uploading files or enter data')
    st.page_link('pages/home.py', label='Go To Upload Page')
