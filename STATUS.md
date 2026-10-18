# Status da campanha SempreTech

Atualizado em 07/10/2026. A carteira tem 321 contas: 22 abordadas e 299 a abordar. Os números de ligação são do primeiro dia, 05/10; não houve registro de contato novo em 06/10 nem em 07/10.

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

## Painel e ofertas (07/10/2026)

- O menu tem **Inteligência** (tela de abertura), **Kanban**, **Tarefas**, **Segmentação**, **Playbook** e **Soluções e catálogo** (os dois últimos só no painel do SDR). As telas Esteiras e Visão geral saíram em 07/10; com a Visão geral saiu o bloco "Qualidade das conversas".
- **Kanban:** uma cor por etapa, com o cabeçalho da coluna pintado; sem valores em reais e sem rolagem interna (só "Não abordada" mostra 25 e um botão para as demais). Cada cartão tem o campo "Evolução até esta etapa", preenchido com os registros de contato e aberto para edição. Mover cartão, escrever na evolução e concluir tarefa ficam só no navegador de quem mexe.
- **Etapas:** "Abordar por WhatsApp" passou a "Abordar por canais de apoio". Nas tarefas, o prazo vencido aparece como "A fazer", sem o termo "Atrasada".
- **Visual:** fonte Montserrat em pesos leves, logotipo da SempreTech em branco na barra lateral e os blocos "Painel" e "Leads" em molduras separadas, com faixa azul de título.
- **Propostas visuais:** `ofertas.py` gera a página de oferta das contas estudadas e das que estão na etapa de apresentar a proposta personalizada (47 em 07/10), em `docs/ofertas/`, com um índice e a mensagem pronta de cada conta. Sem JavaScript, com as fotos embutidas. Para gerar de novo: `uv run python ofertas.py`.
- **PDF de cada proposta:** `uv run python ofertas.py --pdf` gera em `docs/ofertas/pdf/` os PDFs que faltam (caderno de 8 páginas em A4 deitado; usa o Chrome ou o Edge instalado). `--pdf-refazer` gera todos de novo.
- **Na ficha do lead:** os botões "Visualizar proposta" e "Baixar proposta para envio" (PDF ou HTML) aparecem em todas as abas, e a aba "Proposta visual" mostra a página. As contas da primeira rodada usam o combo Escritório em Dia.
- O kanban tem uma só etapa de proposta, "Apresentar a proposta personalizada"; o registro antigo "enviar" cai nela.
- **Desconto:** desde 08/10 todas as propostas saem com 30% de desconto (eram 15% em 07/10) sobre a soma dos itens a preço de site (constante `DESCONTO` em `ofertas.py`). O preço de cada item continua sendo o do site; o desconto aparece na capa, no resumo e nos lotes.
- **Outras ofertas (08/10):** os seis folhetos enviados pela SempreTech em 07/10 (energia solar, aluguel de máquinas gamers, aluguel de máquinas home, Kit PDV, bobinas térmicas 80 x 40 e fardamentos) entram ao fim de cada proposta, na seção "Também na SempreTech", e na tela "Soluções e catálogo" do painel do SDR. Não têm preço, então ficam fora do desconto e saem como orçamento sob consulta. O cadastro está em `outras_ofertas`, no `catalogo.json`, e os folhetos em `docs/ofertas/folhetos/`.
- O botão das ofertas leva ao WhatsApp do site da SempreTech, (71) 3034-9662; os preços são os de varejo do site em 06/10.
- O CRM com banco e login está em outro projeto, `../SempreTech_CRM`, com a mesma carteira carregada.

## Números de 05/10

- 22 contas na carteira daquele dia (26 no início; saíram Hullo, UNIFTC, Conterp e UCSal).
- 22 contas ligadas, 10 atendidas.
- 14 contas na esteira 1 (abordagem inicial), 7 na esteira 2 (proposta objetiva), 1 encerrada.

## Revendas

Em 07/10 foram marcadas como revenda 18 das 25 contas de "Técnicos e assistências" (campo `revenda` em `contas.json`): as que o Google Maps classifica também como loja (de informática, de acessórios, de celulares, de computadores usados) ou fornecedor de peças. É indício público, não confirmação por telefone. As 7 sem categoria de loja ficaram como assistência: Graftecno, Tecno Digital, Merontechx, Inforteck, Gigatech, Central Informática e ESA Tech.

