import copy
import math
from estruturas import *


class Agente:

    CUSTOS = {
        "N": 1,
        "S": 1,
        "L": 1,
        "O": 1,
        "NE": 1.5,
        "SE": 1.5,
        "NO": 1.5,
        "SO": 1.5,
    }

    def __init__(self, objeto_movel):
        self.objeto_movel = objeto_movel
        self.estado_objetivo = []  # Objeto a ser alcançado ao executar o plano
        self.plano_coordenada = []
        self.plano_direcao = []
        self.custo_acumulado = 0
        self.grid = []
        self.grafo = Grafo()

    def definir_estado_objetivo(self, objetivo):
        """
        Define o estado objetivo para o agente.

        Parâmetros:
        - objetivo: Coordenadas (x, y) que representam o estado objetivo no grid.
        """
        self.estado_objetivo = objetivo

    def definir_grid(self, grid):
        self.grid = copy.deepcopy(grid)
        # Altera o objeto móvel e objetivo no grid para uma melhor análise
        altura = len(self.grid)
        estado_atual = self.obter_estado_objeto()
        estado_atual_x = estado_atual[0]
        estado_atual_y = estado_atual[1]
        self.grid[altura - estado_atual_x - 1][estado_atual_y] = "⬜"
        self.grid[altura - self.estado_objetivo[0] - 1][self.estado_objetivo[1]] = "⬜"
        return

    def iniciar_plano_grafo(self):
        altura = len(self.grid)
        largura = len(self.grid[0])

        for x in range(altura):
            for y in range(largura):
                estado_atual = (x, y)
                # Se a posição do grid a ser analisada é válida
                if self.grid[altura - x - 1][y] == "⬜":
                    # Cria um nó no grafo
                    self.grafo.adicionar_no((x, y))
                    # Filtra os vizinhos com apenas aqueles possíveis de se deslocar
                    vizinhos_validos = self.obter_acoes_possiveis(estado_atual)
                    # Para cada vizinho válido, adiciona o vizinho ao no
                    for direcao_vizinho in vizinhos_validos:
                        estado_sucessor = self.estado_sucessor(
                            estado_atual, direcao_vizinho
                        )
                        if estado_sucessor not in self.grafo.nos:
                            self.grafo.adicionar_no(estado_sucessor)
                        self.grafo.adicionar_aresta(
                            estado_atual, estado_sucessor, direcao_vizinho
                        )
        # self.grafo.exibir_grafo()

    def buscar_rota_uniforme(self):
        """
        Executa a busca pelo menor caminho usando uma estratégia baseada na busca de menor custo, algortimo inspirado Dijkstra
        mas apenas realiza a busca até encontrar a saída.

        Retorna:
            - Uma tupla contendo o caminho em direções e coordenadas.
            - None caso não encontre um caminho até o objetivo.
        """

        # Define o objetivo e o ponto inicial como tuplas (imutáveis para facilitar uso em dicionários)
        objetivo = tuple(self.estado_objetivo)
        inicio = tuple(self.obter_estado_objeto())

        # Dicionário para armazenar o menor custo conhecido para cada nó visitado
        custo_minimo = {inicio: 0}

        # Fila de prioridade (MinHeap) para explorar os nós com menor custo primeiro
        heap = MinHeap()

        # Adiciona o estado inicial à heap com custo 0, caminho de direções vazio, caminho de coordenada com o próprio nó e 0 pois não tem heuristica
        heap.inserir(EstadoBusca(inicio, [], [inicio], 0, 0))

        contador = 0  # Contador para verificar quantos passos foram dados

        while heap:
            # Remove o nó com menor custo da heap (garante que expandimos o caminho mais barato primeiro)
            no_atual = heap.remover_min()

            # Se o nó atual for o objetivo, retornamos o caminho encontrado
            if no_atual.identificador == objetivo:
                return no_atual.caminho_direcao, no_atual.caminho_coordenada, contador

            # Explora os vizinhos do nó atual
            for identificador, (direcao, custo_vizinho) in self.grafo.nos[
                no_atual.identificador
            ].vizinhos.items():
                # Calcula o custo total para alcançar este vizinho a partir do nó atual
                custo_total = no_atual.custo_acumulado + custo_vizinho

                # Se o vizinho ainda não foi visitado ou encontramos um caminho mais barato até ele
                if (
                    identificador not in custo_minimo
                    or custo_total < custo_minimo[identificador]
                ):
                    # Atualiza o custo mínimo necessário para chegar até este vizinho
                    custo_minimo[identificador] = custo_total

                    # Constrói os caminhos de direção e coordenadas para este novo estado
                    novo_caminho_direcao = no_atual.caminho_direcao + [direcao]
                    novo_caminho_coordenadas = no_atual.caminho_coordenada + [
                        identificador
                    ]

                    # Insere o novo estado na heap para ser processado futuramente
                    heap.inserir(
                        EstadoBusca(
                            identificador,
                            novo_caminho_direcao,
                            novo_caminho_coordenadas,
                            custo_total,
                            0,
                        )
                    )
                contador = contador + 1

        # Se a heap esvaziar sem encontrar o objetivo, significa que não há caminho possível
        print("Objetivo não encontrado!")
        return None

    def buscar_rota_a_estrela(self):
        """
        Executa a busca pelo menor caminho usando o algoritmo A*.
        O A* busca o caminho de menor custo, utilizando a soma do custo atual do caminho mais a heurística, que estima o custo restante até o objetivo.

        Retorna:
            - Uma tupla contendo o caminho em direções e coordenadas.
            - None caso não encontre um caminho até o objetivo.
        """

        # Define o objetivo e o ponto inicial como tuplas (imutáveis para facilitar uso em dicionários)
        objetivo = tuple(self.estado_objetivo)
        inicio = tuple(self.obter_estado_objeto())

        # Dicionário para armazenar o menor custo conhecido para cada nó visitado
        custo_minimo = {inicio: 0}

        # Fila de prioridade (MinHeap) para explorar os nós com menor f(n) primeiro
        heap = MinHeap()

        # Calcula a heurística do estado inicial
        heuristica_inicial = self.calcular_heuristica(inicio, objetivo)

        # Adiciona o estado inicial à heap com custo 0, caminho de direções vazio, caminho de coordenada com o próprio nó e a f_inicial
        heap.inserir(EstadoBusca(inicio, [], [inicio], 0, heuristica_inicial))

        contador = 0  # Contador para verificar quantos passos foram dados

        while heap:
            # Remove o nó com menor f(n) da heap
            no_atual = heap.remover_min()

            # Se o nó atual for o objetivo, retornamos o caminho encontrado
            if no_atual.identificador == objetivo:
                return no_atual.caminho_direcao, no_atual.caminho_coordenada, contador
            
            # Explora os vizinhos do nó atual
            for identificador, (direcao, custo_vizinho) in self.grafo.nos[no_atual.identificador].vizinhos.items():
                # Calcula o custo total para alcançar este vizinho a partir do nó atual
                custo_total = no_atual.custo_acumulado + custo_vizinho

                # Calcula a heurística do vizinho
                heuristica_vizinho = self.calcular_heuristica(identificador, objetivo)

                # Se o vizinho ainda não foi visitado OU encontramos um caminho mais barato até ele
                if (
                    identificador not in custo_minimo
                    or custo_total < custo_minimo[identificador]
                ):
                    # Atualiza o custo mínimo necessário para chegar até este vizinho
                    custo_minimo[identificador] = custo_total

                    # Constrói os caminhos de direção e coordenadas para este novo estado
                    novo_caminho_direcao = no_atual.caminho_direcao + [direcao]
                    novo_caminho_coordenadas = no_atual.caminho_coordenada + [
                        identificador
                    ]

                    # Insere o novo estado na heap para ser processado futuramente
                    heap.inserir(
                        EstadoBusca(
                            identificador,
                            novo_caminho_direcao,
                            novo_caminho_coordenadas,
                            custo_total,
                            heuristica_vizinho,
                        )
                    )
                contador = contador + 1

        # Se a heap esvaziar sem encontrar o objetivo, significa que não há caminho possível
        print("Objetivo não encontrado!")
        return None

    def calcular_heuristica(self, estado_atual, objetivo):
        """
        Calcula a heurística baseada na distância Euclidiana e na de Chebyshev entre o estado atual e o objetivo, retornando
        a maior entre as duas.

        A distância de Chebyshev é o máximo das diferenças absolutas nas coordenadas x e y dos dois pontos.
        Esse valor representa o número mínimo de movimentos necessários para mover de um ponto ao outro,
        considerando que o agente pode se mover diagonalmente e que um movimento na diagonal nada mais é
        do que a soma de um movimento na vertical com um na horizontal. A heurística por si só é otimista quando
        no labirinto, mas ao ser utilizada junto com custo de deslocamento até o estado atual, resulta em uma solução ótima

        Args:
            estado_atual: O identificador (tupla de coordenadas) do estado atual.
            objetivo: O identificador (tupla de coordenadas) do estado objetivo.

        Returns:
            A distância (heuristica) entre o estado atual e o objetivo.
        """
        x_atual, y_atual = estado_atual
        x_objetivo, y_objetivo = objetivo
        h_chebyshev = max(abs(x_atual - x_objetivo), abs(y_atual - y_objetivo))
        h_euclidiana = int(
            math.sqrt((x_objetivo - x_atual) ** 2 + (y_objetivo - y_atual) ** 2)
        )
        return max(h_chebyshev, h_euclidiana)

    def ir(self, direcao, nova_posicao):
        """
        Executa o movimento do agente na direção especificada.
        """
        self.custo_acumulado += self.CUSTOS[direcao]
        self.objeto_movel.mover(direcao, nova_posicao)

    def obter_acoes_possiveis(self, estado_atual):
        """
        Retorna todos os vizinhos que estão disponíveis para se mover.
        Verifica se a nova posição está dentro dos limites e se a célula
        é acessível (⬜ ou 🟩).

        Parâmetros:
        - estado_atual: Tupla com as coordenadas (x, y) atuais do objeto.

        Retorno:
        - dicionário de vizinhos acessíveis, onde a chave é a posição (x, y)
        e o valor é a direção.
        """
        vizinhos = []
        altura = len(self.grid)
        largura = len(self.grid[0])

        for direcao, (dx, dy) in self.objeto_movel.DIRECOES.items():
            nova_posicao = (estado_atual[0] + dx, estado_atual[1] + dy)

            # Verificar se a nova posição está dentro dos limites do grid
            if 0 <= nova_posicao[0] < altura and 0 <= nova_posicao[1] < largura:
                valor = self.grid[altura - 1 - nova_posicao[0]][nova_posicao[1]]

                # Verificar se a célula é vazia ou se é a célula de saída
                if valor == "⬜" or valor == "🟩":
                    vizinhos.append(
                        direcao
                    )  # Adiciona apenas a direção de vizinhos válidos

        return vizinhos

    def estado_sucessor(self, estado_atual, acao):
        """
        Calcula o estado sucessor a partir da execução de uma ação em um estado.
        """
        dx, dy = self.objeto_movel.DIRECOES[acao]
        nova_posicao = (estado_atual[0] + dx, estado_atual[1] + dy)
        return nova_posicao

    def executar_plano(self, plano):
        for passo in plano:
            deslocamento = self.objeto_movel.DIRECOES[passo]
            nova_posicao = [
                x0 + x for x0, x in zip(self.obter_estado_objeto(), deslocamento)
            ]
            self.ir(passo, nova_posicao)

    def teste_objetivo(self):
        estado = self.obter_estado_objeto()
        return estado == tuple(self.estado_objetivo)

    def obter_estado_objeto(self):
        """
        Retorna o estado atual do objeto móvel.
        """
        return self.objeto_movel.ler_posicao()

    def obter_direcoes_validas(self):
        return self.objeto_movel.DIRECOES

    def definir_plano(self, plano_direcao, plano_coordenada):
        """
        Define o plano de ações para o agente.
        """
        plano_coordenada.pop(0)  # Remove a coordenada inicial
        self.plano_direcao = plano_direcao
        self.plano_coordenada = plano_coordenada

    def obter_rota_caminho(self, caminho):
        """
        Analisa as direções, em ordem, utilizadas para chegar ao objetivo
        """
        caminho.pop(0)  # Remove o inicio, já que o objeto já começa nele
        rota = []
        for direcao, coordenada in caminho:
            rota.append(direcao)
        # Caminho representa uma lista com tuplas da direção seguida e a coordenada a que levou. Ex: [('N', (1, 0)), ('N', (2, 0))]
        return rota

    def ciclo_de_raciocinio(self):
        """
        Executa um ciclo de raciocínio do agente.
        """
        if self.plano_direcao:
            proxima_acao = self.plano_direcao.pop(0)
            nova_posicao = self.plano_coordenada.pop(0)
            self.ir(proxima_acao, nova_posicao)
            return True, nova_posicao
        else:
            print("Plano concluído!")
            return False, None

    def resetar_agente(self, grid, estado_inicial):
        self.plano_coordenada = []
        self.plano_direcao = []
        self.custo_acumulado = 0
        self.grafo = Grafo()
        self.objeto_movel.estado_atual = estado_inicial 
        self.objeto_movel.historico_posicoes = [estado_inicial] 
        self.objeto_movel.historico_movimentos = []
        self.definir_grid(grid)