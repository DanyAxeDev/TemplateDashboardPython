from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np

app = Dash(__name__, title="Dashboard")

quantidade2022 = [30, 78, 57, 34, 100, 46, 12]
quantidade2023 = [27, 68, 86, 74, 10, 4, 87]
meses2022 = ["Jan", "Fev", "Mar", "Abr", "Maio", "Jun", "Jul"]
meses2023 = ["Jan", "Fev", "Mar", "Abr", "Maio", "Jun", "Jul"]

fig = go.Figure(
    data=[go.Bar(x=meses2022, y=quantidade2022, name='2022', marker_color='#00008B'), go.Bar(x=meses2023, y=quantidade2023, name='2023', marker_color='#EE82EE')],
    layout_title_text="Comparativo de atendimento: Barra"
)

opcoes = ['Barra', 'Linha']

app.layout = html.Div(children=[
    # Titulo da página
    html.H1(
        className="titulo",
        children='Tratamento dos dados'
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
def update_output(value):
    # Condição que mostra gráfico geral, caso opção selecionada seja 'Todos'
    if value == "Barra":
        fig = go.Figure(
            data=[go.Bar(x=meses2022, y=quantidade2022, name='2022', marker_color='#00008B'), go.Bar(x=meses2023, y=quantidade2023, name='2023', marker_color='#EE82EE')],
            layout_title_text="Comparativo de atendimento"
        )
        fig.update_layout(
            plot_bgcolor='#f5f5f5',  # Cor de fundo do gráfico
            paper_bgcolor='#ffffff',  # Cor de fundo do papel
            font=dict(color='#333333'),  # Cor da fonte
            xaxis_title='Meses',
            yaxis_title='Quantidade de atendimento',
            width=500,
            height=500,
            yaxis=dict(
                showgrid=True,  # Exibir linhas de marcação no eixo y
                gridcolor='lightgray',  # Cor das linhas de marcação
                gridwidth=0.5,  # Largura das linhas de marcação
                showline=True,  # Exibir linha de eixo y
                linewidth=1,  # Largura da linha de eixo y
                griddash='dot'
            ),
            template='plotly_dark',
            margin=dict(l=0, r=0, t=100, b=0)
        )
    if value == "Linha":
        fig = go.Figure(
            data=[go.Line(x=meses2022, y=quantidade2022, name='2022', marker_color='#00008B'), go.Line      (x=meses2023, y=quantidade2023, name='2023', marker_color='#EE82EE')],
            layout_title_text="Comparativo de atendimento"
        )
        fig.update_layout(
            xaxis_title='Meses',
            yaxis_title='Quantidade de atendimento',
            width=700
        )
    return fig

app.run_server(debug=True)