Em 14/10 o site de cada uma dessas 7 foi consultado: Tecno Digital (loja on-line de acessórios) e Merontechx ("Loja Monte Seu PC") vendem equipamento e passaram a revenda, somando 20. Inforteck e Gigatech só anunciam serviço. Central Informática (site fora do ar), Graftecno e ESA Tech (sem site) seguem sem verificação: perguntar na ligação se vendem equipamento.

Revendas têm proposta própria da SempreTech. Desde 14/10 as 25 contas de "Técnicos e assistências" (20 revendas e 5 a confirmar) saem da fila de clientes finais e vão para `fila_revendas.csv`; nenhuma conta de outro segmento tem sinal de revenda. A fila de clientes finais (`fila_clientes_finais.csv`) tem 295 contas, 292 com telefone discável, agendadas de 15/10 a 26/10.

## Callix (14/10/2026)

- O formulário "Padrão Esparta" ganhou quatro campos opcionais: Data de contato (Data), Horário de contato (Horário), Telefone 2 e Telefone 3. O formulário é compartilhado por todas as campanhas.
- Importada na campanha SempreTech a lista "SempreTech - Dia 15/10 - gerada 2026-10-14 14h30": 19 contas novas de 15/10 (14h às 17h), 19 de 19 aceitas. Os 21 retornos não foram reimportados: já estão na lista "Piloto" de 05/10.
- A lista foi importada **inativa** e sem embaralhar: ativar na manhã de 15/10.

## Listas por oferta (16/10/2026)

- Desde 16/10 as contas em primeira abordagem saem em uma lista por oferta, cada uma com o seu playbook em Word (`playbook/Playbook-sempretech-<oferta>_2026-10-16_14h39.docx`): a SDR ativa uma lista e usa só aquele roteiro.
- Arquivos em `callix/Callix-sempretech-<oferta>_2026-10-16_14h39.csv`: C1 Estação Criativa (110), C2 Laboratório Pronto (56), C3 Posição de Atendimento (14), C4 Caixa Pronto (66), C6 Escritório em Dia (25). Retornos ficam na lista "Piloto"; revendas e os três 0800 ficam fora.
- Importada em 16/10 às 14h44 a lista "SempreTech - C1 Estação Criativa - gerada 2026-10-16 14h39": 106 de 110 aceitas e 4 retiradas pelo filtro de baixa probabilidade (telefones com ligação recente). Inativa e sem embaralhar.
- As 19 contas da lista "Dia 15/10" estão também nas listas por oferta: desativar a "Dia 15/10" antes de ativar as novas.
- Em 16/10 às 15h a C1 foi ativada e a "Piloto 26 contas" foi desativada; a "Dia 15/10" já estava inativa. A C1 é a única lista ativa da campanha, que segue pausada, em modo Power, com o grupo de agentes "David Buena". Os retornos da Piloto ficam fora do discador enquanto ela estiver inativa.
- Às 15h10 de 16/10 a campanha SempreTech passou a "Em andamento", com só o grupo de agentes "Jennifer" (David Buena saiu) e 106 contatos da C1. Modo Power, de segunda a sexta, das 9h às 18h.
- A campanha #12 foi renomeada para "SempreTech - Estação Criativa" (descrição: "Oferta C1 Estação Criativa - projetos e criativos (Salvador/BA)"). Padrão daqui em diante: uma campanha por oferta, "SempreTech - <oferta>".
- Às 15h40 de 16/10, depois de 51 ligações (5,9% de atendimento) e 10 contatos esgotados em meia hora: tentativas por telefone de 5 para 3, agressividade de 3 para 5, e espera antes de religar de 2 horas (não atendeu e caixa postal) e 30 minutos (ocupado). Cada dia sobe a lista do dia seguinte, a partir de `fila_clientes_finais.csv`, com cabeçalhos iguais aos nomes dos campos do formulário.

## Ligações atendidas da Estação Criativa (sincronizadas em 18/10/2026)

A campanha discou de 15h17 a 15h22 de 16/10: 51 ligações, 3 atendidas, todas com a Jennifer. As gravações foram baixadas, transcritas com o Whisper local e avaliadas; a transcrição aparece na ficha de cada lead no painel.

