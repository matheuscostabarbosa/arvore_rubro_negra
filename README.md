# Árvore Rubro-Negra com Persistência Parcial

Este projeto implementa uma **árvore binária de busca rubro-negra com persistência parcial** em Python, permitindo manter múltiplas versões da estrutura de dados sem duplicar toda a árvore a cada modificação.

## Linguagem de Programação

**Python 3.10+**

## Iniciando a Aplicação a Partir do GitHub
Siga os passos abaixo:

Clone o repositório

```bash
git clone https://github.com/matheuscostabarbosa/arvore_rubro_negra
```


Acesse a pasta do projeto

```bash
cd arvore_rubro_negra
```

## Como Executar a Aplicação

### Modo Arquivo (Processamento em Lote)
```bash
python main.py arquivo_entrada.txt arquivo_saida.txt
```

### Modo Interativo
```bash
python main.py -i
# ou
python main.py --interativo
```

### Exemplo Demonstrativo
```bash
python main.py -e
# ou
python main.py --exemplo
```

### Executar Testes
```bash
python testes.py
# ou
pytest testes.py testes.py
```

### Ajuda
```bash
python main.py -h
# ou
python main.py --help
```

### Referências (Caminho de arquivos)
**Making Data Structures Persistent - DRISCOLL:** referencias/Making Data Structures Persistent - Driscoll.pdf
**Deletion The curse of the red-black tree - GERMANE - MIGTH:** referencias/Deletion The curse of the red-black tree - Germane - Migth.pdf
**Árvore Rubro-Negra - Siang Wun Song - Apresentação:** referencias/Árvore Rubro-Negra - Siang Wun Song - Apresentação.pdf
**Arvore rubro-negra - Remocao - Marcelo Albertini:** referencias/Arvore rubro-negra - Remocao - Marcelo Albertini.pdf



### Como foi desenvolvida a Persistência Parcial?

**Persistência parcial** é uma técnica que permite acessar versões anteriores de uma estrutura de dados após modificações, sem duplicar toda a estrutura.

#### Características da Implementação:
- **Histórico por Nó**: Cada nó mantém um histórico de suas modificações por versão
- **Economia de Memória**: Não duplica toda a árvore para cada versão
- **Acesso Eficiente**: Permite consultar qualquer versão anterior em tempo logarítmico
- **Versionamento Automático**: Cada operação de inclusão/remoção cria uma nova versão

#### Como Funciona:
- Cada nó armazena **múltiplos estados** (cor, filhos, pai) indexados por versão
- Quando uma modificação ocorre, apenas os **nós afetados** criam novos estados
- Operações de consulta especificam a **versão desejada**

## Estrutura do Projeto

```
arvore-rubro-negra/
├── main.py                     # Programa principal com interface
├── no.py                       # Classe do nó com persistência
├── arvore_rubro_negra.py       # Implementação da árvore
├── processador_operacoes.py    # Processamento de comandos
├── testes.py                   # Testes unitários básicos
├── referencias/                # Pasta com referências de estudo
├── exemplo.txt         # Arquivo de exemplo
└── README.md                   # Esta documentação
```

## Descrição dos Métodos e Estruturas

### 1. `no.py` - Classe do Nó com Persistência

**Classe Principal:** `No`

Esta classe implementa um nó da árvore que mantém **histórico de modificações por versão**.

#### Enum `Cor`
```python
class Cor(Enum):
    VERMELHO = "R"  # Nó vermelho
    PRETO = "N"     # Nó preto
```

#### Atributos do Nó
- `valor`: Valor inteiro armazenado no nó
- `versao_criacao`: Versão em que o nó foi criado
- `historico_cores`: Dicionário {versão: cor} para persistência da cor
- `historico_filhos`: Dicionário {versão: [filho_esq, filho_dir]} para persistência dos filhos
- `historico_pais`: Dicionário {versão: pai} para persistência do pai
- `versao_remocao`: Versão em que o nó foi removido (None se ativo)

#### Métodos Principais
- `obter_cor(versao)`: Obtém a cor do nó em uma versão específica
- `definir_cor(cor, versao)`: Define a cor do nó para uma versão
- `obter_filho_esquerdo(versao)`: Obtém filho esquerdo na versão
- `obter_filho_direito(versao)`: Obtém filho direito na versão
- `definir_filho_esquerdo(filho, versao)`: Define filho esquerdo
- `definir_filho_direito(filho, versao)`: Define filho direito
- `obter_pai(versao)`: Obtém o pai do nó na versão
- `definir_pai(pai, versao)`: Define o pai do nó
- `esta_ativo(versao)`: Verifica se o nó está ativo (não removido) na versão
- `remover(versao)`: Marca o nó como removido a partir da versão

