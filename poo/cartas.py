"""
Domínio de Cartas — Modelagem Orientada a Objetos

Define a hierarquia de classes para representação de cartas no baralho.
Aplica encapsulamento, herança e polimorfismo.
"""

from abc import ABC, abstractmethod


class Carta(ABC):
    """
    Classe base abstrata para todas as cartas do domínio.
    Encapsula atributos comuns e define interface polimórfica.
    """

    def __init__(self, nome: str, identidade_cor: list[str], custo_mana: int):
        self._nome = str(nome) if nome is not None else ""
        self._identidade_cor = set(identidade_cor) if identidade_cor is not None else set()
        self._custo_mana = int(custo_mana) if custo_mana is not None else 0

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def identidade_cor(self) -> set[str]:
        return set(self._identidade_cor)

    @property
    def custo_mana(self) -> int:
        return self._custo_mana

    def nome_valido(self) -> bool:
        """Verifica se o nome da carta é válido (não vazio)."""
        return len(self._nome.strip()) > 0

    def custo_valido(self) -> bool:
        """Verifica se o custo de mana é válido para este tipo de carta."""
        return self._custo_mana >= 0

    @abstractmethod
    def eh_terreno(self) -> bool:
        """Retorna se a carta é do tipo terreno."""
        pass

    def eh_basica(self) -> bool:
        """
        Retorna se a carta é um terreno básico.
        Por padrão, cartas não são básicas.
        """
        return False

    def sujeita_a_singleton(self) -> bool:
        """
        Polimorfismo: Determina se esta carta está sujeita à regra de singleton.
        Terrenos básicos estão isentos; todas as outras cartas devem obedecer.
        """
        return not self.eh_basica()

    def cores_proibidas(self, cores_commander: set[str]) -> set[str]:
        """Calcula quais cores desta carta violam a identidade do commander."""
        return self._identidade_cor - cores_commander


class CartaTerreno(Carta):
    """
    Especialização para cartas do tipo Terreno.
    Encapsula a propriedade de ser terreno básico ou não-básico.
    """

    def __init__(self, nome: str, identidade_cor: list[str], custo_mana: int = 0, terreno_basico: bool = False):
        super().__init__(nome, identidade_cor, custo_mana)
        self._terreno_basico = bool(terreno_basico)

    def eh_terreno(self) -> bool:
        return True

    def eh_basica(self) -> bool:
        return self._terreno_basico

    def custo_valido(self) -> bool:
        """Polimorfismo: Para terrenos, custo de mana deve ser obrigatoriamente 0."""
        return self._custo_mana == 0


class CartaNaoTerreno(Carta):
    """Especialização para cartas que não são terrenos (mágicas, criaturas, artefatos, etc.)."""

    def __init__(self, nome: str, identidade_cor: list[str], custo_mana: int):
        super().__init__(nome, identidade_cor, custo_mana)

    def eh_terreno(self) -> bool:
        return False


class Commander(CartaNaoTerreno):
    """
    Especialização para a carta designada como Commander do baralho.
    É uma carta não-terreno com a responsabilidade especial de definir a identidade do baralho.
    """

    def __init__(self, nome: str, identidade_cor: list[str], custo_mana: int = 0):
        super().__init__(nome, identidade_cor, custo_mana)