- Monte Moryah Engenharia e Projetos (n27): falou com Alberto, que decide a compra. Microempresa, compra computador no varejo (Dell); sem interesse. Nota da ligação 26%: aceitou a recusa sem perguntar pela próxima compra nem oferecer preço de referência.
- Grab Mídia (m29) e SPNVídeo (m37): caíram em segundos, sem conversa.

## Revisão de porte da lista C1 (18/10/2026)

A C1 foi montada sem corte por porte: as 110 contas estavam com "porte a confirmar" e 107 tinham só celular. Em 18/10 cada uma foi verificada (CNPJ, porte e capital na Receita, sócios, equipe no site, LinkedIn e Google):

- **Manter (32):** 9 dentro do perfil e 23 a confirmar na ligação, com algum sinal de estrutura. Lista nova em `callix/Callix-sempretech-C1-estacao-criativa-revisada_2026-10-18_10h09.csv`, com os nomes corrigidos e todas agendadas para 19/10, das 9h às 16h10.
- **Fora (40):** MEI, fotógrafos e videomakers autônomos, blogs e canais pessoais, empresas de 1 ou 2 pessoas. Inclui a Monte Moryah, pelo que o Alberto disse na ligação.
- **Verificar antes (38):** sem nenhum dado de porte (sem CNPJ, só Instagram ou site fora do ar). Não entram no discador até haver dado.
- A planilha com a decisão, o motivo e as fontes de cada conta está em `callix/Revisao-porte-C1-estacao-criativa_2026-10-18_10h09.csv`. O resultado está também no campo `porte` de cada conta e aparece na ficha do lead no painel.
- No Callix, em 18/10 às 10h34: importada a lista "SempreTech - C1 Estação Criativa revisada - gerada 2026-10-18 10h09" (30 de 32 aceitas; 2 tiradas pelo filtro de caixa postal, indisponível ou número inexistente). Os filtros "não atendeu" e "ligação nos últimos 3 meses" foram desligados para não descartar quem só não atendeu em 16/10. A revisada está ativa e a C1 de 16/10 está inativa; a campanha volta a discar em 19/10 às 9h.
- Regra daqui em diante: nenhuma conta entra numa lista de discagem com porte "a confirmar" sem sinal mínimo de 5 pessoas. As listas C2, C3, C4 e C6 passam pela mesma revisão antes de subir.

## Busca no Nordeste (18/10/2026)

