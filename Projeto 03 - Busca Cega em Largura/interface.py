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
        self.janela.geometry("1250x750")
        self.janela.resizable(False, False)
        self.janela.option_add("*Font", ("Montserrrat", 18))
        self.fonte = ("Montserrrat", 14)

        # Obter as dimensões da tela
        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()
        
        # Calcular a posição central
        pos_x = (largura_tela // 2) - (1250 // 2)
        pos_y = (altura_tela // 2) - (750 // 2)
        
        # Definir a geometria da janela com a posição central
        self.janela.geometry(f"{1250}x{750}+{pos_x}+{pos_y}")

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
        self.frame_input_inicial = CTkFrame(self.janela, width=500, height=750, fg_color=self.preto)
        self.frame_input_principal = CTkFrame(self.janela)

        # Posicionando os frames na grade
        self.frame_labirinto.grid(row=0, column=0, sticky="nsew")
        self.frame_input_inicial.grid(row=0, column=1, sticky="sew")
        self.frame_input_inicial.grid_columnconfigure(0, weight=1)
        self.frame_input_inicial.grid_rowconfigure(0, weight=1)

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
                f"Coordenada X: {self.agente.obter_estado_objeto()[0]}\n"
                f"Coordenada Y: {self.agente.obter_estado_objeto()[1]}"
            ),
            "HISTORICO" : lambda args: self.exibir_mensagem(f"Movimentos: {self.agente.objeto_movel.historico_movimentos}\nCusto: {self.agente.custo_acumulado}"),
            "BUSCAR" : lambda args: self.iniciar_busca(),
        }
    def inicializa_frame_input_inicial(self):
        """
        Inicializa o frame de entrada inicial.
        """
        self.frame_input_inicial_baixo = CTkFrame(self.frame_input_inicial, width=300, height=100, fg_color="transparent")
        self.frame_input_inicial_cima = CTkFrame(self.frame_input_inicial, width=450, height=100, fg_color="transparent")

        self.frame_input_inicial_cima.grid(row=0, column=0, sticky="s")
        self.frame_input_inicial_baixo.grid(row=1, column=0, sticky="ns")

        self.frame_input_inicial_baixo.grid_propagate(False)
        self.frame_input_inicial_cima.grid_propagate(False)

        # Configurando colunas para centralizar elementos
        self.frame_input_inicial_cima.grid_columnconfigure(0, weight=1)
        self.frame_input_inicial_cima.grid_columnconfigure(1, weight=1)
        self.frame_input_inicial_cima.grid_columnconfigure(2, weight=1)
        self.frame_input_inicial_cima.grid_columnconfigure(3, weight=1)
        self.frame_input_inicial_baixo.grid_columnconfigure(0, weight=1)
        
        self.label_altura = CTkLabel(
            self.frame_input_inicial_cima,
            text="Altura",
            text_color=self.branco,
            font=self.fonte
        )
        self.label_altura.grid(row=0, column=0, padx=5, sticky="nsw", pady=0)

        self.input_altura = CTkEntry(
            self.frame_input_inicial_cima,
            placeholder_text="20",
            fg_color=self.branco,
            text_color=self.preto,
            height=35
        )
        self.input_altura.grid(row=1, column=0, padx=5, pady=0, sticky="sew")

        self.label_largura = CTkLabel(
            self.frame_input_inicial_cima,
            text="Largura",
            text_color=self.branco,
            font=self.fonte
        )
        self.label_largura.grid(row=0, column=1, padx=10, sticky="nsw", pady=(0, 0))

        self.input_largura = CTkEntry(
            self.frame_input_inicial_cima,
            placeholder_text="25",
            fg_color=self.branco,
            text_color=self.preto,
            height=35
        )
        self.input_largura.grid(row=1, column=1, padx=10, pady=0, sticky="sew")

        self.label_saida = CTkLabel(
            self.frame_input_inicial_cima,
            text="Objetivo",
            text_color=self.branco,
            font=self.fonte
        )
        self.label_saida.grid(row=0, column=2, padx=10, sticky="nsw", pady=(0, 0))

        self.input_saida = CTkEntry(
            self.frame_input_inicial_cima,
            placeholder_text="0,15",
            fg_color=self.branco,
            text_color=self.preto,
            height=35
        )
        self.input_saida.grid(row=1, column=2, padx=10, pady=0, sticky="sew")

        self.label_comeco = CTkLabel(
            self.frame_input_inicial_cima,
            text="Início",
            text_color=self.branco,
            font=self.fonte
        )
        self.label_comeco.grid(row=0, column=3, padx=10, sticky="nsw", pady=(0, 0))

        self.input_comeco = CTkEntry(
            self.frame_input_inicial_cima,
            placeholder_text="0,0",
            fg_color=self.branco,
            text_color=self.preto,
            height=35
        )
        self.input_comeco.grid(row=1, column=3, padx=10, pady=0, sticky="sew")

        self.botao_enviar = CTkButton(
            self.frame_input_inicial_baixo,
            text="CRIAR",
            height=50,
            width=100,  # Define explicitamente a largura do botão
            command=self.criar_ambiente
        )
        self.botao_enviar.grid(row=0, column=0, pady=(0, 20), sticky="nsew")

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
        self.frame_input_principal = CTkFrame(self.janela, width=500, fg_color=self.preto, corner_radius=0)
        # Posicionando os frames na grade
        self.frame_input_principal.grid(row=0, column=1, sticky="nsew", pady=0)
        # Mantendo os tamanhos definidos
        self.frame_input_principal.grid_propagate(False)

        self.frame_input_principal_baixo = CTkFrame(self.frame_input_principal, fg_color=self.preto, corner_radius=0)
        # Posicionando os frames na grade
        self.frame_input_principal_baixo.grid(row=2, column=0, sticky="sew", pady=0)


        # Configurando colunas e linhas para centralizar o input
        self.frame_input_principal.grid_columnconfigure(0, weight=1)
        self.frame_input_principal.grid_rowconfigure(0, weight=0)
        self.frame_input_principal.grid_rowconfigure(1, weight=1)
        self.frame_input_principal.grid_rowconfigure(2, weight=0)
        
        self.frame_input_principal_baixo.grid_columnconfigure(0, weight=1)
        self.frame_input_principal_baixo.grid_rowconfigure(0, weight=1)

        # Adicionando label
        self.label_console = CTkLabel(
            self.frame_input_principal,
            text="Console",
            text_color=self.branco,
            font=(f"{self.fonte}", 20)
        )
        self.label_console.grid(row=0, column=0, padx=15, pady=(15, 0), sticky="ew")
        
        # Adicionando caixa de texto 
        self.caixa_texto = CTkTextbox(
            self.frame_input_principal,
        )
        self.caixa_texto.insert("0.0", "▶ Ir X: move o objeto movel na direção X ∈ {N, S, L, O, NO, NE, SE, SO}\n"
                                        "▶ Parede x1,y1 x2,y2 ... xn,yn: insere parede nas coordenadas fornecidas\n"
                                        "▶ Lerpos: retorna a posição que o objeto movel se encontra\n"
                                        "▶ Historico: retorna a ordem de movimento e custo total acumulado\n"
                                        "▶ Buscar: inicia uma busca pelo menor caminho, se for possível a executa\n")
        self.caixa_texto.grid(row=1, column=0, padx=15, pady=(15, 0), sticky="nsew")
        self.caixa_texto.tag_add("center", "1.0", "end")
        self.caixa_texto.configure(state="disabled")

        # Adicionando um input de texto centralizado
        self.input_comando = CTkEntry(
            self.frame_input_principal_baixo,
            placeholder_text="Digite um comando...",
            fg_color=self.branco,
            text_color=self.preto
        )
        self.input_comando.grid(row=1, column=0, padx=(15,0), pady=15, sticky="nsew", ipadx=10, ipady=10)
        self.input_comando.bind('<Return>', lambda event: self.receber_comando())

        # Adicionando um botão flutuante
        self.botao_comandos = CTkButton(
            self.frame_input_principal_baixo,
            text="Mostrar Comandos",
            command=lambda : self.exibir_mensagem("Ir X: move o objeto movel na direção X ∈ {N, S, L, O, NO, NE, SE, SO}\n"
                                        "▶ Parede x1,y1 x2,y2 ... xn,yn: insere parede nas coordenadas fornecidas\n"
                                        "▶ Lerpos: retorna a posição que o objeto movel se encontra\n"
                                        "▶ Historico: retorna a ordem de movimento e custo total acumulado\n"
                                        "▶ Buscar: inicia uma busca pelo menor caminho, se for possível a executa")
        )
        self.botao_comandos.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")

        return

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
            self.agente.definir_estado_objetivo(saida)

            posicao_inicial = self.input_comeco.get()
            comecoX, comecoY = map(int, posicao_inicial.split(","))
            posicao_inicial = [comecoX, comecoY]
            validador, mensagem = self.ambiente.definir_inicio(posicao_inicial) 
            if not validador:
                CTkMessagebox(title="Erro", message=mensagem)
                return
            self.agente.definir_grid(self.ambiente.grid)
            self.ambiente.exibir()
        except ValueError:
            CTkMessagebox(title="Erro", message="Entrada inválida.\n"
            "Altura: inteiro entre 3 e 50\nLargura: inteiro entre 3 e 50\n"
            "Saída: dois inteiros separados por vírgula.")
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
        self.frame_labirinto.configure(fg_color=self.preto)

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
            self.exibir_mensagem("Argumento inválido\n"
                                "Clique em Mostrar Comandos para ver o tutorial")     


    def validar_adicionar_parede(self, argumentos):
        """
        Adiciona uma parede no labirinto.
        """
        coordenadas = separar_coordenadas(argumentos)
        if coordenadas is None:
            self.exibir_mensagem("Coordenadas inválidas\n"
                                "Clique em Mostrar Comandos para ver o tutorial")
            return
        validador, mensagem_de_erro = self.ambiente.validar_posicao_parede(coordenadas)
        if validador:
            self.ambiente.adicionar_parede(coordenadas)
            self.agente.definir_grid(self.ambiente.grid)
            self.atualizar_labirinto(coordenadas, "parede")
            self.exibir_mensagem("Obstáculo adicionado ao labirinto!")
        else:
            self.exibir_mensagem(mensagem_de_erro)

    def validar_mover_objeto_movel(self, direcao):
        """
        Valida e move o objeto_movel na direção especificada.
        """
        if direcao is None:
            self.exibir_mensagem("Direção inválida\n"
                                "Clique em Mostrar Comandos para ver o tutorial")
            return False
        validador, mensagem_de_erro, deslocamento = self.ambiente.validar_movimento_objeto_movel(direcao)
        
        if validador:
            self.agente.ir(direcao, deslocamento)
            nova_posicao = self.agente.obter_estado_objeto()
            self.ambiente.atualizar_objeto_movel(nova_posicao)
            self.agente.definir_grid(self.ambiente.grid)
            self.atualizar_labirinto(nova_posicao, "objeto_movel")
            self.exibir_mensagem(f"objeto_movel movido para {direcao}")
            return True
        else:
            self.exibir_mensagem(mensagem_de_erro)
            return False
    
    def iniciar_busca(self):
        """
        Executa um ciclo de raciocínio do agente e atualiza o ambiente e o canvas.
        """
        # Executa o ciclo de raciocínio do agente
        self.exibir_mensagem("Iniciando busca...")
        plano =self.agente.iniciar_plano_grafo()
        self.agente.definir_plano(plano)
        self.exibir_mensagem(f"Plano a ser seguido: {plano}")
        self.executar_plano()

    def executar_plano(self):
        sucesso, nova_posicao = self.agente.ciclo_de_raciocinio()
        self.exibir_mensagem(f"Executando ciclo: indo para {nova_posicao}")
        if sucesso:

            # Atualiza o ambiente e o canvas
            self.ambiente.atualizar_objeto_movel(nova_posicao)
            self.agente.definir_grid(self.ambiente.grid)
            self.atualizar_labirinto(nova_posicao, "objeto_movel")

            # Agendar o próximo ciclo após 500ms
            self.janela.after(1000, self.executar_plano)
        else:
            self.exibir_mensagem("Plano concluído!")


    def exibir_mensagem(self, mensagem):
        """
        Exibe uma mensagem na caixa de texto.
        """
        self.caixa_texto.configure(state="normal")
        self.caixa_texto.insert("end", f"▶ {mensagem}\n")
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
            self.canvas_labirinto.create_rectangle(x0, y0, x1, y1, outline=self.branco, fill=self.preto)
    
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
            if self.agente.teste_objetivo():
                mensagem = f"O objeto_movel chegou ao destino final!\nCusto total: {self.agente.custo_acumulado}"
                CTkMessagebox(title="Objetivo Alcançado", message=mensagem)
            self.canvas_labirinto.moveto(self.imagem_objeto_movel, x0, y0)

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

