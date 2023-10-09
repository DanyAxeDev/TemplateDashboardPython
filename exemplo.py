from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import mysql.connector
from datetime import datetime
import calendar
from collections import Counter

# Modelo básico para conexão com banco

conexao = mysql.connector.connect(
    host='db.zscansoftware.com',
    user='estacio',
    password='M4{t29Aa3IAB',
    database='ilaudomysql'
)

cursor = conexao.cursor()

comando_read = f'SELECT dthr_atendido FROM dsatendimentos WHERE dthr_atendido IS NOT NULL'
cursor.execute(comando_read)
resultado = cursor.fetchall() # Lendo o banco de dados

# Termina a sessão com o banco
cursor.close()
conexao.close()

# Inicialize um array para os meses de todos os anos
meses_2015 = []
meses_2016 = []
meses_2017 = []
meses_2018 = []
meses_2019 = []
meses_2020 = []
meses_2021 = []
meses_2022 = []
meses_2023 = []

# Itere sobre as datas
for tupla in resultado:
    data_obj = tupla[0]
    
    if data_obj.year == 2015:
        meses_2015.append(data_obj.month)
    if data_obj.year == 2016:
        meses_2016.append(data_obj.month)
    if data_obj.year == 2017:
        meses_2017.append(data_obj.month)
    if data_obj.year == 2018:
        meses_2018.append(data_obj.month)
    if data_obj.year == 2019:
        meses_2019.append(data_obj.month)
    if data_obj.year == 2020:
        meses_2020.append(data_obj.month)
    if data_obj.year == 2021:
        meses_2021.append(data_obj.month)
    if data_obj.year == 2022:
        meses_2022.append(data_obj.month)
    if data_obj.year == 2023:
        meses_2023.append(data_obj.month)

# Inicialize um dicionário com contagens de zero para cada mês
contagem_meses_2015 = {mes: 0 for mes in range(1, 13)}
contagem_meses_2016 = {mes: 0 for mes in range(1, 13)}
contagem_meses_2017 = {mes: 0 for mes in range(1, 13)}
contagem_meses_2018 = {mes: 0 for mes in range(1, 13)}
contagem_meses_2019 = {mes: 0 for mes in range(1, 13)}
contagem_meses_2020 = {mes: 0 for mes in range(1, 13)}
contagem_meses_2021 = {mes: 0 for mes in range(1, 13)}
contagem_meses_2022 = {mes: 0 for mes in range(1, 13)}
contagem_meses_2023 = {mes: 0 for mes in range(1, 13)}

for mes in meses_2015:
    contagem_meses_2015[mes] += 1
for mes in meses_2016:
    contagem_meses_2016[mes] += 1
for mes in meses_2017:
    contagem_meses_2017[mes] += 1
for mes in meses_2018:
    contagem_meses_2018[mes] += 1
for mes in meses_2019:
    contagem_meses_2019[mes] += 1
for mes in meses_2020:
    contagem_meses_2020[mes] += 1
for mes in meses_2021:
    contagem_meses_2021[mes] += 1
for mes in meses_2022:
    contagem_meses_2022[mes] += 1
for mes in meses_2023:
    contagem_meses_2023[mes] += 1

# Converta o dicionário para uma lista de tuplas
resultados_2015 = list(contagem_meses_2015.items())
resultados_2016 = list(contagem_meses_2016.items())
resultados_2017 = list(contagem_meses_2017.items())
resultados_2018 = list(contagem_meses_2018.items())
resultados_2019 = list(contagem_meses_2019.items())
resultados_2020 = list(contagem_meses_2020.items())
resultados_2021 = list(contagem_meses_2021.items())
resultados_2022 = list(contagem_meses_2022.items())
resultados_2023 = list(contagem_meses_2023.items())

# Extraia apenas as contagens de ocorrências
contagens_2015 = [contagem for mes, contagem in resultados_2015]
contagens_2016 = [contagem for mes, contagem in resultados_2016]
contagens_2017 = [contagem for mes, contagem in resultados_2017]
contagens_2018 = [contagem for mes, contagem in resultados_2018]
contagens_2019 = [contagem for mes, contagem in resultados_2019]
contagens_2020 = [contagem for mes, contagem in resultados_2020]
contagens_2021 = [contagem for mes, contagem in resultados_2021]
contagens_2022 = [contagem for mes, contagem in resultados_2022]
contagens_2023 = [contagem for mes, contagem in resultados_2023]

lista_meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Maio', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    
app = Dash(__name__, title="Dashboard")

