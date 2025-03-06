import tkinter as tk
import os
import tempfile
import time
import re
import sqlite3
from tkinter import ttk
from escpos.printer import Usb
from tkinter import messagebox
from datetime import datetime
import win32print
import win32ui
import win32con

class Recibo:
    def __init__(self, cliente, endereco, telefone, itens, taxa):
        self.cliente = cliente
        self.endereco = endereco
        self.telefone = telefone
        self.itens = itens
        self.taxa = taxa

    def calcular_total(self):
        total = 0
        for item in self.itens:
            total += item['preco'] * item['quantidade']
        total += self.taxa
        return total

    def gerar_recibo(self):
        recibo = f"Cliente: {self.cliente}\n"
        recibo += f"Endereço: {self.endereco}\n"
        recibo += f"Telefone: {self.telefone}\n\n"
        recibo += "Itens:\n"
        for item in self.itens:
            recibo += f"- {item['nome']} x {item['quantidade']} = R${item['preco'] * item['quantidade']:.2f}\n"
        recibo += f"\nTaxa de Entrega: R${self.taxa:.2f}\n"
        recibo += f"Total: R${self.calcular_total():.2f}"
        return recibo

def criar_banco_dados():
    conexao = sqlite3.connect("recibos.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            endereco TEXT,
            telefone TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            preco REAL
        )
    """)
    conexao.commit()
    conexao.close()

criar_banco_dados()

def adicionar_cliente(nome, endereco, telefone):
    conexao = sqlite3.connect("recibos.db")
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO clientes (nome, endereco, telefone) VALUES (?, ?, ?)", (nome, endereco, telefone))
    conexao.commit()
    conexao.close()

def adicionar_produto(nome, preco):
    conexao = sqlite3.connect("recibos.db")
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome, preco))
    conexao.commit()
    conexao.close()

def alterar_preco_produto(nome_produto, novo_preco):
    conexao = sqlite3.connect("recibos.db")
    cursor = conexao.cursor()
    cursor.execute("UPDATE produtos SET preco = ? WHERE nome = ?", (novo_preco, nome_produto))
    conexao.commit()
    conexao.close()

def obter_clientes():
    conexao = sqlite3.connect("recibos.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT nome FROM clientes")
    clientes = [cliente[0] for cliente in cursor.fetchall()]
    conexao.close()
    return clientes

def obter_produtos():
    conexao = sqlite3.connect("recibos.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT nome FROM produtos")
    produtos = [produto[0] for produto in cursor.fetchall()]
    conexao.close()
    return produtos

def obter_dados_cliente(nome_cliente):
    conexao = sqlite3.connect("recibos.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT endereco, telefone FROM clientes WHERE nome = ?", (nome_cliente,))
    dados = cursor.fetchone()
    conexao.close()
    return dados

def obter_preco_produto(nome_produto):
    conexao = sqlite3.connect("recibos.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT preco FROM produtos WHERE nome = ?", (nome_produto,))
    preco = cursor.fetchone()[0]
    conexao.close()
    return preco

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Recibos")
        self.geometry("1280x720")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

        self.frame_cadastro = tk.Frame(self)
        self.frame_cadastro.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        self.frame_cadastro.columnconfigure(0, weight=1)
        self.frame_cadastro.columnconfigure(1, weight=1)
        self.frame_cadastro.columnconfigure(2, weight=1)

        self.botao_cadastrar_cliente = tk.Button(self.frame_cadastro, text="Cadastrar Cliente", command=self.cadastrar_cliente, bg="#4caf50", fg="white", font=("Arial", 12, "bold"), relief=tk.RAISED, padx=20, pady=10)
        self.botao_cadastrar_cliente.grid(row=0, column=0, padx=10)

        self.botao_cadastrar_produto = tk.Button(self.frame_cadastro, text="Cadastrar Produto", command=self.cadastrar_produto, bg="#2196f3", fg="white", font=("Arial", 12, "bold"), relief=tk.RAISED, padx=20, pady=10)
        self.botao_cadastrar_produto.grid(row=0, column=1, padx=10)

        self.botao_alterar_preco_produto = tk.Button(self.frame_cadastro, text="Alterar Preço Produto", command=self.janela_alterar_preco_produto, bg="#ff9800", fg="white", font=("Arial", 12, "bold"), relief=tk.RAISED, padx=20, pady=10)
        self.botao_alterar_preco_produto.grid(row=0, column=2, padx=10)

        self.frame_cliente = tk.Frame(self)
        self.frame_cliente.grid(row=1, column=0, sticky="new", padx=10, pady=5)

        tk.Label(self.frame_cliente, text="Cliente:").grid(row=0, column=0, sticky="w")
        self.cliente_combobox = ttk.Combobox(self.frame_cliente, values=obter_clientes())
        self.cliente_combobox.grid(row=0, column=1, sticky="ew")
        self.cliente_combobox.bind("<<ComboboxSelected>>", self.selecionar_cliente)

        tk.Label(self.frame_cliente, text="Endereço:").grid(row=1, column=0, sticky="w")
        self.endereco_entry = tk.Entry(self.frame_cliente)
        self.endereco_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(self.frame_cliente, text="Telefone:").grid(row=2, column=0, sticky="w")
        self.telefone_entry = tk.Entry(self.frame_cliente)
        self.telefone_entry.grid(row=2, column=1, sticky="ew")

        self.frame_produto = tk.Frame(self)
        self.frame_produto.grid(row=1, column=1, sticky="new", padx=10, pady=5)

        tk.Label(self.frame_produto, text="Produto:").grid(row=0, column=0, sticky="w")
        self.produto_combobox = ttk.Combobox(self.frame_produto, values=obter_produtos())
        self.produto_combobox.grid(row=0, column=1, sticky="ew")
        self.produto_combobox.bind("<<ComboboxSelected>>", self.selecionar_produto)

        tk.Label(self.frame_produto, text="Preço:").grid(row=1, column=0, sticky="w")
        self.preco_entry = tk.Entry(self.frame_produto)
        self.preco_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(self.frame_produto, text="Quantidade:").grid(row=2, column=0, sticky="w")
        self.quantidade_entry = tk.Entry(self.frame_produto)
        self.quantidade_entry.grid(row=2, column=1, sticky="ew")

        self.adicionar_produto_button = tk.Button(self.frame_produto, text="Adicionar Produto", command=self.adicionar_produto_lista, bg="#42a5f5", fg="white", font=("Arial", 10, "bold"), relief=tk.RAISED)
        self.adicionar_produto_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        self.frame_itens = tk.Frame(self)
        self.frame_itens.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        tk.Label(self.frame_itens, text="Itens:").grid(row=0, column=0, sticky="w")
        self.itens_listbox = tk.Listbox(self.frame_itens, height=5, width=60)
        self.itens_listbox.grid(row=1, column=0, sticky="ew")

        self.frame_taxa = tk.Frame(self)
        self.frame_taxa.grid(row=3, column=0, sticky="new", padx=10, pady=5)

        tk.Label(self.frame_taxa, text="Taxa de Entrega:").grid(row=0, column=0, sticky="w")
        self.taxa_entry = tk.Entry(self.frame_taxa)
        self.taxa_entry.grid(row=0, column=1, sticky="ew")

        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.grid(row=3, column=1, sticky="ne", padx=10, pady=5)

        self.botao_alterar_preco_produto = tk.Button(self.frame_cadastro, text="Alterar Preço Produto", command=self.janela_alterar_preco_produto, bg="#ff9800", fg="white", font=("Arial", 12, "bold"), relief=tk.RAISED, padx=20, pady=10)
        self.botao_alterar_preco_produto.grid(row=0, column=2, padx=10)

        self.impressora_selecionada = tk.StringVar()
        self.impressora_selecionada.set("Windows") # Valor padrão
        self.radio_usb = tk.Radiobutton(self.frame_botoes, text="USB", variable=self.impressora_selecionada, value="USB")
        self.radio_rede = tk.Radiobutton(self.frame_botoes, text="Rede", variable=self.impressora_selecionada, value="Rede")
        self.radio_windows = tk.Radiobutton(self.frame_botoes, text="Windows", variable=self.impressora_selecionada, value="Windows")
        self.radio_usb.grid(row=0, column=1)
        self.radio_rede.grid(row=0, column=2)
        self.radio_windows.grid(row=0,column=3)

        self.imprimir_button = tk.Button(self.frame_botoes, text="Imprimir Recibo", command=self.imprimir_recibo)
        self.imprimir_button.grid(row=0, column=0)

        self.frame_recibo = tk.Frame(self)
        self.frame_recibo.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.recibo_text = tk.Text(self.frame_recibo, height=10)
        self.recibo_text.grid(row=0, column=0, sticky="nsew")

        self.itens = []

    def selecionar_cliente(self, event):
        nome_cliente = self.cliente_combobox.get()
        dados_cliente = obter_dados_cliente(nome_cliente)
        if dados_cliente:
            self.endereco_entry.delete(0, tk.END)
            self.endereco_entry.insert(0, dados_cliente[0])
            self.telefone_entry.delete(0, tk.END)
            self.telefone_entry.insert(0, dados_cliente[1])

    def selecionar_produto(self, event):
        nome_produto = self.produto_combobox.get()
        preco_produto = obter_preco_produto(nome_produto)
        self.preco_entry.delete(0, tk.END)
        self.preco_entry.insert(0, preco_produto)

    def adicionar_produto_lista(self):
        try:
            nome_produto = self.produto_combobox.get()
            quantidade = int(self.quantidade_entry.get())
            preco = float(self.preco_entry.get())
            self.itens.append({"nome": nome_produto, "quantidade": quantidade, "preco": preco})
            self.itens_listbox.insert(tk.END, f"{nome_produto} x {quantidade} = R${preco * quantidade:.2f}")
        except ValueError:
            messagebox.showerror("Erro", "Quantidade e preço devem ser números válidos.")

    def imprimir_recibo(self):
        nome_empresa = "Feito Perfeito"
        endereco_empresa = "Rua 13 de Maio, Recreio dos Bandeirantes - RJ"

        cliente = self.cliente_combobox.get()
        endereco = self.endereco_entry.get()
        telefone = self.telefone_entry.get()
        taxa_str = self.taxa_entry.get()
        if taxa_str:
            try:
                taxa = float(taxa_str)
            except ValueError:
                messagebox.showerror("Erro", "Taxa deve ser um número válido.")
                return
        else:
            taxa = 0.0

        recibo = f"{'=' * 40}\n"
        recibo += f"{nome_empresa}\n{endereco_empresa}\n"
        recibo += f"{'=' * 40}\n"

        recibo += f"Cliente: {cliente}\nEndereço: {endereco}\nTelefone: {telefone}\n\nItens:\n"
        total = 0
        for item in self.itens:
            recibo += f"- {item['nome']} x {item['quantidade']} = R${item['preco'] * item['quantidade']:.2f}\n"
            total += item['preco'] * item['quantidade']
        recibo += f"\nTaxa de Entrega: R${taxa:.2f}\n"
        recibo += f"Total: R${total + taxa:.2f}"

        recibo += f"\n{'=' * 40}\n"
        agora = datetime.now()
        data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
        recibo += f"Data e Hora: {data_hora}\n"
        recibo += f"{'=' * 40}\n"

        self.recibo_text.delete("1.0", tk.END)
        self.recibo_text.insert(tk.END, recibo)

        try:
            if self.impressora_selecionada.get() == "USB":
                self.imprimir_usb(recibo)
            elif self.impressora_selecionada.get() == "Rede":
                self.imprimir_rede(recibo)
            else:
                self.imprimir_windows(recibo)
            messagebox.showinfo("Sucesso", "Recibo enviado para impressão!")
            self.limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao imprimir recibo: {e}")

    def imprimir_usb(self, recibo):
        try:
            printer = Usb(0x0483, 0x7023)
            printer.text(recibo)
            printer.cut()
        except Exception as e:
            messagebox.showerror("Erro", f"Impressora USB não encontrada ou com problemas: {e}")

    def imprimir_rede(self, recibo):
        try:
            import socket
            ip = "192.168.1.100"  # Substitua pelo IP da sua impressora
            porta = 9100  # Substitua pela porta da sua impressora
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, porta))
            s.sendall(recibo.encode())
            s.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao imprimir na impressora de rede: {e}")

    def imprimir_windows(self, recibo):
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC()
        hDC.StartDoc("Recibo")
        hDC.StartPage()
        hDC.SetMapMode(win32con.MM_TWIPS)
        hDC.TextOut(100, -100, recibo)
        hDC.EndPage()
        hDC.EndDoc()
        hDC.SelectPrinter()

    def limpar_campos(self):
        self.cliente_combobox.set("")
        self.endereco_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.produto_combobox.set("")
        self.preco_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)
        self.taxa_entry.delete(0, tk.END)
        self.itens = []
        self.itens_listbox.delete(0, tk.END)
        self.recibo_text.delete("1.0", tk.END)

    def cadastrar_cliente(self):
        self.janela_cadastro_cliente()

    def cadastrar_produto(self):
        self.janela_cadastro_produto()

    def janela_cadastro_cliente(self):
        janela = tk.Toplevel(self)
        janela.title("Cadastrar Cliente")
        janela.geometry("400x200")
        janela.configure(bg="#e0f7fa")

        janela.columnconfigure(1, weight=1)

        tk.Label(janela, text="Nome:", padx=10, pady=5, bg="#e0f7fa").grid(row=0, column=0)
        nome_entry = tk.Entry(janela, width=30)
        nome_entry.grid(row=0, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        tk.Label(janela, text="Endereço:", padx=10, pady=5, bg="#e0f7fa").grid(row=1, column=0)
        endereco_entry = tk.Entry(janela, width=30)
        endereco_entry.grid(row=1, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        tk.Label(janela, text="Telefone:", padx=10, pady=5, bg="#e0f7fa").grid(row=2, column=0)
        telefone_entry = tk.Entry(janela, width=30)
        telefone_entry.grid(row=2, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        tk.Label(janela, text="", bg="#e0f7fa").grid(row=3, column=0, columnspan=2)

        def cadastrar():
            nome = nome_entry.get()
            endereco = endereco_entry.get()
            telefone = telefone_entry.get()
            if not re.match(r'^\+?[1-9]\d{1,14}$', telefone):
                messagebox.showerror("Erro", "Formato de telefone inválido.")
                return
            if nome and endereco and telefone:
                adicionar_cliente(nome, endereco, telefone)
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
                self.cliente_combobox["values"] = obter_clientes()
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Preencha todos os campos.")

        tk.Button(janela, text="Cadastrar", command=cadastrar, padx=10, pady=15, bg="#b2ebf2", fg="black", font=("Arial", 10, "bold"), relief=tk.RAISED).grid(row=4, columnspan=2)

    def alterar_preco_produto(nome_produto, novo_preco):
        conexao = sqlite3.connect("recibos.db")
        cursor = conexao.cursor()
        cursor.execute("UPDATE produtos SET preco = ? WHERE nome = ?", (novo_preco, nome_produto))
        conexao.commit()
        conexao.close()

    def janela_alterar_preco_produto(self):
        janela = tk.Toplevel(self)
        janela.title("Alterar Preço do Produto")
        janela.geometry("300x150")
        janela.configure(bg="#e8f5e9")

        janela.columnconfigure(1, weight=1)

        tk.Label(janela, text="Produto:", padx=10, pady=5, bg="#e8f5e9").grid(row=0, column=0)
        produto_combobox = ttk.Combobox(janela, values=obter_produtos(), width=25)
        produto_combobox.grid(row=0, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        tk.Label(janela, text="Novo Preço:", padx=10, pady=5, bg="#e8f5e9").grid(row=1, column=0)
        preco_entry = tk.Entry(janela, width=25)
        preco_entry.grid(row=1, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        tk.Label(janela, text="", bg="#e8f5e9").grid(row=2, column=0, columnspan=2)

        def alterar():
            nome_produto = produto_combobox.get()
            try:
                novo_preco = float(preco_entry.get())
                alterar_preco_produto(nome_produto, novo_preco)
                messagebox.showinfo("Sucesso", "Preço do produto alterado com sucesso!")
                self.produto_combobox["values"] = obter_produtos()
                janela.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Preço deve ser um número válido.")

        tk.Button(janela, text="Alterar", command=alterar, padx=10, pady=15, bg="#c8e6c9", fg="black", font=("Arial", 10, "bold"), relief=tk.RAISED).grid(row=3, columnspan=2)

    def janela_cadastro_produto(self):
        janela = tk.Toplevel(self)
        janela.title("Cadastrar Produto")
        janela.geometry("300x150")
        janela.configure(bg="#e8f5e9")

        janela.columnconfigure(1, weight=1)

        tk.Label(janela, text="Nome:", padx=10, pady=5, bg="#e8f5e9").grid(row=0, column=0)
        nome_entry = tk.Entry(janela, width=25)
        nome_entry.grid(row=0, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        tk.Label(janela, text="Preço:", padx=10, pady=5, bg="#e8f5e9").grid(row=1, column=0)
        preco_entry = tk.Entry(janela, width=25)
        preco_entry.grid(row=1, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        tk.Label(janela, text="", bg="#e8f5e9").grid(row=2, column=0, columnspan=2)

        def cadastrar():
            nome = nome_entry.get()
            try:
                preco = float(preco_entry.get())
                adicionar_produto(nome, preco)
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
                self.produto_combobox["values"] = obter_produtos()
                janela.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Preço deve ser um número válido.")

        tk.Button(janela, text="Cadastrar", command=cadastrar, padx=10, pady=15, bg="#c8e6c9", fg="black", font=("Arial", 10, "bold"), relief=tk.RAISED).grid(row=3, columnspan=2)

if __name__ == "__main__":
    app = App()
    app.mainloop()