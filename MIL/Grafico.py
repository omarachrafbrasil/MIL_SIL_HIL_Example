
import plotly.graph_objects as go
from plotly.subplots import make_subplots


"""
Gera dashboard HTML interativo com range slider para navegação temporal.
"""
def gerar_grafico_interativo(df, title):
    fig = make_subplots(rows=2, cols=1, 
                        shared_xaxes=True, 
                        vertical_spacing=0.08,
                        subplot_titles=("Posição Física (metros)", "Estados e Comandos"),
                        row_heights=[0.6, 0.4])

    # Gráfico 1: Posição do Portão
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Posicao'],
                             mode='lines', name='Posição',
                             line=dict(color='royalblue', width=2),
                             fill='tozeroy'), row=1, col=1)

    # Gráfico 2: Estados do Controlador (Escada)
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Estado'],
                             mode='lines', name='Estado',
                             line=dict(color='forestgreen', shape='hv')), row=2, col=1)

    # Gráfico 2: Pulsos de Tecla (Rádio)
    df_tecla = df[df['Tecla'] == True]
    fig.add_trace(go.Scatter(x=df_tecla['Hora'], y=[1]*len(df_tecla),
                             mode='markers', name='Toque Rádio',
                             marker=dict(color='red', symbol='line-ns', size=12)), row=2, col=1)

    # Configuração de Navegação e Layout
    fig.update_layout(
        title=title,
        height=700, template="plotly_white",
        xaxis2=dict(rangeslider=dict(visible=True), type="linear"), # Adiciona Scrollbar
        showlegend=True
    )
    
    fig.update_yaxes(tickvals=[0, 1, 2, 3], 
                     ticktext=['FECHADO', 'ABRINDO', 'PARADO', 'FECHANDO'], row=2, col=1)
    
    fig.show()