def formatar_vizinhos(vizinhos):
    """
    Formata os vizinhos em uma matriz 3x3 com os seguintes símbolos:
    ■ para lugares com None ou parede,
    □ para lugares vazios,
    ⊗ no meio para o objeto,
    ★ para a saída.
    """
    # Função auxiliar para obter o valor formatado
    def valor_formatado(chave):
        valor = vizinhos.get(chave)
        if valor is None or valor == '⬛':  # Paredes ou fora dos limites
            return "■"
        elif valor == '⬜':  # Lugar vazio
            return "□"
        elif valor == '🟩':  # Saída
            return "★"
        else:
            return "□"  # Posição livre

    # Monta a matriz 3x3 com as posições correspondentes:
    # Linha 1: [NO, N, NE]
    # Linha 2: [O, Obj, L]
    # Linha 3: [SO, S, SE]
    matriz = [
        [valor_formatado('NO'), valor_formatado('N'),  valor_formatado('NE')],
        [valor_formatado('O'),  "⊗",                  valor_formatado('L')],
        [valor_formatado('SO'), valor_formatado('S'),  valor_formatado('SE')]
    ]
    
    # Cria a string formatada com cada linha separada por nova linha
    linhas_formatadas = [" ".join(linha) for linha in matriz]
    return "\n".join(linhas_formatadas)