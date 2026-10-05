"""Gera o painel da SempreTech: contas do plano de prospecção + ligações do Callix."""

import json
import re
import sqlite3
import unicodedata
from datetime import UTC, datetime
from pathlib import Path

import conversa

RAIZ = Path(__file__).parent
DADOS = RAIZ / "data"

DESLIGAMENTO = {
    1: "Cliente desligou",
    2: "Operador desligou",
    3: "Sistema desligou",
    4: "Interrupção",
    5: "Callback",
    6: "Limite de tempo",
    7: "Supervisor",
    8: "Transferência para WhatsApp",
}


def _normalizar(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", sem_acento.lower()).strip()


def _conta_da_chamada(contas: list[dict], attrs: dict, contato: dict) -> dict | None:
    """Casa a chamada com uma conta do plano pelo nome da empresa."""
    textos = [attrs.get("contact_label"), *contato.values()]
    candidatos = {f" {_normalizar(t)} " for t in textos if isinstance(t, str)}
    # Nomes mais longos primeiro, para um nome curto não capturar a conta errada.
    for conta in sorted(contas, key=lambda c: -len(c["empresa"])):
        nome = f" {_normalizar(conta['empresa'])} "
        if any(nome in c for c in candidatos):
            return conta
    return None


def _conversa(linha: sqlite3.Row) -> dict | None:
    """Transcrição por turnos, métricas e avaliação da conversa, quando já processada."""
    if not linha["turnos"]:
        return None
    return {
        "origem": linha["origem"],
        "turnos": json.loads(linha["turnos"]),
        "metricas": json.loads(linha["metricas"]),
        "analise": json.loads(linha["analise"]) if linha["analise"] else None,
    }


def _chamada(linha: sqlite3.Row) -> dict:
    attrs = json.loads(linha["atributos"])
    rel = json.loads(linha["relacionados"])
    qualificacao = rel.get("qualification", {})
    transcricao = next(iter(rel.get("transcriptions") or []), {})
    return {
        "id": linha["id"],
        "completada": linha["tipo"] == "campaign_completed_calls",
        "inicio": attrs.get("started_at"),
        "falado": attrs.get("service_duration") or 0,
        "telefone": attrs.get("destination_phone"),
        "rotulo": attrs.get("contact_label"),
        "qualificacao": qualificacao.get("name"),
        "sucesso": bool(qualificacao.get("success")),
        "agente": rel.get("agent", {}).get("name"),
        "nota": attrs.get("note"),
        "desligamento": DESLIGAMENTO.get(attrs.get("hangup_cause")),
        "audio": f"audio/{linha['audio_arquivo']}" if linha["audio_arquivo"] else None,
        "resumo": transcricao.get("summary"),
        "conversa": _conversa(linha),
        "contato": {
            k: v
            for k, v in rel.get("campaign_contact", {}).items()
            if v and k not in ("id", "created_at", "updated_at")
        },
    }


def _ofertas(conta: dict, regras: list[dict]) -> list[dict]:
    """Produtos sugeridos para a conta, com a situação de cada um no catálogo."""
    ofertas = []
    for principal, nomes in ((True, conta["produtos"]), (False, conta["complementares"])):
        for nome in nomes:
            regra = next((r for r in regras if r["contem"] in _normalizar(nome)), None)
            ofertas.append(
                {
                    "nome": nome,
                    "principal": principal,
                    "situacao": regra["situacao"] if regra else "nao_conferido",
                    "nota": regra["nota"] if regra else "",
                }
            )
    return ofertas


def _analise(conta_id: str) -> dict | None:
    """Pesquisa da empresa, gravada em analises/<id>.json."""
    arquivo = RAIZ / "analises" / f"{conta_id}.json"
    if not arquivo.exists():
        return None
    analise = json.loads(arquivo.read_text(encoding="utf-8"))
    # Nomes que vêm só do quadro societário do CNPJ não são contato de compra: ficam de fora.
    analise["decisores"] = [
        d for d in analise.get("decisores") or [] if "societ" not in d.get("cargo", "").lower()
    ]
    return analise


def montar(db: sqlite3.Connection, plano: dict, catalogo: dict, playbook: dict) -> dict:
    db.row_factory = sqlite3.Row
    contas = [
        {
            **c,
            "chamadas": [],
            "ofertas": _ofertas(c, catalogo["regras"]),
            "analise": _analise(c["id"]),
        }
        for c in plano["contas"]
    ]
    avulsas = []
    db.execute(conversa.SCHEMA)
    consulta = """
        SELECT c.*, v.origem, v.turnos, v.metricas, v.analise
        FROM chamadas c LEFT JOIN conversas v ON v.tipo = c.tipo AND v.id = c.id
        ORDER BY c.iniciada_em DESC
    """
    for linha in db.execute(consulta):
        chamada = _chamada(linha)
        conta = _conta_da_chamada(contas, json.loads(linha["atributos"]), chamada["contato"])
        (conta["chamadas"] if conta else avulsas).append(chamada)
    return {
        "eixos": plano["eixos"],
        "catalogo": catalogo,
        "playbook": playbook,
        "contas": contas,
        "avulsas": avulsas,
        "gerado_em": datetime.now(UTC).isoformat(),
    }


def gerar(db_arquivo: Path, saida: Path) -> None:
    plano = json.loads((RAIZ / "contas.json").read_text(encoding="utf-8"))
    catalogo = json.loads((RAIZ / "catalogo.json").read_text(encoding="utf-8"))
    playbook = json.loads((RAIZ / "playbook.json").read_text(encoding="utf-8"))
    db = sqlite3.connect(db_arquivo)
    dados = json.dumps(montar(db, plano, catalogo, playbook), ensure_ascii=False).replace("</", "<\\/")
    modelo = (RAIZ / "painel_modelo.html").read_text(encoding="utf-8")
    saida.write_text(modelo.replace("__DADOS__", dados), encoding="utf-8")


if __name__ == "__main__":
    gerar(DADOS / "crm.db", DADOS / "painel.html")
    print(f"Painel gerado em {DADOS / 'painel.html'}")
