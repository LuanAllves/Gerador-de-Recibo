import atualizador.update
import pdv.ui.tela_principal as tela_principal

atualizador.update.verificar_atualizacao()

if __name__ == "__main__":
    app = tela_principal.TelaPrincipal()
    app.mainloop()