import streamlit as st
import pandas as pd
from io import BytesIO

from utilities import make_dataframes

st.title(':blue[Enter your data here]')
st.write('')
with st.container():
    with st.expander('Enter Data for File 1'):
        # File 1
        st.subheader('File 1')
        prefs1 = st.number_input('Enter # of preferences for file 1 objects', min_value=1, value=3)

        if 'data1' not in st.session_state or st.session_state['data1'] is None:
            data1 = []
        else:
            data1 = st.session_state['data1']

        with st.form('File 1'):
            prefs = []
            option_name = st.text_input('Enter Name of Option')
            for i in range(prefs1):
                pref = st.text_input(f'Enter pref {i+1}')
                prefs.append(pref)
            submit = st.form_submit_button('Add to file', type='primary')
            if submit:
                row_data = [option_name] + [p for p in prefs]
                data1.append(row_data)
                st.session_state['data1'] = data1

    with st.expander('Enter Data for File 2'):
        # File 2
        st.subheader('File 2')
        prefs2 = st.number_input('Enter # of preferences for file 2 objects', min_value=1, value=3)

        if 'data2' not in st.session_state or st.session_state['data2'] is None:
            data2 = []
        else:
            data2 = st.session_state['data2']

        with st.form('File 2'):
            prefs = []
            option_name = st.text_input('Enter Name of Option')
            for i in range(prefs2):
                pref = st.text_input(f'Enter pref {i+1}')
                prefs.append(pref)
            submit = st.form_submit_button('Add to file', type='primary')
            if submit:
                row_data = [option_name] + [p for p in prefs]
                data2.append(row_data)
                st.session_state['data2'] = data2

st.write('---')

with st.expander('Download Data Files'):
    st.write('It is strongly recommended to download files')
    download = st.button('Download', type='primary')
    if download:
        make_dataframes(st.session_state['data1'], st.session_state['data2'])

        def convert_df_to_excel(df):
            output = BytesIO()
            # Use ExcelWriter to save DataFrame to Excel in memory
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            output.seek(0)  # Set pointer to the beginning of the file
            return output

        # Create data for Excel file
        excel_data1 = convert_df_to_excel(st.session_state['df1'])
        excel_data2 = convert_df_to_excel(st.session_state['df2'])

        # Provide download button for the Excel file 1
        st.download_button(
            label="Download file 1 as Excel",
            type='secondary',
            data=excel_data1,
            file_name='file1.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        # Provide download button for the Excel file 2
        st.download_button(
            label="Download file 2 as Excel",
            type='secondary',
            data=excel_data2,
            file_name='file2.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

st.write('---')

finished = st.button('Continue to match process', type='primary')
if finished:
    make_dataframes(st.session_state['data1'], st.session_state['data2'])
    st.switch_page('pages/run_process.py')

