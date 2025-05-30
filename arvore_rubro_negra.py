"""
Módulo que implementa a árvore rubro-negra com persistência parcial.
"""

from no import No, Cor

class ArvoreRubroNegra:
    """
    Implementação de uma árvore rubro-negra com persistência parcial.
    
    A árvore mantém múltiplas versões sem duplicar toda a estrutura,
    permitindo acesso eficiente a estados anteriores.
    """
    
    def __init__(self):
        """Inicializa uma árvore vazia."""
        # Array para armazenar as raízes de cada versão (máximo 100 versões)
        self.raizes = [None] * 100
        self.versao_atual = 0
    
    def incluir(self, valor):
        """
        Inclui um valor na árvore, criando uma nova versão.
        
        Args:
            valor (int): Valor a ser incluído
        """
        nova_versao = self.versao_atual + 1
        nova_raiz = self._incluir_recursivo(self.raizes[self.versao_atual], valor, nova_versao)
        
        if nova_raiz:
            nova_raiz.definir_cor(Cor.PRETO, nova_versao)
        
        self.raizes[nova_versao] = nova_raiz
        self.versao_atual = nova_versao
    
    def remover(self, valor):
        """
        Remove um valor da árvore, criando uma nova versão.
        
        Args:
            valor (int): Valor a ser removido
        """
        nova_versao = self.versao_atual + 1
        nova_raiz = self._remover_recursivo(self.raizes[self.versao_atual], valor, nova_versao)
        
        if nova_raiz:
            nova_raiz.definir_cor(Cor.PRETO, nova_versao)
        
        self.raizes[nova_versao] = nova_raiz
        self.versao_atual = nova_versao
    
    def buscar_sucessor(self, valor, versao=None):
        """
        Busca o sucessor de um valor na árvore.
        
        Args:
            valor (int): Valor de referência
            versao (int, opcional): Versão da árvore (padrão: versão atual)
            
        Returns:
            int ou None: Sucessor do valor ou None se não existir
        """
        if versao is None or versao > self.versao_atual:
            versao = self.versao_atual
        
        raiz = self.raizes[versao]
        sucessor = None
        atual = raiz
        
        while atual and atual.esta_ativo(versao):
            if atual.valor > valor:
                sucessor = atual.valor
                atual = atual.obter_filho_esquerdo(versao)
            else:
                atual = atual.obter_filho_direito(versao)
        
        return sucessor
    
    def imprimir_arvore(self, versao=None):
        """
        Imprime a árvore em ordem crescente com profundidade e cor.
        
        Args:
            versao (int, opcional): Versão da árvore (padrão: versão atual)
            
        Returns:
            list: Lista de strings no formato "valor,profundidade,cor"
        """
        if versao is None or versao > self.versao_atual:
            versao = self.versao_atual
        
        resultado = []
        raiz = self.raizes[versao]
        
        if raiz:
            self._percorrer_em_ordem(raiz, versao, 0, resultado)
        
        return resultado
    
    def _incluir_recursivo(self, no, valor, versao):
        """
        Inclui um valor recursivamente na árvore.
        
        Args:
            no (No ou None): Nó atual
            valor (int): Valor a incluir
            versao (int): Versão da operação
            
        Returns:
            No: Novo nó raiz da subárvore
        """
        if no is None:
            return No(valor, Cor.VERMELHO, versao)
        
        # Criar uma nova versão do nó se necessário
        if not no.esta_ativo(versao):
            return No(valor, Cor.VERMELHO, versao)
        
        if valor < no.valor:
            filho_esquerdo = self._incluir_recursivo(no.obter_filho_esquerdo(versao), valor, versao)
            no.definir_filho_esquerdo(filho_esquerdo, versao)
            if filho_esquerdo:
                filho_esquerdo.definir_pai(no, versao)
        elif valor > no.valor:
            filho_direito = self._incluir_recursivo(no.obter_filho_direito(versao), valor, versao)
            no.definir_filho_direito(filho_direito, versao)
            if filho_direito:
                filho_direito.definir_pai(no, versao)
        else:
            # Valor já existe, não faz nada
            return no
        
        return self._balancear_apos_inclusao(no, versao)
    
    def _remover_recursivo(self, no, valor, versao):
        """
        Remove um valor recursivamente da árvore.
        
        Args:
            no (No ou None): Nó atual
            valor (int): Valor a remover
            versao (int): Versão da operação
            
        Returns:
            No ou None: Novo nó raiz da subárvore
        """
        if no is None or not no.esta_ativo(versao):
            return no
        
        if valor < no.valor:
            filho_esquerdo = self._remover_recursivo(no.obter_filho_esquerdo(versao), valor, versao)
            no.definir_filho_esquerdo(filho_esquerdo, versao)
            if filho_esquerdo:
                filho_esquerdo.definir_pai(no, versao)
        elif valor > no.valor:
            filho_direito = self._remover_recursivo(no.obter_filho_direito(versao), valor, versao)
            no.definir_filho_direito(filho_direito, versao)
            if filho_direito:
                filho_direito.definir_pai(no, versao)
        else:
            # Nó encontrado, remover
            return self._remover_no(no, versao)
        
        return self._balancear_apos_remocao(no, versao)
    
    def _remover_no(self, no, versao):
        """
        Remove um nó específico da árvore.
        
        Args:
            no (No): Nó a ser removido
            versao (int): Versão da operação
            
        Returns:
            No ou None: Nó substituto
        """
        filho_esquerdo = no.obter_filho_esquerdo(versao)
        filho_direito = no.obter_filho_direito(versao)
        
        # Caso 1: Nó sem filhos ou com apenas um filho
        if filho_esquerdo is None:
            no.remover(versao)
            return filho_direito
        elif filho_direito is None:
            no.remover(versao)
            return filho_esquerdo
        
        # Caso 2: Nó com dois filhos
        # Encontrar o sucessor (menor valor na subárvore direita)
        sucessor = self._encontrar_minimo(filho_direito, versao)
        
        # Substituir o valor do nó pelo valor do sucessor
        no.valor = sucessor.valor
        
        # Remover o sucessor da subárvore direita
        nova_subarvore_direita = self._remover_recursivo(filho_direito, sucessor.valor, versao)
        no.definir_filho_direito(nova_subarvore_direita, versao)
        if nova_subarvore_direita:
            nova_subarvore_direita.definir_pai(no, versao)
        
        return no
    
    def _encontrar_minimo(self, no, versao):
        """
        Encontra o nó com valor mínimo em uma subárvore.
        
        Args:
            no (No): Raiz da subárvore
            versao (int): Versão da consulta
            
        Returns:
            No: Nó com valor mínimo
        """
        while no and no.obter_filho_esquerdo(versao) and no.obter_filho_esquerdo(versao).esta_ativo(versao):
            no = no.obter_filho_esquerdo(versao)
        return no
    
    def _balancear_apos_inclusao(self, no, versao):
        """
        Balanceia a árvore após uma inclusão seguindo as regras rubro-negras.
        
        Args:
            no (No): Nó a verificar
            versao (int): Versão da operação
            
        Returns:
            No: Nova raiz da subárvore
        """
        # Caso 1: Verificar violação vermelho-vermelho
        filho_esquerdo = no.obter_filho_esquerdo(versao)
        filho_direito = no.obter_filho_direito(versao)
        
        # Balanceamento baseado nos padrões de Okasaki
        if (filho_esquerdo and filho_esquerdo.obter_cor(versao) == Cor.VERMELHO):
            neto_esq_esq = filho_esquerdo.obter_filho_esquerdo(versao)
            neto_esq_dir = filho_esquerdo.obter_filho_direito(versao)
            
            # Caso: nó preto com filho esquerdo vermelho e neto esquerdo vermelho
            if (neto_esq_esq and neto_esq_esq.obter_cor(versao) == Cor.VERMELHO):
                return self._balancear_caso_esquerda_esquerda(no, versao)
            
            # Caso: nó preto com filho esquerdo vermelho e neto direito vermelho
            if (neto_esq_dir and neto_esq_dir.obter_cor(versao) == Cor.VERMELHO):
                return self._balancear_caso_esquerda_direita(no, versao)
        
        if (filho_direito and filho_direito.obter_cor(versao) == Cor.VERMELHO):
            neto_dir_esq = filho_direito.obter_filho_esquerdo(versao)
            neto_dir_dir = filho_direito.obter_filho_direito(versao)
            
            # Caso: nó preto com filho direito vermelho e neto esquerdo vermelho
            if (neto_dir_esq and neto_dir_esq.obter_cor(versao) == Cor.VERMELHO):
                return self._balancear_caso_direita_esquerda(no, versao)
            
            # Caso: nó preto com filho direito vermelho e neto direito vermelho
            if (neto_dir_dir and neto_dir_dir.obter_cor(versao) == Cor.VERMELHO):
                return self._balancear_caso_direita_direita(no, versao)
        
        return no
    
    def _balancear_caso_esquerda_esquerda(self, no, versao):
        """Balanceia o caso esquerda-esquerda (rotação à direita)."""
        filho_esquerdo = no.obter_filho_esquerdo(versao)
        neto_esq_esq = filho_esquerdo.obter_filho_esquerdo(versao)
        neto_esq_dir = filho_esquerdo.obter_filho_direito(versao)
        filho_direito = no.obter_filho_direito(versao)
        
        # Reconfigurar a árvore
        filho_esquerdo.definir_cor(Cor.VERMELHO, versao)
        neto_esq_esq.definir_cor(Cor.PRETO, versao)
        no.definir_cor(Cor.PRETO, versao)
        
        # Reorganizar nós
        filho_esquerdo.definir_filhos(neto_esq_esq, no, versao)
        no.definir_filhos(neto_esq_dir, filho_direito, versao)
        
        # Atualizar pais
        if neto_esq_dir:
            neto_esq_dir.definir_pai(no, versao)
        no.definir_pai(filho_esquerdo, versao)
        neto_esq_esq.definir_pai(filho_esquerdo, versao)
        
        return filho_esquerdo
    
    def _balancear_caso_esquerda_direita(self, no, versao):
        """Balanceia o caso esquerda-direita (rotação dupla)."""
        filho_esquerdo = no.obter_filho_esquerdo(versao)
        neto_esq_dir = filho_esquerdo.obter_filho_direito(versao)
        bisneto_esq = neto_esq_dir.obter_filho_esquerdo(versao)
        bisneto_dir = neto_esq_dir.obter_filho_direito(versao)
        filho_direito = no.obter_filho_direito(versao)
        
        # Reconfigurar cores
        neto_esq_dir.definir_cor(Cor.VERMELHO, versao)
        filho_esquerdo.definir_cor(Cor.PRETO, versao)
        no.definir_cor(Cor.PRETO, versao)
        
        # Reorganizar nós
        neto_esq_dir.definir_filhos(filho_esquerdo, no, versao)
        filho_esquerdo.definir_filhos(filho_esquerdo.obter_filho_esquerdo(versao), bisneto_esq, versao)
        no.definir_filhos(bisneto_dir, filho_direito, versao)
        
        # Atualizar pais
        if bisneto_esq:
            bisneto_esq.definir_pai(filho_esquerdo, versao)
        if bisneto_dir:
            bisneto_dir.definir_pai(no, versao)
        filho_esquerdo.definir_pai(neto_esq_dir, versao)
        no.definir_pai(neto_esq_dir, versao)
        
        return neto_esq_dir
    
    def _balancear_caso_direita_esquerda(self, no, versao):
        """Balanceia o caso direita-esquerda (rotação dupla)."""
        filho_direito = no.obter_filho_direito(versao)
        neto_dir_esq = filho_direito.obter_filho_esquerdo(versao)
        bisneto_esq = neto_dir_esq.obter_filho_esquerdo(versao)
        bisneto_dir = neto_dir_esq.obter_filho_direito(versao)
        filho_esquerdo = no.obter_filho_esquerdo(versao)
        
        # Reconfigurar cores
        neto_dir_esq.definir_cor(Cor.VERMELHO, versao)
        no.definir_cor(Cor.PRETO, versao)
        filho_direito.definir_cor(Cor.PRETO, versao)
        
        # Reorganizar nós
        neto_dir_esq.definir_filhos(no, filho_direito, versao)
        no.definir_filhos(filho_esquerdo, bisneto_esq, versao)
        filho_direito.definir_filhos(bisneto_dir, filho_direito.obter_filho_direito(versao), versao)
        
        # Atualizar pais
        if bisneto_esq:
            bisneto_esq.definir_pai(no, versao)
        if bisneto_dir:
            bisneto_dir.definir_pai(filho_direito, versao)
        no.definir_pai(neto_dir_esq, versao)
        filho_direito.definir_pai(neto_dir_esq, versao)
        
        return neto_dir_esq
    
    def _balancear_caso_direita_direita(self, no, versao):
        """Balanceia o caso direita-direita (rotação à esquerda)."""
        filho_direito = no.obter_filho_direito(versao)
        neto_dir_dir = filho_direito.obter_filho_direito(versao)
        neto_dir_esq = filho_direito.obter_filho_esquerdo(versao)
        filho_esquerdo = no.obter_filho_esquerdo(versao)
        
        # Reconfigurar cores
        filho_direito.definir_cor(Cor.VERMELHO, versao)
        no.definir_cor(Cor.PRETO, versao)
        neto_dir_dir.definir_cor(Cor.PRETO, versao)
        
        # Reorganizar nós
        filho_direito.definir_filhos(no, neto_dir_dir, versao)
        no.definir_filhos(filho_esquerdo, neto_dir_esq, versao)
        
        # Atualizar pais
        if neto_dir_esq:
            neto_dir_esq.definir_pai(no, versao)
        no.definir_pai(filho_direito, versao)
        neto_dir_dir.definir_pai(filho_direito, versao)
        
        return filho_direito
    
    def _balancear_apos_remocao(self, no, versao):
        """
        Balanceia a árvore após uma remoção seguindo as regras rubro-negras.
        
        Args:
            no (No): Nó a verificar
            versao (int): Versão da operação
            
        Returns:
            No: Nova raiz da subárvore
        """
        if no is None:
            return None
        
        # Verificar se há violação das propriedades rubro-negras
        # e aplicar as correções necessárias
        return self._corrigir_violacoes_remocao(no, versao)
    
    def _corrigir_violacoes_remocao(self, no, versao):
        """
        Corrige violações das propriedades rubro-negras após remoção.
        
        Args:
            no (No): Nó atual
            versao (int): Versão da operação
            
        Returns:
            No: Nova raiz da subárvore
        """
        # Implementação simplificada para remoção
        # Em uma implementação completa, seria necessário tratar todos os casos
        # de violação de propriedades após remoção (casos do irmão vermelho,
        # irmão preto com filhos vermelhos, etc.)
        
        # Por enquanto, apenas garantir que a raiz seja preta
        if no and no.obter_pai(versao) is None:
            no.definir_cor(Cor.PRETO, versao)
        
        return no
    
    def _rotacao_esquerda(self, no, versao):
        """
        Executa rotação à esquerda.
        
        Args:
            no (No): Nó para rotacionar
            versao (int): Versão da operação
            
        Returns:
            No: Nova raiz após rotação
        """
        filho_direito = no.obter_filho_direito(versao)
        if filho_direito is None:
            return no
        
        # Atualizar conexões
        no.definir_filho_direito(filho_direito.obter_filho_esquerdo(versao), versao)
        if filho_direito.obter_filho_esquerdo(versao):
            filho_direito.obter_filho_esquerdo(versao).definir_pai(no, versao)
        
        filho_direito.definir_filho_esquerdo(no, versao)
        filho_direito.definir_pai(no.obter_pai(versao), versao)
        no.definir_pai(filho_direito, versao)
        
        return filho_direito
    
    def _rotacao_direita(self, no, versao):
        """
        Executa rotação à direita.
        
        Args:
            no (No): Nó para rotacionar
            versao (int): Versão da operação
            
        Returns:
            No: Nova raiz após rotação
        """
        filho_esquerdo = no.obter_filho_esquerdo(versao)
        if filho_esquerdo is None:
            return no
        
        # Atualizar conexões
        no.definir_filho_esquerdo(filho_esquerdo.obter_filho_direito(versao), versao)
        if filho_esquerdo.obter_filho_direito(versao):
            filho_esquerdo.obter_filho_direito(versao).definir_pai(no, versao)
        
        filho_esquerdo.definir_filho_direito(no, versao)
        filho_esquerdo.definir_pai(no.obter_pai(versao), versao)
        no.definir_pai(filho_esquerdo, versao)
        
        return filho_esquerdo
    
    def _percorrer_em_ordem(self, no, versao, profundidade, resultado):
        """
        Percorre a árvore em ordem, coletando os nós ativos.
        
        Args:
            no (No): Nó atual
            versao (int): Versão da consulta
            profundidade (int): Profundidade atual
            resultado (list): Lista para armazenar o resultado
        """
        if no is None or not no.esta_ativo(versao):
            return
        
        # Percorrer subárvore esquerda
        filho_esquerdo = no.obter_filho_esquerdo(versao)
        if filho_esquerdo:
            self._percorrer_em_ordem(filho_esquerdo, versao, profundidade + 1, resultado)
        
        # Visitar nó atual
        cor_str = no.obter_cor(versao).value
        resultado.append(f"{no.valor},{profundidade},{cor_str}")
        
        # Percorrer subárvore direita
        filho_direito = no.obter_filho_direito(versao)
        if filho_direito:
            self._percorrer_em_ordem(filho_direito, versao, profundidade + 1, resultado)