# 🎛️ RoboControl Studio — Painel Dual-ESP v3.0 & Ambiente de Configuração do Roboldo

[![RoboControl Studio CI](https://github.com/ROBOLDO-UERN/RoboControl-Studio/actions/workflows/robocontrol-studio-ci.yml/badge.svg)](https://github.com/ROBOLDO-UERN/RoboControl-Studio/actions/workflows/robocontrol-studio-ci.yml)

Repositório dedicado do **RoboControl Studio (Dual-ESP v3.0)** — o painel avançado de configuração, calibração cinemática, controle **Dual USB Web Serial** (ESP1 Cabeça + ESP2 Braços 3-DoF), síntese de voz neural offline (**Piper TTS** `pt-BR`) com sincronia labial DWIN e sequenciador de coreografias em tempo real do **Roboldo** (**LAR / UERN**).

---

## 🎯 Funcionalidades Principais

1. **Gerenciador Dual Web Serial Independente**:
   - **USB 1 • ESP Cabeça (`9600 bps`)**: Controle de expressões faciais no display **DWIN HMI** (`Neutral`, `Angry`, `Confused`, `Fear`, `Happy`, `Sad`, `Surprised`), estilos de fala (`Sílabas`, `Animado`, `Rápido`) e controle manual `RAW:earR,earL,neck,speed` dos 3 servos da cabeça (Orelha Direita, Orelha Esquerda e Pescoço MG995).
   - **USB 2 • ESP Braços 3-DoF (`115200 bps`)**: Disparo de coreografias em hardware LEDC 14-Bits (`'n'`, `'ad'`, `'ae'`, `'a2'`, `'ab'`, `'mc'`, `'am'`, `'d'`) e controle de poses customizadas com 6 ângulos independentes (`P_D,R_D,C_D,P_E,R_E,C_E`) e espelhamento simétrico.
2. **Macros Sincronizadas (Cabeça + Braços)**:
   - Disparo simultâneo para ambos os ESP32 (*Neutro Total*, *Olá Feliz*, *Abraço Acolhedor*, *Cumprimento Formal*, *Bravo na Cintura*, *Surpreso / Aceno Duplo* e *Modo Festa / Dança*).
3. **Simulador Cinético 2D em Tempo Real**:
   - Visualização interativa em SVG reproduzindo a expressão facial DWIN, rotação das orelhas/pescoço e interpolação de *keyframes* dos braços 3-DoF.
4. **Painel de Voz Offline (Piper TTS + Auto Lip-Sync DWIN)**:
   - Síntese de voz neural local em português (`pt_BR-faber-medium.onnx`) via `/api/synthesize` com ajuste de Tom (*Pitch*), Velocidade (*Rate*), Volume e fallback automático via *Web Speech API* caso o modelo `.onnx` não esteja presente.
5. **Sequenciador de Scripts & Coreografias Timed**:
   - Timeline interativa em milissegundos combinando comandos da Cabeça, poses de 6 ângulos dos Braços e falas sincronizadas do Piper TTS, com captura instantânea de sliders e importação/exportação JSON.
6. **Inspetor Dual de Payloads & Monitor Serial TX/RX**:
   - Alternância em tempo real entre **Protocolo Nativo (Strings C++)** e **Pacotes JSON (`HeadCommandPacket` / `ArmCommandPacket`)**.

---

## 🚀 Como Executar Localmente

```bash
# 1. Instalar dependências Python (opcional para síntese local Piper TTS)
pip install -r requirements.txt

# 2. Iniciar o servidor local na porta 3000
python server.py
# Ou via Node.js:
npm start
```

Acesse no navegador (**Google Chrome** ou **Microsoft Edge** para suporte à **Web Serial API**):
- **Painel Principal Completo (`RoboControl Studio v3.0`)**: `http://127.0.0.1:3000/painel`
- **Painel Simples de Voz Offline**: `http://127.0.0.1:3000/`

---

## 👥 Equipes Responsáveis (`CODEOWNERS`)

- **Zona 4 (Mecânica, Elétrica & Hardware)**: `@ROBOLDO-UERN/zona-mecanica-hardware` ([📋 Project Zona 4](https://github.com/orgs/ROBOLDO-UERN/projects/4))
- **Zona 2 (Voz & Expressividade)**: `@ROBOLDO-UERN/zona-voz` ([📋 Project Zona 2](https://github.com/orgs/ROBOLDO-UERN/projects/2))
- **Coordenação**: `@ROBOLDO-UERN/professores` & `@ROBOLDO-UERN/bolsistas`
- **Painel Geral da Organização**: [📋 Central Geral de Trabalhos (Project #6)](https://github.com/orgs/ROBOLDO-UERN/projects/6)
