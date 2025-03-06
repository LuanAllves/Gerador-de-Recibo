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
import calendar
from tkcalendar import Calendar
from datetime import datetime, date

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

        self.imprimir_button = tk.Button(self.frame_botoes, text="Imprimir Recibo", command=self.imprimir_recibo)
        self.imprimir_button.grid(row=0, column=0)

        self.frame_recibo = tk.Frame(self)
        self.frame_recibo.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.recibo_text = tk.Text(self.frame_recibo, height=10)
        self.recibo_text.grid(row=0, column=0, sticky="nsew")

        self.balanceamento_button = tk.Button(self.frame_cadastro, text="Balanceamento", command=self.janela_balanceamento, bg="#9c27b0", fg="white", font=("Arial", 12, "bold"), relief=tk.RAISED, padx=20, pady=10)
        self.balanceamento_button.grid(row=0, column=3, padx=10) # Coluna 3

        self.itens = []

    def janela_balanceamento(self):
        janela = tk.Toplevel(self)
        janela.title("Balanceamento de Vendas")
        janela.geometry("600x400")

        style = ttk.Style()
        style.configure("TLabelFrame.Label", font=("Arial", 12, "bold"))

        frame_datas = ttk.LabelFrame(janela, text="Período")
        frame_datas.pack(padx=10, pady=10, fill=tk.X)

        tk.Label(frame_datas, text="Data de Início:").grid(row=0, column=0, padx=5, pady=5)
        self.data_inicio_entry = ttk.Entry(frame_datas)
        self.data_inicio_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_datas, text="Data de Fim:").grid(row=1, column=0, padx=5, pady=5)
        self.data_fim_entry = ttk.Entry(frame_datas)
        self.data_fim_entry.grid(row=1, column=1, padx=5, pady=5)

        # Definir datas padrão para o mês atual
        hoje = date.today()
        primeiro_dia_mes = date(hoje.year, hoje.month, 1)
        ultimo_dia_mes = date(hoje.year, hoje.month, calendar.monthrange(hoje.year, hoje.month)[1])

        self.data_inicio_entry.insert(0, primeiro_dia_mes.strftime("%d/%m/%Y"))
        self.data_fim_entry.insert(0, ultimo_dia_mes.strftime("%d/%m/%Y"))

        tk.Button(janela, text="Calcular", command=self.calcular_balanceamento).pack(pady=10)

        self.tree = ttk.Treeview(janela, columns=("Data", "Vendas", "Total"), show="headings")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Vendas", text="Vendas")
        self.tree.heading("Total", text="Total")
        self.tree.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.total_label = ttk.Label(janela, text="Total Geral: R$ 0.00", font=("Arial", 12, "bold"))
        self.total_label.pack(pady=5)

        tk.Button(frame_datas, text="...", command=lambda: self.selecionar_data(self.data_inicio_entry)).grid(row=0, column=2, padx=5)
        tk.Button(frame_datas, text="...", command=lambda: self.selecionar_data(self.data_fim_entry)).grid(row=1, column=2, padx=5)

        self.data_inicio_entry.bind("<KeyRelease>", lambda event, entry=self.data_inicio_entry: self.formatar_data(event, entry))
        self.data_fim_entry.bind("<KeyRelease>", lambda event, entry=self.data_fim_entry: self.formatar_data(event, entry))

    def calcular_balanceamento(self):
        data_inicio_str = self.data_inicio_entry.get()
        data_fim_str = self.data_fim_entry.get()

        try:
            data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%Y")
            data_fim = datetime.strptime(data_fim_str, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido (DD/MM/AAAA).")
            return

        if data_inicio > data_fim:
            messagebox.showerror("Erro", "Data de início deve ser anterior à data de fim.")
            return

        conexao = sqlite3.connect("recibos.db")
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT data, COUNT(*), SUM(total)
            FROM recibos
            WHERE data BETWEEN ? AND ?
            GROUP BY data
        """, (data_inicio, data_fim))
        resultados = cursor.fetchall()

        self.tree.delete(*self.tree.get_children())
        total_geral = 0
        for resultado in resultados:
            data_str = datetime.strftime(datetime.strptime(resultado[0], "%Y-%m-%d"), "%d/%m/%Y")
            vendas = resultado[1]
            total = resultado[2]
            self.tree.insert("", tk.END, values=(data_str, vendas, f"R$ {total:.2f}"))
            total_geral += total

        self.total_label.config(text=f"Total Geral: R$ {total_geral:.2f}")

        conexao.close()

    def formatar_data(self, event, entry):
        texto = entry.get()
        texto = ''.join(filter(str.isdigit, texto))  # Remove caracteres não numéricos
        if len(texto) > 8:
            texto = texto[:8]  # Limita a 8 dígitos
        if len(texto) >= 2:
            texto = texto[:2] + '/' + texto[2:]
        if len(texto) >= 5:
            texto = texto[:5] + '/' + texto[5:]
        entry.delete(0, tk.END)
        entry.insert(0, texto)

    def selecionar_data(self, entry):
        def definir_data():
            data_selecionada = calendario.get_date()
            entry.delete(0, tk.END)
            entry.insert(0, data_selecionada.strftime("%d/%m/%Y"))
            janela_calendario.destroy()

        janela_calendario = tk.Toplevel(self)
        calendario = Calendar(janela_calendario, date_pattern="dd/mm/yyyy")
        calendario.pack(padx=10, pady=10)

        tk.Button(janela_calendario, text="OK", command=definir_data).pack(pady=5)

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

        impressoras = [impressora[2] for impressora in win32print.EnumPrinters(2)]
        janela_impressoras = tk.Toplevel(self)
        janela_impressoras.title("Selecionar Impressora")
        lista_impressoras = tk.Listbox(janela_impressoras, height=10, width=50)
        for impressora in impressoras:
            lista_impressoras.insert(tk.END, impressora)
        lista_impressoras.pack(padx=10, pady=10)

        def confirmar_selecao():
            try:
                impressora_selecionada = lista_impressoras.get(lista_impressoras.curselection())
                self.imprimir_windows(self.recibo_text.get("1.0", tk.END), impressora_selecionada)
                janela_impressoras.destroy()
                messagebox.showinfo("Sucesso", "Recibo enviado para impressão!")
                self.limpar_campos()
            except IndexError:
                messagebox.showerror("Erro", "Selecione uma impressora.")
            except Exception as e: # Adicionado tratamento de erro aqui
                messagebox.showerror("Erro", f"Erro ao imprimir recibo: {e}")
                janela_impressoras.destroy() # Fechar a janela em caso de erro

        tk.Button(janela_impressoras, text="Confirmar", command=confirmar_selecao).pack(pady=5)

    def imprimir_windows(self, recibo, impressora_selecionada):
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(impressora_selecionada)  # Use a impressora selecionada
        hDC.StartDoc("Recibo")
        hDC.StartPage()
        hDC.SetMapMode(win32con.MM_TWIPS)
        hDC.TextOut(100, -100, recibo)
        hDC.EndPage()
        hDC.EndDoc()
        # Não precisa selecionar a impressora novamente aqui

    def selecionar_impressora(self):
        impressoras = [impressora[2] for impressora in win32print.EnumPrinters(2)]
        janela_impressoras = tk.Toplevel(self)
        janela_impressoras.title("Selecionar Impressora")
        lista_impressoras = tk.Listbox(janela_impressoras, height=10, width=50)
        for impressora in impressoras:
            lista_impressoras.insert(tk.END, impressora)
        lista_impressoras.pack(padx=10, pady=10)

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