#### Método de Versionamento
- `_obter_versao_valida(versao, historico)`: Encontra a versão mais recente válida para um histórico específico

### 2. `arvore_rubro_negra.py` - Implementação da Árvore

**Classe Principal:** `ArvoreRubroNegra`

Implementa a árvore rubro-negra com todas as operações e balanceamento automático.

#### Atributos
- `raizes`: Array de 100 posições para armazenar raízes de cada versão
- `versao_atual`: Versão corrente da árvore

#### Métodos de Operação Principal
- `incluir(valor)`: Inclui um valor na árvore e cria nova versão
- `remover(valor)`: Remove um valor da árvore e cria nova versão  
- `buscar_sucessor(valor, versao=None)`: Busca o sucessor de um valor
- `imprimir_arvore(versao=None)`: Imprime árvore em ordem crescente

#### Métodos de Inclusão
- `_incluir_recursivo(no, valor, versao)`: Inclusão recursiva mantendo BST
- `_balancear_apos_inclusao(no, versao)`: Aplica balanceamento após inclusão

#### Métodos de Remoção
- `_remover_recursivo(no, valor, versao)`: Remoção recursiva
- `_remover_no(no, versao)`: Remove nó específico (folha, 1 filho, 2 filhos)
- `_encontrar_minimo(no, versao)`: Encontra sucessor para caso de 2 filhos
- `_balancear_apos_remocao(no, versao)`: Aplica balanceamento após remoção

#### Métodos de Balanceamento (Baseados nos Padrões de Okasaki)
- `_balancear_caso_esquerda_esquerda(no, versao)`: Rotação simples à direita
- `_balancear_caso_esquerda_direita(no, versao)`: Rotação dupla esquerda-direita
- `_balancear_caso_direita_esquerda(no, versao)`: Rotação dupla direita-esquerda  
- `_balancear_caso_direita_direita(no, versao)`: Rotação simples à esquerda

#### Métodos de Rotação
- `_rotacao_esquerda(no, versao)`: Executa rotação à esquerda
- `_rotacao_direita(no, versao)`: Executa rotação à direita

#### Métodos Auxiliares
- `_percorrer_em_ordem(no, versao, profundidade, resultado)`: Percorrimento em ordem para impressão
- `_corrigir_violacoes_remocao(no, versao)`: Corrige violações após remoção

### 3. `processador_operacoes.py` - Processamento de Comandos

**Classe Principal:** `ProcessadorOperacoes`

Responsável por interpretar comandos e gerenciar entrada/saída.

#### Métodos de Processamento de Arquivo
- `processar_arquivo(caminho_entrada, caminho_saida)`: Processa arquivo completo
- `processar_operacao(linha)`: Processa uma linha de comando individual

#### Métodos de Processamento de Operações Específicas
- `_processar_inclusao(partes)`: Processa comando "INC valor"
- `_processar_remocao(partes)`: Processa comando "REM valor"
- `_processar_sucessor(partes)`: Processa comando "SUC valor versao"
- `_processar_impressao(partes)`: Processa comando "IMP versao"

#### Métodos de Consulta
- `obter_versao_atual()`: Retorna versão atual da árvore
- `obter_estatisticas()`: Retorna estatísticas de uso

### 4. `main.py` - Programa Principal

Fornece interface de linha de comando com múltiplos modos de execução.

#### Classes
- `InterfaceInterativa`: Implementa modo interativo com comandos em tempo real

#### Funções Principais
- `main()`: Função principal que determina modo de execução
- `processar_arquivo(entrada, saida)`: Modo de processamento de arquivos
- `executar_exemplo_simples()`: Executa exemplo demonstrativo
- `exibir_uso()`: Exibe ajuda de uso

#### Métodos da Interface Interativa
- `executar()`: Loop principal do modo interativo
- `exibir_banner()`: Exibe banner do programa
- `exibir_ajuda()`: Mostra comandos disponíveis
- `processar_comando(comando)`: Processa comando interativo
- `exibir_estatisticas()`: Mostra estatísticas da árvore
    - retorna o total de versões como versão atual + 1, pois a versão 0 é considerada uma versão válida (estado inicial da árvore).
- `exibir_historico()`: Mostra histórico de comandos
- `resetar_arvore()`: Reinicia a árvore
- `executar_exemplo()`: Executa exemplo no modo interativo

## Operações Suportadas

