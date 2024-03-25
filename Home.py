import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home Page',
    layout="wide"
)


st.header('Dashboard interativo')

image_path = './images/analysis.jpg'
image = Image.open(image_path)
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Entregamos em toda região!')

st.sidebar.markdown("""---""")
