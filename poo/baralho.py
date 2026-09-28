"""
Agregado Baralho — Modelagem Orientada a Objetos

Define a entidade Baralho como Aggregate Root, agrupando o Commander
e a lista de cartas, encapsulando os comportamentos de contagem e estatística.
"""

from cartas import Carta, Commander
from relatorios import RelatorioEstatistico


class Baralho:
    """
    Agregado principal do domínio.
    Encapsula o Commander e a coleção de cartas do baralho.
    """

    def __init__(self, commander: Commander, cartas: list[Carta]):
        self._commander = commander
        self._cartas = list(cartas) if cartas is not None else []

    @property
    def commander(self) -> Commander:
        return self._commander

    @property
    def cartas(self) -> list[Carta]:
        return list(self._cartas)

    def obter_todas_cartas(self) -> list[Carta]:
        """Retorna a coleção completa de cartas incluindo o commander."""
        if self._commander is not None:
            return [self._commander] + self._cartas
        return list(self._cartas)

    def total_cartas(self) -> int:
        """Calcula a quantidade total de cartas no baralho (incluindo o commander)."""
        return len(self.obter_todas_cartas())

    def obter_cartas_sujeitas_a_singleton(self) -> list[Carta]:
        """
        Usa polimorfismo para filtrar quais cartas da lista do baralho
        devem obedecer à regra de singleton.
        """
        cartas_filtradas = []
        for c in self._cartas:
            if c.sujeita_a_singleton():
                cartas_filtradas.append(c)
        return cartas_filtradas

    def calcular_estatisticas(self) -> RelatorioEstatistico:
        """
        Calcula as métricas estatísticas sobre as cartas agregadas.
        """
        todas = self.obter_todas_cartas()
        total_cartas = len(todas)
        qtd_terrenos = 0
        qtd_nao_terrenos = 0
        soma_custos_nao_terrenos = 0
        distribuicao_cores = {"W": 0, "U": 0, "B": 0, "R": 0, "G": 0}

        for carta in todas:
            if carta.eh_terreno():
                qtd_terrenos += 1
            else:
                qtd_nao_terrenos += 1
                soma_custos_nao_terrenos += carta.custo_mana

            for cor in carta.identidade_cor:
                if cor in distribuicao_cores:
                    distribuicao_cores[cor] += 1

        custo_medio = 0.0
        if qtd_nao_terrenos > 0:
            custo_medio = soma_custos_nao_terrenos / qtd_nao_terrenos

        return RelatorioEstatistico(
            total_cartas=total_cartas,
            terrenos=qtd_terrenos,
            nao_terrenos=qtd_nao_terrenos,
            custo_medio_nao_terrenos=custo_medio,
            distribuicao_cores=distribuicao_cores
        )
