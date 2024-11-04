import pandas as pd
import streamlit as st
#from PIL import Image
import inflection
from currency_converter import CurrencyConverter
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# ====================================================================================
# Defining functions
# ====================================================================================
# Faz cópia do dataframe original e altera os nomes das colunas, tirando o espaço e colocando underline
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
    page_title='Main Page',
    page_icon=':bar_chart:',
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

top_4 = df1.loc[:,['restaurant_id', 'country_name']].groupby(['country_name']).count().sort_values(by='restaurant_id', ascending=False).reset_index()
top_4 = list(top_4.loc[0:3, 'country_name'])
# Seletor de países para ver as métricas
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
st.markdown('<h1 style="text-align: center"> Fome Zero Dashboard </h1>', unsafe_allow_html=True)
st.markdown("""___""")

with st.container():
    st.markdown('<h2> Números gerais da empresa </h2>', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5, gap='medium')
    with col1:
        unique_restaurant = df1['restaurant_id'].nunique()
        col1.metric('Restaurantes cadastrados', unique_restaurant)
    with col2:
        unique_countries = df1['country_code'].nunique()
        col2.metric('Países cadastrados', unique_countries)
    with col3:
        unique_cities = df1['city'].nunique()
        col3.metric('Cidades cadastradas', unique_cities)
    with col4:
        sum_votes = df1['votes'].sum()
        col4.metric('Total de avaliações recebidas', sum_votes)
    with col5:
        unique_cuisines = df1['cuisines'].nunique()
        col5.metric('Tipo de culinária oferecida', unique_cuisines)
st.markdown("""___""")
with st.container():
    st.markdown('<h2> Restaurantes pelo mundo </h2>', unsafe_allow_html=True)
    cols = ['restaurant_name', 'country_name', 'latitude', 'longitude', 'aggregate_rating']
    df_aux = df1_filtered.loc[:, cols]
    map = folium.Map(location = [27.919478, -16.905911], zoom_start=2)
    cluster = MarkerCluster().add_to(map)
    for index, location_info in df_aux.iterrows():
        #iframe = folium.IFrame(location_info['restaurant_name'] + '<br>' + location_info['country_name'])
        folium.Marker([location_info['latitude'], location_info['longitude']],
                    popup=location_info['restaurant_name']).add_to(cluster)
    folium_static(map, width=1150)

# ====================================================================================

