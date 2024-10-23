import streamlit as st
import pandas as pd

st.title('Example File')

data = [
    ['open position 1', 'candidate 1', 'candidate 2', 'candidate 3'],
    ['open position 2', 'candidate 4', 'candidate 5', 'candidate 6'],
    ['open position 3', 'candidate 4', 'candidate 3', 'candidate 1'],
    ['open position 4', 'candidate 3', 'candidate 5', 'candidate 6']
]

df = pd.DataFrame(data, columns=['object', 'preference 1', 'preference 2','preference 3'])
st.write("""
    Below is an example of the structure of the files. In each of the files, the first column contains the 
    objects to be matched, in this case 4 open positions, followed by the corresponding preferences from the 
    opposite set. 
    The file for the opposite set will have 6 rows with the first column consisting of the 6 candidates 
    followed by the columns with their preferences regarding the 4 open positions.
    
    :blue[The files to upload can be Excel or CSV.]
    
    After the files are uploaded the integrity of the data will be checked in three distinct ways:
    
    1. The number of objects in File 1 has to be smaller or equal to the number of objects in File 2.
    2. There can be no duplicates in the preferences of any object, each object has to have 3 distinct preferences.
    3. All preferences have to be one of the objects in the opposite set. 
    
    
""")

st.write('---')
st.write(df)
st.write('---')


