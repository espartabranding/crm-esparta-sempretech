# Status da campanha SempreTech

Atualizado em 05/10/2026, ao fim do primeiro dia de ligações.

## Onde ver

- Relatório do cliente: https://espartabranding.github.io/crm-esparta-sempretech/cliente/
- Painel do SDR: https://espartabranding.github.io/crm-esparta-sempretech/

Os dois são abertos a quem tem o link. O relatório do cliente não traz playbook, roteiros nem ressalvas internas.

## Números do dia

- 22 contas na carteira (26 no início; saíram Hullo, UNIFTC, Conterp e UCSal).
- 22 contas ligadas, 10 atendidas.
- 14 contas na esteira 1 (abordagem inicial), 7 na esteira 2 (proposta objetiva), 1 encerrada.

## Esteira 2: proposta objetiva

| Conta | Contato | Próximo passo |
|---|---|---|
| OCC Empreendimentos | Gesa, gesa.conceicao@occ.eng.br | Enviar a proposta por e-mail |
| Santacruz Engenharia | Antônio, compras@santacruzengenharia.com.br | Enviar a proposta por e-mail |
| Tidelli | Diego, diego@tidelli.com.br | Enviar a proposta por e-mail |
| Total Atacado | Igor, WhatsApp (71) 3183-1115 | Enviar a proposta por WhatsApp |
| Costa Andrade | Sergio, compras, (71) 3018-0988 | Ligar e apresentar a proposta |
| Grupo MAX FORTE | Paulo, suprimentos e tecnologia, (71) 99150-9724 | Ligar e apresentar a proposta |
| Top Engenharia | Lucas e Antonio, Operações e Tecnologia, (71) 2109-4949 | Ligar em 06/10 |

## Esteira 1: abordagem inicial

- Retorno combinado: Online Gestão, Polo Logística (em horário comercial, pela manhã).
- Abordar por WhatsApp: Projet (71) 98818-3740, Escola Rembrandt (71) 99913-2108.
- Nova tentativa: ECMAN, Bahia Logística, Conceito Brasil, Grupo LAS, Line (06/10), TEL (06/10), Labchecap, Construtora Lustosa (telefone fora de área).
- Iplasa: informática terceirizada; pedir compras ou o administrativo.
- EPMAN: ligação falhou e o CNPJ consta como baixado; testar o (71) 3111-9493 uma vez.

Encerrada: Salvador Armazéns Gerais (sem interesse).

## Pendências

- Enviar os três e-mails e as três mensagens de WhatsApp já redigidos (OCC, Santacruz, Tidelli; Total Atacado, Projet, Escola Rembrandt).
- Confirmar com a SempreTech os itens da lista "A confirmar" do playbook, a começar pelo posicionamento "especialistas em logística e performance em informática" e pelos produtos fora do site.
- Criar as qualificações no Callix e tirar da lista da campanha as quatro contas removidas.
- As ligações de 05/10 não passaram pelo Callix: foram registradas à mão em `tentativas.json`, sem gravação nem transcrição.

## Como atualizar

1. Registrar o resultado de cada contato em `tentativas.json` (conta, quando, nota, qualificação, etapa, se conversou).
2. `uv run python main.py` sincroniza o Callix e regenera o painel e o relatório do cliente em `docs/`.
3. Um único `git push` publica os dois endereços. Publicar em lote: envios seguidos cancelam a publicação que está na fila.
