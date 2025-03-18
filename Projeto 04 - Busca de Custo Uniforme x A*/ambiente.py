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

        Parâmetros:
        - altura: Altura do grid (número de linhas).
        - largura: Largura do grid (número de colunas).

        Funcionamento:
        1. Atribui os valores de altura e largura ao ambiente.
        2. Cria um grid vazio, preenchido com o símbolo de espaço vazio ("⬜").
        3. Inverte a ordem das linhas do grid para que a coordenada (0, 0) represente a posição no canto inferior esquerdo do grid, ajustando o sistema de coordenadas para o formato desejado.
        """

        self.altura = altura
        self.largura = largura
        self.grid = [["⬜" for _ in range(largura)] for _ in range(altura)]
        self.grid.reverse()

    def exibir(self):
        """
        Exibe o grid no terminal se a altura e largura forem menores do que 20.
        """
        if self.altura <= 20 and self.largura <= 20:
            for linha in self.grid:
                print("".join(linha))
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
        Define a posição da saída no grid, caso a posição seja válida.

        Parâmetros:
        - saida: Coordenadas (x, y) onde a saída será colocada no grid.

        Funcionamento:
        1. Chama o método `validar_posicao_objetivo` para verificar se a posição da saída é válida.
        2. Se a posição for válida, atualiza o grid, colocando o símbolo da saída ("🟩") na posição indicada.
        3. Define a posição da saída e armazena essa posição como uma tupla (para garantir que não seja alterada acidentalmente).
        4. Retorna a resposta e mensagem do método de validação, indicando se a posição foi validada corretamente ou não.

        Retorno:
        - (bool): Indica se a posição da saída foi definida corretamente.
        - (str): Mensagem de erro (se houver) ou string vazia.
        """
        resposta, mensagem = self.validar_posicao_objetivo(saida)
        if resposta:
            self.grid[self.altura - 1 - saida[0]][saida[1]] = "🟩"
            self.saida = tuple(
                saida
            )  # Transforma o array em uma tupla, tuplas não alteram o valor
            return resposta, mensagem
        return resposta, mensagem

    def definir_inicio(self, estado_inicial):
        """
        Define a posição inicial do objeto móvel no grid, caso a posição seja válida.

        Parâmetros:
        - estado_inicial: Coordenadas (x, y) onde o objeto móvel será colocado no grid.

        Funcionamento:
        1. Chama o método `validar_posicao_inicio` para verificar se a posição inicial é válida.
        2. Se a posição for válida, atualiza o grid, colocando o símbolo do objeto móvel ("🟦") na posição inicial.
        3. Define a posição inicial do objeto móvel e armazena essa posição no histórico de posições.
        4. Retorna a resposta e mensagem do método de validação, que indica se a posição foi validada corretamente ou não.

        Retorno:
        - (bool): Indica se a posição inicial foi definida corretamente.
        - (str): Mensagem de erro (se houver) ou string vazia.
        """
        resposta, mensagem = self.validar_posicao_inicio(estado_inicial)
        if resposta:
            self.grid[self.altura - 1 - estado_inicial[0]][estado_inicial[1]] = "🟦"
            self.comeco = estado_inicial
            self.objeto_movel.definir_estado_inicial(estado_inicial)
            self.objeto_movel.historico_posicoes.append(estado_inicial)
            return resposta, mensagem
        return resposta, mensagem

    def adicionar_parede(self, coordenadas):
        """
        Adiciona paredes ao grid nas coordenadas fornecidas.

        Parâmetros:
        - coordenadas: Lista de tuplas contendo as coordenadas (x, y) onde as paredes serão adicionadas.

        Funcionamento:
        1. Itera sobre as coordenadas fornecidas.
        2. Para cada coordenada, verifica se está dentro dos limites da matriz (grid).
        3. Se a coordenada for válida, atualiza o grid, marcando a posição com o símbolo de parede ("⬛").
        4. Exibe o grid atualizado após a adição das paredes.
        """

        for par in coordenadas:
            if 0 <= par[0] < self.altura and 0 <= par[1] < self.largura:
                self.grid[self.altura - 1 - par[0]][par[1]] = "⬛"

        self.exibir()

    def atualizar_objeto_movel(self, nova_posicao):
        """
        Atualiza a posição de um objeto móvel dentro de um grid.

        Parâmetros:
        - nova_posicao: Tupla contendo as novas coordenadas (x, y) para a posição do objeto móvel.

        Funcionamento:
        1. Recupera as coordenadas da posição anterior do objeto móvel a partir do histórico de posições.
        2. Atualiza a posição no grid, limpando a célula anterior (definida como "⬜") e atribuindo o novo símbolo ("🟦") à célula de destino.
        3. Exibe o grid atualizado após a mudança de posição do objeto.
        4. Retorna `True` indicando que a atualização foi bem-sucedida.

        Retorno:
        - (bool): Sempre retorna `True` após atualizar a posição do objeto.
        """

        antigoX, antigoY = self.objeto_movel.historico_posicoes[-2]

        coordX, coordY = nova_posicao
        self.grid[self.altura - 1 - antigoX][antigoY] = "⬜"  # Limpa a posição antiga
        self.grid[self.altura - 1 - coordX][
            coordY
        ] = "🟦"  # Atualiza para a nova posição

        self.exibir()
        return True

    def obter_estrutura(self):
        """
        Retorna a estrutura do grid.
        """
        return self.grid

    def validar_movimento_objeto_movel(self, argumentos):
        """
        Valida se um movimento de um objeto móvel dentro de um grid é permitido.

        Parâmetros:
        - argumentos: A direção do movimento a ser validado.

        Funcionamento:
        1. Obtém a nova posição do objeto móvel chamando o método `validar_direcao(direcao)`.
        2. Caso a direção seja inválida, retorna `False` com uma mensagem de erro.
        3. Se a nova posição estiver fora dos limites do grid, retorna `False` com uma mensagem apropriada.
        4. Caso a nova posição corresponda a uma parede (representada por "⬛" no grid),
        retorna `False` informando que há um obstáculo no caminho.
        5. Se todas as verificações forem bem-sucedidas, retorna `True`, uma mensagem vazia e a nova posição.

        Retorno:
        - (bool): Indica se o movimento é válido.
        - (str): Mensagem de erro (caso o movimento seja inválido) ou string vazia.
        - (tuple ou None): Nova posição do objeto móvel, se válida, ou `None` caso contrário.
        """

        direcao = argumentos
        nova_posicao = self.objeto_movel.validar_direcao(direcao)
        if nova_posicao != False:
            if (
                0 > nova_posicao[0]
                or nova_posicao[0] >= self.altura
                or 0 > nova_posicao[1]
                or nova_posicao[1] >= self.largura
            ):
                return (
                    False,
                    "Impossível realizar um movimento para fora do grid.",
                    None,
                )
            else:
                if (
                    self.grid[self.altura - 1 - nova_posicao[0]][nova_posicao[1]]
                    == "⬛"
                ):
                    return (
                        False,
                        "Impossível realizar o movimento, obstáculo no caminho!",
                        None,
                    )

            return True, "", nova_posicao

        return False, "Impossível realiza o movimento, direção inválida.", None

    def validar_posicao_objetivo(self, estado_final):
        """
        Valida a posição de um objetivo dentro da matriz.

        Parâmetros:
        - estado_final: Coordenadas (x, y) do objetivo a ser validado.

        Funcionamento:
        1. Verifica se a coordenada x do objetivo está dentro dos limites definidos pela altura da matriz.
        2. Verifica se a coordenada y do objetivo está dentro dos limites definidos pela largura da matriz.
        3. Se qualquer uma das coordenadas estiver fora do limite da matriz, retorna `False` com uma mensagem indicando que o objetivo não pode ser colocado fora da matriz.
        4. Caso as coordenadas sejam válidas e dentro dos limites, retorna `True` e uma string vazia, indicando que a posição do objetivo é válida.

        Retorno:
        - (bool): Indica se a posição é válida ou não.
        - (str): Mensagem de erro (caso a posição seja inválida) ou string vazia.
        """
        if (
            0 > estado_final[0]
            or estado_final[0] >= self.altura
            or 0 > estado_final[1]
            or estado_final[1] >= self.largura
        ):
            return False, "O objetivo não pode ser inicializado fora da matriz"
        return True, ""

    def validar_posicao_inicio(self, estado_inicial):
        """
        Valida se a posição inicial do objeto móvel é válida dentro do grid.

        Parâmetros:
        - estado_inicial: Tupla representando a posição inicial do objeto móvel no formato (linha, coluna).

        Funcionamento:
        1. Verifica se a posição inicial está dentro dos limites do grid. Caso contrário, retorna `False` com uma mensagem de erro.
        2. Confere se a posição inicial coincide com o objetivo (🟩). Se for o caso, retorna `False` indicando que o objeto
            não pode ser inicializado nessa posição.
        3. Se todas as verificações forem bem-sucedidas, retorna `True` e uma string vazia, indicando que a posição é válida.

        Retorno:
        - (bool): `True` se a posição inicial for válida, `False` caso contrário.
        - (str): Mensagem de erro, caso aplicável, ou string vazia se a posição for válida.
        """
        if (
            0 > estado_inicial[0]
            or estado_inicial[0] >= self.altura
            or 0 > estado_inicial[1]
            or estado_inicial[1] >= self.largura
        ):
            return False, "O objeto não pode ser inicializado fora da matriz"
        # Verifica se é a mesma posição que o objetivo
        elif self.grid[self.altura - 1 - estado_inicial[0]][estado_inicial[1]] == "🟩":
            return False, "O objeto não pode ser inicializado junto à entrada"
        return True, ""

    def validar_posicao_parede(self, coordenadas):
        """
        Valida se uma parede pode ser inserida nas coordenadas fornecidas dentro do grid.

        Parâmetros:
        - coordenadas: Lista de tuplas representando as posições onde se deseja inserir uma parede.

        Funcionamento:
        1. Percorre cada coordenada fornecida.
        2. Verifica se a coordenada está dentro dos limites do grid. Caso contrário, retorna `False` com uma mensagem de erro.
        3. Checa se a posição já está ocupada pelo objetivo (🟩) ou pelo objeto móvel (🟦).
        Se estiver, retorna `False` com uma mensagem indicando que a parede não pode ser inserida nesse local.
        4. Se todas as verificações forem bem-sucedidas, retorna `True` e uma string vazia, indicando que a posição é válida.

        Retorno:
        - (bool): `True` se a parede pode ser inserida, `False` caso contrário.
        - (str): Mensagem de erro, caso aplicável, ou string vazia se a posição for válida.
        """
        for coordenada in coordenadas:
            if (
                0 > coordenada[0]
                or coordenada[0] >= self.altura
                or 0 > coordenada[1]
                or coordenada[1] >= self.largura
            ):
                return False, "A parede não pode ser inserida fora da matriz"
            # Verifica se é a mesma posição que o objetivo ou objeto
            elif (
                self.grid[self.altura - 1 - coordenada[0]][coordenada[1]] == "🟩"
                or self.grid[self.altura - 1 - coordenada[0]][coordenada[1]] == "🟦"
            ):
                return (
                    False,
                    "Não é possível inserir uma parede no objetivo ou objeto móvel",
                )
        return True, ""
    
    def resetar_ambiente(self):

        self.grid = [["⬜" for _ in range(self.largura)] for _ in range(self.altura)]
        self.grid[self.comeco[0]][self.comeco[1]] = "🟦"
        self.grid[self.saida[0]][self.saida[1]] = "🟩"
        self.grid.reverse()
        print("\nAmbiente resetado\n")
        self.exibir()
