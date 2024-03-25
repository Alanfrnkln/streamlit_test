#===================================================================
#                           IMPORTS
#===================================================================
import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px
data_pre = pd.read_csv('./train_pre.csv')
data_pre['Order_Date'] = pd.to_datetime(data_pre['Order_Date'])

#=========================================================
#                      Sidebar StreamLit
#=========================================================
st.header(' Marketplace - Visão Cliente')

image_path = './images/analysis.jpg'
image = Image.open(image_path)
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Entregamos em toda região!')

st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')
data_slider = st.sidebar.slider(
      "Até qual valor ?",
      value=30,
      min_value=0,
      max_value=60,
)

st.sidebar.markdown("""---""")

traffic_side = st.sidebar.multiselect(
      'Quais as condições do transito ?',
      ['Low', 'Medium', 'High', 'Jam'],
      default=['Low', 'Medium', 'High', 'Jam']
)

#=========================================================
#               Filtro Interativo StreamLit
#=========================================================

linhas_selecionadas = data_pre['Road_traffic_density'].isin(traffic_side)
data_pre = data_pre.loc[linhas_selecionadas, :]

#=========================================================
#                   Funções
#=========================================================
def mean_dev(data_pre):
    #4. A avaliação média e o desvio padrão por tipo de tráfego.
    std_mean = data_pre.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby('Road_traffic_density').agg({
        'Delivery_person_Ratings': ['mean', 'std']
        })
    std_mean.columns = ['média', 'desvio_padrão']
    std_mean.reset_index()
    return std_mean
    
def mean_ratings(data_pre):
    #3. A avaliação média por entregador.
    mean = data_pre.loc[:, ['Delivery_person_Ratings','Delivery_person_ID']].groupby('Delivery_person_ID').mean().reset_index()
    return mean

#===================================================================
#                           LAYOUT
#===================================================================
tab1, tab2, tab3 = st.tabs(["Visão tática", "Visão Estratégica", "Visão Geográfica"])

with tab1:
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        menor_idade = data_pre["Delivery_person_Age"].min()
        maior_idade = data_pre["Delivery_person_Age"].max()
        pior_veic = data_pre["Vehicle_condition"].min()
        melhor_veic = data_pre["Vehicle_condition"].max()
        col1.metric(label="Menor idade dos entregadores:", value=menor_idade)
        col2.metric("Maior idade dos entregadores:", maior_idade)
        col3.metric("Pior condição de veículo: ", pior_veic )
        col4.metric("Melhor condição de veículo: ", melhor_veic)
        
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("## Média de avaliações: ")
            st.dataframe(mean_ratings(data_pre), use_container_width=True)         
        
        with col2:
            st.markdown("## Média e Desvio Padrão por tráfego: ")
            st.dataframe(mean_dev(data_pre))

#===================================================================
#                           QUESTIONAMENTOS
#===================================================================



# # 5. A avaliação média e o desvio padrão por condições climáticas.
# filtro = data_pre['Weatherconditions'] != 'conditions NaN'
# data_pre = data_pre[filtro]
# std_mean = data_pre.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']].groupby('Weatherconditions').agg({
#     'Delivery_person_Ratings': ['mean', 'std']
#     })
# std_mean.columns = ['média', 'desvio_padrão']
# std_mean.reset_index()

# #6. Os 10 entregadores mais rápidos por cidade.
# data_pre['Time_taken(min)'].min()
