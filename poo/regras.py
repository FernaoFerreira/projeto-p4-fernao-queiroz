"""
Regras de Legalidade — Padrão Strategy / Polimorfismo

Define a interface abstrata RegraLegalidade e as implementações concretas de cada
regra do domínio (Strategy Pattern).
"""

from abc import ABC, abstractmethod
from baralho import Baralho
from relatorios import Violacao


class RegraLegalidade(ABC):
    """
    Interface polimórfica para validação de regras de legalidade de um Baralho.
    Cada classe concreta implementa a validação de uma regra específica.
    """

    @abstractmethod
    def validar(self, baralho: Baralho) -> list[Violacao]:
        """Valida a regra contra o baralho fornecido e retorna a lista de violações."""
        pass


class RegraNomeNaoVazio(RegraLegalidade):
    """Garante que tanto o Commander quanto as cartas do baralho possuem nomes válidos."""

    def validar(self, baralho: Baralho) -> list[Violacao]:
        violacoes = []
        if baralho.commander is not None and not baralho.commander.nome_valido():
            violacoes.append(Violacao("nome não vazio", "O commander possui um nome vazio ou inválido"))

        posicao = 1
        for carta in baralho.cartas:
            if not carta.nome_valido():
                violacoes.append(Violacao("nome não vazio", f"A carta na posição {posicao} do baralho possui nome vazio"))
            posicao += 1

        return violacoes


class RegraTamanho(RegraLegalidade):
    """Garante que o baralho possui exatamente 100 cartas no total."""

    def validar(self, baralho: Baralho) -> list[Violacao]:
        violacoes = []
        total = baralho.total_cartas()
        if total != 100:
            violacoes.append(Violacao("tamanho do baralho", f"esperado 100, encontrado {total}"))
        return violacoes


class RegraCommanderNoBaralho(RegraLegalidade):
    """Garante que o Commander não é listado novamente como carta comum do baralho."""

    def validar(self, baralho: Baralho) -> list[Violacao]:
        violacoes = []
        if baralho.commander is None or not baralho.commander.nome_valido():
            return violacoes

        nome_cmd = baralho.commander.nome
        for carta in baralho.cartas:
            if carta.nome == nome_cmd:
                violacoes.append(Violacao(
                    "commander no baralho",
                    f"a carta '{nome_cmd}' é o commander e não pode estar na lista do baralho"
                ))
                break
        return violacoes


class RegraSingleton(RegraLegalidade):
    """
    Garante a regra de singleton (máximo de 1 cópia).
    Delega ao baralho a identificação de cartas sujeitas ao singleton.
    """

    def validar(self, baralho: Baralho) -> list[Violacao]:
        violacoes = []
        cartas_singleton = baralho.obter_cartas_sujeitas_a_singleton()
        contagens = {}

        for carta in cartas_singleton:
            nome = carta.nome
            if nome:
                contagens[nome] = contagens.get(nome, 0) + 1

        for nome, qtd in contagens.items():
            if qtd > 1:
                violacoes.append(Violacao("singleton", f"'{nome}' aparece {qtd} vezes, máximo permitido é 1"))

        return violacoes


class RegraIdentidadeCor(RegraLegalidade):
    """Garante que todas as cartas do baralho pertencem à identidade de cor do Commander."""

    def validar(self, baralho: Baralho) -> list[Violacao]:
        violacoes = []
        if baralho.commander is None:
            return violacoes

        cores_cmd = baralho.commander.identidade_cor
        cores_cmd_fmt = "{" + ", ".join(sorted(list(cores_cmd))) + "}"

        for carta in baralho.cartas:
            proibidas = carta.cores_proibidas(cores_cmd)
            if len(proibidas) > 0:
                proibidas_str = ", ".join(sorted(list(proibidas)))
                violacoes.append(Violacao(
                    "identidade de cor",
                    f"'{carta.nome}' tem cor {proibidas_str}, fora da identidade do commander {cores_cmd_fmt}"
                ))

        return violacoes


class RegraCustoMana(RegraLegalidade):
    """Garante que os custos de mana obedecem aos limites do tipo da carta."""

    def validar(self, baralho: Baralho) -> list[Violacao]:
        violacoes = []
        for carta in baralho.cartas:
            if not carta.custo_valido():
                if carta.custo_mana < 0:
                    violacoes.append(Violacao("custo de mana", f"a carta '{carta.nome}' possui custo de mana negativo: {carta.custo_mana}"))
                elif carta.eh_terreno() and carta.custo_mana > 0:
                    violacoes.append(Violacao("custo de mana", f"o terreno '{carta.nome}' possui custo de mana maior que zero: {carta.custo_mana}"))
        return violacoes
