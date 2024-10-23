import streamlit as st

# Site Pages
home_page = st.Page(
    page='pages/home.py',
    title='Upload Files',
    default=True
    )

run_process = st.Page(
    page='pages/run_process.py',
    title='Run Match Process'
    )

result_page = st.Page(
    page='pages/results.py',
    title='Results',
    )

enter_data_page = st.Page(
    page='pages/enter_data.py',
    title='Enter Data',
    )

example_file_page = st.Page(
    page='pages/example_file.py',
    title='Example File'
    )

# Navigation
pg = st.navigation(pages={
    'Run Match Algorithm': [home_page, run_process, result_page,],
    'Prepare Data': [enter_data_page, example_file_page]
    })
pg.run()
