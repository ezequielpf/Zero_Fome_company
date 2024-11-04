import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
#from PIL import Image
from currency_converter import CurrencyConverter
import inflection

# ====================================================================================
# Defining functions
# ====================================================================================
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

def currency_code(currency):
    """
    Retorna o código da moeda baseado na informação da coluna currency
    """
    CURRENCY = {
            "Indian Rupees(Rs.)": "INR",
            "Dollar($)": "AUD",
            "Brazilian Real(R$)": "BRL",
            "Dollar($)": "CAD",
            "Indonesian Rupiah(IDR)": "IDR",
            "NewZealand($)": "NZD",
            "Botswana Pula(P)": "PHP",
            "Qatari Rial(QR)": "QAR",
            "Dollar($)": "SGD",
            "Rand(R)": "ZAR",
            "Sri Lankan Rupee(LKR)": "LKR",
            "Turkish Lira(TL)": "TRY",
            "Emirati Diram(AED)": "AED",
            "Pounds(£)": "GBP",
            "Dollar($)": "USD"
        }
    return CURRENCY[currency]

def country_name(country_ID):
    """Função que recebe o ID do país e retorna seu nome"""
    # Cria dicionário código do país -> nome do país
    COUNTRY = {
        1: "India",
        14: "Australia",
        30: "Brazil",
        37: "Canada",
        94: "Indonesia",
        148: "New Zeland",
        162: "Philippines",
        166: "Qatar",
        184: "Singapure",
        189: "South Africa",
        191: "Sri Lanka",
        208: "Turkey",
        214: "United Arab Emirates",
        215: "England",
        216: "United States of America"
    }
    return COUNTRY[country_ID]

def country_with_top_records(df, group): 
    cols = ['country_name', group]
    df_aux = df1_filtered.loc[:, cols].groupby(['country_name']).nunique()
    df_aux = df_aux.sort_values(by=[group], ascending=False).reset_index()
    return df_aux