### INC - Inclusão
```
INC <valor>
```
Inclui um elemento na árvore e cria uma nova versão.
- **Entrada**: `INC 42`
- **Saída**: Nenhuma (operação silenciosa)
- **Efeito**: Versão incrementada, elemento inserido com balanceamento

### REM - Remoção
```
REM <valor>
```
Remove um elemento da árvore e cria uma nova versão.
- **Entrada**: `REM 42`
- **Saída**: Nenhuma (operação silenciosa)
- **Efeito**: Versão incrementada, elemento removido com balanceamento

### SUC - Sucessor
```
SUC <valor> <versao>
```
Busca o sucessor de um valor em uma versão específica.
- **Entrada**: `SUC 50 5`
- **Saída**:
  ```
  SUC 50 5
  52
  ```
- **Comportamento**: Retorna menor valor maior que o especificado, ou "infinito" se não existir

### IMP - Impressão
```
IMP <versao>
```
Imprime todos os elementos da árvore em uma versão específica.
- **Entrada**: `IMP 3`
- **Saída**:
  ```
  IMP 3
  10,1,N 20,0,N 30,1,R
  ```
- **Formato**: `valor,profundidade,cor` onde cor é R (vermelho) ou N (preto)

## Algoritmos de Balanceamento

### Inclusão (Baseado em Okasaki)
1. **Inserção**: Novo nó inserido como vermelho (não viola altura preta)
2. **Detecção**: Verifica violações vermelho-vermelho
3. **Correção**: Aplica um dos 4 padrões de balanceamento:
   - Esquerda-Esquerda → Rotação direita simples
   - Esquerda-Direita → Rotação dupla
   - Direita-Esquerda → Rotação dupla  
   - Direita-Direita → Rotação esquerda simples
4. **Finalização**: Raiz sempre pintada de preto

### Remoção
1. **Localização**: Encontra nó a ser removido
2. **Casos de Remoção**:
   - **Folha**: Remove diretamente
   - **1 Filho**: Substitui pelo filho
   - **2 Filhos**: Substitui pelo sucessor in-order
3. **Balanceamento**: Corrige violações de altura preta
4. **Persistência**: Marca nó como removido na versão atual


## Exemplo Completo de Uso

### Arquivo de Entrada (exemplo.txt)
```
INC 50
INC 25
INC 75
INC 10
INC 30
IMP 5
SUC 40 5
REM 25
IMP 6
SUC 25 6
SUC 25 5
```

### Execução
```bash
python main.py exemplo.txt resultado.txt
```

### Arquivo de Saída (resultado.txt)
```
IMP 5
10,2,R 25,1,R 30,2,R 50,0,N 75,1,R
SUC 40 5
50
IMP 6
10,2,R 30,1,R 50,0,N 75,1,R
SUC 25 6
30
SUC 25 5
30
```

## Versionamento 

### Funcionamento das Versões
- **Versão 0**: Árvore vazia (estado inicial)
- **Versão 1+**: Cada INC/REM incrementa a versão
- **Máximo**: 100 versões (99 operações de modificação)
- **Consultas**: SUC e IMP não alteram versão
>  **Obs**: A função exibir_estatisticas() — que mostra estatísticas da árvore na InterfaceInterativa — retorna o total de versões como versão atual + 1, pois a versão 0 é considerada uma versão válida (estado inicial da árvore).

## Testes e Validação

### Tipos de Teste Implementados
- **Testes Unitários** (`testes.py`): Testa classes individuais

### Casos de Teste Cobertos
- Inclusão sequencial, reversa e aleatória
- Remoção com verificação de persistência
- Busca de sucessor em casos limite
- Operações intercaladas
- Stress test com múltiplas versões
- Validação de propriedades rubro-negras
- Verificação de altura logarítmica

## Requisitos e Limitações

### Requisitos de Sistema
- **Python**: 3.10 ou superior
- **Módulos**: Apenas biblioteca padrão (unittest, sys, os)
- **Memória**: Proporcional ao número de nós únicos criados

### Limitações da Implementação
- **Versões**: Máximo 100 versões (versões 0-99)
- **Valores**: Apenas números inteiros
- **Operações de Modificação**: Máximo 99 (INC + REM)
- **Operações de Consulta**: Ilimitadas (SUC + IMP)

### Garantias Oferecidas
- **Balanceamento**: Altura sempre O(log n)
- **Persistência**: Acesso a qualquer versão anterior
- **Consistência**: Propriedades rubro-negras sempre mantidas
- **Eficiência**: Operações logarítmicas garantidas
