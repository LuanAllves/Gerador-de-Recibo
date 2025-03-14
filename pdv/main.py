import atualizador.update
import pdv.ui.tela_principal as tela_principal
import pdv.modelos.database as banco_de_dados

atualizador.update.verificar_atualizacao()
banco_de_dados.criar_banco_dados() # Chame a função aqui

if __name__ == "__main__":
    app = tela_principal.TelaPrincipal()
    app.mainloop()