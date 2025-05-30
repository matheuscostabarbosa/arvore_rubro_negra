"""
Testes unitários para a árvore rubro-negra com persistência parcial.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from no import No, Cor
from arvore_rubro_negra import ArvoreRubroNegra
from processador_operacoes import ProcessadorOperacoes

class TestNo(unittest.TestCase):
    """Testes para a classe No."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.no = No(10, Cor.VERMELHO, 0)
    
    def test_criacao_no(self):
        """Testa a criação de um nó."""
        self.assertEqual(self.no.valor, 10)
        self.assertEqual(self.no.versao_criacao, 0)
        self.assertEqual(self.no.obter_cor(0), Cor.VERMELHO)
        self.assertTrue(self.no.esta_ativo(0))
        self.assertIsNone(self.no.versao_remocao)
    
    def test_mudanca_cor(self):
        """Testa a mudança de cor do nó."""
        self.no.definir_cor(Cor.PRETO, 1)
        self.assertEqual(self.no.obter_cor(1), Cor.PRETO)
        # Versão anterior deve manter a cor original
        self.assertEqual(self.no.obter_cor(0), Cor.VERMELHO)
    
    def test_definir_filhos(self):
        """Testa a definição de filhos."""
        filho_esq = No(5, Cor.PRETO, 0)
        filho_dir = No(15, Cor.PRETO, 0)
        
        self.no.definir_filho_esquerdo(filho_esq, 0)
        self.no.definir_filho_direito(filho_dir, 0)
        
        self.assertEqual(self.no.obter_filho_esquerdo(0), filho_esq)
        self.assertEqual(self.no.obter_filho_direito(0), filho_dir)
    
    def test_remocao_no(self):
        """Testa a remoção do nó."""
        self.assertTrue(self.no.esta_ativo(0))
        self.assertTrue(self.no.esta_ativo(1))
        
        self.no.remover(2)
        
        self.assertTrue(self.no.esta_ativo(0))
        self.assertTrue(self.no.esta_ativo(1))
        self.assertFalse(self.no.esta_ativo(2))
        self.assertFalse(self.no.esta_ativo(3))

class TestArvoreRubroNegra(unittest.TestCase):
    """Testes para a classe ArvoreRubroNegra."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.arvore = ArvoreRubroNegra()
    
    def test_arvore_vazia(self):
        """Testa árvore recém-criada."""
        self.assertEqual(self.arvore.versao_atual, 0)
        self.assertIsNone(self.arvore.raizes[0])
        resultado = self.arvore.imprimir_arvore()
        self.assertEqual(resultado, [])
    
    def test_inclusao_simples(self):
        """Testa inclusão de elementos."""
        self.arvore.incluir(10)
        self.assertEqual(self.arvore.versao_atual, 1)
        self.assertIsNotNone(self.arvore.raizes[1])
        
        resultado = self.arvore.imprimir_arvore()
        self.assertEqual(len(resultado), 1)
        self.assertIn("10,0,N", resultado)  # Raiz deve ser preta
    
    def test_inclusao_multipla(self):
        """Testa inclusão de múltiplos elementos."""
        valores = [10, 5, 15, 3, 7, 12, 18]
        
        for valor in valores:
            self.arvore.incluir(valor)
        
        self.assertEqual(self.arvore.versao_atual, len(valores))
        resultado = self.arvore.imprimir_arvore()
        
        # Verificar se todos os valores estão presentes
        valores_resultado = [int(item.split(',')[0]) for item in resultado]
        self.assertEqual(sorted(valores_resultado), sorted(valores))
        
        # Verificar ordem crescente
        self.assertEqual(valores_resultado, sorted(valores_resultado))
    
    def test_busca_sucessor(self):
        """Testa busca de sucessor."""
        valores = [10, 5, 15, 3, 7, 12, 18]
        
        for valor in valores:
            self.arvore.incluir(valor)
        
        # Testes de sucessor
        self.assertEqual(self.arvore.buscar_sucessor(6), 7)
        self.assertEqual(self.arvore.buscar_sucessor(10), 12)
        self.assertEqual(self.arvore.buscar_sucessor(18), None)  # Não tem sucessor
        self.assertEqual(self.arvore.buscar_sucessor(0), 3)     # Menor que todos
    
    def test_remocao_simples(self):
        """Testa remoção de elementos."""
        # Inserir elementos
        valores = [10, 5, 15]
        for valor in valores:
            self.arvore.incluir(valor)
        
        versao_antes_remocao = self.arvore.versao_atual
        
        # Remover elemento
        self.arvore.remover(5)
        
        # Verificar que a versão aumentou
        self.assertEqual(self.arvore.versao_atual, versao_antes_remocao + 1)
        
        # Verificar que o elemento foi removido na nova versão
        resultado_atual = self.arvore.imprimir_arvore()
        valores_atuais = [int(item.split(',')[0]) for item in resultado_atual]
        self.assertNotIn(5, valores_atuais)
        
        # Verificar que o elemento ainda existe na versão anterior
        resultado_anterior = self.arvore.imprimir_arvore(versao_antes_remocao)
        valores_anteriores = [int(item.split(',')[0]) for item in resultado_anterior]
        self.assertIn(5, valores_anteriores)
    
    def test_persistencia_versoes(self):
        """Testa a persistência entre versões."""
        # Construir árvore gradualmente
        self.arvore.incluir(10)  # versão 1
        self.arvore.incluir(5)   # versão 2
        self.arvore.incluir(15)  # versão 3
        
        # Verificar versão 1
        resultado_v1 = self.arvore.imprimir_arvore(1)
        self.assertEqual(len(resultado_v1), 1)
        self.assertIn("10", resultado_v1[0])
        
        # Verificar versão 2
        resultado_v2 = self.arvore.imprimir_arvore(2)
        self.assertEqual(len(resultado_v2), 2)
        valores_v2 = [int(item.split(',')[0]) for item in resultado_v2]
        self.assertEqual(sorted(valores_v2), [5, 10])
        
        # Verificar versão 3
        resultado_v3 = self.arvore.imprimir_arvore(3)
        self.assertEqual(len(resultado_v3), 3)
        valores_v3 = [int(item.split(',')[0]) for item in resultado_v3]
        self.assertEqual(sorted(valores_v3), [5, 10, 15])

class TestProcessadorOperacoes(unittest.TestCase):
    """Testes para a classe ProcessadorOperacoes."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.processador = ProcessadorOperacoes()
    
    def test_operacao_inclusao(self):
        """Testa operação de inclusão."""
        resultado = self.processador.processar_operacao("INC 42")
        self.assertIsNone(resultado)  # Inclusão não gera saída
        self.assertEqual(self.processador.obter_versao_atual(), 1)
    
    def test_operacao_impressao(self):
        """Testa operação de impressão."""
        # Incluir alguns elementos
        self.processador.processar_operacao("INC 10")
        self.processador.processar_operacao("INC 5")
        self.processador.processar_operacao("INC 15")
        
        resultado = self.processador.processar_operacao("IMP 3")
        self.assertIsNotNone(resultado)
        self.assertEqual(len(resultado), 2)  # Linha de comando + resultado
        self.assertEqual(resultado[0], "IMP 3")
    
    def test_operacao_sucessor(self):
        """Testa operação de sucessor."""
        # Incluir alguns elementos
        self.processador.processar_operacao("INC 10")
        self.processador.processar_operacao("INC 5")
        self.processador.processar_operacao("INC 15")
        
        resultado = self.processador.processar_operacao("SUC 6 3")
        self.assertIsNotNone(resultado)
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0], "SUC 6 3")
        self.assertEqual(resultado[1], "10")  # Sucessor de 6 é 10
    
    def test_operacao_remocao(self):
        """Testa operação de remoção."""
        # Incluir elemento
        self.processador.processar_operacao("INC 42")
        versao_antes = self.processador.obter_versao_atual()
        
        resultado = self.processador.processar_operacao("REM 42")
        self.assertIsNone(resultado)  # Remoção não gera saída
        self.assertEqual(self.processador.obter_versao_atual(), versao_antes + 1)
    
    def test_operacoes_invalidas(self):
        """Testa tratamento de operações inválidas."""
        # Comando inválido
        resultado = self.processador.processar_operacao("XYZ 123")
        self.assertIsNone(resultado)
        
        # Formato inválido
        resultado = self.processador.processar_operacao("INC")
        self.assertIsNone(resultado)

