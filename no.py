"""
Módulo que define a classe Nó para a árvore rubro-negra com persistência parcial.
"""

from enum import Enum

class Cor(Enum):
    """Enum para as cores dos nós na árvore rubro-negra."""
    VERMELHO = "R"
    PRETO = "N"

class No:
    """
    Classe que representa um nó da árvore rubro-negra com persistência parcial.
    
    Cada nó mantém um histórico de suas modificações por versão,
    permitindo acesso a estados anteriores sem duplicação completa da árvore.
    """
    
    def __init__(self, valor, cor=Cor.VERMELHO, versao_criacao=0):
        """
        Inicializa um novo nó.
        
        Args:
            valor (int): Valor armazenado no nó
            cor (Cor): Cor inicial do nó (padrão: VERMELHO)
            versao_criacao (int): Versão em que o nó foi criado
        """
        self.valor = valor
        self.versao_criacao = versao_criacao
        
        # Histórico de cores por versão
        self.historico_cores = {versao_criacao: cor}
        
        # Histórico de filhos por versão (esquerdo, direito)
        self.historico_filhos = {versao_criacao: [None, None]}
        
        # Histórico de pais por versão
        self.historico_pais = {versao_criacao: None}
        
        # Versão em que o nó foi removido (None se ainda ativo)
        self.versao_remocao = None
    
    def obter_cor(self, versao):
        """
        Obtém a cor do nó em uma versão específica.
        
        Args:
            versao (int): Versão desejada
            
        Returns:
            Cor: Cor do nó na versão especificada
        """
        versao_valida = self._obter_versao_valida(versao, self.historico_cores)
        return self.historico_cores.get(versao_valida, Cor.PRETO)
    
    def definir_cor(self, cor, versao):
        """
        Define a cor do nó para uma versão específica.
        
        Args:
            cor (Cor): Nova cor do nó
            versao (int): Versão para aplicar a mudança
        """
        self.historico_cores[versao] = cor
    
    def obter_filho_esquerdo(self, versao):
        """
        Obtém o filho esquerdo do nó em uma versão específica.
        
        Args:
            versao (int): Versão desejada
            
        Returns:
            No ou None: Filho esquerdo na versão especificada
        """
        versao_valida = self._obter_versao_valida(versao, self.historico_filhos)
        filhos = self.historico_filhos.get(versao_valida, [None, None])
        return filhos[0]
    
    def obter_filho_direito(self, versao):
        """
        Obtém o filho direito do nó em uma versão específica.
        
        Args:
            versao (int): Versão desejada
            
        Returns:
            No ou None: Filho direito na versão especificada
        """
        versao_valida = self._obter_versao_valida(versao, self.historico_filhos)
        filhos = self.historico_filhos.get(versao_valida, [None, None])
        return filhos[1]
    
    def definir_filho_esquerdo(self, filho, versao):
        """
        Define o filho esquerdo do nó para uma versão específica.
        
        Args:
            filho (No ou None): Novo filho esquerdo
            versao (int): Versão para aplicar a mudança
        """
        filhos_atuais = self.obter_filhos(versao)
        self.historico_filhos[versao] = [filho, filhos_atuais[1]]
    
    def definir_filho_direito(self, filho, versao):
        """
        Define o filho direito do nó para uma versão específica.
        
        Args:
            filho (No ou None): Novo filho direito
            versao (int): Versão para aplicar a mudança
        """
        filhos_atuais = self.obter_filhos(versao)
        self.historico_filhos[versao] = [filhos_atuais[0], filho]
    
    def obter_filhos(self, versao):
        """
        Obtém ambos os filhos do nó em uma versão específica.
        
        Args:
            versao (int): Versão desejada
            
        Returns:
            list: Lista com [filho_esquerdo, filho_direito]
        """
        versao_valida = self._obter_versao_valida(versao, self.historico_filhos)
        return self.historico_filhos.get(versao_valida, [None, None]).copy()
    
    def definir_filhos(self, filho_esquerdo, filho_direito, versao):
        """
        Define ambos os filhos do nó para uma versão específica.
        
        Args:
            filho_esquerdo (No ou None): Novo filho esquerdo
            filho_direito (No ou None): Novo filho direito
            versao (int): Versão para aplicar a mudança
        """
        self.historico_filhos[versao] = [filho_esquerdo, filho_direito]
    
    def obter_pai(self, versao):
        """
        Obtém o pai do nó em uma versão específica.
        
        Args:
            versao (int): Versão desejada
            
        Returns:
            No ou None: Pai na versão especificada
        """
        versao_valida = self._obter_versao_valida(versao, self.historico_pais)
        return self.historico_pais.get(versao_valida)
    
    def definir_pai(self, pai, versao):
        """
        Define o pai do nó para uma versão específica.
        
        Args:
            pai (No ou None): Novo pai
            versao (int): Versão para aplicar a mudança
        """
        self.historico_pais[versao] = pai
    
    def esta_ativo(self, versao):
        """
        Verifica se o nó está ativo (não removido) em uma versão específica.
        
        Args:
            versao (int): Versão a verificar
            
        Returns:
            bool: True se o nó está ativo na versão
        """
        return (versao >= self.versao_criacao and 
                (self.versao_remocao is None or versao < self.versao_remocao))
    
    def remover(self, versao):
        """
        Marca o nó como removido a partir de uma versão específica.
        
        Args:
            versao (int): Versão em que o nó foi removido
        """
        self.versao_remocao = versao
    
    def _obter_versao_valida(self, versao, historico):
        """
        Obtém a versão mais recente válida para um histórico específico.
        
        Args:
            versao (int): Versão desejada
            historico (dict): Histórico a consultar
            
        Returns:
            int: Versão válida mais recente
        """
        versoes_disponiveis = [v for v in historico.keys() if v <= versao]
        return max(versoes_disponiveis) if versoes_disponiveis else 0
    
    def __str__(self):
        """Representação string do nó."""
        return f"No({self.valor})"
    
    def __repr__(self):
        """Representação para debug do nó."""
        return f"No(valor={self.valor}, versao_criacao={self.versao_criacao})"