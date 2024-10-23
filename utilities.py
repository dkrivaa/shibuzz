import streamlit as st
import chardet
from io import StringIO
import pandas as pd


# Checking csv file encoding and making csv string
def encoding_csv(file):
    # Open the file in binary mode and read a chunk to detect encoding
    # Read the uploaded file in binary mode to detect encoding
    raw_data = file.read()

    # Use chardet to detect the encoding
    result = chardet.detect(raw_data)

    # Display the detected encoding and confidence level
    encoding = result['encoding']
    # Decode content to string using detected encoding (if not None) and re-encode as utf-8
    if encoding:
        text_data = raw_data.decode(encoding)
    else:
        text_data = raw_data.decode('utf-8')

    # Use StringIO to load the content into memory as a file-like object
    csv_data = StringIO(text_data)

    return csv_data


# Read file content
def read_file(file):
    if file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        df = pd.read_excel(file)
    elif file.type == 'text/csv':
        csv_data = encoding_csv(file)
        # Load the CSV content into a pandas DataFrame
        df = pd.read_csv(csv_data)

    return df


# make dataframe from data entered
def make_dataframes(data1, data2):
    data1 = st.session_state['data1']
    data2 = st.session_state['data2']

    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    st.session_state['df1'] = df1
    st.session_state['df2'] = df2
