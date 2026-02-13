"""
=============================================================================
PROJETO: SIMULADOR DE PORTÃO DE GARAGEM - NÍVEL SIL (Software-in-the-Loop)
=============================================================================
DESCRIÇÃO:
    Este script carrega o arquivo 'controlador.dll' (compilado do C++) e o
    utiliza para controlar o modelo físico da planta em Python.
    O objetivo é garantir que o código C++ se comporte exatamente como o MIL.
    
    Autor: Omar Achraf (omarachraf@gmail.com)
    Data: 12/02/2026       

PRÉ-REQUISITOS:
    - controlador.dll (deve estar na mesma pasta que este script)
    - Bibliotecas: pandas, plotly, numpy
    - Ira abrir uma aba no browser default com o grafico resultado da
      simulaçãol. No grafico inferior arraste o retangulo vertical branco da
      esquerda e o da direita para delimitar a window de tempo desejada para
      poder visualizar detalhes em curto período de tempo.
=============================================================================
"""

import ctypes
import pandas as pd
import os
import sys

import sys
import os
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
raiz_projeto = os.path.dirname(diretorio_atual)
sys.path.append(raiz_projeto)
from MIL.SimulationLoop import SimulationLoop
from MIL.Grafico import gerar_grafico_interativo



CSV_NOME    = "simulacao_portao_24h_SIL.csv"



# --- CARREGAMENTO DA DLL (CONTROLADOR C++) ---
def carregar_controlador():
    # Garante que o Python procure a DLL na pasta onde o script está
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    dll_path = os.path.join(diretorio_script, "controlador.dll")

    if not os.path.exists(dll_path):
        raise FileNotFoundError(f"ERRO: O arquivo {dll_path} não existe. Compile o C++ primeiro!")

    try:
        # winmode=0 é necessário em algumas versões de Python 3.8+ para carregar DLLs locais
        if sys.platform == "win32":
            lib = ctypes.CDLL(dll_path, winmode=0)
        else:
            lib = ctypes.CDLL(dll_path)
            
        # Configura as assinaturas das funções C++
        lib.processar_controlador.argtypes = [ctypes.c_bool, ctypes.c_bool, ctypes.c_bool]
        lib.processar_controlador.restype = ctypes.c_int32
        
        return lib
    
    except Exception as e:
        print(f"ERRO CRÍTICO AO CARREGAR DLL: {e}")
        sys.exit(1)



def executar_simulação(controlador):
    data = SimulationLoop(controlador)

    # Finalização e Exportação
    df = pd.DataFrame(data, columns=['Hora', 'Tecla', 'Posicao', 'Estado'])
    df.to_csv(CSV_NOME, index=False)
    print(f"Simulação concluída. Gerado '{CSV_NOME}'.")
    
    gerar_grafico_interativo(df, f"SIL: Simulação de 24h com Zona Morta")    
    


if __name__ == "__main__":
    print("--- Iniciando Simulação SIL (Software-in-the-Loop) ---")
    executar_simulação(carregar_controlador())  