"""Inclui no plano (contas.json) as contas das listas da Estação Criativa importadas no Callix.

As listas de 18/10/2026 subiram direto para o discador, sem passar pelo plano: as ligações
delas ficavam no painel como avulsas, sem ficha nem etapa. Este script cria a ficha de cada
conta a partir da lista do Callix e da planilha de revisão de porte que a originou.
Conta que já está no plano (mesmo nome ou mesmo telefone) não é duplicada.

Uso: uv run python contas_das_listas.py
"""

import csv
import json
import re
from pathlib import Path

from painel import _normalizar

RAIZ = Path(__file__).parent
PASTA = RAIZ / "callix"

# Lista ativa no Callix -> (nome da lista, planilha de revisão de porte)
LISTAS = {
    "Callix-sempretech-C1-estacao-criativa-revisada-pente-fino_2026-10-18_15h03.csv": (
        "Salvador e região",
        "Revisao-porte-C1-estacao-criativa_2026-10-18_10h09.csv",
    ),
    "Callix-sempretech-C1-estacao-criativa-nordeste_2026-10-18_10h53.csv": (
        "Capitais do Nordeste",
        "Revisao-porte-nordeste_2026-10-18_10h53.csv",
    ),
    "Callix-sempretech-C1-estacao-criativa-bahia-interior_2026-10-18_11h16.csv": (
        "Bahia interior",
        "Revisao-porte-bahia-interior_2026-10-18_11h16.csv",
    ),
    "Callix-sempretech-C1-estacao-criativa-interior-nordeste_2026-10-18_12h03.csv": (
        "Interior do Nordeste",
        "Revisao-porte-interior-nordeste_2026-10-18_12h03.csv",
    ),
    "Callix-sempretech-C1-estacao-criativa-capitais-novos-perfis-pente-fino_2026-10-18_15h03.csv": (
        "Capitais novos perfis",
        "Revisao-porte-C1-capitais-novos-perfis_2026-10-18_12h29.csv",
    ),
    "Callix-sempretech-C1-estacao-criativa-receita-leva1-pente-fino_2026-10-18_15h03.csv": (
        "Receita leva 1",
        "Revisao-porte-C1-receita-leva1_2026-10-18_14h05.csv",
    ),
}

# Valores padrão das contas C1 do plano (as 110 da base têm os mesmos)
PADRAO_C1 = {
    "segmento": "Projetos e criativos",
    "fit": [3, 1, 2, 2],
    "onda": "listas",
    "ader": [10, 6, 8, 2, 5, 3],
    "produtos": ["Desktop i7 com placa de vídeo", 'Monitor de 22"', "Nobreak de 1500 VA"],
    "complementares": [
        "Desktop i3 de 10ª geração",
        'Monitor de 18,5"',
        "Nobreak de 600 VA",
        "Teclado e mouse Logitech",
    ],
    "angulo": "",
    "gancho": "Quando entra um profissional novo na equipe, como a empresa monta a estação dele?",
    "combo": "C1 Estação Criativa",
    "combo_secundario": "C6 Escritório em Dia",
    "porte_decisao": "dentro",
}


def _digitos(telefone: str) -> str:
    """Últimos 8 dígitos: casam o mesmo número escrito com ou sem +55 e DDD."""
    return re.sub(r"\D", "", telefone or "")[-8:]


def _ler(arquivo: Path) -> list[dict]:
    texto = arquivo.read_text(encoding="utf-8-sig")
    separador = ";" if texto.split("\n", 1)[0].count(";") > texto.split("\n", 1)[0].count(",") else ","
    return list(csv.DictReader(texto.splitlines(), delimiter=separador))


def _indice_revisao(arquivo: Path) -> dict[str, dict]:
    """Linhas da revisão de porte, por telefone e por cada nome que a conta já teve."""
    indice = {}
    for linha in _ler(arquivo):
        for nome in ("Nome", "Nome corrigido", "Empresa no Maps", "Empresa na lista"):
            if linha.get(nome):
                indice[_normalizar(linha[nome])] = linha
        if linha.get("Telefone"):
            indice[_digitos(linha["Telefone"])] = linha
    return indice