- Apify (Google Maps, `compass/crawler-google-places`), 8 capitais fora Salvador × 4 termos (escritório de engenharia, escritório de arquitetura, agência de publicidade, produtora de vídeo): 644 empresas, US$ 2,58. Dados brutos em `data/apify_nordeste_2026-10-18.json` (fora do git). A conta do Apify é a do plano gratuito, com limite de US$ 10 por mês; sobrou cerca de US$ 1,40 em outubro.
- Pré-filtro: telefone válido com DDD do Nordeste, sem nome de pessoa, fora da carteira, com telefone fixo ou site e avaliações. Passaram 185, verificadas uma a uma.
- Resultado (`callix/Revisao-porte-nordeste_2026-10-18_10h53.csv`): 43 para a C1 Estação Criativa, 23 construtoras e incorporadoras para a C6 Escritório em Dia, 8 grandes demais (mais de 100 funcionários: TPF, A. Gaspar, Maia Melo, Delta, Dois A, AC Engenharia, Escudo, Agência Um), 14 fora e 97 a verificar.
- Listas prontas, ainda não importadas: `callix/Callix-sempretech-C1-estacao-criativa-nordeste_2026-10-18_10h53.csv` (43) e `callix/Callix-sempretech-C6-escritorio-em-dia-nordeste_2026-10-18_10h53.csv` (23), agendadas para 20 e 21/10.
- O Rodrigo confirmou em 18/10 que a SempreTech atende o Nordeste. Importada e ativa às 11h12 a lista "SempreTech - C1 Estação Criativa Nordeste - gerada 2026-10-18 10h53" (43 de 43).
- Interior da Bahia (Feira de Santana, Vitória da Conquista, Ilhéus, Itabuna, Juazeiro, Barreiras, Teixeira de Freitas): 301 empresas por US$ 1,20 e 82 verificadas. Resultado em `callix/Revisao-porte-bahia-interior_2026-10-18_11h16.csv`: 14 para a C1, 6 para a C6, 3 grandes demais, 13 fora e 46 a verificar. Importada e ativa às 11h18 a lista "SempreTech - C1 Estação Criativa Bahia interior - gerada 2026-10-18 11h16" (14 de 14).
- Interior do Nordeste, pelo Google Maps no Chrome (sem Apify): 31 buscas em Campina Grande, Caruaru, Petrolina, Juazeiro do Norte, Sobral, Mossoró, Imperatriz e Arapiraca; 409 empresas, 81 verificadas. Resultado em `callix/Revisao-porte-interior-nordeste_2026-10-18_12h03.csv`: 9 para a C1, 20 para a C6, 3 grandes demais, 2 fora e 47 a verificar. Importada e ativa às 12h04 a lista "SempreTech - C1 Estação Criativa interior Nordeste - gerada 2026-10-18 12h03" (9 de 9).
- Novos perfis C1 nas capitais, pelo Google Maps no Chrome (agência de comunicação e de marketing, produtora audiovisual, estúdio de animação, projeto estrutural, topografia, projetos de engenharia; Salvador com todos os termos): 113 candidatas novas verificadas. Resultado em `callix/Revisao-porte-C1-capitais-novos-perfis_2026-10-18_12h29.csv`: 38 dentro, 12 fora e 63 a verificar. Importada e ativa às 12h30 a lista "SempreTech - C1 Estação Criativa capitais novos perfis - gerada 2026-10-18 12h29" (38 de 38: Salvador 16, Recife 10, Fortaleza 10, Natal 2).
- A campanha Estação Criativa tem cinco listas ativas: Salvador revisada (30), Nordeste (43), Bahia interior (14), interior do Nordeste (9) e capitais novos perfis (38), 134 contatos.
- Base da Receita local (`D:\cnpj_database\cnpj.db`, extrato de 12/04/2026): extraídas em `data/receita_c1_nordeste.json` 186 mil empresas ativas do Nordeste com CNAE da C1 (publicidade, audiovisual, arquitetura, engenharia, topografia, design). Corte: sem MEI, sem empresário individual, sem construtora, com telefone, porte EPP ou Demais e abertura até 2023: 2.017 no núcleo da C1 (`data/receita_c1_A.json`). Leva 1, com fixo, 2+ sócios e capital de R$ 50 mil ou mais: 391, conferidas na internet (site e LinkedIn). Resultado em `callix/Revisao-porte-C1-receita-leva1_2026-10-18_14h05.csv`: 259 entram, 79 fora do ramo (outdoor e mídia exterior, holdings, TV), 24 grandes, 16 filiais repetidas, 10 já em outras listas, 3 inativas.
- Importada e ativa às 14h07 a lista "SempreTech - C1 Estação Criativa Receita leva 1 - gerada 2026-10-18 14h05": 228 de 259 (31 tiradas pelo filtro de baixa probabilidade), agendadas de 26/10 a 03/11. A campanha passa a 362 contatos em seis listas.
- Pente fino em 18/10 às 15h (`callix/Pente-fino-C1-contas-retiradas_2026-10-18_15h03.csv`): saíram 51 contas das seis listas: 18 com telefone da Receita compartilhado por 5 ou mais empresas (é o do contador), 10 com DDD de fora do Nordeste (decisão na sede), 6 com o mesmo telefone de outra conta, 8 MEI, empresário individual ou ME sem estrutura, 3 gráficas, marcas pessoais, holding, comércio e uma grande demais. Em 21 contas da Receita o telefone principal foi trocado pelo segundo, que é exclusivo da empresa. As listas Salvador revisada, Capitais novos perfis e Receita leva 1 foram desativadas e reimportadas limpas ("... pente fino - gerada 2026-10-18 15h03"): 26, 36 e 195 contatos aceitos. Ativas: Salvador pente fino (26), Nordeste (43), Bahia interior (14), interior do Nordeste (9), capitais pente fino (36) e Receita pente fino (195): 323 contatos.
- Em 18/10 às 15h20 as listas foram renomeadas no Callix com o nome da oferta, sem o código C1: ativas "SempreTech - Estação Criativa - Salvador e região", "- Capitais do Nordeste", "- Bahia interior", "- Interior do Nordeste", "- Capitais novos perfis" e "- Receita leva 1"; as inativas levam "(substituída)". Descrição da campanha: "Estação Criativa - agências, produtoras, arquitetura e engenharia de projetos (Nordeste)". Campanha conferida: Power, agressividade 5, preditivo, 3 tentativas por telefone, grupo Jennifer, segunda a sexta das 9h às 18h, 323 contatos; status "Fora de agendamento" no domingo, começa sozinha às 9h de 19/10. Rechamada (agendar retorno pelo agente) está desligada e as qualificações são as padrão.
- Próximas levas: as cerca de 1.600 restantes do núcleo (`data/receita_c1_A.json`), tirando o CNAE 7312-2 (agenciamento de espaço, quase sempre outdoor).
- Cerca de 200 contas da C1 ficaram "a verificar" porque a cota de buscas na web da sessão acabou; reverificar quando ela voltar.
- C6 Escritório em Dia: 23 construtoras do Nordeste, 6 do interior da Bahia e 20 do interior do Nordeste (49) em arquivo, à espera de uma campanha "SempreTech - Escritório em Dia".
- O crédito do Apify do ciclo de 16/10 a 15/11 acabou (US$ 9,72 de 10).
- As 97 "a verificar" ficaram sem dado porque a cota de buscas na web acabou no meio da verificação; dá para refazer depois.

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
- Abordar por canais de apoio (WhatsApp): Projet (71) 98818-3740, Escola Rembrandt (71) 99913-2108.
- Nova tentativa: ECMAN, Bahia Logística, Conceito Brasil, Grupo LAS, Line (06/10), TEL (06/10), Labchecap, Construtora Lustosa (telefone fora de área).
- Iplasa: informática terceirizada; pedir compras ou o administrativo.
- EPMAN: ligação falhou e o CNPJ consta como baixado; testar o (71) 3111-9493 uma vez.

