# Zero Fome Company

## Descrição do problema de negócio

A empresa Zero Fome é uma marketplace de restaurantes. Seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Zero Fome, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.

O CEO da empresa foi contratado recentemente e pediu que fosse gerado um dashboard que permitisse a visualização das principais informações do negócio. Seu objetivo, inicialmente, é entender melhor o negócio para poder tomar as melhores decisões estratégicas e alavancar ainda mais a Zero Fome.

Minha função como cientista de dados é fazer a análise dos dados, apresentar algumas métricas importantes, gerar gráficos e obter alguns insights do ponto de vista dos países e cidades cadastrados, bem como dos restaurantes e tipos de culinárias oferecidas.

## Premissas assumidas para a análise

1. Utilizado um banco de dados público ([https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv](https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv))
2. Marketplace é o modelo de negócio utilizado
3. As visões de negócio foram: Visão geográfica de atuação (países e cidades) e visão gastronômica (restaurantes e tipos de culinária) 

## Estratégia de solução

O painel de informações foi desenvolvido utilizando as métricas que refletem as principais visões do modelo de negócio da empresa:

### Visão Geral da empresa

1. Quantidade de restaurantes cadastrados
2. Quantidade de países que possuem restaurantes cadastrados
3. Quantidade de cidades que possuem restaurantes cadastrados
4. Total de avaliações recebidas
5. Quantidade de tipos de culinária cadastradas

### Métricas por país

1. Quantidade de restaurantes registrados por país
2. Quantidade de cidades registradas por país
3. Quantidade de avaliaçẽos por país
4. Nota média por país
5. Quantidade de tipos de culinária oferecida por país
6. Valor médio de um prato para duas pessoas por país 

### Métricas por cidade

1. Cidades com maior número de restaurantes cadastrados
2. Cidades com maior oferta de tipos de culinária
3. Cidades com maior valor médio de um prato médio para dois
4. Cidades com restaurantes com nota média acima de 4
5. Cidades com restaurantes com nota média abaixo de 2,5

### Métricas por tipo de culinária

1. Restaurantes com maiores notas
2. Maiores notas médias por tipo de culinária
3. Menores notas médias por tipo de culinária

## Top 3 insights a partir dos dados

- Índia e EUA são os países com maior número de restaurantes, sendo que a Índia possui mais do que o dobro de restaurantes quando comparado aos EUA.
- Índia e EUA, juntos, possuem 65% dos restaurantes cadastrados.
- Embora a Índia não seja um país com apelo turístico, é o país que apresenta a maior diversificação dos tipos de culinária oferecidos.

## O produto final do projeto

Painel online, hospedado em uma Cloud e disponível para acesso em qualquer dispositivo conectado à internet através do link:

[https://zero-fome-company.streamlit.app/](https://zero-fome-company.streamlit.app/)

## Conclusão

O objetivo deste projeto foi criar um conjunto de gŕaficos e/ou tabelas que exibam as métricas da melhor forma possível para a avaliação do CEO.

Podemos concluir que Índia e EUA são os locais com mais ofertas. Seria de se esperar que EUA apresentasse tal resultado por seu potencial econômico. A surpresa é a Índia que, mesmo não sendo um país com forte apelo turístico, seja o maior consumidor. Tal fato pode ser explicado por sua grande população.
