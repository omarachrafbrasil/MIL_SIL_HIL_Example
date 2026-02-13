"""
=============================================================================
PROJETO: SIMULADOR DE PORTÃO DE GARAGEM - NÍVEL MIL (Model-in-the-Loop)
=============================================================================
DESCRIÇÃO:
    Este script implementa a fase MIL do desenvolvimento de um sistema 
    embarcado. O objetivo é validar a lógica da máquina de estados (Controlador) 
    contra um modelo matemático da física (Planta) antes de gerar código C/C++.
    
    Autor: Omar Achraf (omarachraf@gmail.com)
    Data: 12/02/2026    

FUNCIONALIDADES:
    - Simulação física com lógica de "Zona Morta" (folga mecânica).
    - Máquina de estados cíclica (Single-Button).
    - Simulação de 24 horas com eventos probabilísticos de uso.
    - Geração de telemetria em CSV.
    - Visualização interativa com Zoom e Scroll (Plotly).

PRÉ-REQUISITOS:
    - Python versão: 3.8 ou superior (Recomendado 3.10+)
    - Bibliotecas externas: pandas, numpy, plotly

INSTRUÇÕES DE INSTALAÇÃO:
    No terminal, execute:
    $ pip install pandas numpy plotly

COMO EXECUTAR:
    $ python mil.py
=============================================================================
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from SimulationLoop import SimulationLoop
from LogicaControlador import LogicaControlador
from Grafico import gerar_grafico_interativo



CSV_NOME    = "simulacao_portao_24h_MIL.csv"


        
def carregar_controlador()->LogicaControlador: 
    return LogicaControlador()       
    


def executar_simulação(controlador):
    data = SimulationLoop(controlador)

    # Finalização e Exportação
    df = pd.DataFrame(data, columns=['Hora', 'Tecla', 'Posicao', 'Estado'])
    df.to_csv(CSV_NOME, index=False)
    print(f"Simulação concluída. Gerado '{CSV_NOME}'.")
    
    gerar_grafico_interativo(df, f"MIL: Simulação de 24h com Zona Morta")

    
        
if __name__ == "__main__":
    print("--- Iniciando Simulação MIL (Model-in-the-Loop) ---")
    executar_simulação(carregar_controlador())    