#######################
# Imports and installations
import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import requests
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import geopandas as gpd
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

#pip install -r requirements.txt

#######################
# Page configuration
st.set_page_config(
    page_title="InfoBrasil",
    page_icon="icon/brasil.png",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# Loading the CSV
df = pd.read_csv('data/df.csv')

#######################
# Components

# Organizando a distribuição das colunas para exibir 2 gráficos por linha
col0 = st.columns(1)
col1, col2 = st.columns([1, 1])  # Primeira linha de colunas para População e PIB por Região
col3 = st.columns(1)  # Linha para o PIB por Estado
col4 = st.columns(1)  # Linha para o gráfico de População por Estado
col5 = st.columns(1)

# Tamanho padrão dos gráficos
plot_height = 400
plot_width = 400

#######################
# Interface

# Sidebar
with st.sidebar:
    st.title('População e PIB do Brasil')

    # Opções de filtro
    option_list = ['População', 'Riqueza em Milhões']
    selected_option = st.selectbox('Selecione uma opção', option_list)
    if selected_option == 'População': 
        option = 'Population'
    else: 
        option = 'GDP'

#######################
# Gráficos principais

# Gráfico de População por Região

# URL do arquivo ZIP no GitHub
url = "https://raw.githubusercontent.com/Erickhbs/streamlit-ml-app/main/ne_110m_admin_0_countries.zip"
output_file = "ne_110m_admin_0_countries.zip"

# Baixar o arquivo ZIP
response = requests.get(url)
with open(output_file, "wb") as file:
    file.write(response.content)

# Carregar shapefile diretamente do arquivo ZIP
brasil = gpd.read_file(f"zip://{output_file}")

# Filtrar apenas o Brasil
brasil = brasil[brasil['SOVEREIGNT'] == 'Brazil']

# Preparar os dados para o HeatMap
heat_data = [
    [row['Latitude'], row['Longitude'], row[option]]
    for _, row in df.iterrows()
]



# Criar o mapa base centrado no Brasil
with col0[0]:
    st.title("INFORMAÇÕES SOBRE O BRASIL: 2019")
    st.markdown('<style>div.block-container{padding-right:3rem;}</style>', unsafe_allow_html=True)      
    mapa = folium.Map(location=[-14.2350, -51.9253], zoom_start=3.5)

# Adicionar o HeatMap ao mapa
HeatMap(heat_data, radius=50, blur=5).add_to(mapa)

# Exibir o mapa
folium_static(mapa)

# Gráfico de População por Região
with col1:
    st.subheader("População por Região")
    fig = px.pie(
        df,
        values="Population",
        names="Region",
        title="População por Região",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=100, r=10, t=30, b=10),
        height=plot_height,
        width=plot_width
    )
    st.plotly_chart(fig, use_container_width=False)

# Gráfico de PIB por Região
with col2:
    st.subheader("PIB em Milhões por Região")
    fig = px.pie(
        df,
        values="GDP",
        names="Region",
        title="PIB por Região",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=100, r=10, t=30, b=10),
        height=plot_height,
        width=plot_width
    )
    st.plotly_chart(fig, use_container_width=False)

# Gráfico de PIB por Estado
# Gráfico de PIB em Milhões por Estado
col3[0].subheader("PIB em Milhões por Estado")

# Formatando o valor do PIB
df['formatted_GDP'] = df['GDP'].apply(lambda x: f"{x:,.0f} mi")

fig = px.bar(
    df,
    x="State",
    y="GDP",
    text="formatted_GDP",
    template="seaborn",
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig.update_traces(textposition='outside')

# Atualizando o layout para formatar o eixo Y com 'mi'
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=100, r=10, t=30, b=10),
    height=plot_height,
    width=1000,
    yaxis=dict(
        tickprefix="R$ ",  # Prefixo para o eixo Y, opcional
        tickformat=".1s",  # Formatação em "milhões" com o sufixo
        showticklabels=True  # Mostrar os rótulos de cada valor
    )
)

col3[0].plotly_chart(fig, use_container_width=False)


# Gráfico de População por Estado
# Formatando a população para exibir em milhões
df['formatted_population_mi'] = (df['Population'] / 1e6).apply(lambda x: f"{x:,.2f} mi")

# Gráfico de barras
fig = px.bar(
    df, 
    x="State",
    y="Population",
    text="formatted_population_mi",  # Usando a coluna formatada em milhões
    title="População por Estado",
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Atualizando o gráfico
fig.update_traces(textposition='outside')  # Exibindo texto fora da barra
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=100, r=10, t=30, b=10),
    height=plot_height,
    width=1000
)

# Plotando o gráfico
col4[0].plotly_chart(fig, use_container_width=False)

