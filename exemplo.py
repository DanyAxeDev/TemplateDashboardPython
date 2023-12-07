from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import mysql.connector

# Modelo básico para conexão com banco
'''
conexao = mysql.connector.connect(
    host='',
    user='',
    password='',
    database=''
)

cursor = conexao.cursor()

comando_read = f'SELECT COLUNA FROM TABELA'
cursor.execute(comando_read)
resultado = cursor.fetchall() # Lendo o banco de dados

# Termina a sessão com o banco
cursor.close()
conexao.close()
'''

# Exemplo de dados 
contagens_2015 = [100, 134, 200, 345, 90, 127, 500, 439, 285, 741, 211, 121]
contagens_2016 = [234, 300, 123, 763, 337, 776, 235, 763, 643, 862, 252, 125]
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
        children='Gráfico que contempla a quantidade de atendimentos feitos pela equipe de suporte, desde 2015 até 2016'
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
def update_output(tipo_grafico):
    if tipo_grafico == "Barra":
        fig = go.Figure(
            data=[go.Bar(x=lista_meses, y=contagens_2015, name='2015', marker_color='#00008B'), 
                  go.Bar(x=lista_meses, y=contagens_2016, name='2016', marker_color='#EE82EE')],
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
                  go.Line(x=lista_meses, y=contagens_2016, name='2016', marker_color='#EE82EE')],
            layout_title_text="Comparativo de atendimento"
        )
        fig.update_layout(
            xaxis_title='Meses',
            yaxis_title='Quantidade de atendimento',
            width=800
        )
    return fig

app.run_server(debug=True)
