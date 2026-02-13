# =============================================================================
# MÓDULO: PLANTA (MODELO FÍSICO)
# =============================================================================

"""
Simula o comportamento físico do portão de garagem.
Aplica atraso de movimento (Zona Morta) quando há inversão de sentido.
"""
class PlantaPortao:
    
    def __init__(self, velocidade, curso_total, zona_morta):
        self.posicao = 0.0          
        self.folga_acumulada = 0.0   
        self.direcao_atual = 0  # -1 (fechando), 0 (parado), 1 (abrindo)
        self.velocidade = velocidade
        self.curso_total = curso_total
        self.zona_morta = zona_morta



    def calcular(self, motor_cmd, dt):
        # Se o comando inverter ou sair do repouso, reseta a folga acumulada
        if motor_cmd != 0 and motor_cmd != self.direcao_atual:
            self.folga_acumulada = 0.0
            self.direcao_atual = motor_cmd
        
        # Lógica de Zona Morta: O motor gira mas o portão só move após vencer a folga
        if motor_cmd != 0 and self.folga_acumulada < self.zona_morta:
            distancia_tentada = abs(self.velocidade * dt)
            self.folga_acumulada += distancia_tentada
            return self.posicao 

        # Movimento Linear Efetivo
        if motor_cmd == 1: # Abrindo
            self.posicao = min(self.curso_total, self.posicao + self.velocidade * dt)
        elif motor_cmd == -1: # Fechando
            self.posicao = max(0.0, self.posicao - self.velocidade * dt)
        
        return self.posicao