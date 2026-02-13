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

### 📋 Guia de Portabilidade: SIL para HIL

#### Tipagem e Largura de Banda (Data Width)

O quê: O tamanho em bits de tipos como int ou long.

O Problema: No PC (x64), um int tem 32 bits. No Arduino Mega (AVR), um int tem apenas 16 bits. Se você contar segundos em um int no Arduino, após 9 horas o valor estoura e fica negativo, enquanto no PC ele continuaria contando por anos.

Por que observar: Para evitar Overflow (transbordamento) e garantir que o cálculo matemático seja idêntico em ambas as máquinas.

Solução: Use tipos de largura fixa (<stdint.h>): int32_t, uint8_t, int16_t.

#### Endianness (Ordenação de Bytes)

O quê: A ordem em que os bytes de um número multi-byte são armazenados na memória.

O Problema: Se o PC enviar o número 0x1234 e o hardware ler como 0x3412, sua lógica de controle receberá valores errados.

Por que observar: Essencial se você enviar dados binários brutos por Serial ou via protocolos de rede.

Solução: Como seu projeto usa strings ASCII ("1,0,1"), este problema é mitigado. Se usar binário, use funções como htons() ou garanta que ambos sejam Little-Endian.

#### Padding e Alinhamento (Memory Alignment)

O quê: Espaços vazios que o compilador insere entre variáveis dentro de uma struct.

O Problema: Processadores de 64 bits gostam de dados alinhados em endereços múltiplos de 8. Eles podem inserir "buracos" (padding) na sua estrutura de dados. O Arduino (8 bits) não faz isso.

Por que observar: Se você mapear uma struct diretamente sobre um buffer de dados recebido, os campos podem estar "deslocados" no PC em relação ao hardware.

Solução: Use o atributo __attribute__((packed)) em C++ para forçar o compilador a remover espaços vazios.

#### Representação de Ponto Flutuante

O quê: Como números decimais são processados.

O Problema: O Python usa double (64 bits) por padrão. O Arduino Mega (AVR) não possui suporte nativo a double; ele trata double como float (32 bits).

Por que observar: Erros de arredondamento acumulados podem fazer com que o portão pare em 4.999m no Arduino e 5.000m no Python, impedindo o acionamento de um sensor de fim de curso por uma diferença infinitesimal.

Solução: Utilize float no SIL para simular com a mesma (baixa) precisão que o hardware real terá.


#### Promoção de Inteiros e Divisão
O quê: Como o compilador lida com cálculos entre tipos diferentes.

O Problema: int a = 5 / 2; resulta em 2 (inteiro). No Python, 5 / 2 resulta em 2.5.

Por que observar: Se a sua lógica de controle depende de divisões, o comportamento de truncamento do C++ deve ser testado rigorosamente no SIL antes de ir para o HIL.

Solução: Sempre force o tipo desejado (ex: 5.0f / 2.0f) para garantir que o resultado seja decimal onde necessário.

#### 🚀 Resumo

A paridade entre SIL e HIL é garantida pelo uso de tipos Fixed-Width (stdint.h), eliminando divergências de arquitetura (16 vs 64 bits), e pela comunicação baseada em Strings ASCII, o que torna o sistema imune a discrepâncias de Endianness e Memory Padding.


### 📂 Estrutura de Arquivos

```Plaintext  
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
    │   └ LogicaControlador.h <-- Fonte Única da Verdade (C++ Header)  
    └ hil.py               <-- Script de sincronismo Tempo Real PC <-> Arduino  
```

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