fig = go.Figure()

opcoes = ['Barra', 'Linha']

app.layout = html.Div(children=[
    # Titulo da página
    html.H1(
        className="titulo",
        children='Tratamento dos dados'
    ),

    html.H2(
        children='Gráfico que contempla a quantidade de atendimentos feitos pela equipe de suporte, desde 2015 até 2023'
    ),

    html.Div(
        className="flexGrafico",
        children=[
            html.Div(
                className="containerGrafico",
                children=[
                    # Módelo para lista de filtros
                    html.Div(
                        className="flexFiltro",
                        children=[
                            html.Label(children=["Tipo de gráfico:"]),
                            html.Div(
                                className="filtro",
                                children=[dcc.Dropdown(
                                    opcoes, 
                                    value='Barra', 
                                    id='lista_grafico',
                                    style={'width': '400px', 'margin-left': '5px', 'border-radius': '20px'}
                                )]
                            ),
                        ]
                    ),

                    dcc.Checklist(
                        lista_meses,
                        lista_meses,
                        inline=True,
                        id='checklist-meses',
                        style={'margin-top': '20px', 'margin-bottom': '20px'}
                    ),

                    dcc.Graph(
                    id='grafico',
                    figure=fig,
                    ),
                ]
            ),
        ]
    )
])

@app.callback(
    Output('grafico', 'figure'),
     Input('lista_grafico', 'value')
)
def update_output(tipo_grafico):
    if tipo_grafico == "Barra":
        fig = go.Figure(
            data=[go.Bar(x=lista_meses, y=contagens_2015, name='2015', marker_color='#00008B'), 
                  go.Bar(x=lista_meses, y=contagens_2016, name='2016', marker_color='#EE82EE'), 
                  go.Bar(x=lista_meses, y=contagens_2017, name='2017', marker_color='orange'), 
                  go.Bar(x=lista_meses, y=contagens_2018, name='2018', marker_color='black'), 
                  go.Bar(x=lista_meses, y=contagens_2019, name='2019', marker_color='purple'), 
                  go.Bar(x=lista_meses, y=contagens_2020, name='2020', marker_color='green'), 
                  go.Bar(x=lista_meses, y=contagens_2021, name='2021', marker_color='yellow'), 
                  go.Bar(x=lista_meses, y=contagens_2022, name='2022', marker_color='gray'), 
                  go.Bar(x=lista_meses, y=contagens_2023, name='2023', marker_color='red')],
            layout_title_text="Comparativo de atendimento"
        )
        fig.update_layout(
            plot_bgcolor='#f5f5f5',  # Cor de fundo do gráfico
            paper_bgcolor='#ffffff',  # Cor de fundo do papel
            font=dict(color='#333333'),  # Cor da fonte
            xaxis_title='Meses',
            yaxis_title='Quantidade de atendimento',
            width=800,
            height=500,
            yaxis=dict(
                showgrid=True,  # Exibir linhas de marcação no eixo y
                gridcolor='lightgray',  # Cor das linhas de marcação
                gridwidth=0.5,  # Largura das linhas de marcação
                showline=True,  # Exibir linha de eixo y
                linewidth=1,  # Largura da linha de eixo y
                griddash='dot'
            ),
            margin=dict(l=0, r=0, t=100, b=0)
        )
    if tipo_grafico == "Linha":
        fig = go.Figure(
            data=[go.Line(x=lista_meses, y=contagens_2015, name='2015', marker_color='#00008B'), 
                  go.Line(x=lista_meses, y=contagens_2016, name='2016', marker_color='#EE82EE'), 
                  go.Line(x=lista_meses, y=contagens_2017, name='2017', marker_color='orange'), 
                  go.Line(x=lista_meses, y=contagens_2018, name='2018', marker_color='black'), 
                  go.Line(x=lista_meses, y=contagens_2019, name='2019', marker_color='purple'), 
                  go.Line(x=lista_meses, y=contagens_2020, name='2020', marker_color='green'), 
                  go.Line(x=lista_meses, y=contagens_2021, name='2021', marker_color='yellow'), 
                  go.Line(x=lista_meses, y=contagens_2022, name='2022', marker_color='gray'), 
                  go.Line(x=lista_meses, y=contagens_2023, name='2023', marker_color='red')],
            layout_title_text="Comparativo de atendimento"
        )
        fig.update_layout(
            xaxis_title='Meses',
            yaxis_title='Quantidade de atendimento',
            width=800
        )
    return fig

app.run_server(debug=True)