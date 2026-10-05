# Prompts da SempreTech

Prompts prontos para usar em qualquer conversa com o Claude. Cada um carrega o contexto de que precisa. Troque só o que está entre chaves.

## 1. Abordagem para uma conta nova

```
Você vai escrever a abordagem de primeira ligação para uma conta.

Quem vende: SempreTech, loja e assistência técnica de informática de Salvador (BA), que monta computadores X-Linne e vende nobreaks, monitores, kits de upgrade e periféricos. Venda transacional.
Objetivo da ligação: sair com um pedido de cotação (o quê, quantos, para quando).
Plano B: nome e contato direto de quem compra, data provável da próxima compra e permissão para mandar a tabela.

Só pode oferecer o que está neste catálogo (preços do site em 05/10/2026):
- Computador montado com SSD: de R$ 1.449,99 (i3, 8 GB, SSD 240 GB) a R$ 4.029,99 (i5, 32 GB, SSD 480 GB)
- Monitor: R$ 499,99 (18,5") a R$ 999,90 (22" revisado, com ajuste de altura)
- Kit de upgrade (placa-mãe, processador, memória): R$ 999,99 a R$ 1.039,99
- Nobreak: R$ 555,96 (600 VA), R$ 1.057,85 (1500 VA), R$ 3.042,96 (2000 VA)
- Estabilizador: a partir de R$ 149,85. Filtro de linha: a partir de R$ 63,96
- Câmera AHD 1080p avulsa: R$ 99,99 a R$ 149,99 (sem gravador)
- Headset: Intelbras CHS 40 RJ9 revisado R$ 59,90, CHS 40 USB R$ 347,96, Logitech H111 R$ 130,96
- Teclado a partir de R$ 29,85, mouse a partir de R$ 14,85, kit sem fio Logitech MK270 R$ 259,90
- Assistência técnica própria: limpeza, diagnóstico e teste de peças, diagnóstico em até 3 dias úteis
Não prometa notebook, impressora, smartphone, roteador, webcam, kit de CFTV com gravador, prazo de entrega, desconto ou condição para empresa: nada disso está confirmado. Se fizer sentido para a conta, vire pergunta ("vocês também compram...?").

Conta: {empresa}, {segmento}, {cidade}. O que se sabe: {sinal, porte, site}.
Telefone é de {central ou direto}.

Escreva, em português do Brasil e no jeito que se fala ao telefone em Salvador:
1. A fala para a recepção, se o telefone for da central: uma pergunta pedindo quem cuida da compra.
2. A abertura com quem decide, em até 10 segundos: cumprimento, nome, quem é e de onde, e o anúncio de que há uma proposta objetiva para a empresa.
3. A proposta, em até três frases: o fato da empresa ou a situação típica do segmento; "A SempreTech propõe..."; uma pergunta aberta.
4. Três perguntas de qualificação, na ordem.
5. A oferta: um produto de entrada e até dois complementares, uma frase cada, com preço de referência.
6. As duas objeções mais prováveis nesta conta, com resposta.
7. O pedido final e o plano B, com data.

Registro corporativo, fluido e propositivo: sem "a gente", "pra", "né", diminutivo ou gíria, e sem pedir desculpa por ligar. O pedido final começa por "Proponho o seguinte:". Nada de "soluções completas" e nada com cara de tradução do inglês ("você não esperava minha ligação", "talvez você possa me ajudar").
Se faltar informação para alguma parte, diga o que falta em vez de inventar.
```

## 2. Resumo pós-ligação para o CRM

```
A partir da transcrição abaixo, de uma ligação de prospecção da SempreTech (informática, Salvador), preencha os campos do CRM. Use só o que foi dito; onde não houver informação, escreva "não informado".

Transcrição: {transcrição}

Campos:
- Falou com (nome e cargo):
- É quem decide a compra? Se não, quem é:
- O que compram e com que frequência:
- Fornecedor atual:
- Próxima compra (o quê e quando):
- Produtos ofertados na ligação:
- Produtos em que demonstrou interesse:
- Produtos pedidos que não estão no catálogo:
- Objeção principal, nas palavras do cliente:
- Próximo passo combinado e data:
- Qualificação sugerida, escolhendo uma: Pediu cotação; Compra prevista com data; Decisor identificado; Retornar em data combinada; Enviar material; Sem interesse: fornecedor atual; Sem interesse: compra pela matriz; Sem interesse: sem demanda; Produto fora do catálogo; Não atendeu / caixa postal; Número errado; Não ligar mais.
```

## 3. Avaliar uma ligação gravada

```
Você vai avaliar a transcrição de uma ligação de prospecção para ajudar o agente a melhorar.

Contexto: a SempreTech, de Salvador, monta computadores e vende nobreaks, monitores, kits de upgrade e periféricos, com assistência técnica própria. O objetivo da ligação era sair com um pedido de cotação, ou ao menos com o contato de quem compra e a data da próxima compra. O agente só pode oferecer computador montado, monitor, kit de upgrade, nobreak, estabilizador, câmera AHD avulsa, headset, teclado, mouse e assistência técnica.

Transcrição: {transcrição}

Avalie de 0 a 2 cada item, citando o trecho literal:
1. Abertura (nome, identificação, licença com motivo)
2. Motivo claro nos primeiros 30 segundos
3. Falou do problema do cliente antes do produto
4. Perguntas de qualificação e pergunta de acompanhamento
5. Oferta com dado concreto e dentro do catálogo
6. Tratamento da objeção
7. Pedido único com data
8. Encerramento e registro

Depois diga: o que foi prometido que não está no catálogo, as três mudanças de maior efeito e a fala reescrita de cada uma.
Seja direto e específico. O agente vai ler isso para aplicar na próxima ligação.
```
