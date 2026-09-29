"""
Serviço Validador — Modelagem Orientada a Objetos

Serviço de domínio que orquestra a execução das regras de legalidade (Strategy Pattern)
e a geração do relatório unificado do baralho.
"""

from baralho import Baralho
from cartas import Carta, CartaNaoTerreno, CartaTerreno, Commander
from regras import (
    RegraCommanderNoBaralho,
    RegraCustoMana,
    RegraIdentidadeCor,
    RegraLegalidade,
    RegraNomeNaoVazio,
    RegraSingleton,
    RegraTamanho,
)
from relatorios import RelatorioBaralho, Violacao


class ValidadorBaralho:
    """
    Serviço de domínio responsável por validar um Baralho executando
    uma coleção configurável de regras de legalidade (composição de estratégias).
    """

    def __init__(self, regras: list[RegraLegalidade] = None):
        if regras is not None:
            self._regras = list(regras)
        else:
            # Conjunto padrão de regras do domínio
            self._regras = [
                RegraNomeNaoVazio(),
                RegraTamanho(),
                RegraCommanderNoBaralho(),
                RegraSingleton(),
                RegraIdentidadeCor(),
                RegraCustoMana()
            ]

    def adicionar_regra(self, regra: RegraLegalidade):
        """Permite estender dinamicamente o validador adicionando novas regras."""
        self._regras.append(regra)

    def validar(self, baralho: Baralho) -> RelatorioBaralho:
        """
        Executa todas as regras cadastradas contra o baralho,
        coleta as violações e gera o relatório final unificado.
        """
        todas_violacoes = []
        for regra in self._regras:
            violacoes = regra.validar(baralho)
            todas_violacoes.extend(violacoes)

        estatisticas = baralho.calcular_estatisticas()
        return RelatorioBaralho(todas_violacoes, estatisticas)


# Factory / Adaptação para interface de dicionários primitiva (Compatibilidade com contrato)
def fabricar_carta_de_dicionario(d: dict) -> Carta:
    """Fabrica o objeto de carta adequado (herança) a partir de um dicionário."""
    tipo = d.get("tipo")
    nome = d.get("nome", "")
    identidade = d.get("identidade_cor", [])
    custo = d.get("custo_mana", 0)
    eh_basico = d.get("terreno_basico", False)

    if tipo == "terreno":
        return CartaTerreno(nome, identidade, custo, eh_basico)
    else:
        return CartaNaoTerreno(nome, identidade, custo)


def fabricar_commander_de_dicionario(d: dict) -> Commander:
    """Fabrica o objeto Commander a partir de um dicionário."""
    if not d:
        return Commander("", [], 0)
    return Commander(
        nome=d.get("nome", ""),
        identidade_cor=d.get("identidade_cor", []),
        custo_mana=d.get("custo_mana", 0)
    )


def analisar_baralho(commander_input, cartas_input) -> dict:
    """
    Ponto de adaptação que converte entradas estruturadas (dicionários/objetos)
    em objetos de domínio OO, executa o ValidadorBaralho e retorna o relatório em dicionário.
    """
    if isinstance(commander_input, Commander):
        cmd_obj = commander_input
    elif isinstance(commander_input, dict):
        cmd_obj = fabricar_commander_de_dicionario(commander_input)
    else:
        cmd_obj = Commander("", [], 0)

    cartas_objs = []
    if cartas_input:
        for c in cartas_input:
            if isinstance(c, Carta):
                cartas_objs.append(c)
            elif isinstance(c, dict):
                cartas_objs.append(fabricar_carta_de_dicionario(c))

    baralho = Baralho(cmd_obj, cartas_objs)
    validador = ValidadorBaralho()
    relatorio = validador.validar(baralho)

    return relatorio.para_dicionario()
