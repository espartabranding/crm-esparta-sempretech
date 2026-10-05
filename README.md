# CRM Esparta — SempreTech

Mesa de ligação da campanha de prospecção da SempreTech: junta o plano de contas, a pesquisa de cada empresa, o playbook de ligação e os dados das chamadas feitas no Callix.

## O que faz

- Busca as ligações da campanha no Callix (dados, qualificação e gravação).
- Transcreve as gravações nesta máquina e avalia cada conversa.
- Gera o painel em `data/painel.html`, com uma aba por lead (roteiro, análise da empresa, BI e histórico), segmentação, playbook e catálogo.

## Como rodar

1. Copie `.env.example` para `.env` e preencha o token do Callix (`Configurações > APIs > Acesso à API`).
2. `uv sync`
3. `uv run python main.py` sincroniza, transcreve, avalia e regenera o painel.
   - `--dias N` muda a janela de busca (até 31 dias).
   - `--sem-audio` não baixa as gravações.
   - `--sem-analise` não transcreve nem avalia.
4. `uv run python painel.py` só regenera o painel a partir do que já foi sincronizado.

A transcrição usa a instalação do Esparta Transcribe em `C:\Scripts\esparta-transcribe` (variável `ESPARTA_TRANSCRIBE` para outro caminho). A avaliação das conversas chama o Claude pela linha de comando (`claude -p`).

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `main.py` | Sincronização com o Callix |
| `callix.py` | Cliente da API do Callix |
| `conversa.py` | Transcrição, métricas e avaliação das conversas |
| `transcritor.py` | Transcrição com vocabulário da conta (roda no Python do Esparta Transcribe) |
| `painel.py`, `painel_modelo.html` | Geração do painel |
| `contas.json` | As contas do plano, com fit e aderência |
| `analises/` | Pesquisa de cada empresa |
| `catalogo.json` | Catálogo da SempreTech (site, consultado em 05/10/2026) |
| `playbook.json` | Soluções, roteiros por segmento, objeções e qualificações |
| `prompts.md` | Prompts prontos para abordagem, resumo e avaliação |

## Dados fora do repositório

`.env` (token) e `data/` (banco, gravações, transcrições e painel gerado) não são versionados: contêm segredo e dados pessoais.
