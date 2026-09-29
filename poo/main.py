"""
Ponto de entrada executável — Implementação Orientada a Objetos [P4-ETAPA-04]

Demonstra a solução modelada em objetos, regras polimórficas e agregados.
"""

from baralho import Baralho
from cartas import CartaNaoTerreno, CartaTerreno, Commander
from validador import ValidadorBaralho


def criar_baralho_exemplo_oo():
    """Fabrica objetos do domínio para o Exemplo 1."""
    cmd = Commander(
        nome="Marisi, Breaker of the Coil",
        identidade_cor=["R", "G", "W"],
        custo_mana=4
    )

    cartas = []

    # 36 Terrenos básicos
    for _ in range(12):
        cartas.append(CartaTerreno("Floresta", [], custo_mana=0, terreno_basico=True))
        cartas.append(CartaTerreno("Montanha", [], custo_mana=0, terreno_basico=True))
        cartas.append(CartaTerreno("Planície", [], custo_mana=0, terreno_basico=True))

    # 63 Cartas não-terreno distintas
    for i in range(1, 64):
        cartas.append(CartaNaoTerreno(f"Card {i}", ["G"], custo_mana=2))

    return Baralho(cmd, cartas)


def main():
    print("[ETAPA 04 - IMPLEMENTAÇÃO ORIENTADA A OBJETOS]")
    print("Instanciando Agregado Baralho e Objetos de Domínio...")
    baralho = criar_baralho_exemplo_oo()

    print("Instanciando Serviço ValidadorBaralho com estratégias polimórficas de regra...")
    validador = ValidadorBaralho()

    print("Executando validação...")
    relatorio = validador.validar(baralho)

    print("=" * 60)
    print("         RELATÓRIO DE LEGALIDADE (ORIENTADO A OBJETOS)")
    print("=" * 60)
    print(f"Status: {'LEGAL ✅' if relatorio.eh_legal else 'ILEGAL ❌'}")

    print("\n[Violações Encontradas]")
    if len(relatorio.violacoes) == 0:
        print("  Nenhuma violação encontrada.")
    else:
        for idx, v in enumerate(relatorio.violacoes, 1):
            print(f"  {idx}. [{v.regra}] {v.detalhe}")

    est = relatorio.estatisticas
    print("\n[Relatório Estatístico]")
    print(f"  Total de cartas: {est.total_cartas}")
    print(f"  Terrenos: {est.terrenos}")
    print(f"  Não-terrenos: {est.nao_terrenos}")
    print(f"  Custo de mana médio (não-terrenos): {est.custo_medio_nao_terrenos:.2f}")
    print("  Distribuição de cores:")
    for cor, qtd in est.distribuicao_cores.items():
        print(f"    - {cor}: {qtd}")
    print("=" * 60)


if __name__ == "__main__":
    main()
