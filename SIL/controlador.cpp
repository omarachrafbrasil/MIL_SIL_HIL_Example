/**
 * =============================================================================
 * PROJETO: SIMULADOR DE PORTÃO DE GARAGEM - NÍVEL SIL (Software-in-the-Loop)
 * MÓDULO: CONTROLADOR DE ESTADOS (FIRMWARE)
 * =============================================================================
 * 
 * DESCRIÇÃO:
 * Este código implementa a lógica de controle que será embarcada. No SIL,
 * ele é compilado como uma DLL para ser validado pelo Python.
 * 
 * ESTADOS: 
 *   0: FECHADO, 1: ABRINDO, 2: PARADO, 3: FECHANDO
 * 
 * COMANDOS DE COMPILAÇÃO NO VS CODE TERMINAL:
 * 
 * MinGW (GCC):
 *   g++ -shared -o controlador.dll controlador.cpp
 * 
 * Visual Studio (MSVC):
 *   Usar o "Developer PowerShell for VS 2022":
 * 
 * 1-Pressione a tecla Win no teclado e digite: 
 *   x64 Native Tools Command Prompt for VS 2022
 * 2-Abra esse terminal especial (ele já vem com todos os caminhos do compilador configurados).
 * 3-Navegue até sua pasta onde esta o fonte do controlador.cpp, digamos:
 *   cd C:\development\projects\estudo_MIL_SIL_HIL\SIL 
 * 4-Execute o comando:
 *   cl /LD controlador.cpp /Fe:controlador.dll
 * 
 * REQUISITOS DE SISTEMA:
 * - Compilador C++ (GCC ou MSVC)
 * - Arquitetura compatível com o Python instalado (ex: x64)
 * =============================================================================
 */

#include <stdint.h>

#include "..\HIL\firmware\LogicaControlador.h"

LogicaControlador controlador;



// Macro para exportação de funções (Garante compatibilidade Windows/DLL)
#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif



extern "C" {

    /**
     * Processa um ciclo da máquina de estados.
     * @param tecla True se o rádio foi pressionado.
     * @param fc_a True se o sensor de fim de curso aberto está ativo.
     * @param fc_f True se o sensor de fim de curso fechado está ativo.
     * @return int32_t Comando para o motor: 1 (Abrir), -1 (Fechar), 0 (Parar).
     */
    EXPORT int32_t processar_controlador(bool tecla, bool fc_a, bool fc_f) {
        return controlador.processar_controlador(tecla, fc_a, fc_f);
    }



    /**
     * Reseta o estado do controlador (útil para reiniciar simulações)
     */
    EXPORT void reset_controlador() {
        controlador.reset();
    }
}