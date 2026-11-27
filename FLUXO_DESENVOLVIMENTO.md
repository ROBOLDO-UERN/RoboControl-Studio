# Fluxo de Desenvolvimento — Ecossistema Lojinha do Roboldo

Este documento define o fluxo de desenvolvimento, organização de branches e empacotamento dos aplicativos do **Roboldo** no repositório [`Misians/Roboldo-Game-Perguntas-e-Respostas`](https://github.com/Misians/Roboldo-Game-Perguntas-e-Respostas).

---

## 1. Arquitetura dos Apps no Repositório

Cada aplicativo do Roboldo vive em sua própria branch independente (órfã ou dedicada) no mesmo repositório, permitindo versionamento e deploy separados sem conflitos:

| App ID | Nome | Branch | Status na Lojinha | Função |
| :--- | :--- | :--- | :--- | :--- |
| `roboldo-config` | **Ambiente de Configuração do Roboldo** (`RoboControl Studio`) | `ambiente-configuracao` | **Pré-instalado** (`preinstalled: true`) | Controle Dual USB Serial (ESP Cabeça + ESP Braços), voz offline (Piper TTS), simulador cinemático e sequenciador de coreografias. |
| `roboldo-perguntas-e-respostas` | **Roboldo Educa — Perguntas e Respostas** | `master` | **Instalável na Lojinha** (`installable: true`) | Jogo educacional interativo (Flutter + Web) com telemetria UDP. |

Os metadados de integração ficam padronizados em:
- `roboldo-app.json` — Manifesto individual do app (porta, comando de start, rota de entrada, capacidades, flag `preinstalled`).
- `lojinha-catalog.json` — Catálogo de referência da **Lojinha do Roboldo** mapeando cada app à sua respectiva branch.

---

## 2. Como Rodar o Ambiente de Configuração Localmente

### Pré-requisitos
- **Python 3.10+** (acessível via `py` no Windows ou `python3` no Linux)
- **Node.js 18+** (opcional, se preferir iniciar via `node server.mjs` / `npm start`)
- Modelo de voz Piper offline na raiz do projeto:
  - `pt_BR-faber-medium.onnx` (não versionado no Git por ser binário de ~63 MB)
  - `pt_BR-faber-medium.onnx.json` (versionado no repositório)

### Instalação e Execução
```bash
# 1. Instalar dependência do Piper TTS
pip install -r requirements.txt

# 2. Iniciar o servidor local (porta 3000)
py server.py
# ou via Node:
npm start
```

Acesse no navegador (Chrome/Edge para suporte à Web Serial API):
- **Painel Principal (Configuração Dual-ESP):** `http://127.0.0.1:3000/painel`
- **Painel Simples de Voz:** `http://127.0.0.1:3000/`

---

## 3. Fluxo de Trabalho Git (Desenvolvimento Paralelo)

### A. Trabalhando no Ambiente de Configuração (Pré-instalado)
1. Garanta que está na branch `ambiente-configuracao`:
   ```bash
   git checkout ambiente-configuracao
   ```
2. Edite o painel (`painel_de_controle_rob_social_usb(2).html`), servidor (`server.py` / `server.mjs`) ou manifesto (`roboldo-app.json`).
3. Teste localmente em `http://127.0.0.1:3000/painel` (verificando responsividade, Web Serial e `/api/synthesize`).
4. Atualize a versão em `roboldo-app.json` e `package.json` se for um release.
5. Envie para o GitHub:
   ```bash
   git add .
   git commit -m "feat(config): descreva sua alteração"
   git push origin ambiente-configuracao
   ```

### B. Trabalhando no App Perguntas e Respostas (Lojinha)
1. Troque para a branch `master` (ou use `git worktree` para manter as duas pastas abertas simultaneamente):
   ```bash
   git checkout master
   ```
2. Desenvolva e teste o app Flutter/Web normalmente.
3. Publique na `master` para disponibilizar a atualização na **Lojinha do Roboldo**.

### Dica: Usando `git worktree` (Recomendado)
Para não precisar ficar trocando de branch toda hora na mesma pasta:
```bash
# A partir do clone principal (na branch master):
git worktree add ../roboldo-config ambiente-configuracao
```
Assim você terá uma pasta só para o **Jogo (master)** e outra só para o **Ambiente de Configuração (ambiente-configuracao)**.

---

## 4. Contrato com a Lojinha do Roboldo

Quando a **Lojinha do Roboldo** lê este repositório:
1. Ela consulta o catálogo (`lojinha-catalog.json`) ou as branches registradas.
2. Apps com `"preinstalled": true` (`roboldo-config`) já vêm prontos no sistema e aparecem como **Instalado (Sistema)**, sem botão de desinstalar.
3. Apps com `"installable": true` (`roboldo-perguntas-e-respostas`) aparecem disponíveis para download/instalação sob demanda no tablet/sistema do Roboldo.
