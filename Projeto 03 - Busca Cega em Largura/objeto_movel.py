class ObjetoMovel:
    """
    Classe que representa um objeto_movel no ambiente do labirinto.
    """
    # Constantes de dicionário para direções já que nesse caso qualquer objeto iria para as mesmas direções
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
        self.estado_inicial = []
        self.estado_atual = [] # Posição atual do objeto_movel no grid
        self.historico_posicoes = []   # Histórico de movimentos do objeto_movel
        self.historico_movimentos = []

    def definir_estado_inicial(self, posicao):
        self.estado_inicial = posicao
        self.estado_atual = posicao

    def ler_posicao(self):
        """
        Retorna a posição atual do objeto_movel.
        """
        return self.estado_atual

    def mover(self, direcao, deslocamento):
        """
        Movimenta o objeto_movel para a nova posição especificada.
        """
        self.estado_atual = deslocamento
        self.historico_movimentos.append(direcao)
        self.historico_posicoes.append(self.estado_atual)


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
            novo_x = self.DIRECOES[direcao][0] + self.estado_atual[0]
            novo_y = self.DIRECOES[direcao][1] + self.estado_atual[1]
            return novo_x, novo_y
        return False
    