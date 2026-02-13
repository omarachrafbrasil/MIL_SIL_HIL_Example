/**
 * @file LogicaControlador.h
 * @brief Definição da Máquina de Estados do Controlador de Portão.
 * @version 1.0
 * @author Omar Achraf (omarachraf@gmail.com)
 * @date 2026-02-12
 **/

#ifndef LOGICA_CONTROLADOR_H
#define LOGICA_CONTROLADOR_H

#include <stdint.h>

/*
    Máquina de Estados de um botão: 0:FECHADO, 1:ABRINDO, 2:PARADO, 3:FECHANDO.
*/
class LogicaControlador {
private:
    int32_t estado_atual;

public:
    LogicaControlador() : estado_atual(0) {

    }

    int32_t processar_controlador(bool tecla, bool fc_a, bool fc_f) {
        // Transição por pulso de rádio
        if (tecla) {
            estado_atual = (estado_atual + 1) % 4;
        }

        // Proteção por Fim de Curso (FC)
        if (fc_a && estado_atual == 1) estado_atual = 2; // Travou aberto
        if (fc_f && estado_atual == 3) estado_atual = 0; // Travou fechado

        // Mapeamento do Estado para saída do Motor
        if (estado_atual == 1) return 1;  // Comando Abrir
        if (estado_atual == 3) return -1; // Comando Fecahr

        return 0;                         // Motor Parado
    }



    void reset() { 
        estado_atual = 0; 
    }
};

#endif