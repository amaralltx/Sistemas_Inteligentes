class Agente:

    CUSTOS = {
        "N": 1,   
        "S": 1,  
        "L": 1,   
        "O": 1,  
        "NE": 1.5,  
        "SE": 1.5, 
        "NO": 1.5, 
        "SO": 1.5 
    }


    def __init__(self, objeto_movel):
        self.objeto_movel = objeto_movel
        self.estado_inicial = []  # Ex: (0, 0)
        self.estado_objetivo = []   # Ex: (7, 8)
        self.grid_interno = []    # Ex: matriz 10x10 com 0 e 1 (1 = parede)
        self.plano = []
        self.custo_acumulado = 0
    # cada vez que o grid coloca uma nova parede ou atualiza o objetivo
    def atualiza_grid_interno(self, grid):
        return
    
    def ir(self, direcao, nova_posicao):
        print(f"Agente: Executando movimento {direcao}")
        self.custo_acumulado += self.CUSTOS[direcao]
        self.objeto_movel.mover(direcao, nova_posicao)

    def lerPos(self):
        return self.objeto_movel.ler_posicao()

    def calcular_acoes_possiveis(self, estado):
        # Exemplo: calcula ações possíveis considerando limites e paredes do grid_interno
        acoes = []
        movimentos = self.objeto_movel.DIRECOES
        for direcao, (dx, dy) in movimentos.items():
            novo_estado = (estado[0] + dx, estado[1] + dy)
            if self.estado_valido(novo_estado):
                acoes.append(direcao)
        return acoes

    # Retorna as ações possíveis de realizar a partir das coordenadas possíveis
    def obter_acoes_possiveis(self, coordenadas_validas):
        acoes_possiveis = []
        for direcao in self.objeto_movel.DIRECOES:
            if direcao in coordenadas_validas:
                acoes_possiveis.append(direcao)
        # Envia ao objeto_movel os estados possiveis em formato de coordenada e retorna as respectivas direções

        return acoes_possiveis

    def estado_sucessor(self, estado, acao):
        """
        Calcula o estado sucessor a partir da execução de uma ação em um estado.
        """
        if acao in self.objeto_movel.DIRECOES:
            dx, dy = self.objeto_movel.DIRECOES[acao]
            nova_posicao = (estado[0] + dx, estado[1] + dy)
            if 0 <= nova_posicao[0] < self.altura and 0 <= nova_posicao[1] < self.largura:
                if self.grid[self.altura - 1 - nova_posicao[0]][nova_posicao[1]] != '⬛':
                    return nova_posicao
        return estado  # Retorna o estado atual se a ação não for válida

    def executar_plano(self, plano):
        passos = plano.split()
        for passo in passos:
            print(passo)

    # def estado_valido(self, estado):
    #     x, y = estado
    #     linhas = len(self.grid_interno)
    #     colunas = len(self.grid_interno[0])
    #     # Verifica limites do grid
    #     if x < 0 or x >= colunas or y < 0 or y >= linhas:
    #         return False
    #     # Verifica se há parede (supondo 1 = parede, 0 = livre)
    #     if self.grid_interno[y][x] == 1:
    #         return False
    #     return True

    # def calcular_sucessor(self, estado, acao):
    #     movimentos = {
    #         "N": (0, 1), "NE": (1, 1), "L": (1, 0), "SE": (1, -1),
    #         "S": (0, -1), "SO": (-1, -1), "O": (-1, 0), "NO": (-1, 1)
    #     }
    #     dx, dy = movimentos.get(acao, (0, 0))
    #     return (estado[0] + dx, estado[1] + dy)

    def teste_objetivo(self, estado):
        return estado == self.estado_objetivo

    # def calcular_custo(self, acao):
    #     # Custo: 1 para movimentos cardeais e 1.5 para diagonais
    #     if acao not in 
    #     if acao in ["N", "S", "L", "O"]:
    #         return 1
    #     else:
    #         return 1.5

    # def ciclo_raciocinio(self):
    #     print("\n--- Ciclo de Raciocínio do Agente ---")
    #     estado_atual = self.lerPos()
    #     print("Crenças do agente (grid interno):")
    #     for linha in self.grid_interno:
    #         print(linha)
    #     acoes_possiveis = self.calcular_acoes_possiveis(estado_atual)
    #     print("Ações possíveis a partir do estado atual:", acoes_possiveis)
    #     # Retira a próxima ação do plano
    #     proxima = self.plano.proxima_acao()
    #     if proxima is None:
    #         print("Plano esgotado.")
    #         return
    #     print("Próxima ação do plano:", proxima)
    #     # Executa a ação
    #     self.ir(proxima)
    #     custo = self.calcular_custo(proxima)
    #     self.custo_acumulado += custo
    #     print("Custo acumulado:", self.custo_acumulado)
    #     if self.teste_objetivo(self.lerPos()):
    #         print("Objetivo atingido!")


# # Exemplo de ciclo de raciocínio
# while not plano.is_empty():
#     agente.ciclo_raciocinio()
#     # Aqui também poderíamos imprimir o estado atual do ambiente (usando métodos da classe Ambiente)
    def obter_estado_objeto(self):
        return self.objeto.estado_atual