def bar_plot(df, x_axis, y_axis, plot_title):
    fig = px.bar(df,
                x=df[x_axis],
                y=df[y_axis],
                title=plot_title,
                text_auto=True)
    fig.update_layout(title={
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                    yaxis_title=None,
                    xaxis_title=None)
    return fig
# ====================================================================================

# ====================================================================================
# Data loading and cleaning
# ====================================================================================
df = pd.read_csv('dataset/zomato.csv')
df1 = rename_columns(df)
df1 = df1.dropna()
# Categoriza os restaurantes somente por um tipo de cuisines
df1['cuisines'] = df1.loc[:, 'cuisines'].apply(lambda x: x.split(',')[0])

# Insere colunas com o código da moeda e com o custo do prato para dois em USD
c = CurrencyConverter('./dataset/currencies.csv')
df1['currency_code'] = df1['currency'].apply(currency_code)
df1['average_cost_for_two_us_dollar'] = df1[['average_cost_for_two', 'currency_code']].apply(lambda x: 
                                                                                             c.convert(x['average_cost_for_two'], x['currency_code'], 'USD'), axis=1)

# Remove a linha com valor average_cost_for_two = 2500000
cols = ['restaurant_name', 'average_cost_for_two_us_dollar']
lines = df1['restaurant_name'] == "d'Arry's Verandah Restaurant"
df1.drop(df1.index[385], inplace=True)

# Cria coluna com o nome dos países
df1['country_name'] = df1['country_code'].apply(country_name)
# ====================================================================================

# ====================================================================================
# Main Page
# ====================================================================================
st.set_page_config(
    page_title='Visão Países',
    page_icon=':earth_americas:',
    layout='wide'
)
# ====================================================================================

# ====================================================================================
# Side bar
# ====================================================================================
#image = Image.open('logo.jpeg')
#st.sidebar.image(image, width=120)
st.sidebar.markdown('<h2 style="text-align: center"> Zero Fome Company </h2>', unsafe_allow_html=True)
st.sidebar.markdown("""___""")

top_4 = df1.loc[:,['restaurant_id', 'country_name']].groupby(['country_name']).count().sort_values(by='restaurant_id', ascending=False).reset_index()
top_4 = list(top_4.loc[0:3, 'country_name'])
country_selector = st.sidebar.multiselect(
    'Selecione o(s) país(es) para ver os restaurantes.',
    df1["country_name"].unique(),
    default=top_4
)
# Filtro para países
lines = df1['country_name'].isin(country_selector)
df1_filtered = df1.loc[lines, :]
# ====================================================================================

# ====================================================================================
# Page
# ====================================================================================
st.markdown('<h1 style="text-align: center"> Métricas por país </h1>', unsafe_allow_html=True)
st.markdown("""___""")

with st.container():
    col1, col2, col3, col4, col5, col6 = st.columns(6, gap='medium')
    with col1:
        st.markdown('<p style="text-align: left"> Mais restaurantes registrados </p>', unsafe_allow_html=True)
        # País com maior número de restaurantes
        cols = ['country_name', 'restaurant_id']
        df_aux = df1.loc[:, cols].groupby(['country_name']).nunique()
        df_aux = df_aux.sort_values(by=['restaurant_id'], ascending=False).reset_index()
        aux = [df_aux.loc[0, 'country_name'], df_aux.loc[0, 'restaurant_id']]
        col1.metric(aux[0], aux[1])
    with col2:
        st.markdown('<p style="text-align: left"> Mais cidades registradas </p>', unsafe_allow_html=True)
        # País com maior número de cidades registradas
        cols = ['country_name', 'city']
        df_aux = df1.loc[:, cols].groupby(['country_name']).nunique()
        df_aux = df_aux.sort_values(by=['city'], ascending=False).reset_index()
        aux = [df_aux.loc[0, 'country_name'], df_aux.loc[0, 'city']]
        col2.metric(aux[0], aux[1])
    with col3:
        st.markdown('<p style="text-align: left"> Maior número de avaliações </p>', unsafe_allow_html=True)
        # País com maior número de cidades registradas
        cols = ['country_name', 'votes']
        df_aux = df1.loc[:, cols].groupby(['country_name']).count()
        df_aux = df_aux.sort_values(by=['votes'], ascending=False).reset_index()
        aux = [df_aux.loc[0, 'country_name'], df_aux.loc[0, 'votes']]
        col3.metric(aux[0], aux[1])
    with col4:
        st.markdown('<p style="text-align: left"> Maior nota média registrada </p>', unsafe_allow_html=True)
        # Maior nota média registradas
        cols = ['country_name', 'aggregate_rating']
        df_aux = df1.loc[:, cols].groupby(['country_name']).mean()
        df_aux = df_aux.sort_values(by=['aggregate_rating'], ascending=False).reset_index()
        aux = [df_aux.loc[0, 'country_name'], df_aux.loc[0, 'aggregate_rating']]
        col4.metric(aux[0], aux[1])
    with col5:
        st.markdown('<p style="text-align: left"> Mais tipos de culinárias oferecidas </p>', unsafe_allow_html=True)
        # Maior quantidade de culinárias
        cols = ['country_name', 'cuisines']
        df_aux = df1.loc[:, cols].groupby(['country_name']).nunique()
        df_aux = df_aux.sort_values(by=['cuisines'], ascending=False).reset_index()
        aux = [df_aux.loc[0, 'country_name'], df_aux.loc[0, 'cuisines']]
        col5.metric(aux[0], aux[1])
    with col6:
        st.markdown('<p style="text-align: left"> Maior média de prato para dois em US$ </p>', unsafe_allow_html=True)
        # Maior valor médio de um prato para dois
        cols = ['country_name', 'average_cost_for_two_us_dollar']
        df_aux = df1.loc[:, cols].groupby(['country_name']).mean()
        df_aux = df_aux.sort_values(by=['average_cost_for_two_us_dollar'], ascending=False).reset_index()
        aux = [df_aux.loc[0, 'country_name'], df_aux.loc[0, 'average_cost_for_two_us_dollar']]
        col6.metric(aux[0], np.round(aux[1],2))
    

st.markdown("""___""")

with st.container():
    col1, col2 = st.columns(2, gap='medium')
    with col1:
        # Número de restaurantes registrados por país
        country_r = country_with_top_records(df=df1_filtered, group='restaurant_id')
        fig = bar_plot(df=country_r, x_axis='country_name', y_axis='restaurant_id', plot_title='Quantidade de restaurantes registradas por país')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        df_aux = df1.loc[:, ['restaurant_id', 'country_name']].groupby(['country_name']).count().sort_values(by='restaurant_id', ascending=False).reset_index()
        fig = px.pie(df_aux, values='restaurant_id', names='country_name')
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    #Países que possuiem mais cidades registradas
    country_c = country_with_top_records(df= df1_filtered, group='city')  
    fig = bar_plot(df=country_c, x_axis='country_name', y_axis='city', plot_title='Quantidade de cidades registradas por país')
    st.plotly_chart(fig, use_container_width=True)


with st.container():
    col1, col2 = st.columns(2, gap='medium')
    with col1:
        # Países com maior quantidade de avaliações feitas
        cols = ['country_name', 'votes']
        country_rating = df1_filtered.loc[:, cols].groupby(['country_name']).count().sort_values(by=['votes'], ascending=False).reset_index()
        fig = bar_plot(df=country_rating, x_axis='country_name', y_axis='votes', plot_title='Quantidade de avaliações por país')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        # Países com a maior nota média
        cols = ['country_name', 'aggregate_rating']
        country_avg_rating = df1_filtered.loc[:, cols].groupby(['country_name']).mean().sort_values(by=['aggregate_rating'], ascending=False).reset_index()
        fig = bar_plot(df=country_avg_rating, x_axis='country_name', y_axis='aggregate_rating', plot_title='Nota média por país')
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1, col2 = st.columns(2, gap='medium')
    with col1:
        # Países com maior quantidade de culinárias
        cols = ['country_name', 'cuisines']
        country_rating = df1_filtered.loc[:, cols].groupby(['country_name']).nunique().sort_values(by=['cuisines'], ascending=False).reset_index()
        fig = bar_plot(df=country_rating, x_axis='country_name', y_axis='cuisines', plot_title='Quantidade de culinárias oferecidas por país')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        # Média de preços de pratos para dois
        cols = ['country_name', 'average_cost_for_two_us_dollar']
        country_avg_rating = df1_filtered.loc[:, cols].groupby(['country_name']).mean().sort_values(by=['average_cost_for_two_us_dollar'], ascending=False).reset_index()
        fig = bar_plot(df=country_avg_rating, x_axis='country_name', y_axis='average_cost_for_two_us_dollar', plot_title='Valor médio de um prato para dois')
        st.plotly_chart(fig, use_container_width=True)


