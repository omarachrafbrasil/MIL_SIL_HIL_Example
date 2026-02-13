"""
=============================================================================
PROJETO: SIMULADOR DE PORTÃO DE GARAGEM - NÍVEL HIL (Hardware-in-the-Loop)
=============================================================================
DESCRIÇÃO:
    Este script executa a simulação da Planta Física em Python e comunica-se
    em tempo real com o hardware (Arduino) via Serial.
    
    Autor: Omar Achraf (omarachraf@gmail.com)
    Data: 12/02/2026       
    
REQUISITOS:
    - Arduino com firmware.ino carregado.
    - Biblioteca: pip install pyserial pandas plotly
    - Ajustar a variável PORTA_SERIAL para a sua porta COM.
=============================================================================
"""

import serial
import time
import pandas as pd
import os

import sys
import os
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
raiz_projeto = os.path.dirname(diretorio_atual)
sys.path.append(raiz_projeto)
from MIL.SimulationLoop import SimulationLoop
from MIL.Grafico import gerar_grafico_interativo



CSV_NOME    = "simulacao_portao_24h_HIL.csv"



# --- CONFIGURAÇÕES DO HARDWARE ---
PORTA_SERIAL = 'COM3'  # <--- ALTERE PARA A SUA PORTA (Ex: COM3, COM4, /dev/ttyACM0)
BAUD_RATE    = 115200  # Deve ser igual ao do firmware.ino
TIMEOUT      = 0.5     # Tempo máximo de espera pela resposta do Arduino



# --- CONEXÃO SERIAL ---
def get_serial():
    try:
        processador_hw = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=TIMEOUT)
        time.sleep(2)  # Aguarda o Arduino dar o boot (reset automático do DTR)
        print(f"✓ Conectado ao Arduino na porta {PORTA_SERIAL}")
        return processador_hw
    
    except Exception as e:
        print(f"✗ ERRO DE CONEXÃO: {e}")
        print("Verifique se o Arduino está conectado e se a porta COM está correta.")
        exit()



# =============================================================================
# CONTROLADOR Wrapper para o Hardware Cotnrolador
# =============================================================================
class LogicaControlador:
    
    def __init__(self, processador_hw):
        self.processador_hw = processador_hw
        
        
        
    def processar_controlador(self, tecla, fc_a, fc_f)->int:
        # COMUNICAÇÃO HIL: Enviar "T,A,F\n"
        payload = f"{tecla},{fc_a},{fc_f}\n"
        self.processador_hw.write(payload.encode('ascii'))   
        
        # RECEBER RESPOSTA DO HARDWARE: "Motor\n"
        try:
            resposta = self.processador_hw.readline().decode('ascii').strip()
            cmd_motor = int(resposta) if resposta else 0
        except:
            cmd_motor = 0 # Fallback de segurança se falhar a serial             
                        
        return cmd_motor
    


def carregar_controlador(processador_hw)->LogicaControlador: 
    return LogicaControlador(processador_hw)    



def executar_simulação(controlador):
    data = SimulationLoop(controlador)

    df = pd.DataFrame(data, columns=['Hora', 'Tecla', 'Posicao', 'Estado'])
    df.to_csv(CSV_NOME, index=False)
    print(f"Simulação concluída. Gerado '{CSV_NOME}'.")
    
    gerar_grafico_interativo(df, f"HIL: Simulação de 24h com Zona Morta")  
    


if __name__ == "__main__":
    print("--- Iniciando Simulação HIL (Hardware-in-the-Loop) ---")
    
    serial_comm = get_serial()
    executar_simulação(carregar_controlador(serial_comm))  