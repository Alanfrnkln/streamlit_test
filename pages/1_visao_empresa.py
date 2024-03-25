# Libraries
import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px
import streamlit_folium as st_folium
data_pre = pd.read_csv('./train_pre.csv')
data_pre['Order_Date'] = pd.to_datetime(data_pre['Order_Date'])

st.set_page_config(
      page_title="Visão Empresa",
      layout='wide'
)
#=========================================================
#                      Funções
#=========================================================
def plot_map(data_pre):
      st.markdown('Visão Geográfica')
      columns = [
      'City',
      'Road_traffic_density',
      'Delivery_location_latitude',
      'Delivery_location_longitude'
      ]

      columns_groupby = ['City', 'Road_traffic_density']

      data_plot = data_pre.loc[:, columns].groupby(columns_groupby).median().reset_index()

      #Desenhar o mapa
      import folium
      map_ = folium.Map(zoom_starts=5)

      for index, location_info in data_plot.iterrows():
            folium.Marker(location=[location_info['Delivery_location_latitude'],
                        location_info['Delivery_location_longitude']], 
                        popup=location_info[['City','Road_traffic_density']]).add_to(map_)

      st_folium.folium_static(map_, width=720)

def order_by_week(data_pre):      
      #Quantidade de pedidos por semana
      data_pre['week_of_year'] = data_pre['Order_Date'].dt.strftime('%U')
      pedidos_por_semana = data_pre.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
      pedidos_por_semana.columns = ['semana', 'qtde_pedidos']

      # Gráfico
      linha = px.line(pedidos_por_semana, x='semana', y='qtde_pedidos')
      return linha

def order_by_traffic( data_pre ):
      # Distribuição de pedidos por tipo de tráfego
      pedido_por_trafego = data_pre.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()

      pedido_por_trafego['perc'] = (pedido_por_trafego['ID'] / pedido_por_trafego['ID'].sum()) * 100

      #gráfico
      pie = px.pie(pedido_por_trafego, values='perc', names='Road_traffic_density')
      return pie

def order_by_day( data_pre ):
      """Define a quantidade de pedidos por dia

      Args:
          data_pre (dataframe): De onde as colunas serão obtidas

      Returns:
          Plotly_express graphic: retorna um gráfico do plotly.express
      """
      pedidos_dia = data_pre.loc[:, ["ID", "Order_Date"]].groupby("Order_Date").count().reset_index()
      pedidos_dia.columns = ['order_date', 'qtde_entregas']

      fig = px.bar(pedidos_dia, x='order_date', y='qtde_entregas')
      return fig
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
#                 Footer Sidebar StreamLit
#=========================================================
st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')

#=========================================================
#                      Layout StreamLit
#=========================================================

tab1, tab2, tab3 = st.tabs(['Visão empresa', 'Visão tática', 'Visão Geográfica'])


with tab1:
      with st.container():
            st.markdown('### Pedidos por dia:')
            fig = order_by_day(data_pre)
            st.plotly_chart(fig, use_container_width=True)
      
      with st.container():
            col1, col2 = st.columns(2)
            with col1:
                  st.markdown('### Pedidos por Densidade de tráfego:')
                  pie = order_by_traffic( data_pre )
                  st.plotly_chart(pie, use_container_width=True)

            with col2:
                  st.markdown("### Pedidos por semana: ")
                  linha = order_by_week(data_pre)
                  st.plotly_chart(linha, use_container_width=True)
                  
with tab2:
      st.markdown('Visão tática')

with tab3:
      st.markdown("### Localização dos restaurantes: ")
      plot_map(data_pre)
