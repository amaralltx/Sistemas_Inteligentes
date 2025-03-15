import copy
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
        self.estado_objetivo = []  # Objeto a ser alcançado ao executar o plano
        self.grid_interno = []  # Representação interna do grid
        self.plano = []
        self.custo_acumulado = 0
        self.grid = []
        # Dicionário para as listas de adjacência. 
        # Ex: (0, 0): [('N', (1, 0)), ('L', (0,1))] = nó (0,0) liga a (1,0) pelo norte e (0,1) pelo leste
        self.grafo = {} 

    def definir_estado_objetivo(self, objetivo):
        self.estado_objetivo = objetivo
    
    def definir_grid(self, grid):
        self.grid = copy.deepcopy(grid)
        # Altera o objeto móvel e objetivo no grid para uma melhor análise
        altura = len(self.grid)
        estado_atual = self.obter_estado_objeto()
        estado_atual_x = estado_atual[0]
        estado_atual_y = estado_atual[1]
        self.grid[altura - estado_atual_x -1][estado_atual_y] = "⬜"
        self.grid[altura - self.estado_objetivo[0] -1][self.estado_objetivo[1]] = "⬜"
        return

    def iniciar_plano_grafo(self):
        altura = len(self.grid)
        largura = len(self.grid[0])

        for x in range(altura):
            for y in range(largura):
                # Se a posição do grid a ser analisada é válida
                if self.grid[altura - x - 1][y] == "⬜":
                    self.grafo[(x, y)] = []  # Cria um nó no grafo se for uma posição válida
                    vizinhos = self.obter_vizinhos([x, y])
                    # Filtra os vizinhos com apenas aqueles possíveis de se deslocar
                    vizinhos_validos = self.obter_acoes_possiveis(vizinhos)
                    # Recebe as direções de cada vizinho válido
                    direcoes = list(vizinhos_validos.keys())
                    # Para cada direção válida, adiciona a posição da casa ao grafo
                    for direcao in direcoes:
                        estado_sucessor = self.estado_sucessor(direcao, (x, y))
                        self.grafo[(x, y)].append((direcao, estado_sucessor))

        return self.buscar_rota_largura()
    
    def buscar_rota_largura(self):
        # Define o objetivo e inicio como tuplas, já que não serão alteradas
        objetivo = tuple(self.estado_objetivo)
        inicio = tuple(self.obter_estado_objeto())
        visitados = set()
        # Começa com uma string vazia pois não houve direção para chegar ao começo
        fila = [(("",inicio), [inicio])]

        while fila:
            # Remove o primeiro elemento da fila e altera o caminho para qual foi o caminho até ele
            no_atual, caminho = tuple(fila.pop(0)) 
            # no_atual[0] = direção
            # no_atual[1] = coordenadas
            if no_atual[1] == objetivo:
                # Retorna a rota formatada, a partir do caminho
                return self.obter_rota_caminho(caminho)
            elif no_atual[1] not in visitados:
                visitados.add(no_atual)
                # Percorre todos os vizinhos do no atual
                for vizinho in self.grafo[no_atual[1]]:
                    if vizinho not in visitados:
                        # Adiciona o vizinho na fila, adicionando ele mesmo ao caminho percorrido
                        fila.append((vizinho, caminho + [vizinho]))
        '''
        Fila
        A fila armazena os nós que ainda precisam ser explorados.
        Cada elemento da fila é uma tupla no formato (vizinho, caminho_até_agora), onde:
            vizinho: O próximo nó a ser visitado.
            caminho_até_agora: Uma lista que contém o caminho percorrido até chegar a esse nó.
        
        Vizinho:
        vizinho é um nó conectado ao nó atual (no_atual) no grafo.
        Ele representa uma posição no grid que pode ser alcançada a partir do nó atual.
        
        Caminho:
        caminho é a lista de nós visitados até o nó atual.
        caminho + [vizinho] cria uma nova lista que adiciona o vizinho ao final do caminho atual, representando o caminho atualizado até o próximo nó.
         '''
        return None
            
    def ir(self, direcao, nova_posicao):
        """
        Executa o movimento do agente na direção especificada.
        """
        print(f"Agente: Executando movimento {direcao}")
        self.custo_acumulado += self.CUSTOS[direcao]
        self.objeto_movel.mover(direcao, nova_posicao)

    def obter_vizinhos(self, estado_atual):
        """
        Retorna um dicionário com as direções e os valores do grid nas posições vizinhas
        a partir do estado atual do objeto_movel.
        """
        vizinhos = {}
        altura = len(self.grid)
        largura = len(self.grid[0])
        for direcao, (dx, dy) in self.objeto_movel.DIRECOES.items():
            nova_posicao = (estado_atual[0] + dx, estado_atual[1] + dy)
            # Verifica se a nova posição está dentro dos limites do grid
            if (0 <= nova_posicao[0] < altura and 
                0 <= nova_posicao[1] < largura):
                valor = self.grid[altura - 1 - nova_posicao[0]][nova_posicao[1]]
                vizinhos[direcao] = valor
            else:
                vizinhos[direcao] = None  # Fora dos limites do grid

        return vizinhos
    
    def obter_acoes_possiveis(self, vizinhos):
        """
        Retorna todos os vizinhos que estão disponíveis para se mover.
        """
        return {chave: valor for chave, valor in vizinhos.items() if valor == '⬜' or valor == '🟩'}

    def estado_sucessor(self, acao, estado):
        """
        Calcula o estado sucessor a partir da execução de uma ação em um estado.
        """
        dx, dy = self.objeto_movel.DIRECOES[acao]
        nova_posicao = (estado[0] + dx, estado[1] + dy)
        return nova_posicao

    def executar_plano(self, plano):
        for passo in plano:
            deslocamento = self.objeto_movel.DIRECOES[passo]
            nova_posicao = [x0 + x for x0, x in zip(self.obter_estado_objeto(), deslocamento)]
            self.ir(passo, nova_posicao)

    def teste_objetivo(self):
        estado = self.obter_estado_objeto()
        return estado == self.estado_objetivo

    def obter_estado_objeto(self):
        """
        Retorna o estado atual do objeto móvel.
        """
        return self.objeto_movel.ler_posicao()
    
    def obter_direcoes_validas(self):
        return  self.objeto_movel.DIRECOES

    def definir_plano(self, plano):
        """
        Define o plano de ações para o agente.
        """
        self.plano = plano

    def obter_rota_caminho(self, caminho):
        """
        Analisa as direções, em ordem, utilizadas para chegar ao objetivo
        """
        caminho.pop(0) # Remove o inicio, já que o objeto já começa nele
        rota = []
        for direcao, coordenada in caminho:
            rota.append(direcao)
        # Caminho representa uma lista com tuplas da direção seguida e a coordenada a que levou. Ex: [('N', (1, 0)), ('N', (2, 0))]
        return rota

    def ciclo_de_raciocinio(self):
        """
        Executa um ciclo de raciocínio do agente.
        """
        estado_atual = self.obter_estado_objeto()
        # breakpoint()
        if self.plano:
            proxima_acao = self.plano.pop(0)
            nova_posicao = self.estado_sucessor(proxima_acao, estado_atual)
            self.ir(proxima_acao, nova_posicao)
            return True, nova_posicao
        else:
            print("Plano concluído!")
            return False, None