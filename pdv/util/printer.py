import win32print
import win32ui
import win32con
from datetime import datetime

class Recibo:
    def __init__(self, cliente, itens, taxa_entrega):
        self.cliente = cliente
        self.itens = itens
        self.taxa_entrega = taxa_entrega

    def gerar_recibo(self):
        recibo_text = f"Recibo para: {self.cliente['nome']}\n"
        recibo_text += f"Endereço: {self.cliente['endereco']}\n"
        recibo_text += f"Telefone: {self.cliente['telefone']}\n\n"
        recibo_text += "Itens:\n"
        total = 0
        for item in self.itens:
            recibo_text += f"{item['nome']} - R$ {item['preco']} x {item['quantidade']} = R$ {item['preco'] * item['quantidade']}\n"
            total += item['preco'] * item['quantidade']
        recibo_text += f"\nTaxa de Entrega: R$ {self.taxa_entrega}\n"
        recibo_text += f"Total: R$ {total + self.taxa_entrega}\n"
        recibo_text += f"\nData: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        return recibo_text
    
    def imprimir_recibo(recibo_text, limpar_campos):
        try:
            impressora_padrao = win32print.GetDefaultPrinter()
            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(impressora_padrao)
            hDC.StartDoc("Recibo")
            hDC.StartPage()
            hDC.TextOut(0, 0, recibo_text)
            hDC.EndPage()
            hDC.EndDoc()
            hDC.DeleteDC()
            limpar_campos()
        except Exception as e:
            print(f"Erro ao imprimir recibo: {e}")

    def imprimir_windows(recibo, impressora_selecionada):
        try:
            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(impressora_selecionada)
            hDC.StartDoc("Recibo")
            hDC.StartPage()
            hDC.TextOut(0, 0, recibo)
            hDC.EndPage()
            hDC.EndDoc()
            hDC.DeleteDC()
        except Exception as e:
            print(f"Erro ao imprimir no Windows: {e}")