class Grafo:
    # Dicionário para criar uma aresta entre o nó de saída ao nó de chegada junto
    DIRECAO_OPOSTA = {
        "N": "S",
        "S": "N",
        "L": "O",
        "O": "L",
        "NE": "SO",
        "SE": "NO",
        "NO": "SE",
        "SO": "NE",
    }

    def __init__(self):
        self.nos = {}  # Dicionário em que a chave é a coordenada e o valor o próprio nó

    def adicionar_no(self, identificador):
        if identificador not in self.nos:
            self.nos[identificador] = No(identificador)

    def adicionar_aresta(self, no_saida, no_chegada, direcao):
        if (
            no_saida in self.nos
            and no_chegada in self.nos
            and no_chegada not in self.nos[no_saida].vizinhos
        ):
            self.nos[no_saida].adicionar_vizinho(no_chegada, direcao)
            self.nos[no_chegada].adicionar_vizinho(
                no_saida, self.DIRECAO_OPOSTA[direcao]
            )

    def obter_vizinhos(self, no):
        return self.no.vizinhos if no in self.nos else []

    def exibir_grafo(self):
        """
        Exibe o grafo com seus nós, vizinhos e custos das arestas.
        """
        for identificador, no in self.nos.items():
            print(f"Nó {identificador}:")
            if no.vizinhos:
                for vizinho, (direcao, custo) in no.vizinhos.items():
                    print(f"  Vizinho: {vizinho} - Direção: {direcao}, Custo: {custo}")
            else:
                print("  Sem vizinhos.")
            print()


class No:
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

    def __init__(self, identificador):
        self.identificador = identificador
        self.vizinhos = (
            {}
        )  # Dicionário com os identificadores dos vizinhos e uma tupla de direção e custo da aresta

    def adicionar_vizinho(self, vizinho, direcao):
        if vizinho not in self.vizinhos:
            self.vizinhos[vizinho] = (direcao, self.CUSTOS[direcao])


# Utilizamos uma classe que guarda o estado atual da busca em vez de um dicionário devido ao tamanho do problema ser pequeno e por garantir uma melhor legibilidade
class EstadoBusca:
    def __init__(
        self, identificador, caminho_direcao, caminho_coordenada, custo_acumulado, heuristica
    ):
        self.identificador = identificador
        self.caminho_direcao = caminho_direcao
        self.caminho_coordenada = caminho_coordenada
        self.custo_acumulado = custo_acumulado
        self.heuristica = heuristica
        self.fatorial_de_custo = custo_acumulado + heuristica

class MinHeap:
    """Implementação de uma Min-Heap que armazena objetos da classe EstadoBusca, ordenando de modo que o elemento de menor custo acumulado sempre fica na raiz."""

    def __init__(self):
        """Inicializa a heap como uma lista vazia."""
        self.heap = []

    def heapfy_subir(self, index):
        """Move o elemento para cima até encontrar um menor que ele"""
        pai = (index - 1) // 2
        if (
            index > 0
            and self.heap[index].fatorial_de_custo < self.heap[pai].fatorial_de_custo
        ):
            # Troca o elemento com o pai se for menor
            self.heap[index], self.heap[pai] = self.heap[pai], self.heap[index]
            self.heapfy_subir(pai)  # Continua ajustando recursivamente

    def heapfy_descer(self, index):
        """Move o elemento para baixo até encontrar um maior que ele."""
        esquerda = 2 * index + 1  # Índice do filho esquerdo
        direita = 2 * index + 2  # Índice do filho direito
        menor = index  # Assume que o menor é o próprio índice atual

        # Verifica se o filho esquerdo é menor
        if (
            esquerda < len(self.heap)
            and self.heap[esquerda].fatorial_de_custo < self.heap[menor].fatorial_de_custo
        ):
            menor = esquerda
        # Verifica se o filho direito é menor
        if (
            direita < len(self.heap)
            and self.heap[direita].fatorial_de_custo < self.heap[menor].fatorial_de_custo
        ):
            menor = direita

        # Se o menor elemento não for o atual, troca e continua descendo
        if menor != index:
            self.heap[index], self.heap[menor] = self.heap[menor], self.heap[index]
            self.heapfy_descer(menor)

    def inserir(self, estado):
        """Insere um novo estado na heap e mantém a ordem mínima."""
        self.heap.append(estado)  # Adiciona no final
        self.heapfy_subir(len(self.heap) - 1)  # Ajusta a posição do novo elemento de acordo com seu custo acumulado

    def remover_min(self):
        """Remove e retorna o menor elemento da heap."""
        if not self.heap:
            return None  # Heap vazia
        if len(self.heap) == 1:
            return self.heap.pop()  # Apenas um elemento

        menor_elemento = self.heap[0]  # Menor elemento está na raiz
        self.heap[0] = self.heap.pop()  # Substitui a raiz pelo último elemento
        self.heapfy_descer(0)  # Reorganiza a heap
        return menor_elemento
