#Import the necessary packages
import streamlit as st
from pygwalker.api.streamlit import init_streamlit_comm

from src.util import preprocess_df, get_pyg_renderer, plot_corr
#Setting the web app page name
st.set_page_config(page_title='Exploratory Data Analysis App', 
                #    page_icon=":smiley", 
                   layout="wide"
                   )

#Injecting custom CSS for assigning theme to app
custom_css = """
body {
  background-color: #FFFFFF;
}

h1, h2, h3, h4, h5, h6 {
  color: #057A27;
}
"""
st.write('<style>' + custom_css + '</style>', unsafe_allow_html=True)

#Setting markdown
st.markdown("<h1 style='text-align: center;'>Exploratory Data Analysis: meteo data </h1>", unsafe_allow_html=True)

# st.divider()
#Creating dynamic file upload option in sidebar
uploaded_file = st.sidebar.file_uploader("*Upload file (csv)*")


init_streamlit_comm()

# # Inject custom CSS
# st.markdown("""
# <style>
#     .stForm > div {
#         width: 50%;
#     }
# </style>
# """, unsafe_allow_html=True)

if uploaded_file is not None:
    file_path = uploaded_file

    data_df = preprocess_df(file_path)

    # data = load_data(file_path)
#=======================================================================
    with st.expander("Original dataset", expanded=False):
        st.dataframe(data_df, use_container_width=True,hide_index=True)
    #Horizontal divider
    # st.sidebar.divider()

    renderer = get_pyg_renderer(data_df)
    renderer.explorer()


    #Horizontal divider
    # st.divider()


    with st.form("my_form"):
        st.write("Choose options to plot Pearson correlation")


        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
        
        submitted = st.form_submit_button("Apply changes")
        
        with col1:
            years_lst = list(data_df['year'].unique())
            idx = years_lst.index(2023)
            year_option = st.selectbox(
                "Choose a year?",
                years_lst,
                index=idx)
        with col2:
            month_n_hour_option = st.selectbox("Choose timeframe to aggregate",
                                            ['month_hour', 'month_3hour', 'month_6hour'],
                                            index=1)
        with col3:
            agg_function = st.selectbox("Choose aggregation function",
                                            ['mean', 'sum', 'min', 'max'],
                                            index=0)
        
        if submitted:
            plot_corr(data_df, year_option, month_n_hour_option, agg_function)
        else:
            plot_corr(data_df, year_option, month_n_hour_option, agg_function)


    # st.divider()