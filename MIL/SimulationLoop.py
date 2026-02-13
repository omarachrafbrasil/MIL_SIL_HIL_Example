
import random

import sys
import os
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
raiz_projeto = os.path.dirname(diretorio_atual)
sys.path.append(raiz_projeto)
from MIL.PlantaPortao import PlantaPortao



# =============================================================================
# CONFIGURAÇÕES GLOBAIS DA SIMULAÇÃO (PARAMETRIZAÇÃO)
# =============================================================================

VELOCIDADE  = 0.5       # Velocidade nominal do portão (metros por segundo)
CURSO_TOTAL = 5.0       # Comprimento total do trilho (metros)
ZONA_MORTA  = 0.2       # Folga mecânica/engrenagem a ser vencida (metros)

DT          = 0.1       # Passo de tempo (segundos) - Frequência de 10Hz
TOTAL_HORAS = 24        # Duração total da simulação (1 dia de uso)
SEMENTE     = 42        # Semente aleatória para repetibilidade



def SimulationLoop(controlador)->None:
    planta = PlantaPortao(VELOCIDADE, CURSO_TOTAL, ZONA_MORTA)      
        
    passos = int((TOTAL_HORAS * 3600) / DT)
    data = []

    random.seed(SEMENTE)

    for i in range(passos):
        t = i * DT
        hora = t / 3600
        
        # Simulação de eventos de rádio (Picos de manhã e tarde)
        prob = 0.00001
        if (7.9 < hora < 8.1) or (17.9 < hora < 18.1):
            prob = 0.005 
        
        tecla = random.random() < prob
        
        # Ciclo de Controle
        
        # Sensores Fim de Curso
        fc_a = (planta.posicao >= CURSO_TOTAL)
        fc_f = (planta.posicao <= 0.0)
        
        # Chamado ao Controlador Modelo em Python 
        cmd_motor = controlador.processar_controlador(tecla, fc_a, fc_f)
        
        # Atualiza a física
        posicao_atual = planta.calcular(cmd_motor, DT)
        
        # Salva dados para o gráfico se houver atividade
        if tecla or cmd_motor != 0 or i % 100 == 0:
            data.append([hora, tecla, posicao_atual, cmd_motor])

    # Finalização e Exportação
    return data    