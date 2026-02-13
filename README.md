# 🌀 Simulador de Automação de Portão: MIL, SIL & HIL

Este projeto demonstra o ciclo de vida de desenvolvimento de um sistema crítico de automação de portão residencial, utilizando a metodologia V-Model para garantir que a lógica de controle seja validada exaustivamente antes de chegar ao hardware final.

Autor: Omar Achraf  
Contato: omarachraf@gmail.com  
Data: Fevereiro de 2026  

## 🛠️ O que é este projeto?  

O objetivo é desenvolver um controlador de portão de garagem robusto. Em vez de escrever o código e testar diretamente no motor (correndo o risco de danos físicos), utilizamos três níveis de abstração e simulação para validar a lógica e o hardware.

## 🏗️ Níveis de Simulação

### MIL (Model-in-the-Loop)

Pasta: MIL/  

O que é:  

Tudo é puramente matemático e escrito em Python. Tanto o controlador (o "cérebro") quanto a planta (a física do portão, inércia, sensores) são modelos virtuais.  

Objetivo:  

Validar se a lógica da máquina de estados (Abrir -> Parar -> Fechar -> Parar) funciona conforme o esperado.  

### SIL (Software-in-the-Loop)

Pasta: SIL/  

O que é:  

O controlador é traduzido para C++ e compilado como uma DLL (binário). O Python continua simulando a física, mas agora ele "chama" o código C++ real.  

Objetivo:  

Validar a tradução da lógica para C++ e garantir que não existam erros de tipos de dados (16/32/64 bits) ou transbordamento de memória. É o código que será usado no chip, mas rodando no Windows.  

### HIL (Hardware-in-the-Loop)

Pasta: HIL/  

O que é:  

O código C++ é carregado em um microcontrolador real (Arduino Mega). O Python simula a planta física no PC e troca dados em tempo real com o Arduino via Serial (USB).  

Objetivo:  

Validar o hardware e a performance em tempo real. O controlador "acha" que está controlando um portão real, enquanto o Python fornece as leituras de sensores e recebe os comandos do motor.  

### 📂 Estrutura de Arquivos

Plaintext  
estudo_MIL_SIL_HIL/  
├ README.md                <-- Este documento  
├ MIL/  
│   ├ LogicaControlador.py <-- Modelo da lógica do Controlador em Python  
│   ├ PlantaPortao.py      <-- Modelo da lógica do Portão em Python  
│   ├ SimulationLoop.py    <-- Loop da Simulação em Python  
│   ├ Grafico.py           <-- Utilitário par ageraçao de grafico interativo em Python  
│   └ mil.py               <-- Script de simulação puramente Python  
├ SIL/  
│   ├ controlador.cpp      <-- Wrapper C++ para gerar a DLL. Instruções de compilação no header  
│   └ sil.py               <-- Script que carrega a DLL e testa a física  
└ HIL/  
    ├ firmware/            <-- Pasta do código Arduino (.ino) e do fonte do controlador efetivo  
    │   ├ firmware.ino  
    │   ─ LogicaControlador.h <-- Fonte Única da Verdade (C++ Header)  
    └ hil.py               <-- Script de sincronismo Tempo Real PC <-> Arduino  

### 🚀 Como Executar

Pré-requisitos
Python 3.8+ (x64 recomendado)

Compilador C++ (MSVC ou MinGW)

Arduino IDE (para o nível HIL)

Bibliotecas: pip install pandas plotly pyserial

Executando o SIL (Exemplo)
Compile a DLL: cl /LD controlador.cpp /Fe:controlador.dll

Rode a simulação: python sil.py

### 🧠 Filosofia de Design: "Single Source of Truth"

Para evitar divergências entre o simulador e o hardware, este projeto utiliza o arquivo LogicaControlador.h como fonte única.

No SIL, o compilador do Windows lê este arquivo.

No HIL, o compilador do Arduino (AVR) lê este mesmo arquivo via Symlink.
Isso garante que qualquer melhoria na lógica seja refletida instantaneamente em todos os níveis de teste.