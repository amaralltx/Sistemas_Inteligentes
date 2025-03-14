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

    def definir_estado_objetivo(self, objetivo):
        self.estado_objetivo = objetivo

    def ir(self, direcao, nova_posicao):
        """
        Executa o movimento do agente na direção especificada.
        """
        print(f"Agente: Executando movimento {direcao}")
        self.custo_acumulado += self.CUSTOS[direcao]
        self.objeto_movel.mover(direcao, nova_posicao)

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

    def ciclo_de_raciocinio(self, vizinhos):
        """
        Executa um ciclo de raciocínio do agente.
        """

        # Obtém o estado atual
        estado_atual = self.obter_estado_objeto()


        # Obtém as ações possíveis no estado atual
        acoes_possiveis = self.obter_acoes_possiveis(vizinhos)

        # Retira a próxima ação do plano
        if self.plano:
            proxima_acao = self.plano.pop(0)
            print(f"Próxima ação: {proxima_acao}")

            # Verifica se a ação é válida
            if proxima_acao in acoes_possiveis:
                nova_posicao = self.estado_sucessor(proxima_acao, estado_atual)
                self.ir(proxima_acao, nova_posicao)
                return True, nova_posicao
            else:
                print(f"Ação inválida: {proxima_acao}")
                return False, None
        else:
            print("Plano concluído!")
            return False, None