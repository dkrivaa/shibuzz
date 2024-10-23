import pandas as pd
import streamlit as st
import time

from utilities import read_file

# #2668B7

with st.container():
    st.title(':blue[Shibuzz]')
    st.subheader('Upload your data, our algorithm will do the :blue[match]')
    with st.expander('Read more', ):
        st.write("""
            The match process involves using user defined data from two sets, 
            each represented in a separate file. 
            The structure of the two files are the same - 
            the first column with the names of the object to be matched 
            followed by a number of columns with that objects preferences in the opposite set.
            
            You can either upload the data files (Excel or CSV) below or enter your data online 
            (Go to 'Enter Data' page).
            
            :blue[With your data and our algorithm, you will have the best matches within seconds.]
        
        """)
st.write('---')

# Container with upload buttons
with st.container(border=True):
    st.subheader('Upload your files')
    file1 = st.file_uploader('Upload file 1', type=['xlsx', 'csv'], )
    file2 = st.file_uploader('Upload file 2', type=['xlsx', 'csv'], )

    col1, col2 = st.columns([4.2, 1])
    with col2:
        upload_button = st.button('Upload Files', type="primary")

# If all ok when pressing upload files button
if upload_button and file1 is not None and file2 is not None:
    # Reading content of files and making dataframes
    df1 = read_file(file1)
    df2 = read_file(file2)

    # Saving dataframes in session state
    st.session_state['df1'] = df1
    st.session_state['df2'] = df2

    message = st.success('Files uploaded successfully')
    time.sleep(2)
    st.switch_page('pages/run_process.py')

# If missing file
elif upload_button and (file1 is None or file2 is None):
    message = st.warning('File or files missing. Please upload both files')


