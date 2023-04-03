import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from PIL import Image
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

def bar_plot(df, x_axis, y_axis, bar_color, plot_title):
    fig = px.bar(df,
                x=df[x_axis],
                y=df[y_axis],
                color=bar_color,
                title=plot_title,
                text_auto=True,
                color_discrete_sequence=px.colors.qualitative.D3)
    fig.update_layout(title={
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                    yaxis_title=None,
                    xaxis_title= 'Cidade',
                    legend_title='País')
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
    page_title='Visão Cidades',
    page_icon=':cityscape:',
    layout='wide'
)
# ====================================================================================

# ====================================================================================
# Side bar
# ====================================================================================
#image = Image.open('logo.jpeg')
#st.sidebar.image(image, width=120)
st.sidebar.markdown('<h2 style="text-align: center"> Fome Zero Company </h2>', unsafe_allow_html=True)
st.sidebar.markdown("""___""")

#top_4 = df1.loc[:,['restaurant_id', 'country_name']].groupby(['country_name']).count().sort_values(by='restaurant_id', ascending=False).reset_index()
#top_4 = list(top_4.loc[0:3, 'country_name'])
country_selector = st.sidebar.multiselect(
    'Selecione o(s) país(es) para ver os restaurantes.',
    df1["country_name"].unique(),
    default=['India', 'Brazil', 'Canada', 'South Africa', 'Singapure']#top_4
)
# Filtro para países
lines = df1['country_name'].isin(country_selector)
df1_filtered = df1.loc[lines, :]
# ====================================================================================

# ====================================================================================
# Page
# ====================================================================================
st.markdown('<h1 style="text-align: center"> Métricas por cidade </h1>', unsafe_allow_html=True)
st.markdown("""___""")

with st.container():
    # top 10 cidades com mais restaurantes cadastrados
    cols = ['country_name', 'city', 'restaurant_id']
    df_aux = df1_filtered.loc[:, cols].groupby(['country_name', 'city']).nunique().sort_values(by=['restaurant_id', 'country_name'], ascending=False).reset_index()
    fig = bar_plot(df=df_aux.iloc[0:10, :], x_axis='city', y_axis='restaurant_id', bar_color='country_name', plot_title='Top 10 cidades com mais restaurantes cadastrados')
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    # Top 10 cidades que oferecem a maior diversidade de tipos de culinária
    cols = ['country_name', 'city', 'cuisines']
    df_aux = df1_filtered.loc[:, cols].groupby(['country_name', 'city']).nunique().sort_values(by='cuisines', ascending=False).reset_index()
    fig = bar_plot(df=df_aux.iloc[0:10, :], x_axis='city', y_axis='cuisines', bar_color='country_name', plot_title='Top 10 cidades que oferecem a maior diversidade de tipos de culinária')
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    # Top 10 cidades com o maior valor médio de um prato para dois
    cols = ['country_name', 'city', 'average_cost_for_two_us_dollar']
    df_aux = df1_filtered.loc[:, cols].groupby(['country_name', 'city']).mean().sort_values(by='average_cost_for_two_us_dollar', ascending=False).reset_index()
    fig = bar_plot(df=df_aux.iloc[0:10, :], x_axis='city', y_axis='average_cost_for_two_us_dollar', bar_color='country_name', plot_title='Top 10 cidades com o maior valor médio de um prato para dois')
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1, col2 = st.columns(2, gap='medium')
    with col1:
        # cidades que possuem mais restaurantes com nota média acima de 4
        cols = ['country_name', 'city', 'aggregate_rating']
        lines = df1['aggregate_rating'] > 4
        df_aux = df1_filtered.loc[lines, cols].groupby(['country_name', 'city']).count().sort_values(by='aggregate_rating', ascending=False).reset_index()
        fig = bar_plot(df=df_aux.iloc[0:7, :], x_axis='city', y_axis='aggregate_rating', bar_color='country_name', plot_title='Cidades com restaurantes com nota média acima de 4')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        # cidades que possuem mais restaurantes com nota média abaixo de 2,5
        cols = ['country_name', 'city', 'aggregate_rating']
        lines = df1['aggregate_rating'] < 2.5
        df_aux = df1_filtered.loc[lines, cols].groupby(['country_name', 'city']).count().sort_values(by='aggregate_rating', ascending=False).reset_index()
        fig = bar_plot(df=df_aux.iloc[0:7, :], x_axis='city', y_axis='aggregate_rating', bar_color='country_name', plot_title='Cidades com restaurantes com nota média abaixo de 2,5')
        st.plotly_chart(fig, use_container_width=True)