def _porte(rev: dict | None) -> str:
    if not rev:
        return "dentro ou a confirmar (18/10/2026): sem linha na revisão de porte."
    receita = []
    if rev.get("Porte Receita") and "não encontrado" not in rev["Porte Receita"]:
        receita.append(f"porte {rev['Porte Receita']}")
    capital = rev.get("Capital") or rev.get("Capital social")
    if capital and "não encontrado" not in capital:
        receita.append(f"capital {capital}")
    socios = rev.get("Sócios")
    if socios and socios.isdigit():
        receita.append(f"{socios} sócio(s)")
    texto = f"dentro (18/10/2026): {rev.get('Motivo', '').strip()}"
    return texto + (f" Receita: {', '.join(receita)}." if receita else "")


def _fontes(linha: dict, rev: dict | None) -> list[dict]:
    fontes = []
    if linha.get("Site"):
        fontes.append({"t": "Site", "u": linha["Site"]})
    cnpj = re.sub(r"\D", "", (rev or {}).get("CNPJ", ""))
    if len(cnpj) == 14:
        fontes.append({"t": "CNPJ na Receita", "u": f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"})
    for url in ((rev or {}).get("Fontes") or "").split():
        if url.startswith("http") and all(f["u"] != url for f in fontes):
            fontes.append({"t": "Revisão de porte", "u": url})
    if (rev or {}).get("Google Maps"):
        fontes.append({"t": "Google Maps", "u": rev["Google Maps"]})
    return fontes


def main() -> None:
    arquivo_plano = RAIZ / "contas.json"
    plano = json.loads(arquivo_plano.read_text(encoding="utf-8"))
    contas = plano["contas"]
    nomes = {_normalizar(c["empresa"]): c for c in contas}
    telefones = {_digitos(c["telefone"]): c for c in contas if c.get("telefone")}
    proximo_id = 1 + max((int(c["id"][1:]) for c in contas if c["id"].startswith("e")), default=0)

    novas, apelidos = 0, 0
    for nome_csv, (lista, revisao) in LISTAS.items():
        indice = _indice_revisao(PASTA / revisao)
        for linha in _ler(PASTA / nome_csv):
            empresa = linha["Empresa"].strip()
            existente = nomes.get(_normalizar(empresa)) or telefones.get(_digitos(linha["Telefone"]))
            if existente:
                # O Callix mostra o nome da lista; sem o apelido, a ligação não casa com a ficha.
                if _normalizar(empresa) not in {_normalizar(n) for n in [existente["empresa"], *existente.get("apelidos", [])]}:
                    existente.setdefault("apelidos", []).append(empresa)
                    apelidos += 1
                continue
            rev = indice.get(_digitos(linha["Telefone"])) or indice.get(_normalizar(empresa))
            conta = {
                "id": f"e{proximo_id}",
                "empresa": empresa,
                "cidade": f"{linha['Cidade']}/{linha['UF']}" if linha.get("UF") else linha["Cidade"],
                **PADRAO_C1,
                "telefone": linha["Telefone"],
                "site": linha.get("Site") or "",
                "porte": _porte(rev),
                "perfil": [p for p in [(rev or {}).get("Sinal de equipe") or (rev or {}).get("Sinal online")] if p],
                "sinal": f"Conta da lista \"{lista}\" (18/10/2026), ainda sem pesquisa individual.",
                "fontes": _fontes(linha, rev),
                "proximo": f"Lista \"SempreTech - Estação Criativa - {lista}\" no Callix, agendada para {linha['Data de contato']}.",
                "tipo": None,
                "rota": None,
            }
            contas.append(conta)
            nomes[_normalizar(empresa)] = conta
            telefones[_digitos(linha["Telefone"])] = conta
            proximo_id += 1
            novas += 1

    arquivo_plano.write_text(json.dumps(plano, ensure_ascii=False), encoding="utf-8")
    print(f"contas novas: {novas}; apelidos em contas existentes: {apelidos}; total no plano: {len(contas)}")


if __name__ == "__main__":
    main()