Encerrada: Salvador Armazéns Gerais (sem interesse).

## Pendências

- Enviar os três e-mails e as três mensagens de WhatsApp já redigidos (OCC, Santacruz, Tidelli; Total Atacado, Projet, Escola Rembrandt).
- Importar no Callix as contas novas, a começar pelas 15 da semana 1. As 13 contas antigas voltaram ao painel em 07/10 e seguem na campanha.
- As 7 contas da esteira 2 têm proposta pronta para baixar no painel (HTML e PDF), no combo Escritório em Dia com 30% de desconto. O combo foi escolhido pela entrada "computador e nobreak" do estudo de cada conta; confirmar se alguma pediu outra coisa por telefone.
- Confirmar com a SempreTech a validade e as condições do desconto de 30% (prazo, quantidade mínima, forma de pagamento); a proposta não traz nenhuma.
- Definir o tratamento das 18 revendas: tabela própria, outra oferta ou saída da campanha.
- O disco C: da máquina tem cerca de 4,5 GB livres; a geração dos PDFs chegou a enchê-lo em 07/10.
- Confirmar com a SempreTech os itens da lista "A confirmar" do playbook, a começar pelo posicionamento "especialistas em logística e performance em informática" e pelos produtos fora do site.
- Criar as qualificações no Callix e tirar da lista da campanha as quatro contas removidas (Hullo, UNIFTC, Conterp e UCSal).
- As ligações de 05/10 não passaram pelo Callix: foram registradas à mão em `tentativas.json`, sem gravação nem transcrição.

## Como atualizar

1. Registrar o resultado de cada contato em `tentativas.json` (conta, quando, nota, qualificação, etapa, se conversou, e, se quiser fixar o prazo da tarefa, `prazo` no formato `2026-10-08`). Etapas mudadas no kanban, textos escritos em "Evolução até esta etapa" e tarefas concluídas no painel ficam só no navegador de quem mexeu: o kanban tem um botão que copia os movimentos prontos para colar neste arquivo.
2. `uv run python main.py` sincroniza o Callix e regenera o painel e o relatório do cliente em `docs/`. Se mudou conta, combo, preço ou etapa de proposta, rodar antes `uv run python ofertas.py --pdf` para atualizar as propostas.
3. Um único `git push` publica os dois endereços. Publicar em lote: envios seguidos cancelam a publicação que está na fila.
