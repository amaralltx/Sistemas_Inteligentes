from interface import Interface
from agente import Agente
from ambiente import Ambiente
from objeto_movel import ObjetoMovel
from customtkinter import *

objeto_movel = ObjetoMovel()
ambiente = Ambiente(objeto_movel)
agente = Agente(objeto_movel)

# Inicializa a interface gráfica e coleta as entradas do usuário
if __name__ == "__main__":
    janela = CTk()
    app = Interface(janela, ambiente, agente)
    janela.mainloop()

# Obtém o ambiente criado pela interface gráfica
ambiente = app.ambiente
