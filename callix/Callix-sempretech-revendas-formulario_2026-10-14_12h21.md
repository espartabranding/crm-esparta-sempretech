# Formulário da campanha no Callix

A importação do Callix não tem CSV fixo: ela obedece ao **formulário da campanha**.
Crie o formulário abaixo antes de importar, com os nomes **exatamente** assim —
tudo minúsculo, inclusive a inicial.

| Campo | Tipo | Tamanho | Obrigatório | Editável |
|---|---|---|---|---|
| `nome` | Texto | 50 | Sim | Sim |
| `tipo_pessoa` | Texto | 1 | Sim | Sim |
| `documento` | Texto | 18 | Não (esta lista não tem CNPJ) | Sim |
| `telefone1` | Telefone | — | Sim | Sim |
| `telefone2` | Telefone | — | Não | Sim |
| `telefone3` | Telefone | — | Não | Sim |
| `empresa` | Texto | 50 | Não | Sim |
| `cidade` | Texto | 40 | Não | Sim |
| `uf` | Texto | 2 | Não | Sim |
| `categoria` | Texto | 40 | Não | Sim |
| `site` | Texto | 100 | Não | Sim |
| `email` | Texto | 80 | Não | Sim |
| `contato` | Texto | 50 | Não | Sim |
| `ordem` | Número | — | Não | Não |
| `revenda` | Texto | 12 | Não | Sim |

**Telefone gravado como:** `51999998888`

## Na importação
1. Discador → Mailing/Campanhas → Importar → a partir de arquivo CSV.
2. Separador: **vírgula**.
3. Mapear coluna a coluna. `nome` e `telefone1` são os dois campos que travam o avanço.
4. Vincular à campanha e confirmar a contagem antes de concluir.

## Antes de subir a lista inteira
Suba **20 linhas** primeiro. Confirme três coisas na tela do Callix: acento
correto, telefone completo com DDD, e nenhum registro colado no anterior.
Só então importe o arquivo cheio.
