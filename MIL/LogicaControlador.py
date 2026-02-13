"""
Módulo: logica_controlador
Descrição: Implementação da lógica de controle para simulação MIL.
Autor: Omar Achraf (omarachraf@gmail.com)
Data: 12/02/2026
"""


# =============================================================================
# MÓDULO: CONTROLADOR (LÓGICA DE CONTROLE - MIL)
# =============================================================================
"""
Máquina de Estados de um botão: 0:FECHADO, 1:ABRINDO, 2:PARADO, 3:FECHANDO.
"""
class LogicaControlador:

    def __init__(self):
        self.estado_atual = 0 
        

    def processar_controlador(self, tecla, fc_a, fc_f)->int:
        # Transição por pulso de rádio
        if tecla:
            self.estado_atual = (self.estado_atual + 1) % 4
        
        # Proteção por Fim de Curso (FC)
        if fc_a and self.estado_atual == 1: self.estado_atual = 2 # Travou aberto
        if fc_f and self.estado_atual == 3: self.estado_atual = 0 # Travou fechado
        
        # Mapeamento do Estado para saída do Motor
        if self.estado_atual == 1: return 1   # Comando Abrir
        if self.estado_atual == 3: return -1  # Comando Fechar
        
        return 0                              # Motor Parado

