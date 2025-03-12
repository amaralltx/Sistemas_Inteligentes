from customtkinter import *
from CTkMessagebox import *
from PIL import Image, ImageTk
from re import *
from time import *

class Interface:
    """
    Classe que representa a interface gráfica do labirinto.
    """
    def __init__(self, janela, ambiente, agente):
        """
        Inicializa a interface gráfica.
        """
        self.janela = janela
        self.janela.title("Labirinto")
        self.janela.geometry("750x850")
        self.janela.resizable(False, False)
        self.janela.option_add("*Font", ("Montserrrat", 18))
        self.fonte = ("Montserrrat", 14)

        # Obter as dimensões da tela
        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()
        
        # Calcular a posição central
        pos_x = (largura_tela // 2) - (750 // 2)
        pos_y = (altura_tela // 2) - (850 // 2)
        
        # Definir a geometria da janela com a posição central
        self.janela.geometry(f"{750}x{850}+{pos_x}+{pos_y}")

        # Configurar as linhas e colunas
        self.janela.grid_rowconfigure(0, weight=1)
        self.janela.grid_rowconfigure(1, weight=0)
        self.janela.grid_columnconfigure(0, weight=1)

        # Cores
        self.branco = "#D9D9D9"
        self.preto = "#343638"

        self.ambiente = ambiente
        self.agente = agente

        # Criando os frames para as áreas
        self.frame_labirinto = CTkFrame(self.janela, width=750, height=750, bg_color=self.branco, fg_color=self.branco, corner_radius=0)
        self.frame_input_inicial = CTkFrame(self.janela, width=750, height=100, fg_color=self.preto)
        self.frame_input_principal = CTkFrame(self.janela)

        # Posicionando os frames na grade
        self.frame_labirinto.grid(row=0, column=0, sticky="nsew")
        self.frame_input_inicial.grid(row=1, column=0, sticky="nsew")

        # Mantendo os tamanhos definidos
        self.frame_labirinto.grid_propagate(False)
        self.frame_input_inicial.grid_propagate(False)
    
        self.inicializa_frame_input_inicial()
        self.configurar_bind_enter()

        # Criando dicionário para os comandos disponíveis
        self.comandos_disponiveis = {
            "IR": self.validar_mover_objeto_movel,
            "PAREDE": self.validar_adicionar_parede,
            # lambda args: para garantir que a chamada comandos_disponiveis[comando](argumentos) funcione sem argumentos
            "LERPOS": lambda args: self.exibir_mensagem(
                f"Coordenada X: {self.ambiente.obter_posicao_objeto_movel()[0]}\n"
                f"Coordenada Y: {self.ambiente.obter_posicao_objeto_movel()[1]}"
            ),
            "ANALISAR" : lambda args: self.exibir_analise(),
            "HISTORICO" : lambda args: self.exibir_mensagem(f"Movimentos: {self.agente.objeto_movel.historico_movimentos}\nCusto: {self.agente.custo_acumulado}"),
            "PLANO" : self.validar_executar_plano,
        }
    def inicializa_frame_input_inicial(self):
        """
        Inicializa o frame de entrada inicial.
        """
        self.frame_input_inicial_direita = CTkFrame(self.frame_input_inicial, width=300, height=100, fg_color="transparent")
        self.frame_input_inicial_esquerda = CTkFrame(self.frame_input_inicial, width=450, height=100, fg_color="transparent")

        self.frame_input_inicial_esquerda.grid(row=0, column=0, sticky="nsew")
        self.frame_input_inicial_direita.grid(row=0, column=1, sticky="nsew")

        self.frame_input_inicial_direita.grid_propagate(False)
        self.frame_input_inicial_esquerda.grid_propagate(False)

        # Configurando colunas para centralizar elementos
        self.frame_input_inicial_esquerda.grid_columnconfigure(0, weight=1)
        self.frame_input_inicial_esquerda.grid_columnconfigure(1, weight=1)
        self.frame_input_inicial_esquerda.grid_columnconfigure(2, weight=1)
        self.frame_input_inicial_esquerda.grid_columnconfigure(3, weight=1)
        self.frame_input_inicial_esquerda.grid_rowconfigure(0, weight=1)
        self.frame_input_inicial_esquerda.grid_rowconfigure(1, weight=1)
        self.frame_input_inicial_direita.grid_columnconfigure(0, weight=1)
        self.frame_input_inicial_direita.grid_rowconfigure(0, weight=1)
        
        self.label_altura = CTkLabel(self.frame_input_inicial_esquerda, text="Altura", text_color=self.branco, font=self.fonte)
        self.label_altura.grid(row=0, column=0, padx=(25, 10), sticky="nsw", pady=(0,0))
        self.input_altura = CTkEntry(self.frame_input_inicial_esquerda , placeholder_text="20", fg_color=self.branco, text_color=self.preto)
        self.input_altura.grid(row=1, column=0, padx=(25, 10), pady=(0,20), sticky="nsew")

        self.label_largura = CTkLabel(self.frame_input_inicial_esquerda, text="Largura", text_color=self.branco, font=self.fonte)
        self.label_largura.grid(row=0, column=1, padx=10, sticky="nsw", pady=(0,0))
        self.input_largura = CTkEntry(self.frame_input_inicial_esquerda, placeholder_text="25", fg_color=self.branco, text_color=self.preto)
        self.input_largura.grid(row=1, column=1, padx=10, pady=(0,20), sticky="nsew")

        self.label_saida = CTkLabel(self.frame_input_inicial_esquerda, text="Saida", text_color=self.branco, font=self.fonte)
        self.label_saida.grid(row=0, column=2, padx=10, sticky="nsw", pady=(0,0))
        self.input_saida = CTkEntry(self.frame_input_inicial_esquerda, placeholder_text="0,15", fg_color=self.branco, text_color=self.preto)
        self.input_saida.grid(row=1, column=2, padx=10, pady=(0,20), sticky="nsew")

        self.label_comeco = CTkLabel(self.frame_input_inicial_esquerda, text="Começo", text_color=self.branco, font=self.fonte)
        self.label_comeco.grid(row=0, column=3, padx=10, sticky="nsw", pady=(0,0))
        self.input_comeco = CTkEntry(self.frame_input_inicial_esquerda, placeholder_text="0,0", fg_color=self.branco, text_color=self.preto)
        self.input_comeco.grid(row=1, column=3, padx=10, pady=(0,20), sticky="nsew")

        self.botao_enviar = CTkButton(self.frame_input_inicial_direita, text="CRIAR", command=self.criar_ambiente)
        self.botao_enviar.grid(row=0, column=0, padx=(10,25), pady=15, sticky="nsew")

    def configurar_bind_enter(self):
        """
        Configura o bind da tecla Enter para os widgets de entrada.
        """
        self.input_altura.bind('<Return>', lambda event: self.criar_ambiente())
        self.input_largura.bind('<Return>', lambda event: self.criar_ambiente())
        self.input_saida.bind('<Return>', lambda event: self.criar_ambiente())
        self.input_comeco.bind('<Return>', lambda event: self.criar_ambiente())
        if hasattr(self, 'input_comando'):
            self.input_comando.bind('<Return>', lambda event: self.receber_comando())
    
    def inicializa_frame_input_principal(self):
        self.frame_input_principal = CTkFrame(self.janela, width=750, height=100, fg_color=self.preto, corner_radius=0)
        # Posicionando os frames na grade
        self.frame_input_principal.grid(row=1, column=0, sticky="nsew", pady=0)
        # Mantendo os tamanhos definidos
        self.frame_input_principal.grid_propagate(False)

        # Configurando colunas e linhas para centralizar o input
        self.frame_input_principal.grid_columnconfigure(0, weight=1)
        self.frame_input_principal.grid_columnconfigure(1, weight=0)
        self.frame_input_principal.grid_columnconfigure(1, weight=0)
        self.frame_input_principal.grid_rowconfigure(0, weight=1)

        # Adicionando um input de texto centralizado
        self.input_comando = CTkEntry(self.frame_input_principal, placeholder_text="Digite um comando...", fg_color=self.branco, text_color=self.preto)
        self.input_comando.grid(row=0, column=0, padx=(20,0), pady=15, sticky="nsew", ipadx=10, ipady=10)
        self.input_comando.bind('<Return>', lambda event: self.receber_comando())
        # Adicionando caixa de texto 
        self.caixa_texto = CTkTextbox(self.frame_input_principal, state="disable", width=350)
        self.caixa_texto.grid(row=0, column=1, padx=(10, 0), pady=15, sticky="nsew")
        self.caixa_texto.tag_add("center", "1.0", "end")

        # Adicionando um botão flutuante
        self.botao_modal = CTkButton(self.frame_input_principal, text="Mostrar Comandos", command=self.abrir_modal)
        self.botao_modal.grid(row=0, column=2, padx=(10,20), pady=15, sticky="nsew")

        return

    def abrir_modal(self):
        # Criando uma nova janela modal
        self.modal = CTkToplevel(self.janela)
        self.modal.title("Comandos")
        self.modal.geometry("500x300")  # Aumentando o tamanho da modal

        self.modal.grid_columnconfigure(0, weight=1)
        self.modal.grid_rowconfigure(0, weight=2)
        self.modal.grid_rowconfigure(1, weight=1)

        # Adicionando conteúdo à modal
        msg = "Ir X: move o objeto_movel na direção X\nX ∈ {N, S, L, O, NO, NE, SE, SO}\n\nLerpos: retorna a posição que o objeto_movel se encontra\n\nParede x1,y1 x2,y2 ... xn,yn: insere parede nas coordenadas fornecidas"
        label_modal = CTkLabel(self.modal, text=msg, wraplength=480)
        label_modal.grid(row=0, column=0, sticky="nsew", pady=(25,0), padx=10)

        botao_fechar = CTkButton(self.modal, text="Fechar", width=150, height=50, command=self.modal.destroy)
        botao_fechar.grid(row=1, column=0, sticky="ns", pady=25, padx=10)

    def criar_ambiente(self):
        """
        Coleta as entradas do usuário e cria o ambiente.
        """
        try:
            altura = int(self.input_altura.get())
            largura = int(self.input_largura.get())
            if self.ambiente.definir_altura(altura) == -1:
                CTkMessagebox(title="Erro", message="Altura válida: 3 a 50")
                return
            if self.ambiente.definir_largura(largura) == -1:
                CTkMessagebox(title="Erro", message="Largura válida: 3 a 50")
                return
            
            self.ambiente.iniciar_ambiente(altura, largura)

            saidas = self.input_saida.get()
            saidaX, saidaY = map(int, saidas.split(","))
            saida = [saidaX, saidaY]
            validador, mensagem = self.ambiente.definir_saida(saida) 
            if not validador:
                CTkMessagebox(title="Erro", message=mensagem)
                return

            posicao_inicial = self.input_comeco.get()
            comecoX, comecoY = map(int, posicao_inicial.split(","))
            posicao_inicial = [comecoX, comecoY]
            validador, mensagem = self.ambiente.definir_inicio(posicao_inicial) 
            if not validador:
                CTkMessagebox(title="Erro", message=mensagem)
                return

            self.ambiente.exibir()
        except ValueError:
            self.exibir_mensagem("Entrada inválida.\nAltura: inteiro entre 3 e 50\nLargura: inteiro entre 3 e 50\nSaída: dois inteiros separados por vírgula.")
            return
        self.mostrar_labirinto()
        self.alternar_widgets()
    
    def mostrar_labirinto(self):
        """
        Configura e exibe o labirinto no canvas.
        """
        # Configurando colunas e linhas para centralizar o canvas
        self.frame_labirinto.grid_columnconfigure(0, weight=1)
        self.frame_labirinto.grid_columnconfigure(1, weight=1)
        self.frame_labirinto.grid_rowconfigure(0, weight=1)
        self.frame_labirinto.grid_rowconfigure(1, weight=1)
        self.frame_labirinto.configure(fg_color="#343630")

        # Criando o canvas no frame_labirinto
        self.canvas_labirinto = CTkCanvas(self.frame_labirinto, width=710, height=710)
        self.canvas_labirinto.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Definindo a altura e largura do labirinto
        altura = self.ambiente.altura
        largura = self.ambiente.largura

        # Calculando o tamanho das células do labirinto
        largura_celula = 710 / largura
        altura_celula = 710 / altura 

        # Carregando a imagem da saída
        self.imagem_saida = Image.open("images/chegada.png")
        self.imagem_saida = self.imagem_saida.resize((int(largura_celula), int(altura_celula)), Image.Resampling.LANCZOS)
        self.imagem_saida_tk = ImageTk.PhotoImage(self.imagem_saida)
        # Carregando a imagem do objeto_movel
        self.imagem_objeto_movel = Image.open("images/explorador.png")
        self.imagem_objeto_movel = self.imagem_objeto_movel.resize((int(largura_celula), int(altura_celula)), Image.Resampling.LANCZOS)
        self.imagem_objeto_movel_tk = ImageTk.PhotoImage(self.imagem_objeto_movel)

        # Obtendo a estrutura do labirinto do ambiente
        estrutura_labirinto = self.ambiente.obter_estrutura()

        # Preenchendo o canvas com retângulos representando o labirinto
        for i in range(altura):
            for j in range(largura):
                x0 = j * largura_celula
                y0 = i * altura_celula 
                x1 = x0 + largura_celula
                y1 = y0 + altura_celula
                if estrutura_labirinto[i][j] == '⬛':  # '⬛' representa uma parede
                    cor = self.preto
                    self.canvas_labirinto.create_rectangle(x0, y0, x1, y1, outline="#C1C1C1", fill=cor)
                elif estrutura_labirinto[i][j] == '🟩':  # '🟩' representa a saída
                    cor = self.branco
                    self.canvas_labirinto.create_rectangle(x0, y0, x1, y1, outline="#C1C1C1", fill=cor)
                    self.imagem_saida = self.canvas_labirinto.create_image(x0, y0, anchor="nw", image=self.imagem_saida_tk)
                elif estrutura_labirinto[i][j] == '🟦':  # '🟦' representa o objeto_movel explorador
                    cor = self.branco
                    self.canvas_labirinto.create_rectangle(x0, y0, x1, y1, outline="#C1C1C1", fill=cor)
                    self.imagem_objeto_movel = self.canvas_labirinto.create_image(x0, y0, anchor="nw", image=self.imagem_objeto_movel_tk)
                    self.canvas_labirinto.tag_raise(self.imagem_objeto_movel)
                else:
                    cor = self.branco
                    self.canvas_labirinto.create_rectangle(x0, y0, x1, y1, outline="#C1C1C1", fill=cor)

        # Adicionando uma linha ao redor do labirinto
        # self.canvas_labirinto.create_rectangle(1, 1, 709, 709, outline="#C1C1C1", width=1)

    def alternar_widgets(self):
        """
        Alterna a visibilidade dos frames de entrada inicial e principal.
        """
        if self.frame_input_inicial.winfo_ismapped():  # Se está visível
            self.frame_input_inicial.grid_forget()  # Esconder frame inicial
            self.inicializa_frame_input_principal()   # Mostrar frame principal
        else:
            self.frame_input_principal.grid_forget()  # Esconder frame principal
            self.inicializa_frame_input_inicial() # Mostrar frame inicial
 
    def receber_comando(self):
        """
        Recebe e processa o comando do usuário.
        """
        comando, argumentos = dividir_string(self.input_comando.get())
        if comando in self.comandos_disponiveis:
            self.comandos_disponiveis[comando](argumentos)
        else:
            self.exibir_mensagem("Argumento inválido\nClique em Mostrar Comandos para ver o tutorial")     


    def validar_adicionar_parede(self, argumentos):
        """
        Adiciona uma parede no labirinto.
        """
        coordenadas = separar_coordenadas(argumentos)
        if coordenadas is None:
            self.exibir_mensagem("Coordenadas inválidas\nClique em Mostrar Comandos para ver o tutorial")
            return

        validador, mensagem_de_erro = self.ambiente.validar_posicao_elemento(coordenadas, "parede")
        if validador:
            self.ambiente.adicionar_parede(coordenadas)
            self.atualizar_labirinto(coordenadas, "parede")
            self.caixa_texto.delete("0.0", "end")
            self.caixa_texto.insert("0.0", "Parede adicionada com sucesso!\n")
        else:
            self.exibir_mensagem(mensagem_de_erro)

    def validar_mover_objeto_movel(self, direcao):
        """
        Valida e move o objeto_movel na direção especificada.
        """
        if direcao is None:
            self.exibir_mensagem("Direção inválida\nClique em Mostrar Comandos para ver o tutorial")
            return False
        validador, mensagem_de_erro, nova_posicao = self.ambiente.validar_posicao_elemento(direcao, "objeto_movel")
        
        if validador:
            self.agente.ir(direcao, nova_posicao)
            self.ambiente.atualizar_objeto_movel(nova_posicao)
            self.atualizar_labirinto(self.ambiente.obter_posicao_objeto_movel(), "objeto_movel")
            self.exibir_mensagem(f"objeto_movel movido para {direcao}")
            return True
        else:
            self.exibir_mensagem(mensagem_de_erro)
            return False
    
    # TODO: pensar em uma maneira que utilize o estado futuro recursivamente simulando o caminho antes de executar
    def validar_executar_plano(self, plano):
        estado_atual = self.agente.obter_estado_objeto()
        passos = plano.split()
        for passo in passos:
            if passo not in self.ambiente.validar_passo_plano(passo):
                return False
            estado_atual =  self.agente.estado_sucessor
        indice_passo = 0 # Índice do primeiro passo do plano para começar a função recursiva
        self.proximo_passo(indice_passo, passos)

    def proximo_passo(self, indice_passo, passos):
            if indice_passo < len(passos):
                validador, mensagem_de_erro, nova_posicao = self.ambiente.validar_posicao_elemento(passos[indice_passo], "objeto_movel")
                if validador == False:
                    self.exibir_mensagem("Movimento do plano impossível de realizar")
                else: 
                    self.agente.ir(passos[indice_passo], nova_posicao)
                    self.ambiente.atualizar_objeto_movel(nova_posicao)
                    self.atualizar_labirinto(self.ambiente.obter_posicao_objeto_movel(), "objeto_movel")
                    self.exibir_mensagem(f"objeto_movel movido para {passos[indice_passo]}")
                self.janela.after(1000, self.proximo_passo,indice_passo + 1,passos)

    def exibir_mensagem(self, mensagem):
        """
        Exibe uma mensagem na caixa de texto.
        """
        self.caixa_texto.configure(state="normal")
        self.caixa_texto.delete("0.0", "end")
        self.caixa_texto.insert("0.0", mensagem)
        self.caixa_texto.configure(state="disable")
        
    def atualizar_labirinto(self, coordenadas, elemento):
        """
        Atualiza o labirinto com o novo elemento.
        """
        altura = self.ambiente.altura
        largura = self.ambiente.largura

        # Tela fixa no tamanho 710x710
        largura_celula = 710 / largura
        altura_celula = 710 / altura

        if elemento == "parede":
            self.atualizar_parede(coordenadas, largura_celula, altura_celula)
        elif elemento == "objeto_movel":
            self.atualizar_objeto_movel(coordenadas, largura_celula, altura_celula)

    def atualizar_parede(self, coordenadas, largura_celula, altura_celula):
        """
        Atualiza o canvas com as novas paredes.
        """
        for par in coordenadas:
            x0 = par[1] * largura_celula
            y0 = (self.ambiente.altura - 1 - par[0]) * altura_celula
            x1 = x0 + largura_celula
            y1 = y0 + altura_celula
            self.canvas_labirinto.create_rectangle(x0, y0, x1, y1, outline="#C1C1C1", fill=self.preto)
    
    def atualizar_objeto_movel(self, coordenadas, largura_celula, altura_celula):
        """
        Atualiza o canvas com a nova posição do objeto_movel.
        """
        x0 = coordenadas[1] * largura_celula
        y0 = (self.ambiente.altura - 1 - coordenadas[0]) * altura_celula
        self.mover_imagem_objeto_movel(x0, y0)
        
    def mover_imagem_objeto_movel(self, x0, y0):
        """
        Move a imagem do objeto_movel até (x0, y0) suavemente.
        """
        coords = self.canvas_labirinto.bbox(self.imagem_objeto_movel)
        if not coords:
            return  # Se a imagem não for encontrada, sai da função

        x = coords[0]
        y = coords[1]

        passo_x = 1 if x < x0 else -1
        passo_y = 1 if y < y0 else -1
        
        if abs(x - x0) > 1 or abs(y - y0) > 1:
            self.canvas_labirinto.move(self.imagem_objeto_movel, passo_x, passo_y)
            self.canvas_labirinto.tag_raise(self.imagem_objeto_movel)
            self.janela.after(3, lambda: self.mover_imagem_objeto_movel(x0, y0))
        else:
            if self.ambiente.verifica_estado() == "chegou ao destino":
                mensagem = f"O objeto_movel chegou ao destino final!\nCusto total: {self.agente.custo_acumulado}"
                CTkMessagebox(title="Objetivo Alcançado", message=mensagem)
            self.canvas_labirinto.moveto(self.imagem_objeto_movel, x0, y0)
    
    def exibir_analise(self):
        coordenadas_validas = []
        # Para cada ponto cardial, verifica com o ambiente quais é possível ir
        for direcao in self.agente.objeto_movel.DIRECOES:
            validador, posicao = self.ambiente.validar_movimento_objeto_movel(direcao)
            if validador == True:
                coordenadas_validas.append(direcao)
        acoes_disponiveis = self.agente.obter_acoes_possiveis(coordenadas_validas)
        string_direcoes = ', '.join(acoes_disponiveis)
        self.exibir_mensagem(f"Direções disponíveis para mover: {string_direcoes}")
########################################################################################
# Funções de manipulação de string
 
def dividir_string(s):
    """
    Divide a string em comando e argumentos.
    """
    partes = s.split(maxsplit=1)
    comando = partes[0].upper() if partes else ""
    argumentos = partes[1].upper() if len(partes) > 1 else ""
    return comando, argumentos

def separar_coordenadas(s):
    """
    Separa as coordenadas da string.
    """
    padrao = r"^(\d+),(\d+)(\s+(\d+),(\d+))*$"
    
    if not fullmatch(padrao, s.strip()):
        return None  # Retorna None se o formato estiver incorreto

    coordenadas = []
    pares = s.split()
    for par in pares:
        x, y = map(int, par.split(','))
        coordenadas.append((x, y))
    return coordenadas