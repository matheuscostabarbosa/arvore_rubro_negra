"""
Módulo responsável por processar as operações da árvore rubro-negra.
"""

from arvore_rubro_negra import ArvoreRubroNegra

class ProcessadorOperacoes:
    """
    Classe responsável por processar comandos e operações na árvore rubro-negra.
    """
    
    def __init__(self):
        """Inicializa o processador com uma árvore vazia."""
        self.arvore = ArvoreRubroNegra()
    
    def processar_arquivo(self, caminho_entrada, caminho_saida):
        """
        Processa um arquivo de entrada e gera um arquivo de saída.
        
        Args:
            caminho_entrada (str): Caminho do arquivo de entrada
            caminho_saida (str): Caminho do arquivo de saída
        """
        try:
            with open(caminho_entrada, 'r', encoding='utf-8') as arquivo_entrada:
                linhas = arquivo_entrada.readlines()
            
            resultado = []
            
            for linha in linhas:
                linha = linha.strip()
                if linha:  # Ignora linhas vazias
                    saida_operacao = self.processar_operacao(linha)
                    if saida_operacao:
                        resultado.extend(saida_operacao)
            
            with open(caminho_saida, 'w', encoding='utf-8') as arquivo_saida:
                for linha_saida in resultado:
                    arquivo_saida.write(linha_saida + '\n')
                    
        except FileNotFoundError:
            print(f"Erro: Arquivo '{caminho_entrada}' não encontrado.")
        except Exception as e:
            print(f"Erro ao processar arquivo: {e}")
    
    def processar_operacao(self, linha):
        """
        Processa uma linha de operação.
        
        Args:
            linha (str): Linha contendo a operação
            
        Returns:
            list ou None: Lista de linhas para o arquivo de saída, ou None se não há saída
        """
        partes = linha.split()
        
        if not partes:
            return None
        
        operacao = partes[0].upper()
        
        try:
            if operacao == "INC":
                return self._processar_inclusao(partes)
            elif operacao == "REM":
                return self._processar_remocao(partes)
            elif operacao == "SUC":
                return self._processar_sucessor(partes)
            elif operacao == "IMP":
                return self._processar_impressao(partes)
            else:
                print(f"Operação desconhecida: {operacao}")
                return None
                
        except (ValueError, IndexError) as e:
            print(f"Erro ao processar operação '{linha}': {e}")
            return None
    
    def _processar_inclusao(self, partes):
        """
        Processa uma operação de inclusão.
        
        Args:
            partes (list): Partes da linha de comando
            
        Returns:
            None: Operação de inclusão não gera saída
        """
        if len(partes) != 2:
            raise ValueError("Operação INC deve ter formato: INC <valor>")
        
        valor = int(partes[1])
        self.arvore.incluir(valor)
        return None
    
    def _processar_remocao(self, partes):
        """
        Processa uma operação de remoção.
        
        Args:
            partes (list): Partes da linha de comando
            
        Returns:
            None: Operação de remoção não gera saída
        """
        if len(partes) != 2:
            raise ValueError("Operação REM deve ter formato: REM <valor>")
        
        valor = int(partes[1])
        self.arvore.remover(valor)
        return None
    
    def _processar_sucessor(self, partes):
        """
        Processa uma operação de busca de sucessor.
        
        Args:
            partes (list): Partes da linha de comando
            
        Returns:
            list: Linhas de saída para o arquivo
        """
        if len(partes) != 3:
            raise ValueError("Operação SUC deve ter formato: SUC <valor> <versao>")
        
        valor = int(partes[1])
        versao = int(partes[2])
        
        sucessor = self.arvore.buscar_sucessor(valor, versao)
        
        # Linha de eco da operação
        linha_operacao = f"SUC {valor} {versao}"
        
        # Resultado do sucessor
        if sucessor is not None:
            linha_resultado = str(sucessor)
        else:
            linha_resultado = "infinito"
        
        return [linha_operacao, linha_resultado]
    
    def _processar_impressao(self, partes):
        """
        Processa uma operação de impressão.
        
        Args:
            partes (list): Partes da linha de comando
            
        Returns:
            list: Linhas de saída para o arquivo
        """
        if len(partes) != 2:
            raise ValueError("Operação IMP deve ter formato: IMP <versao>")
        
        versao = int(partes[1])
        
        elementos = self.arvore.imprimir_arvore(versao)
        
        # Linha de eco da operação
        linha_operacao = f"IMP {versao}"
        
        # Elementos da árvore em ordem
        if elementos:
            linha_elementos = " ".join(elementos)
        else:
            linha_elementos = ""
        
        return [linha_operacao, linha_elementos]
    
    def obter_versao_atual(self):
        """
        Obtém a versão atual da árvore.
        
        Returns:
            int: Versão atual
        """
        return self.arvore.versao_atual
    
    def obter_estatisticas(self):
        """
        Obtém estatísticas da árvore.
        
        Returns:
            dict: Dicionário com estatísticas
        """
        return {
            "versao_atual": self.arvore.versao_atual,
            "total_versoes": self.arvore.versao_atual #+ 1
        }