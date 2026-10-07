# Status da campanha SempreTech

Atualizado em 06/10/2026, com a entrada do novo ICP. Os números de ligação são do primeiro dia, 05/10.

## Onde ver

- Relatório do cliente: https://espartabranding.github.io/crm-esparta-sempretech/cliente/
- Painel do SDR: https://espartabranding.github.io/crm-esparta-sempretech/

Os dois são abertos a quem tem o link. O relatório do cliente não traz playbook, roteiros nem ressalvas internas.

## Carteira a partir de 06/10/2026

O ICP foi refeito a partir do catálogo real da SempreTech (empresa local de 5 a 100 funcionários, que compra de 5 a 40 computadores de mesa). A carteira passou a ter 308 contas:

- 9 contas da lista antiga, mantidas por estarem ativas: as 7 da esteira 2 e as 2 com retorno combinado (Online Gestão e Polo Logística).
- 40 contas novas, estudadas a fundo, com identificador `n1` a `n40`: 15 na semana 1, 15 na semana 2 e 10 em "validar dados antes". Valor de referência somado: R$ 395.469, a preço de site.

- 259 contas restantes da base de 300 (prioridade A), com identificador `m1` a `m259`, sem estudo individual: entram como não abordadas, com o roteiro da frente e o combo indicado na planilha. O fit delas é preliminar (avaliações no Google, site e celular) e nunca chega à faixa A.

Em 07/10 voltaram ao painel as 13 contas da lista antiga que tinham saído com o novo ICP (EPMAN, Iplasa, Salvador Armazéns Gerais, Labchecap, Projet, ECMAN, Construtora Lustosa, Line, Bahia Logística, Escola Rembrandt, TEL, Grupo LAS e Conceito Brasil): todas foram abordadas em 05/10 e precisam aparecer no kanban. A carteira tem 321 contas, 22 delas já abordadas.

As ofertas das contas novas são os combos C1 a C7 (Estação Criativa, Laboratório Pronto, Posição de Atendimento, Caixa Pronto, Parceiro Técnico, Escritório em Dia e Segurança). Só entram máquinas que rodam o Windows 11. O fit das contas novas foi derivado do estudo: compra local, quantidade estimada, aderência e acesso a quem decide.

## Painel e ofertas (06/10/2026)

- O painel abre na tela **Inteligência** (o que já foi abordado, status, fila com técnica e oferta, combos) e ganhou **Kanban** e **Tarefas**. Mover cartão e concluir tarefa ficam só no navegador de quem mexe.
- **Propostas visuais:** `ofertas.py` gera a página de oferta das contas estudadas e das que estão na etapa de apresentar a proposta personalizada (47 em 07/10), em `docs/ofertas/`, com um índice e a mensagem pronta de cada conta. Sem JavaScript, com as fotos embutidas. Para gerar de novo: `uv run python ofertas.py`.
- **PDF de cada proposta:** `uv run python ofertas.py --pdf` gera em `docs/ofertas/pdf/` os PDFs que faltam (caderno de 7 páginas em A4 deitado; usa o Chrome ou o Edge instalado). `--pdf-refazer` gera todos de novo.
- **Na ficha do lead:** os botões "Visualizar proposta" e "Baixar proposta para envio" (PDF ou HTML) aparecem em todas as abas, e a aba "Proposta visual" mostra a página. As contas da primeira rodada usam o combo Escritório em Dia.
- O kanban tem uma só etapa de proposta, "Apresentar a proposta personalizada"; o registro antigo "enviar" cai nela.
- **Desconto:** desde 07/10 todas as propostas saem com 15% de desconto sobre a soma dos itens a preço de site (constante `DESCONTO` em `ofertas.py`). O preço de cada item continua sendo o do site; o desconto aparece na capa, no resumo e nos lotes.
- O botão das ofertas leva ao WhatsApp do site da SempreTech, (71) 3034-9662; os preços são os de varejo do site em 06/10.
- O CRM com banco e login está em outro projeto, `../SempreTech_CRM`, com a mesma carteira carregada.

## Números de 05/10

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
- Importar no Callix as contas novas, a começar pelas 15 da semana 1, e tirar da campanha as 13 que saíram.
- Rever as propostas da esteira 2 antes do envio: os preços do site subiram entre 05/10 e 06/10 (o i3 6100 passou de R$ 1.449,99 para R$ 1.659,99), e a referência do posto de trabalho passou para o i3 10100, de R$ 1.920,91.
- Confirmar com a SempreTech os itens da lista "A confirmar" do playbook, a começar pelo posicionamento "especialistas em logística e performance em informática" e pelos produtos fora do site.
- Criar as qualificações no Callix e tirar da lista da campanha as quatro contas removidas.
- As ligações de 05/10 não passaram pelo Callix: foram registradas à mão em `tentativas.json`, sem gravação nem transcrição.

## Como atualizar

1. Registrar o resultado de cada contato em `tentativas.json` (conta, quando, nota, qualificação, etapa, se conversou, e, se quiser fixar o prazo da tarefa, `prazo` no formato `2026-10-08`). Etapas mudadas no kanban e tarefas concluídas no painel ficam só no navegador de quem mexeu: o kanban tem um botão que copia os movimentos prontos para colar neste arquivo.
2. `uv run python main.py` sincroniza o Callix e regenera o painel e o relatório do cliente em `docs/`.
3. Um único `git push` publica os dois endereços. Publicar em lote: envios seguidos cancelam a publicação que está na fila.
