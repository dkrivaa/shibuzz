import streamlit as st
import time

from data_tests import data_integrity
from match_engine import match

try:
    df1 = st.session_state['df1']
    df2 = st.session_state['df2']

    with st.expander('See your data'):
        with st.container():
            st.subheader('File 1')
            st.write(df1)

        with st.container():
            st.subheader('File 2')
            st.write(df2)

    st.write('---')

    with st.container(border=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.subheader('Data checks:')
        with col2:
            checks = st.button('Check data', type="primary")

    if checks:
        tests = data_integrity(df1, df2)
        with st.container():
            if tests[1] == 0:
                st.success('Passed all checks. Continuing to match process')
                try:
                    match_result = match(df1, df2)
                    with st.spinner('Running Match Algorithm.....'):
                        time.sleep(5)
                    st.session_state['match_result'] = match_result
                    st.page_link('pages/results.py', label='Go To Results')

                except:
                    st.write('Something went wrong.')

            else:
                st.warning(f'{tests[0]}. Please correct the problem and upload files again')
                st.page_link('pages/home.py', label='Go To Upload Page')

except:
    st.subheader('Please start by uploading files or enter data')
    st.page_link('pages/home.py', label='Go To Upload Page')