/**
 * =============================================================================
 * PROJETO: SIMULADOR DE PORTÃO - NÍVEL HIL (Hardware-in-the-Loop)
 * FIRMWARE: CONTROLADOR EMBARCADO (LOGICA DE ESTADOS)
 * =============================================================================
 * 
 * @author Omar Achraf (omarachraf@gmail.com)
 * @date 2026-02-12
 * 
 * ARQUITETURAS ALVO: 
 * - AVR (Arduino Uno, Nano, Mega): 8-bit, 16MHz, Word: 16-bit (int), SRAM: 2KB-8KB.
 * - ARM (Arduino Due, ESP32, STM32): 32-bit, 80MHz+, Word: 32-bit (int), SRAM: 20KB+.
 * 
 * DETALHES TÉCNICOS:
 * - Endianness: Little-Endian (Padrão na maioria dos microcontroladores modernos).
 * - Tipagem: Uso de <stdint.h> (int32_t) para garantir 4 bytes em qualquer arquitetura.
 * - Comunicação: Serial assíncrona (UART) via USB.
 * - Latência: Loop otimizado para resposta determinística (Real-Time).
 * 
 * PROTOCOLO DE MENSAGEM:
 * - Entrada (PC -> HW): "T,A,F\n" (Tecla, Fim de Curso Aberto, Fim de Curso Fechado)
 * - Saída (HW -> PC): "M\n" (Comando do Motor: -1, 0, 1)
 * =============================================================================
 */

#include "LogicaControlador.h"



LogicaControlador controlador;


void setup() {
  Serial.begin(115200);
}



void loop() {
  // Verifica se há dados no buffer (Recebimento da planta física do Python)
  if (Serial.available() > 0) {
    
    // Leitura da string de comando: Formato esperado "T,A,F\n"
    String payload = Serial.readStringUntil('\n');
    
    if (payload.length() >= 5) {
      // Parse manual (Seguro para 8-bit e 32-bit)
      // O caractere '0' é subtraído para converter ASCII em inteiro
      bool tecla = payload[0] - '0';
      bool fc_a  = payload[2] - '0';
      bool fc_f  = payload[4] - '0';

      int32_t cmd_motor = controlador.processar_controlador(tecla, fc_a, fc_f);

      // --- RESPOSTA PARA O PYTHON (PLANTA) ---
      // Enviamos apenas o comando do motor seguido de newline
      Serial.println(cmd_motor);
    }
  }
}