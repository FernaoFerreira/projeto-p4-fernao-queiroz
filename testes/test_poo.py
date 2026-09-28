"""
Suíte de Testes Automatizados para a Implementação Orientada a Objetos

Valida o módulo /poo/validador.py e as classes de domínio OO contra todos
os casos de teste definidos em /testes/casos.md (Casos 1 a 5 e Casos-limite 1 a 3).
"""

import os
import sys
import unittest

# Adiciona o diretório /poo ao path do Python para importação dos módulos OO
SYS_PATH_POO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "poo"))
if SYS_PATH_POO not in sys.path:
    sys.path.insert(0, SYS_PATH_POO)

from baralho import Baralho
from cartas import CartaNaoTerreno, CartaTerreno, Commander
from validador import ValidadorBaralho, analisar_baralho


class TestPOO(unittest.TestCase):

    def setUp(self):
        """Configura os dados básicos do commander padrão."""
        self.commander_marisi_dict = {
            "nome": "Marisi, Breaker of the Coil",
            "identidade_cor": ["R", "G", "W"],
            "custo_mana": 4,
            "tipo": "não-terreno"
        }
        self.commander_marisi_obj = Commander(
            nome="Marisi, Breaker of the Coil",
            identidade_cor=["R", "G", "W"],
            custo_mana=4
        )

    def _gerar_terrenos_basicos(self, qtd_cada):
        """Função auxiliar para gerar terrenos básicos como dicionários."""
        terrenos = []
        for _ in range(qtd_cada):
            terrenos.append({"nome": "Floresta", "identidade_cor": [], "tipo": "terreno", "custo_mana": 0, "terreno_basico": True})
            terrenos.append({"nome": "Montanha", "identidade_cor": [], "tipo": "terreno", "custo_mana": 0, "terreno_basico": True})
            terrenos.append({"nome": "Planície", "identidade_cor": [], "tipo": "terreno", "custo_mana": 0, "terreno_basico": True})
        return terrenos

    def _gerar_terrenos_basicos_oo(self, qtd_cada):
        """Função auxiliar para gerar terrenos básicos como objetos CartaTerreno."""
        terrenos = []
        for _ in range(qtd_cada):
            terrenos.append(CartaTerreno("Floresta", [], custo_mana=0, terreno_basico=True))
            terrenos.append(CartaTerreno("Montanha", [], custo_mana=0, terreno_basico=True))
            terrenos.append(CartaTerreno("Planície", [], custo_mana=0, terreno_basico=True))
        return terrenos

    def test_caso_1_baralho_legal_simples(self):
        """Caso 1 (Exemplo 1): Baralho legal simples de 100 cartas (36 terrenos + 63 não-terrenos + commander)"""
        cartas = self._gerar_terrenos_basicos(12)  # 36 terrenos
        for i in range(1, 64):
            cartas.append({
                "nome": f"Card {i}",
                "identidade_cor": ["G"],
                "tipo": "não-terreno",
                "custo_mana": 2,
                "terreno_basico": False
            })

        res = analisar_baralho(self.commander_marisi_dict, cartas)

        self.assertTrue(res["legal"])
        self.assertEqual(len(res["violacoes"]), 0)

        est = res["estatisticas"]
        self.assertEqual(est["total_cartas"], 100)
        self.assertEqual(est["terrenos"], 36)
        self.assertEqual(est["nao_terrenos"], 64)
        self.assertAlmostEqual(est["custo_medio_nao_terrenos"], 2.03125, places=4)
        self.assertEqual(est["distribuicao_cores"], {"W": 1, "U": 0, "B": 0, "R": 1, "G": 64})

    def test_caso_1_usando_objetos_diretos(self):
        """Validação usando objetos de domínio OO diretamente."""
        cartas = self._gerar_terrenos_basicos_oo(12)
        for i in range(1, 64):
            cartas.append(CartaNaoTerreno(f"Card {i}", ["G"], custo_mana=2))

        baralho = Baralho(self.commander_marisi_obj, cartas)
        validador = ValidadorBaralho()
        relatorio = validador.validar(baralho)

        self.assertTrue(relatorio.eh_legal)
        self.assertEqual(len(relatorio.violacoes), 0)
        self.assertEqual(relatorio.estatisticas.total_cartas, 100)

    def test_caso_2_tamanho_incorreto(self):
        """Caso 2 (Exemplo 2): Baralho com tamanho incorreto (80 cartas no baralho + 1 commander = 81)"""
        cartas = self._gerar_terrenos_basicos(10)  # 30 terrenos
        for i in range(1, 51):
            cartas.append({
                "nome": f"Card {i}",
                "identidade_cor": ["G"],
                "tipo": "não-terreno",
                "custo_mana": 2,
                "terreno_basico": False
            })

        res = analisar_baralho(self.commander_marisi_dict, cartas)

        self.assertFalse(res["legal"])
        regras_violadas = [v["regra"] for v in res["violacoes"]]
        self.assertIn("tamanho do baralho", regras_violadas)
        self.assertEqual(res["estatisticas"]["total_cartas"], 81)

    def test_caso_3_singleton_duplicada(self):
        """Caso 3 (Exemplo 3): Carta não-terreno e não-básica duplicada ('Sol Ring' x2)"""
        cartas = self._gerar_terrenos_basicos(12)  # 36 terrenos
        for i in range(1, 62):
            cartas.append({
                "nome": f"Card {i}",
                "identidade_cor": ["G"],
                "tipo": "não-terreno",
                "custo_mana": 2,
                "terreno_basico": False
            })
        cartas.append({"nome": "Sol Ring", "identidade_cor": [], "tipo": "não-terreno", "custo_mana": 1, "terreno_basico": False})
        cartas.append({"nome": "Sol Ring", "identidade_cor": [], "tipo": "não-terreno", "custo_mana": 1, "terreno_basico": False})

        res = analisar_baralho(self.commander_marisi_dict, cartas)

        self.assertFalse(res["legal"])
        regras_violadas = [v["regra"] for v in res["violacoes"]]
        self.assertIn("singleton", regras_violadas)

    def test_caso_4_identidade_cor_invalida(self):
        """Caso 4 (Exemplo 4): Violação de identidade de cor ('Counterspell' [U] fora de R/G/W)"""
        cartas = self._gerar_terrenos_basicos(12)  # 36 terrenos
        for i in range(1, 63):
            cartas.append({
                "nome": f"Card {i}",
                "identidade_cor": ["G"],
                "tipo": "não-terreno",
                "custo_mana": 2,
                "terreno_basico": False
            })
        cartas.append({
            "nome": "Counterspell",
            "identidade_cor": ["U"],
            "tipo": "não-terreno",
            "custo_mana": 2,
            "terreno_basico": False
        })

        res = analisar_baralho(self.commander_marisi_dict, cartas)

        self.assertFalse(res["legal"])
        regras_violadas = [v["regra"] for v in res["violacoes"]]
        self.assertIn("identidade de cor", regras_violadas)

    def test_caso_5_multiplas_violacoes(self):
        """Caso 5 (Exemplo 5): Múltiplas violações simultâneas (tamanho, singleton e identidade de cor)"""
        cartas = self._gerar_terrenos_basicos(10)  # 30 terrenos
        for i in range(1, 58):
            cartas.append({
                "nome": f"Card {i}",
                "identidade_cor": ["G"],
                "tipo": "não-terreno",
                "custo_mana": 2,
                "terreno_basico": False
            })
        cartas.append({"nome": "Sol Ring", "identidade_cor": [], "tipo": "não-terreno", "custo_mana": 1, "terreno_basico": False})
        cartas.append({"nome": "Sol Ring", "identidade_cor": [], "tipo": "não-terreno", "custo_mana": 1, "terreno_basico": False})
        cartas.append({"nome": "Counterspell", "identidade_cor": ["U"], "tipo": "não-terreno", "custo_mana": 2, "terreno_basico": False})

        res = analisar_baralho(self.commander_marisi_dict, cartas)

        self.assertFalse(res["legal"])
        regras_violadas = set(v["regra"] for v in res["violacoes"])
        self.assertIn("tamanho do baralho", regras_violadas)
        self.assertIn("singleton", regras_violadas)
        self.assertIn("identidade de cor", regras_violadas)

    def test_caso_6_baralho_vazio(self):
        """Caso 6 (Caso-Limite 1): Baralho vazio (apenas o commander)"""
        res = analisar_baralho(self.commander_marisi_dict, [])

        self.assertFalse(res["legal"])
        self.assertEqual(len(res["violacoes"]), 1)
        self.assertEqual(res["violacoes"][0]["regra"], "tamanho do baralho")

        est = res["estatisticas"]
        self.assertEqual(est["total_cartas"], 1)
        self.assertEqual(est["terrenos"], 0)
        self.assertEqual(est["nao_terrenos"], 1)
        self.assertEqual(est["custo_medio_nao_terrenos"], 4.0)

    def test_caso_7_limites_tamanho(self):
        """Caso 7 (Caso-Limite 2): Limites estritos de tamanho (99 vs 100 vs 101 cartas totais)"""
        c_98 = self._gerar_terrenos_basicos(12)  # 36
        for i in range(1, 63):  # 62 cartas não-terreno
            c_98.append({"nome": f"C{i}", "identidade_cor": ["G"], "tipo": "não-terreno", "custo_mana": 1, "terreno_basico": False})
        res_99 = analisar_baralho(self.commander_marisi_dict, c_98)
        self.assertFalse(res_99["legal"])

        c_99 = list(c_98)
        c_99.append({"nome": "Extra Card", "identidade_cor": ["G"], "tipo": "não-terreno", "custo_mana": 1, "terreno_basico": False})
        res_100 = analisar_baralho(self.commander_marisi_dict, c_99)
        self.assertTrue(res_100["legal"])

        c_100 = list(c_99)
        c_100.append({"nome": "Extra Card 2", "identidade_cor": ["G"], "tipo": "não-terreno", "custo_mana": 1, "terreno_basico": False})
        res_101 = analisar_baralho(self.commander_marisi_dict, c_100)
        self.assertFalse(res_101["legal"])

    def test_caso_8_regras_especificas(self):
        """Caso 8 (Caso-Limite 3): Terreno não-básico duplicado, commander no baralho, nome vazio e custos inválidos"""
        # 8a: Terreno não-básico duplicado
        cartas_8a = self._gerar_terrenos_basicos(12)
        for i in range(1, 62):
            cartas_8a.append({"nome": f"C{i}", "identidade_cor": ["G"], "tipo": "não-terreno", "custo_mana": 1, "terreno_basico": False})
        cartas_8a.append({"nome": "Reliquary Tower", "identidade_cor": [], "tipo": "terreno", "custo_mana": 0, "terreno_basico": False})
        cartas_8a.append({"nome": "Reliquary Tower", "identidade_cor": [], "tipo": "terreno", "custo_mana": 0, "terreno_basico": False})
        res_8a = analisar_baralho(self.commander_marisi_dict, cartas_8a)
        self.assertIn("singleton", [v["regra"] for v in res_8a["violacoes"]])

        # 8b: Commander na lista do baralho
        cartas_8b = self._gerar_terrenos_basicos(12)
        for i in range(1, 63):
            cartas_8b.append({"nome": f"C{i}", "identidade_cor": ["G"], "tipo": "não-terreno", "custo_mana": 1, "terreno_basico": False})
        cartas_8b.append({"nome": "Marisi, Breaker of the Coil", "identidade_cor": ["R", "G", "W"], "tipo": "não-terreno", "custo_mana": 4, "terreno_basico": False})
        res_8b = analisar_baralho(self.commander_marisi_dict, cartas_8b)
        self.assertIn("commander no baralho", [v["regra"] for v in res_8b["violacoes"]])

        # 8c: Nome vazio
        cartas_8c = list(cartas_8b)
        cartas_8c[0] = {"nome": "", "identidade_cor": [], "tipo": "terreno", "custo_mana": 0, "terreno_basico": True}
        res_8c = analisar_baralho(self.commander_marisi_dict, cartas_8c)
        self.assertIn("nome não vazio", [v["regra"] for v in res_8c["violacoes"]])

        # 8d: Terreno com custo > 0 ou custo negativo
        cartas_8d = list(cartas_8b)
        cartas_8d[0] = {"nome": "Terreno Inválido", "identidade_cor": [], "tipo": "terreno", "custo_mana": 3, "terreno_basico": True}
        res_8d = analisar_baralho(self.commander_marisi_dict, cartas_8d)
        self.assertIn("custo de mana", [v["regra"] for v in res_8d["violacoes"]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
