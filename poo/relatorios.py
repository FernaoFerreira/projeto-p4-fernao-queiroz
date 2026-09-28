"""
Relatórios e Objetos de Valor — Modelagem Orientada a Objetos

Define os objetos de transferência de dados e relatórios gerados
pela validação e análise do baralho.
"""


class Violacao:
    """Objeto de Valor representando uma violação de regra encontrada."""

    def __init__(self, regra: str, detalhe: str):
        self._regra = regra
        self._detalhe = detalhe

    @property
    def regra(self) -> str:
        return self._regra

    @property
    def detalhe(self) -> str:
        return self._detalhe

    def para_dicionario(self) -> dict:
        return {
            "regra": self._regra,
            "detalhe": self._detalhe
        }


class RelatorioEstatistico:
    """Objeto encapsulando os dados estatísticos calculados sobre o baralho."""

    def __init__(self, total_cartas: int, terrenos: int, nao_terrenos: int, custo_medio_nao_terrenos: float, distribuicao_cores: dict):
        self._total_cartas = total_cartas
        self._terrenos = terrenos
        self._nao_terrenos = nao_terrenos
        self._custo_medio_nao_terrenos = custo_medio_nao_terrenos
        self._distribuicao_cores = dict(distribuicao_cores)

    @property
    def total_cartas(self) -> int:
        return self._total_cartas

    @property
    def terrenos(self) -> int:
        return self._terrenos

    @property
    def nao_terrenos(self) -> int:
        return self._nao_terrenos

    @property
    def custo_medio_nao_terrenos(self) -> float:
        return self._custo_medio_nao_terrenos

    @property
    def distribuicao_cores(self) -> dict:
        return dict(self._distribuicao_cores)

    def para_dicionario(self) -> dict:
        return {
            "total_cartas": self._total_cartas,
            "terrenos": self._terrenos,
            "nao_terrenos": self._nao_terrenos,
            "custo_medio_nao_terrenos": self._custo_medio_nao_terrenos,
            "distribuicao_cores": self._distribuicao_cores
        }


class RelatorioBaralho:
    """Relatório final unificado contendo o resultado da legalidade e estatísticas."""

    def __init__(self, violacoes: list[Violacao], estatisticas: RelatorioEstatistico):
        self._violacoes = list(violacoes)
        self._estatisticas = estatisticas
        self._legal = (len(self._violacoes) == 0)

    @property
    def eh_legal(self) -> bool:
        return self._legal

    @property
    def violacoes(self) -> list[Violacao]:
        return list(self._violacoes)

    @property
    def estatisticas(self) -> RelatorioEstatistico:
        return self._estatisticas

    def para_dicionario(self) -> dict:
        """Exporta o relatório para o formato dicionário esperado pelo contrato semântico."""
        return {
            "legal": self._legal,
            "violacoes": [v.para_dicionario() for v in self._violacoes],
            "estatisticas": self._estatisticas.para_dicionario()
        }
