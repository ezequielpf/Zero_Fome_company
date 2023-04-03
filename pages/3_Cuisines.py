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
    page_title='Visão Culinárias',
    page_icon=':knife_fork_plate:',
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
st.sidebar.markdown("""___""")

cuisines_selector = st.sidebar.multiselect(
    'Selecione o(s) tipo(s) de culinária.',
    df1["cuisines"].unique(),
    default=['Brazilian', 'Japanese', 'Italian', 'Arabian', 'BBQ']
)

st.sidebar.markdown("""___""")

qtd_restaurant = st.sidebar.slider(
    'Selecione o número de restaurantes para visualizar na tabela.',
    value=10,
    min_value=1,
    max_value=20)

# Filtro para países
lines = (df1['country_name'].isin(country_selector)) & (df1['cuisines'].isin(cuisines_selector))
df1_filtered = df1.loc[lines, :]
# ====================================================================================

# ====================================================================================
# Page
# ====================================================================================
st.markdown('<h1 style="text-align: center"> Métricas por tipo de culinária </h1>', unsafe_allow_html=True)
st.markdown("""___""")

with st.container():
    st.markdown('<h3> Top 5 restaurantes com maior pontuação </h3>', unsafe_allow_html=True)
    top5 = df1[['cuisines', 'aggregate_rating', 'restaurant_name']].sort_values(by='aggregate_rating',ascending=False).reset_index(drop=True)
    top5 = top5.iloc[0:5, :]
    col1, col2, col3, col4, col5 = st.columns(5, gap='medium')
    with col1:
        col1.metric(top5.loc[0,'restaurant_name']+'/'+top5.loc[0,'cuisines'], str(top5.loc[0, 'aggregate_rating'])+'/'+str(5.0))
    with col2:
        col2.metric(top5.loc[1,'restaurant_name']+'/'+top5.loc[1,'cuisines'], str(top5.loc[1, 'aggregate_rating'])+'/'+str(5.0))
    with col3:
        col3.metric(top5.loc[2,'restaurant_name']+'/'+top5.loc[2,'cuisines'], str(top5.loc[2, 'aggregate_rating'])+'/'+str(5.0))
    with col4:
        col4.metric(top5.loc[3,'restaurant_name']+'/'+top5.loc[3,'cuisines'], str(top5.loc[3, 'aggregate_rating'])+'/'+str(5.0))
    with col5:
        col5.metric(top5.loc[4,'restaurant_name']+'/'+top5.loc[4,'cuisines'], str(top5.loc[4, 'aggregate_rating'])+'/'+str(5.0))
    st.markdown("""___""")

with st.container():
    st.markdown('<h3> Top restaurantes com maior pontuação </h3>', unsafe_allow_html=True)
    cols = ['restaurant_id', 'restaurant_name', 'country_name', 'city', 'cuisines', 'average_cost_for_two_us_dollar', 'aggregate_rating', 'votes']
    #df_aux = df1_filtered.loc[0,cols]
    #df_aux = df1_filtered.loc[:, cols].groupby(['restaurant_id']).sort_values(by='aggregate_rating', ascending=False).reset_index(drop=True)
    df_aux = df1_filtered.loc[:, cols].groupby(['restaurant_id']).max().sort_values(by='aggregate_rating', ascending=False).reset_index()
    st.dataframe(df_aux.loc[0:qtd_restaurant, cols])

with st.container():
    col1, col2 = st.columns(2, gap='medium')
    with col1:
        cols = ['cuisines', 'aggregate_rating']
        best_cuisines = df1.loc[:, cols].groupby(['cuisines']).mean().sort_values(by='aggregate_rating',ascending=False).reset_index()
        fig = bar_plot(df=best_cuisines.loc[0:8, :], x_axis='cuisines', y_axis='aggregate_rating', bar_color=None ,plot_title='Nota média máxima por tipo de culinária')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        cols = ['cuisines', 'aggregate_rating']
        lines = df1['aggregate_rating'] != 0.0
        best_cuisines = df1.loc[lines, cols].groupby(['cuisines']).mean().sort_values(by='aggregate_rating',ascending=True).reset_index()
        fig = bar_plot(df=best_cuisines.loc[0:8, :], x_axis='cuisines', y_axis='aggregate_rating', bar_color=None ,plot_title='Nota média mínima por tipo de culinária')
        st.plotly_chart(fig, use_container_width=True)