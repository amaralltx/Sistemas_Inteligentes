class ObjetoMovel:
    """
    Classe que representa um objeto_movel no ambiente do labirinto.
    """
            # Constantes para direções
    DIRECOES = {
        "N": (1, 0),   # Norte (sobe no eixo Y)
        "NE": (1, 1),  # Nordeste
        "L": (0, 1),   # Leste (direita no eixo X)
        "SE": (-1, 1), # Sudeste
        "S": (-1, 0),  # Sul (desce no eixo Y)
        "SO": (-1, -1),# Sudoeste
        "O": (0, -1),  # Oeste (esquerda no eixo X)
        "NO": (1, -1)  # Noroeste
    }

    def __init__(self):
        """
        Inicializa o objeto_movel com a posição inicial e configurações básicas.
        """
        self.estado_incial = []
        self.estado_atual = [] # Posição atual do objeto_movel no grid
        self.historico_posicoes = []   # Histórico de movimentos do objeto_movel
        self.historico_movimentos = []
        self.posicao_objetivo = []       # Posição objetivo do objeto_movel
        self.estados_possiveis = []
        self.plano_de_acoes = []

    def definir_estado_inicial(self, posicao):
        self.estado_incial = posicao
        self.estado_atual = posicao

    def definir_objetivo(self, coordX, coordY):
        """
        Define a posição objetivo do objeto_movel.
        """
        self.posicao_objetivo = [coordX, coordY]

    def ler_posicao(self):
        """
        Retorna a posição atual do objeto_movel.
        """
        return self.posicao

    def mover(self, direcao, nova_posicao):
        """
        Movimenta o objeto_movel para a nova posição especificada.
        """
        self.historico_movimentos.append(direcao)
        self.posicao = nova_posicao
        self.historico_posicoes.append(nova_posicao)
        return True

    def obter_historico_movimentos(self):
        """
        Retorna o histórico de movimentos do objeto_movel.
        """
        return self.historico_movimentos

    def resetar_historico(self):
        """
        Reseta o histórico de movimentos do objeto_movel.
        """
        self.historico_movimentos = []

    def validar_direcao(self, direcao):
        """
        Valida se a direção especificada é válida no ambiente atual.
        """
        if direcao in self.DIRECOES:
            novo_x = self.DIRECOES[direcao][0] + self.posicao[0]
            novo_y = self.DIRECOES[direcao][1] + self.posicao[1]
            return novo_x, novo_y
        return -1
    
    def executar_plano(self, plano):
        return