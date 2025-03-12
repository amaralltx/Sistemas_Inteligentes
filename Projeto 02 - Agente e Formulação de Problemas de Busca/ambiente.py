from objeto_movel import ObjetoMovel

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
        Define a posição da saída no grid se a posição for válida.
        """
        resposta, mensagem = self.validar_posicao_elemento([saida], "saida")
        if resposta:
            self.grid[self.altura - 1 - saida[0]][saida[1]] = '🟩'
            self.saida = tuple(saida)  # Transforma o array em uma tupla, tuplas não alteram o valor
            return resposta, mensagem
        return resposta, mensagem

    def definir_inicio(self, estado_inicial):
        """
        Define a posição inicial do objeto_movel no grid se a posição for válida.
        """
        resposta, mensagem = self.validar_posicao_elemento([estado_inicial], "inicio")
        if resposta:
            self.grid[self.altura - 1 - estado_inicial[0]][estado_inicial[1]] = '🟦'
            self.comeco = estado_inicial
            self.objeto_movel.posicao= estado_inicial
            self.objeto_movel.estado_inicial = estado_inicial
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

    # TODO essa função e a validar_movimento_objeto_movel são muito feias, separar uma função para cada ocasião para melhor entendimento do código
    def validar_posicao_elemento(self, argumentos, elemento):
        """
        Valida se a posição fornecida é válida para o elemento especificado.
        """
        if elemento == "objeto_movel":
            validador, nova_posicao = self.validar_movimento_objeto_movel(argumentos)
            if validador == True:
                return True, "Sem erro", nova_posicao 
            else:
                return False, "Impossível realizar o movimento", None
        else:
            # Para cada posição a ser validada...
            for posicao in argumentos:
                # Verifica se a posição está fora dos limites do grid
                if posicao[0] < 0 or posicao[0] >= self.altura or posicao[1] < 0 or posicao[1] >= self.largura:
                    return False, "Posição não pertence à Matriz"
                # Se for uma parede, a chegada não é uma posição válida
                if elemento == "parede" and (self.grid[self.altura - 1 - posicao[0]][posicao[1]] == '🟩' or self.grid[self.altura - 1 - posicao[0]][posicao[1]] == '🟦'):
                    return False, "Não é possível adicionar uma parede no objeto_movel ou objetivo\n"
            return True, "Sem erro"
    
    def validar_movimento_objeto_movel(self, argumentos):
        # Checa com o objeto_movel se é uma direção válida dentre as possiveis
        nova_posicao = self.objeto_movel.validar_direcao(argumentos)
        if nova_posicao != -1:
            # Verifica se a nova posição está fora dos limites do grid
            if 0 > nova_posicao[0] or nova_posicao[0]>= self.altura or 0 > nova_posicao[1] or nova_posicao[1] >= self.largura:
                return False, -1
            else:
                # Verifica se a nova posição é uma parede
                if self.grid[self.altura - 1 - nova_posicao[0]][nova_posicao[1]] == '⬛':
                    return False, -1
                
        return True, nova_posicao

    def verifica_estado(self):
        """
        Verifica se o objeto_movel chegou ao destino.
        """
        if self.saida == self.objeto_movel.ler_posicao():
            return "chegou ao destino"
    
    def obter_posicao_objeto_movel(self):
        return self.objeto_movel.ler_posicao()