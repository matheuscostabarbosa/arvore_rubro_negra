"""
Programa principal para executar operações na árvore rubro-negra com persistência parcial.
Suporte para modo arquivo e modo interativo.
"""

import sys
import os
from processador_operacoes import ProcessadorOperacoes

class InterfaceInterativa:
    """Interface interativa para operações na árvore rubro-negra."""
    
    def __init__(self):
        """Inicializa a interface interativa."""
        self.processador = ProcessadorOperacoes()
        self.historico = []
    
    def executar(self):
        """Executa o modo interativo."""
        self.exibir_banner()
        self.exibir_ajuda()
        
        while True:
            try:
                comando = input("\n> ").strip()
                
                if not comando:
                    continue
                    
                if comando.upper() in ['QUIT', 'EXIT', 'SAIR']:
                    print("Encerrando programa...")
                    break
                elif comando.upper() in ['HELP', 'AJUDA']:
                    self.exibir_ajuda()
                elif comando.upper() == 'STATS':
                    self.exibir_estatisticas()
                elif comando.upper() == 'HIST':
                    self.exibir_historico()
                elif comando.upper() == 'CLEAR':
                    self.limpar_tela()
                elif comando.upper() == 'RESET':
                    self.resetar_arvore()
                elif comando.upper() == 'EXEMPLO':
                    self.executar_exemplo()
                else:
                    self.processar_comando(comando)
                    
            except KeyboardInterrupt:
                print("\n\nPrograma interrompido pelo usuário.")
                break
            except EOFError:
                print("\nEncerrando programa...")
                break
            except Exception as e:
                print(f"Erro inesperado: {e}")
    
    def exibir_banner(self):
        """Exibe o banner do programa."""
        print("=" * 60)
        print("    ÁRVORE RUBRO-NEGRA COM PERSISTÊNCIA PARCIAL")
        print("=" * 60)
        print("Modo Interativo Ativo")
        print("Digite 'help' para ver os comandos disponíveis")
    
    def exibir_ajuda(self):
        """Exibe a ajuda com comandos disponíveis."""
        print("\n📋 COMANDOS DISPONÍVEIS:")
        print("  Operações da Árvore:")
        print("    INC <valor>        - Insere valor na árvore")
        print("    REM <valor>        - Remove valor da árvore")
        print("    SUC <valor> <ver>  - Busca sucessor do valor na versão")
        print("    IMP <versao>       - Imprime árvore da versão")
        print()
        print("  Comandos do Sistema:")
        print("    HELP / AJUDA       - Mostra esta ajuda")
        print("    STATS              - Mostra estatísticas da árvore")
        print("    HIST               - Mostra histórico de comandos")
        print("    CLEAR              - Limpa a tela")
        print("    RESET              - Reinicia a árvore")
        print("    EXEMPLO            - Executa exemplo demonstrativo")
        print("    QUIT / EXIT / SAIR - Encerra o programa")
        print()
        print("💡 Exemplos:")
        print("    > INC 10")
        print("    > INC 5")
        print("    > IMP 2")
        print("    > SUC 7 2")
        print("    > REM 5")
    
    def processar_comando(self, comando):
        """Processa um comando do usuário."""
        try:
            # Adiciona ao histórico
            self.historico.append(comando)
            
            # Processa a operação
            resultado = self.processador.processar_operacao(comando)
            
            if resultado:
                print("📤 Resultado:")
                for linha in resultado:
                    print(f"   {linha}")
            else:
                partes = comando.split()
                if partes[0].upper() in ['INC', 'REM']:
                    print(f"✅ Operação {partes[0].upper()} executada com sucesso")
                    print(f"   Versão atual: {self.processador.obter_versao_atual()}")
                    
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def exibir_estatisticas(self):
        """Exibe estatísticas da árvore."""
        stats = self.processador.obter_estatisticas()
        print("\n📊 ESTATÍSTICAS:")
        print(f"   Versão atual: {stats['versao_atual']}")
        print(f"   Total de versões: {stats['total_versoes']}")
        print(f"   Comandos executados: {len(self.historico)}")
    
    def exibir_historico(self):
        """Exibe o histórico de comandos."""
        print("\n📜 HISTÓRICO DE COMANDOS:")
        if not self.historico:
            print("   Nenhum comando executado ainda")
        else:
            for i, cmd in enumerate(self.historico[-10:], 1):  # Últimos 10
                print(f"   {i:2d}. {cmd}")
            if len(self.historico) > 10:
                print(f"   ... (mostrando últimos 10 de {len(self.historico)} comandos)")
    
    def limpar_tela(self):
        """Limpa a tela do terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')
        self.exibir_banner()
    
    def resetar_arvore(self):
        """Reinicia a árvore."""
        resposta = input("⚠️  Tem certeza que deseja reiniciar a árvore? (s/N): ")
        if resposta.lower() in ['s', 'sim', 'y', 'yes']:
            self.processador = ProcessadorOperacoes()
            self.historico = []
            print("✅ Árvore reiniciada com sucesso!")
        else:
            print("❌ Operação cancelada")
    
    def executar_exemplo(self):
        """Executa um exemplo demonstrativo."""
        print("\n🎯 EXECUTANDO EXEMPLO DEMONSTRATIVO:")
        
        operacoes = [
            "INC 10",
            "INC 5", 
            "INC 15",
            "INC 3",
            "INC 7",
            "IMP 5",
            "SUC 6 5",
            "REM 5",
            "IMP 6",
            "SUC 3 6"
        ]
        
        for operacao in operacoes:
            print(f"\n📝 Executando: {operacao}")
            resultado = self.processador.processar_operacao(operacao)
            self.historico.append(operacao)
            
            if resultado:
                for linha in resultado:
                    print(f"   📤 {linha}")
            else:
                print(f"   ✅ Operação executada (versão: {self.processador.obter_versao_atual()})")
        
        print(f"\n🏁 Exemplo concluído! Versão final: {self.processador.obter_versao_atual()}")

def executar_exemplo_simples():
    """Executa um exemplo simples para demonstração."""
    print("=== Exemplo de Uso da Árvore Rubro-Negra ===")
    
    processador = ProcessadorOperacoes()
    
    # Operações de exemplo
    operacoes = [
        "INC 10",
        "INC 5", 
        "INC 15",
        "INC 3",
        "INC 7",
        "IMP 5",
        "SUC 6 5",
        "REM 5",
        "IMP 6",
        "SUC 10 5"
    ]
    
    resultado = []
    for operacao in operacoes:
        print(f"Executando: {operacao}")
        saida = processador.processar_operacao(operacao)
        if saida:
            resultado.extend(saida)
            for linha in saida:
                print(f"  -> {linha}")
    
    print(f"\nVersão final: {processador.obter_versao_atual()}")

def processar_arquivo(arquivo_entrada, arquivo_saida):
    """Processa um arquivo de entrada e gera um arquivo de saída."""
    # Verificar se o arquivo de entrada existe
    if not os.path.exists(arquivo_entrada):
        print(f"Erro: Arquivo de entrada '{arquivo_entrada}' não encontrado.")
        sys.exit(1)
    
    # Criar processador e executar operações
    processador = ProcessadorOperacoes()
    
    print(f"Processando arquivo: {arquivo_entrada}")
    print(f"Arquivo de saída: {arquivo_saida}")
    
    try:
        processador.processar_arquivo(arquivo_entrada, arquivo_saida)
        
        # Exibir estatísticas
        stats = processador.obter_estatisticas()
        print(f"Processamento concluído!")
        print(f"Versão final da árvore: {stats['versao_atual']}")
        print(f"Total de versões criadas: {stats['total_versoes']}")
        
    except Exception as e:
        print(f"Erro durante o processamento: {e}")
        sys.exit(1)

def exibir_uso():
    """Exibe informações de uso do programa."""
    print("=" * 60)
    print("    ÁRVORE RUBRO-NEGRA COM PERSISTÊNCIA PARCIAL")
    print("=" * 60)
    print()
    print("📋 MODOS DE EXECUÇÃO:")
    print()
    print("1️⃣  Modo Arquivo:")
    print("   python main.py <arquivo_entrada> <arquivo_saida>")
    print("   Exemplo: python main.py entrada.txt saida.txt")
    print()
    print("2️⃣  Modo Interativo:")
    print("   python main.py -i")
    print("   python main.py --interativo")
    print()
    print("3️⃣  Exemplo Demonstrativo:")
    print("   python main.py -e")
    print("   python main.py --exemplo")
    print()
    print("4️⃣  Esta Ajuda:")
    print("   python main.py -h")
    print("   python main.py --help")
    print()

def main():
    """Função principal do programa."""
    
    # Sem argumentos - modo interativo por padrão
    if len(sys.argv) == 1:
        interface = InterfaceInterativa()
        interface.executar()
        return
    
    # Um argumento - verificar flags especiais
    if len(sys.argv) == 2:
        arg = sys.argv[1].lower()
        
        if arg in ['-i', '--interativo', '--interactive']:
            interface = InterfaceInterativa()
            interface.executar()
            return
        elif arg in ['-e', '--exemplo', '--example']:
            executar_exemplo_simples()
            return
        elif arg in ['-h', '--help', '--ajuda']:
            exibir_uso()
            return
        else:
            print(f"Argumento desconhecido: {sys.argv[1]}")
            exibir_uso()
            sys.exit(1)
    
    # Dois argumentos - modo arquivo
    elif len(sys.argv) == 3:
        arquivo_entrada = sys.argv[1]
        arquivo_saida = sys.argv[2]
        processar_arquivo(arquivo_entrada, arquivo_saida)
        return
    
    # Número incorreto de argumentos
    else:
        print("Número incorreto de argumentos.")
        exibir_uso()
        sys.exit(1)

if __name__ == "__main__":
    main()