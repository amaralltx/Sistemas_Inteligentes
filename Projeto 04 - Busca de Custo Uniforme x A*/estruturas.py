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

# Dicionário para criar uma aresta entre o nó de saída ao nó de chegada junto
DIRECAO_OPOSTA = {
    "N": "S",
    "S": "N",
    "L": "O",
    "O": "L",
    "NE": "SE",
    "SE": "NE",
    "NO": "SO",
    "SO": "NO",
}
class Grafo:
    def __init__(self):
        self.nos = {} # Dicionário em que a chave é a coordenada e o valor o próprio nó
    
    def adicionar_no(self, identificador):
        if identificador not in self.nos:
            self.nos[identificador] = No(identificador)

    def adicionar_aresta(self, no_saida, no_chegada, direcao):
        if (no_saida in self.nos and 
            no_chegada in self.nos and 
            no_chegada not in self.nos[no_saida].vizinhos):
            self.nos[no_saida].adicionar_vizinho(no_chegada, direcao)
            self.nos[no_chegada].adicionar_vizinho(no_saida, DIRECAO_OPOSTA[direcao])
    
    def obter_vizinhos(self, no):
        return self.no.vizinhos if no in self.nos else []
    
    def obter_custo_total(self, no):
        return self.no.custo_total if no in self.nos else []
    
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
    def __init__(self, identificador):
        self.identificador = identificador
        self.vizinhos = {} # Dicionário com os identificadores dos vizinhos e uma tupla de direção e custo da aresta
        self.caminho = [] # caminho percorrido até chegar ao nó
        self.custo_total = float('inf') # custo total até chegar ao nó
        self.visitado = False # validador para quando o nó for visitado não ser adicionado novamente à fila
    
    def adicionar_vizinho(self, vizinho, direcao):
        if vizinho not in self.vizinhos:
            self.vizinhos[vizinho] = (direcao, CUSTOS[direcao])

    def obter_custo(self, vizinho):
        return self.vizinhos.get(vizinho, (None, None))