class TestIntegracao(unittest.TestCase):
    """Testes de integração do sistema completo."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.processador = ProcessadorOperacoes()
    
    def test_sequencia_operacoes_completa(self):
        """Testa uma sequência completa de operações."""
        operacoes = [
            "INC 10",
            "INC 5", 
            "INC 15",
            "INC 3",
            "INC 7",
            "SUC 6 5",
            "IMP 5",
            "REM 5",
            "IMP 6",
            "SUC 10 5"
        ]
        
        resultados_esperados = []
        
        for operacao in operacoes:
            resultado = self.processador.processar_operacao(operacao)
            if resultado:
                resultados_esperados.extend(resultado)
        
        # Verificar que temos resultados das operações SUC e IMP
        self.assertTrue(any("SUC" in linha for linha in resultados_esperados))
        self.assertTrue(any("IMP" in linha for linha in resultados_esperados))
    
    def test_persistencia_completa(self):
        """Testa a persistência completa entre versões."""
        # Construir árvore com modificações
        self.processador.processar_operacao("INC 50")   # v1
        self.processador.processar_operacao("INC 25")   # v2  
        self.processador.processar_operacao("INC 75")   # v3
        self.processador.processar_operacao("REM 25")   # v4
        self.processador.processar_operacao("INC 60")   # v5
        
        # Verificar diferentes versões
        # Versão 2: deve ter 25, 50
        resultado_v2 = self.processador.processar_operacao("IMP 2")
        self.assertIn("25", resultado_v2[1])
        self.assertIn("50", resultado_v2[1])
        
        # Versão 4: não deve ter 25
        resultado_v4 = self.processador.processar_operacao("IMP 4")
        self.assertNotIn("25", resultado_v4[1])
        self.assertIn("50", resultado_v4[1])
        self.assertIn("75", resultado_v4[1])
        
        # Versão 5: deve ter 50, 60, 75
        resultado_v5 = self.processador.processar_operacao("IMP 5")
        valores_v5 = resultado_v5[1]
        self.assertIn("50", valores_v5)
        self.assertIn("60", valores_v5)
        self.assertIn("75", valores_v5)
        self.assertNotIn("25", valores_v5)

def executar_testes():
    """Executa todos os testes unitários."""
    unittest.main(verbosity=2)

if __name__ == "__main__":
    executar_testes()