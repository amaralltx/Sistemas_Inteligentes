class Ambiente:
    """
    Classe que representa o ambiente do labirinto.
    """
    def __init__(self, objeto):
        """
        Inicializa os atributos do ambiente.
        """
        self.altura = 0
        self.largura = 0
        self.saida = ()
        self.comeco = None
        self.grid = []
        self.objeto_movel = objeto
        self.plano = []

    def iniciar_ambiente(self, altura, largura):
        """
        Define a altura e largura do ambiente e inicializa o grid.
        """
        self.altura = altura
        self.largura = largura
        self.grid = [['⬜' for _ in range(largura)] for _ in range(altura)]
        self.grid.reverse()  # Inverte a ordem das linhas para que (0, 0) seja a casa da esquerda embaixo

    def exibir(self):
        """
        Exibe o grid no terminal.
        """
        for linha in self.grid:
            print(''.join(linha))
        print("\n")

    def definir_altura(self, altura):
        """
        Define a altura do ambiente se estiver no intervalo permitido.
        """
        if 3 <= altura <= 50:
            self.altura = altura
            return 0
        return -1

    def definir_largura(self, largura):
        """
        Define a largura do ambiente se estiver no intervalo permitido.
        """
        if 3 <= largura <= 50:
            self.largura = largura
            return 0
        return -1

    def definir_saida(self, saida):
        """
        Define a posição do estado final no grid se a posição for válida.
        """
        resposta, mensagem = self.validar_posicao_objetivo(saida)
        if resposta:
            self.grid[self.altura - 1 - saida[0]][saida[1]] = '🟩'
            self.saida = tuple(saida)  # Transforma o array em uma tupla, tuplas não alteram o valor
            return resposta, mensagem
        return resposta, mensagem

    def definir_inicio(self, estado_inicial):
        """
        Define a posição inicial do objeto_movel no grid se a posição for válida.
        """
        resposta, mensagem = self.validar_posicao_inicio(estado_inicial)
        if resposta:
            self.grid[self.altura - 1 - estado_inicial[0]][estado_inicial[1]] = '🟦'
            self.comeco = estado_inicial
            self.objeto_movel.definir_estado_inicial(estado_inicial)
            self.objeto_movel.historico_posicoes.append(estado_inicial)
            return resposta, mensagem
        return resposta, mensagem

    def adicionar_parede(self, coordenadas):
        """
        Adiciona paredes no grid nas coordenadas fornecidas.
        """
        for par in coordenadas:
            if 0 <= par[0] < self.altura and 0 <= par[1] < self.largura:
                self.grid[self.altura - 1 - par[0]][par[1]] = '⬛'
        
        self.exibir()

    def atualizar_objeto_movel(self, nova_posicao):
        """
        Atualiza o objeto_movel no ambiente.
        """
        # Libera a posição anterior do objeto no grid 
        antigoX, antigoY = self.objeto_movel.historico_posicoes[-2]

        # Novas coordenadas do objeto
        coordX, coordY = nova_posicao
        self.grid[self.altura - 1 - antigoX][antigoY] = '⬜'  # Limpa a posição antiga
        self.grid[self.altura - 1 - coordX][coordY] = '🟦'  # Atualiza para a nova posição

        # Exibe o novo grid
        self.exibir()
        return True

    def obter_estrutura(self):
        """
        Retorna a estrutura do grid.
        """
        return self.grid

    def validar_movimento_objeto_movel(self, argumentos):
        # Checa com o objeto_movel se é uma direção válida dentre as possiveis
        direcao = argumentos
        nova_posicao = self.objeto_movel.validar_direcao(direcao)
        if nova_posicao != False:
            # Verifica se a nova posição está fora dos limites do grid
            if 0 > nova_posicao[0] or nova_posicao[0]>= self.altura or 0 > nova_posicao[1] or nova_posicao[1] >= self.largura:
                return False, "Impossível realizar um movimento para fora do grid", None
            else:
                # Verifica se a nova posição é uma parede
                if self.grid[self.altura - 1 - nova_posicao[0]][nova_posicao[1]] == '⬛':
                    return False, "Impossível realizar o movimento, obstáculo no caminho!", None
                
        return True, "", nova_posicao

         
         
    def validar_posicao_objetivo(self, estado_final):
        if 0 > estado_final[0] or estado_final[0]>= self.altura or 0 > estado_final[1] or estado_final[1] >= self.largura:
                return False, "O objetivo não pode ser inicializado fora da matriz"
        return True, ""
    
    def validar_posicao_inicio(self, estado_inicial):
        if 0 > estado_inicial[0] or estado_inicial[0]>= self.altura or 0 > estado_inicial[1] or estado_inicial[1] >= self.largura:
                return False, "O objeto não pode ser inicializado fora da matriz"
        # Verifica se é a mesma posição que o objetivo
        elif self.grid[self.altura - 1 - estado_inicial[0]][estado_inicial[1]] == '🟩':
                return False, "O objeto não pode ser inicializado junto à entrada"
        return True, ""
    
    def validar_posicao_parede(self, coordenadas):
        for coordenada in coordenadas:
            if 0 > coordenada[0] or coordenada[0]>= self.altura or 0 > coordenada[1] or coordenada[1] >= self.largura:
                    return False, "A parede não pode ser inserida fora da matriz"
            # Verifica se é a mesma posição que o objetivo ou objeto
            elif self.grid[self.altura - 1 - coordenada[0]][coordenada[1]] == '🟩' or self.grid[self.altura - 1 - coordenada[0]][coordenada[1]] == '🟦':
                    return False, "Não é possível inserir uma parede no objetivo ou objeto móvel"
        return True, ""
    
    def obter_vizinhos(self, estado_atual):
        """
        Retorna um dicionário com as direções e os valores do grid nas posições vizinhas
        a partir do estado atual do objeto_movel.
        """
        vizinhos = {}

        for direcao, (dx, dy) in self.objeto_movel.DIRECOES.items():
            nova_posicao = (estado_atual[0] + dx, estado_atual[1] + dy)
            # Verifica se a nova posição está dentro dos limites do grid
            if 0 <= nova_posicao[0] < self.altura and 0 <= nova_posicao[1] < self.largura:
                valor = self.grid[self.altura - 1 - nova_posicao[0]][nova_posicao[1]]
                vizinhos[direcao] = valor
            else:
                vizinhos[direcao] = None  # Fora dos limites do grid

        return vizinhos
